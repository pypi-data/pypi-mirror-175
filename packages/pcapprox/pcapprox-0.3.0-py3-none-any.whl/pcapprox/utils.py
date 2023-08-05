from functools import wraps
import numpy as np
import torch.nn as nn


def construct_layer_list(node_list: list, act):
    """
    Construct a list of layers for feedforward neural networks (FNN).

    node_list: hidden layer nodes ([64, 64, 64])
    act: activation function
    """
    layer_list = nn.ModuleList()  # to be tracked by torch
    for i in range(1, len(node_list)):
        node_prev = node_list[i-1]
        node = node_list[i]
        layer_list.append(nn.Linear(node_prev, node))
        if i is not len(node_list)-1:
            layer_list.append(act)
    return layer_list


def normalise_forward(func):
    @wraps(func)
    def inner(self, x, u, **kwargs):
        device = next(self.parameters()).device.type
        x = x.to(device)
        u = u.to(device)
        if self.normalise_factor[0] is not None:
            self.normalise_factor[0] = self.normalise_factor[0].to(device)
        if self.normalise_factor[1] is not None:
            self.normalise_factor[1] = self.normalise_factor[1].to(device)
        if self.normalise_factor[2] is not None:
            self.normalise_factor[2] = self.normalise_factor[2].to(device)
        if self.normalise_factor[0] is None:
            x_normalised = x
        else:
            x_normalised = x / self.normalise_factor[0]
        if self.normalise_factor[1] is None:
            u_normalised = u
        else:
            u_normalised = u / self.normalise_factor[1]
        f_normalised = func(self, x_normalised, u_normalised, **kwargs)
        if self.normalise_factor[2] is None:
            f = f_normalised
        else:
            f = f_normalised * self.normalise_factor[2]
        return f
    return inner


def normalise_minimise(func):
    @wraps(func)
    def inner(self, x, **kwargs):
        device = next(self.parameters()).device.type
        if self.normalise_factor[0] is not None:
            self.normalise_factor[0] = self.normalise_factor[0].to(device)
        if self.normalise_factor[1] is not None:
            self.normalise_factor[1] = self.normalise_factor[1].to(device)
        if self.normalise_factor[2] is not None:
            self.normalise_factor[2] = self.normalise_factor[2].to(device)
        # type check
        x_normal = self.normalise_factor[0]
        u_normal = self.normalise_factor[1]
        if type(x) is np.ndarray and self.normalise_factor[0] is not None:
            x_normal = self.normalise_factor[0].detach().cpu().numpy()
        if type(x) is np.ndarray and self.normalise_factor[1] is not None:
            u_normal = self.normalise_factor[1].detach().cpu().numpy()
        # normalisation
        x_normalised = x if x_normal is None else x / x_normal
        u_normalised = func(self, x_normalised, **kwargs)
        u = u_normalised if u_normal is None else u_normalised * u_normal
        return u
    return inner
