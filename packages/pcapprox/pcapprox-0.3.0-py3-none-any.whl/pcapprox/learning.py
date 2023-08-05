from tqdm import tqdm
import torch
from torch.utils.data import DataLoader, random_split


def split_data(dataset, ratio=0.7, seed=0):
    """
    ratio:1-ratio = train:test
    """
    assert ratio >= 0.0 and ratio <= 1.0
    size_train = int(len(dataset) * ratio)
    size_test = len(dataset) - size_train
    dataset_train, dataset_test = random_split(
        dataset, [size_train, size_test],
        generator=torch.Generator().manual_seed(seed),
    )
    return dataset_train, dataset_test


def split_data3(dataset, r_train, r_validate, r_test, seed=0):
    """
    r_train:r_validate:1-(r_train+r_validate) = train:validate:test
    """
    assert abs(r_train + r_validate + r_test - 1.0) < 1e-12
    dataset_train, dataset_validate_test = split_data(
        dataset, r_train, seed=seed,
    )
    dataset_validate, dataset_test = split_data(
        dataset_validate_test, r_validate/(1.0-r_train), seed=seed,
    )
    return dataset_train, dataset_validate, dataset_test


class SupervisedLearning:
    """
    device:
       "cpu"
       "cuda"
    Notes:
       If your problem has not high dimensional, use device "cpu".
    """
    def __init__(
        self, dataset_train, dataset_test, optimiser,
        loss_fn=torch.nn.MSELoss(reduction="sum"),
        epochs=100, batch_size_train=512, batch_size_test=512,
        device="cpu", seed=0,
    ):
        # data setting
        self.optimiser = optimiser

        self.loss_fn = loss_fn
        self.device = device
        self.epochs = epochs
        self.seed = seed
        self.batch_size_train = batch_size_train
        self.batch_size_test = batch_size_test
        self.initialise_loaders(dataset_train, dataset_test)

    def initialise_loaders(self, dataset_train, dataset_test):
        self.loader_train = DataLoader(dataset_train, batch_size=self.batch_size_train, shuffle=True)
        self.loader_test = DataLoader(dataset_test, batch_size=self.batch_size_test)

    def train_cycle(self, network,):
        network.to(self.device)
        network.train()
        i = 0
        loss_mean = 0.0
        for x, u, f in self.loader_train:
            x = x.to(self.device)
            u = u.to(self.device)
            f = f.to(self.device)
            # self.optimiser.zero_grad()
            f_pred = network(x, u)
            loss = self.loss_fn(f_pred, f)
            loss = loss / len(self.loader_train.dataset)
            # loss.backward()

            def closure():
                # Zero gradients
                self.optimiser.zero_grad()

                # Forward pass
                f_pred = network(x, u)

                # Compute loss
                loss = self.loss_fn(f_pred, f)
                loss = loss / len(self.loader_train.dataset)
                # Backward pass
                loss.backward()
                return loss

            self.optimiser.step(closure)
            i += 1
            loss_mean += loss.item()
        loss_mean = loss_mean / i
        return loss_mean

    @torch.no_grad()
    def test_cycle(self, network):
        network.to(self.device)
        network.eval()
        i = 0
        loss_mean = 0.0
        for x, u, f in self.loader_test:
            x = x.to(self.device)
            u = u.to(self.device)
            f = f.to(self.device)
            f_pred = network(x, u)
            loss = self.loss_fn(f_pred, f)
            loss = loss / len(self.loader_test.dataset)
            i += 1
            loss_mean += loss.item()
        loss_mean = loss_mean / i
        return loss_mean

    def train(self, network, verbose=False):
        results = []
        for epoch in tqdm(range(1+self.epochs), desc="Supervised learning"):
            info = {}
            info["epoch"] = epoch
            if epoch != 0:
                loss_train = self.train_cycle(network)
                info["loss_train"] = loss_train
            loss_test = self.test_cycle(network)
            info["loss_test"] = loss_test
            results.append(info)
            if verbose:
                print(f"info: {info}")
        return results
