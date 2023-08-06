import torchvision
import torch

from opennn_pytorch import datasets


def cifar10(tr_part, va_part, te_part, transform):
    '''
    Return splited into train, val, test parts cifar10 dataset.

    Parameterts
    -----------
    tr_part : float
        percent of train data.

    va_part : float
        percent of valid data.

    te_part : float
        percent of test data.

    transform : torchvision.transforms
        torchvision transforms object with augmentations.
    '''
    dataset = torchvision.datasets.CIFAR10(root='.',
                                           download=True,
                                           transform=transform)

    tr_part = int(tr_part * len(dataset))
    va_part = int(va_part * len(dataset))
    te_part = int(te_part * len(dataset))

    if tr_part + va_part + te_part != len(dataset):
        sizes = [tr_part,
                 va_part,
                 te_part,
                 len(dataset) - tr_part - va_part - te_part]
    else:
        sizes = [tr_part, va_part, te_part]

    datasets = torch.utils.data.random_split(dataset, sizes)
    train_dataset = datasets[0]
    valid_dataset = datasets[1]
    test_dataset = datasets[2]

    return train_dataset, valid_dataset, test_dataset


def cifar100(tr_part, va_part, te_part, transform):
    '''
    Return splited into train, val, test parts cifar100 dataset.

    Parameterts
    -----------
    tr_part : float
        percent of train data.

    va_part : float
        percent of valid data.

    te_part : float
        percent of test data.

    transform : torchvision.transforms
        torchvision transforms object with augmentations.
    '''
    dataset = torchvision.datasets.CIFAR100(root='.',
                                            download=True,
                                            transform=transform)

    tr_part = int(tr_part * len(dataset))
    va_part = int(va_part * len(dataset))
    te_part = int(te_part * len(dataset))

    if tr_part + va_part + te_part != len(dataset):
        sizes = [tr_part,
                 va_part,
                 te_part,
                 len(dataset) - tr_part - va_part - te_part]
    else:
        sizes = [tr_part, va_part, te_part]

    datasets = torch.utils.data.random_split(dataset, sizes)
    train_dataset = datasets[0]
    valid_dataset = datasets[1]
    test_dataset = datasets[2]

    return train_dataset, valid_dataset, test_dataset
