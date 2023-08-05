import numpy as np
import math
import torch
import torch.nn as nn
import scipy
import random
from numpy.linalg import norm
import torch.nn.init as init
import cvxpy as cp
from scipy.optimize import minimize

from pcapprox.utils import construct_layer_list, normalise_forward, normalise_minimise
from pcapprox.interface import AbstractBivariateApproximator, ConvexApproximator, ParameterisedConvexApproximator


def retrieve_solver(name):
    """
    Mostly for CVXPY
    """
    if name == "ECOS":
        solver = cp.ECOS
    elif name == "MOSEK":
        solver = cp.MOSEK
    else:
        raise ValueError("Undefined solver")
    return solver


class FNN(AbstractBivariateApproximator):
    def __init__(
        self, n: int, m: int, _node_list, act,
        u_min=None, u_max=None,
        x_normal=None, u_normal=None, f_normal=None,
        solver="COBYLA",
    ):
        super().__init__(x_normal, u_normal, f_normal)
        self.n = n
        self.m = m
        node_list = [n+m, *_node_list, 1]
        self.layer_list = construct_layer_list(node_list, act)
        u_min_normalised, u_max_normalised = u_min, u_max
        if self.normalise_factor[1] is not None:
            if u_min is not None and u_max is not None:
                u_min_normalised, u_max_normalised = u_min / self.normalise_factor[1], u_max / self.normalise_factor[1]
        self.u_min = u_min
        self.u_max = u_max
        self.u_min_normalised = u_min_normalised
        self.u_max_normalised = u_max_normalised
        self.solver = solver

    @normalise_forward
    def forward(self, xs, us):
        zs = torch.cat((xs, us), dim=-1)
        for layer in self.layer_list:
            zs = layer(zs)
        return zs

    @normalise_minimise
    def minimise_np(self, x):
        """
        COBYLA info:
            https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cobyla.html
        """
        assert type(x) is np.ndarray
        assert len(x.shape) == 1
        device = next(self.parameters()).device.type
        x = torch.Tensor(x.reshape(1, *x.shape)).to(device)  # 1 x n

        def obj_func(u):
            u = torch.Tensor(u.reshape(1, *u.shape)).to(device)
            return self.forward.__wrapped__(self, x, u)

        if self.u_min is not None and self.u_max is not None:
            u_min_normalised = self.u_min_normalised
            u_max_normalised = self.u_max_normalised
            if torch.is_tensor(u_min_normalised):
                u_min_normalised = u_min_normalised.detach().numpy()
            if torch.is_tensor(u_max_normalised):
                u_max_normalised = u_max_normalised.detach().numpy()
            # initial guess
            u0 = (
                u_min_normalised
                + (u_max_normalised-u_min_normalised)
                * np.random.uniform()*np.ones(self.m)
            )
            # box constraints
            constraints = [
                dict(
                    type="ineq",
                    fun=lambda u: -u + u_max_normalised,
                ),
                dict(
                    type="ineq",
                    fun=lambda u: u - u_min_normalised,
                ),
            ]
        else:
            # initial guess
            u0 = np.random.multivariate_normal(
                np.ones(self.m), np.eye(self.m),
            )
            # no constraints
            constraints = []

        res = minimize(obj_func, u0, method=self.solver, constraints=constraints)
        u = res.x
        return u


class _PLSE(ParameterisedConvexApproximator):
    def __init__(
        self, n: int, m: int, i_max: int, T: float, _node_list, act, u_min=None, u_max=None, act_output=None,
        x_normal=None, u_normal=None, f_normal=None,
        solver="ECOS",
    ):
        node_list = [n, *_node_list, i_max*(m+1)]
        super().__init__(n, m, i_max, node_list, act, x_normal, u_normal, f_normal)
        self.T = T
        self.initialise_cvxpylayer(u_min, u_max, act_output)
        self.solver = retrieve_solver(solver)

    @normalise_forward
    def forward(self, xs, us):
        d = xs.shape[0]
        i_max, m, T = self.i_max, self.m, self.T
        X = torch.reshape(self.NN(xs), (d, i_max, m+1))
        alpha_is = X[:, :, 0:-1]  # d x i_max x m
        beta_is = X[:, :, -1]  # d x i_max
        tmp = torch.einsum("bm,bim->bi", us, alpha_is) + beta_is  # each row corresponds to us[i, :] @ alpha_is[i, :, :].T
        return T * torch.logsumexp((1/T)*tmp, dim=-1, keepdim=True)

    @normalise_minimise
    def minimise_np(self, x):
        """
        We recommend you to use cp.MOSEK if possible (it tends to be more stable)
        """
        assert type(x) is np.ndarray
        assert len(x.shape) == 1
        device = next(self.parameters()).device.type
        i_max, m = self.i_max, self.m
        x = torch.Tensor(x.reshape(1, *x.shape)).to(device)  # 1 x n
        X = torch.reshape(self.NN(x), (i_max, m+1)).detach().cpu().numpy()
        self.parameters_cp[0].value = X[:, 0:-1]  # i_max x m
        self.parameters_cp[1].value = X[:, -1]  # i_max
        if self.shift is not None:
            self.parameters_cp[2].value = self.forward(self.shift[0].reshape(1, self.n),
                                                       self.shift[1].reshape(1, self.m),).detach().cpu().numpy().reshape(1,)  # TODO
        self.prob.solve(solver=self.solver)
        u = self.u_cp.value
        return u

    @normalise_minimise
    def minimise_tch(self, xs):
        assert type(xs) is torch.Tensor
        assert len(xs.shape) == 2
        d = xs.shape[0]
        i_max, m = self.i_max, self.m
        X = torch.reshape(self.NN(xs), (d, i_max, m+1))
        alpha_is = X[:, :, 0:-1]  # d x i_max x m
        beta_is = X[:, :, -1]  # d x i_max
        if self.shift is not None:
            x_shift, u_shift = self.shift
            offset_value = self.forward(x_shift.reshape(1, self.n),
                                        u_shift.reshape(1, self.m),).reshape(1,)
            us, = self.cvxpylayer(alpha_is, beta_is, offset_value.repeat(d, 1))
        else:
            us, = self.cvxpylayer(alpha_is, beta_is)
        return us


class PLSE(_PLSE):
    def __init__(self, *args, x_shift=None, u_shift=None, **kwargs):
        """
        LSE considering shift
        """
        self.set_shift(x_shift, u_shift)
        super().__init__(*args, **kwargs)

    def forward(self, xs, us):
        if self.shift is None:
            fs = super().forward(xs, us)
        else:
            x_shift, u_shift = self.shift
            fs = super().forward(xs, us) - super().forward(x_shift.reshape(1, self.n), u_shift.reshape(1, self.m))
        return fs


class GPLSE(nn.Module):
    """
    Generalized PLSE
    """
    def __init__(self, plse: PLSE, nn: AbstractBivariateApproximator):
        super().__init__()
        if plse.shift is not None:
            raise ValueError("shifted PLSE is not supported yet for GPLSE construction")
        self.plse = plse
        self.nn = nn

    def forward(self, xs, us):
        us_star = self.plse.minimise_tch(xs)
        tmp1, tmp2 = self.nn(xs, us), self.nn(xs, us_star)
        return self.plse(xs, us) + torch.max(tmp1 - tmp2, torch.zeros_like(tmp1))

    def minimise_np(self, x):
        return self.plse.minimise_np(x)

    def minimise_tch(self, xs):
        return self.plse.minimise_tch(xs)


class SGPLSE(nn.Module):
    """
    Smoothed GPLSE
    """
    def __init__(self, plse: PLSE, nn: AbstractBivariateApproximator, beta):
        super().__init__()
        if plse.shift is not None:
            raise ValueError("shifted PLSE is not supported yet for SGPLSE construction")
        self.plse = plse
        self.nn = nn
        self.softplus = torch.nn.Softplus(beta=beta)
        self.beta = beta

    def forward(self, xs, us):
        us_star = self.plse.minimise_tch(xs)
        tmp1, tmp2 = self.nn(xs, us), self.nn(xs, us_star)
        return self.plse(xs, us) + self.softplus(tmp1 - tmp2) - (torch.log(2*torch.ones_like(tmp1)) / self.beta)

    def minimise_np(self, x):
        return self.plse.minimise_np(x)

    def minimise_tch(self, xs):
        return self.plse.minimise_tch(xs)


class _LSE(ConvexApproximator):
    def __init__(
        self, n: int, m: int, i_max: int, T: float, u_min=None, u_max=None, act_output=None,
        x_normal=None, u_normal=None, f_normal=None,
        solver="ECOS",
    ):
        assert T > 0
        alpha_is = torch.empty((i_max, n+m))
        beta_is = torch.empty((i_max,))
        # see the source code of torch.nn.modules.linear
        # https://github.com/pytorch/pytorch/blob/master/torch/nn/modules/linear.py
        init.kaiming_uniform_(alpha_is, a=math.sqrt(5))
        fan_in, _ = init._calculate_fan_in_and_fan_out(alpha_is)
        bound = 1 / math.sqrt(fan_in) if fan_in > 0 else 0
        init.uniform_(beta_is, -bound, bound)
        super().__init__(n, m, alpha_is, beta_is, x_normal, u_normal, f_normal)
        self.T = T
        # cvxpylayer
        self.initialise_cvxpylayer(u_min, u_max, act_output)
        self.solver = retrieve_solver(solver)

    @normalise_forward
    def forward(self, xs, us):
        T = self.T
        n = self.n
        alpha_is_u = self.alpha_is[:, n:]
        beta_is_plus_alpha_is_times_x = xs @ self.alpha_is[:, 0:n].T + self.beta_is
        tmp = us @ alpha_is_u.T + beta_is_plus_alpha_is_times_x
        fs = T * torch.logsumexp((1/T)*tmp, dim=-1, keepdim=True)
        return fs

    @normalise_minimise
    def minimise_np(self, x):
        """
        We recommend you to use cp.MOSEK if possible (it tends to be more stable)
        """
        assert type(x) is np.ndarray
        assert len(x.shape) == 1
        n = self.n
        alpha_is_u = self.alpha_is[:, n:].detach().cpu().numpy()
        beta_is_plus_alpha_is_times_x = x @ self.alpha_is[:, 0:n].T.detach().cpu().numpy() + self.beta_is.detach().cpu().numpy()  # TODO
        self.parameters_cp[0].value = alpha_is_u
        self.parameters_cp[1].value = beta_is_plus_alpha_is_times_x
        if self.shift is not None:
            self.parameters_cp[2].value = self.forward(self.shift[0].reshape(1, self.n),
                                                       self.shift[1].reshape(1, self.m),).detach().cpu().numpy().reshape(1,)
        self.prob.solve(solver=self.solver)
        u = self.u_cp.value
        return u

    @normalise_minimise
    def minimise_tch(self, xs):
        assert type(xs) is torch.Tensor
        assert len(xs.shape) == 2
        d = xs.shape[0]
        n = self.n
        beta_is_plus_alpha_is_times_x = xs @ torch.t(self.alpha_is[:, 0:n]) + torch.t(self.beta_is)  # x A[:, 0:n].T + b.T (d x 1)
        alpha_is_u = self.alpha_is[:, n:]  # A[:, n:]
        if self.shift is not None:
            x_shift, u_shift = self.shift
            offset_value = self.forward(x_shift.reshape(1, self.n),
                                        u_shift.reshape(1, self.m)).reshape(1,)
            us, = self.cvxpylayer(alpha_is_u.repeat(d, 1, 1), beta_is_plus_alpha_is_times_x,
                                  offset_value.repeat(d, 1))
        else:
            us, = self.cvxpylayer(alpha_is_u.repeat(d, 1, 1), beta_is_plus_alpha_is_times_x)
        return us


class LSE(_LSE):
    def __init__(self, *args, x_shift=None, u_shift=None, **kwargs):
        """
        LSE considering shift
        """
        self.set_shift(x_shift, u_shift)
        super().__init__(*args, **kwargs)

    def forward(self, xs, us):
        if self.shift is None:
            fs = super().forward(xs, us)
        else:
            x_shift, u_shift = self.shift
            fs = super().forward(xs, us) - super().forward(x_shift.reshape(1, self.n), u_shift.reshape(1, self.m))
        return fs


# Notes: DLSE network would be deprecated.
# The approximation performance is not satisfying
# (even with the source code, see https://github.com/Corrado-possieri/DLSE_neural_networks/issues/1)
class DLSE(nn.Module):
    """
    Difference of log-sum-exp (DLSE) network
    Refs:
        [1] G. C. Calafiore, S. Gaubert, and C. Possieri, “A Universal Approximation Result for Difference of Log-Sum-Exp Neural Networks,” IEEE Transactions on Neural Networks and Learning Systems, vol. 31, no. 12, pp. 5603–5612, Dec. 2020, doi: 10.1109/TNNLS.2020.2975051.
    """
    def __init__(self, lse1: LSE, lse2: LSE):
        super().__init__()
        if lse1.shift is not None or lse2.shift is not None:
            raise ValueError("shifted LSE is not supported yet for DLSE construction")
        assert lse1.solver == lse2.solver
        self.solver = lse1.solver
        self.lse1 = lse1
        self.lse2 = lse2
        self.initialise_cvxpy_prob()

    def initialise_cvxpy_prob(self):
        m = self.lse1.m
        self.v_now_cp = cp.Parameter((m,))
        constraints = self.lse1.prob.constraints
        obj = cp.Minimize(self.lse1.prob.objective.expr - self.lse1.u_cp @ self.v_now_cp)
        prob = cp.Problem(obj, constraints)
        self.prob = prob

    def forward(self, xs, us):
        output1 = self.lse1(xs, us)
        output2 = self.lse2(xs, us)
        output = output1 - output2
        return output

    def _iterate(self, x, chi_now, solver):
        n = self.lse2.n
        T = self.lse2.T
        # get gradient
        gamma_ks = self.lse2.alpha_is[:, n:].detach().cpu().numpy()
        delta_ks = self.lse2.beta_is.detach().cpu().numpy() + x @ self.lse2.alpha_is[:, :n].detach().cpu().numpy().T
        _tmp = (1/T) * (gamma_ks @ chi_now + delta_ks)
        v_now = gamma_ks.T @ scipy.special.softmax(_tmp)
        self.v_now_cp.value = v_now

        alpha_ks = self.lse1.alpha_is[:, n:].detach().cpu().numpy()
        beta_ks = self.lse1.beta_is.detach().cpu().numpy() + x @ self.lse1.alpha_is[:, :n].detach().cpu().numpy().T
        self.lse1.parameters_cp[0].value = alpha_ks
        self.lse1.parameters_cp[1].value = beta_ks
        self.prob.solve(solver)
        chi_next = self.lse1.u_cp.value
        return chi_next

    def minimise_np(
        self, x, u0=None, tol=1e-3, verbose=True, i_max=50,
    ):

        i = 0
        """
        u0: initial guess (decision variable)
        Notes:
            LSE(x, u) = T log(sum(exp(
                (1/T) * (dot(alpha_i, cat(x, u)) + beta_i))
            ))
            = T log(sum(exp(
                (1/T) * (dot(alpha_i, u) + (beta_i + dot(alpha_i, x))))
            ))
        """
        if u0 is None:
            n = self.lse1.n
            # constraints not specified
            if self.lse1.u_min is None or self.lse1.u_max is None:
                mean = np.zeros((n))
                cov = np.eye(n)
                u0 = np.random.multivariate_normal(mean, cov, 1)
            # constraints specified
            else:
                u0 = np.array([
                    random.uniform(_u_min, _u_max) for _u_min, _u_max in zip(self.lse1.u_min, self.lse1.u_max)
                ])

        chi_now = u0
        while True:
            if verbose:
                value_now = self.forward(torch.Tensor(x), torch.Tensor(chi_now))
            chi_next = self._iterate(x, chi_now, self.solver)
            criterion = norm(chi_next - chi_now) / (1 + norm(chi_now))
            if verbose:
                i += 1
                print(f"iteration: i = {i}")
                print(f"criterion: {criterion} (tol: {tol})")
            elif i >= i_max:
                print("W: DLSE `minimise_np` exceeds the maximum iteration")
                break
            chi_now = chi_next
            if verbose:
                value_updated = self.forward(torch.Tensor(x), torch.Tensor(chi_now))
                print(f"current value: {value_now}")
                print(f"updated value: {value_updated}")
                print(f"value difference: {value_updated - value_now}")
            if criterion < tol:
                break
        u_star_np = chi_now
        # while True:
        #     value_brute = self.forward(torch.Tensor(x), torch.randn(3))
        #     print(f"brute forcing... {value_brute}")
        #     if value_brute < value_updated:
        #         break
        return u_star_np
