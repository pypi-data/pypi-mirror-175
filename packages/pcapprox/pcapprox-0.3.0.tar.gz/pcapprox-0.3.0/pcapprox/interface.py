import torch
import torch.nn as nn
from torch.nn.parameter import Parameter
import cvxpy as cp
from cvxpylayers.torch import CvxpyLayer

from pcapprox.utils import construct_layer_list


class AbstractBivariateApproximator(nn.Module):
    """
    The "bivariate" does not mean that the dimension of the argument of this approximator would be two;
    Instead, it means that the approximator has two arguments as `f(x, u)`.
    """
    def __init__(self, x=None, u=None, f=None):
        super().__init__()
        self.set_normalise_factor(x, u, f)

    def minimise_np(self, xs):
        raise NotImplementedError("TODO: for non-parameterised convex approximators, we should add an ad-hoc minimise algorithm.")

    def minimise_tch(self, xs):
        raise NotImplementedError("TODO: for non-parameterised convex approximators, we should add an ad-hoc minimise algorithm.")

    def set_normalise_factor(self, x, u, f):
        assert type(x) is torch.Tensor or x is None
        assert type(u) is torch.Tensor or u is None
        assert type(f) is torch.Tensor or f is None
        self.normalise_factor = [x, u, f]


class AbstractParameterisedConvexApproximator(AbstractBivariateApproximator):
    def __init__(
        self,
        x_normal=None, u_normal=None, f_normal=None,
    ):
        super().__init__(x_normal, u_normal, f_normal)

    def minimise_np(self, xs):
        raise NotImplementedError("TODO: add cvxpy-like minimise algorithm")

    def minimise_tch(self, xs):
        raise NotImplementedError("TODO: add cvxpylayers-like minimise algorithm")

    def set_shift(self, x_shift, u_shift):
        if x_shift is None and u_shift is None:
            self.shift = None
        elif x_shift is not None and u_shift is not None:
            assert type(x_shift) is torch.Tensor
            assert type(u_shift) is torch.Tensor
            assert len(x_shift.shape) == 1
            assert len(u_shift.shape) == 1
            self.shift = [x_shift, u_shift]
        else:
            raise ValueError("`x_shift` and `u_shift` should be both None or both not None")

    def _cvxpylayer_wrapper(self, u, obj, u_min, u_max):
        m = self.m
        constraints = []
        if u_min is not None:
            if u_min is torch.Tensor:
                u_min = u_min.numpy()
            if len(u_min.shape) == 1:
                u_min = u_min.reshape((m,))
            constraints += [u >= u_min]
        if u_max is not None:
            if u_max is torch.Tensor:
                u_max = u_max.numpy()
            if len(u_max.shape) == 1:
                u_max = u_max.reshape((m,))
            constraints += [u <= u_max]
        prob = cp.Problem(obj, constraints)
        cvxpylayer = CvxpyLayer(
            prob,
            parameters=[*self.parameters_cp],
            variables=[u],
        )
        return prob, cvxpylayer

    def initialise_cvxpylayer(self, u_min, u_max, act):
        # normalisation
        u_min_normalised, u_max_normalised = u_min, u_max
        if self.normalise_factor[1] is not None:
            if u_min is not None and u_max is not None:
                u_min_normalised, u_max_normalised = u_min / self.normalise_factor[1], u_max / self.normalise_factor[1]
        m, T, i_max = self.m, self.T, self.i_max
        self.u_cp = cp.Variable((m,))
        alpha_is_u_cp = cp.Parameter((i_max, m))
        beta_is_plus_alpha_is_times_x_cp = cp.Parameter((i_max,))
        tmp_cp = self.u_cp @ alpha_is_u_cp.T + beta_is_plus_alpha_is_times_x_cp  # u @ A.T + b
        # network shift
        if self.shift is None:
            _tmp = T * cp.log_sum_exp((1/T)*tmp_cp)
            self.parameters_cp = [alpha_is_u_cp, beta_is_plus_alpha_is_times_x_cp]
        else:
            offset_value = cp.Parameter((1,))
            _tmp = T * cp.log_sum_exp((1/T)*tmp_cp) - offset_value
            self.parameters_cp = [alpha_is_u_cp, beta_is_plus_alpha_is_times_x_cp, offset_value]
        # output activation
        if act is None:
            pass
        elif act == "relu":
            _tmp = cp.pos(_tmp)
        # normalisation
        if self.normalise_factor[2] is not None:
            _tmp = self.normalise_factor[2].squeeze() * _tmp  # to make normalise_factor a scalar
        obj = cp.Minimize(_tmp)
        self.prob, self.cvxpylayer = self._cvxpylayer_wrapper(self.u_cp, obj, u_min_normalised, u_max_normalised)
        self.u_min = u_min
        self.u_max = u_max
        self.u_min_normalised = u_min_normalised
        self.u_max_normalised = u_max_normalised


class ConvexApproximator(AbstractParameterisedConvexApproximator):
    def __init__(
        self, n: int, m: int, alpha_is, beta_is,
        x_normal=None, u_normal=None, f_normal=None,
    ):
        """
        alpha_is: i_max x (n+m) Tensor
        beta_is: i_max x (1) Tensor
        """
        super().__init__(x_normal, u_normal, f_normal)
        self.n = n
        self.m = m
        i_max = alpha_is.shape[0]
        assert beta_is.shape[0] == i_max
        assert alpha_is.shape[1] == n + m
        self.i_max = i_max
        self.alpha_is = Parameter(alpha_is)  # torch
        self.beta_is = Parameter(beta_is)  # torch


class ParameterisedConvexApproximator(AbstractParameterisedConvexApproximator):
    def __init__(
        self, n: int, m: int, i_max: int, node_list, act,
        x_normal=None, u_normal=None, f_normal=None,
    ):
        super().__init__(x_normal, u_normal, f_normal)
        self.n = n
        self.m = m
        self.i_max = i_max
        self.layer_list = construct_layer_list(node_list, act)

    def NN(self, xs):
        for layer in self.layer_list:
            xs = layer(xs)
        return xs
