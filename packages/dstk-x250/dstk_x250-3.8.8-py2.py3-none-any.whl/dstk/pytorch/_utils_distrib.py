#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fonctions et classes pour facilité les multi-gpu.

Created on Sat Oct 22 14:50:47 2022

@author: Cyrile Delestre
"""

import os
from typing import Optional, Dict, Any, Callable
from itertools import product
from warnings import warn

import torch
import torch.distributed as dist
from torch.nn import Module, SyncBatchNorm
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.distributed import DistributedSampler

from dstk.pytorch._utils import is_dist_avail_and_initialized
from dstk.pytorch._base import BaseEnvironnement
from dstk.pytorch._classifier import BaseClassifier, BaseClassifierOnline
from dstk.pytorch._regressor import BaseRegressor, BaseRegressorOnline


def is_main_process():
    r"""
    Permet de check si le process ce trouve sur le device maître.
    """
    return get_rank() == 0


def get_rank():
    r"""
    Returne l'ID de device sur le quel tourne le process.
    """
    if not is_dist_avail_and_initialized():
        return 0
    return dist.get_rank()


def save_on_master(*args, **kwargs):
    r"""
    Permet de sauvegarder via torch.save sur le device maître.
    """
    if is_main_process():
        torch.save(*args, **kwargs)


def init_distributed(dist_url: str = "env://", backend: str = "nccl"):
    r"""
    Fonction d'initialisation de la partie distribution de PyTorch. Une fois
    initalisé la fonction is_dist_avail_and_initialized retournera True.

    Parameters
    ----------
    dist_url: str (="env://")
        URL spécifiant comment initialiser le groupe de processus. Par défaut
        env:// est utilisé.
    backend: str (="nccl")
        Type de backend utilisé pour la paralléisation multi GPU multi node.
        Le backend nccl est très conseillé car il est performant et stable
        quelque soit le cas de figure (simple/multi node(s)). Le backend
        NCCL est spécifique pour le multi-GPU et GLOO spécifique au
        multi-CPU. Voir la documentation PyTorch pour les autres backend
        possible.
    """
    try:
        rank = int(os.environ['RANK'])
        world_size = int(os.environ['WORLD_SIZE'])
        local_rank = int(os.environ['LOCAL_RANK'])
    except KeyError as e:
        warn(
            f"La variable {e} non présent dans les variables d'environnement."
        )
        return None
    dist.init_process_group(
        backend=backend.lower(),
        init_method=dist_url,
        world_size=world_size,
        rank=rank
    )
    torch.cuda.set_device(local_rank)
    dist.barrier()
    return local_rank


def _overload_distributed_data_parallel(
    model: Module,
    master_class: Optional[Callable] = None
):
    r"""
    Fonction qui vien surchargé la classe
    torch.nn.parallel.DistributedDataParallel afin de s'interfacer avec
    les classes DSTK. Pour connaitre les arguements de cette classe ce
    référer à la doc PyTorch.

    Parameters
    ----------
    model: Module
        Modèle PyTorch vania ou hérité des classes DSTK.
    master_class: Optional[Callable]
        Classe mère que l'on souhaite faire hérité. Si cette variable est
        a None une recherce de maching sera exécutée sur les classes types
        de base de DSTK.
    """
    def gen_class(module):
        class DistributedDataParallel(DDP, module):
            def __init__(
                self,
                module,
                device_ids=None,
                output_device=None,
                dim=0,
                broadcast_buffers=True,
                process_group=None,
                bucket_cap_mb=25,
                find_unused_parameters=False,
                check_reduction=False,
                gradient_as_bucket_view=False,
                static_graph=False,
            ):
                super().__init__(
                    module=module,
                    device_ids=device_ids,
                    output_device=output_device,
                    dim=dim,
                    broadcast_buffers=broadcast_buffers,
                    process_group=process_group,
                    bucket_cap_mb=bucket_cap_mb,
                    find_unused_parameters=find_unused_parameters,
                    check_reduction=check_reduction,
                    gradient_as_bucket_view=gradient_as_bucket_view,
                    static_graph=static_graph,
                )
        return DistributedDataParallel

    if not master_class is None:
        return gen_class(master_class)

    mother_model = model.__class__.__bases__
    dstk_module = [BaseEnvironnement, BaseClassifier, BaseClassifierOnline,
                   BaseRegressor, BaseRegressorOnline]
    match = list(
        filter(
            lambda x: x[0] == x[1],
            product(mother_model, dstk_module)
        )
    )
    if len(match) == 0:
        return DDP
    elif len(match) == 1:
        return gen_class(match[0][1])
    else:
        match = list(filter(lambda x: x[0] != BaseEnvironnement, match))
        if len(match) == 1:
            return gen_class(match[0][1])
        else:
            raise AttributeError(
                "L'héritage du module PyTorch est incompatible avec le "
                "système d'hérithage de DSTK."
            )


def overload_distributed_data_parallel(model: Module):
    r"""
    Fonction qui vien surchargé la classe
    torch.nn.parallel.DistributedDataParallel afin de s'interfacer avec
    les classes DSTK. Pour connaitre les arguements de cette classe ce
    référer à la doc PyTorch.

    Parameters
    ----------
    model: Module
        Modèle PyTorch vania ou hérité des classes DSTK.
    """
    class DistributedDataParallel(DDP):
        def __init__(
            self,
            module,
            device_ids=None,
            output_device=None,
            dim=0,
            broadcast_buffers=True,
            process_group=None,
            bucket_cap_mb=25,
            find_unused_parameters=False,
            check_reduction=False,
            gradient_as_bucket_view=False,
            static_graph=False,
        ):
            super().__init__(
                module=module,
                device_ids=device_ids,
                output_device=output_device,
                dim=dim,
                broadcast_buffers=broadcast_buffers,
                process_group=process_group,
                bucket_cap_mb=bucket_cap_mb,
                find_unused_parameters=find_unused_parameters,
                check_reduction=check_reduction,
                gradient_as_bucket_view=gradient_as_bucket_view,
                static_graph=static_graph,
            )
    attr = list(filter(lambda x: not x.startswith('__'), dir(model)))
    attr_ddp = list(filter(lambda x: not x.startswith('__'), dir(DDP)))
    for ii in attr:
        if not ii in attr_ddp:
            setattr(DistributedDataParallel, ii, getattr(model, ii))
    return DistributedDataParallel


def auto_init_distributed(
    model: Module,
    train_dataset: Dataset,
    kwargs_train_dataloader: Dict[str, Any],
    eval_dataset: Optional[Dataset] = None,
    kwargs_eval_dataloader: Optional[Dict[str, Any]] = None,
    dist_url: str = "env://",
    backend: str = "nccl",
    seed: int = 42,
    master_class: Optional[Callable] = None
):
    r"""
    
    Parameters
    ----------
    model: Module
        Modèle PyTorch a paralléliser.
    train_dataset: Dataset
        Dataset d'entraînement.
    kwargs_train_dataloader: Dict[str, Any]
        Argument à destination du DataLoader du dataset d'entraînement.
    eval_dataset: Optional[Dataset]
        Dataset d'évaluation.
    kwargs_eval_dataloader: Optional[Dict[str, Any]]
        Argument à destination du DataLoader du dataset d'évaluation.
    dist_url: str (="env://")
        URL spécifiant comment initialiser le groupe de processus. Par défaut
        env:// est utilisé.
    backend: str (="nccl")
        Type de backend utilisé pour la paralléisation multi GPU multi node.
        Le backend nccl est très conseillé car il est performant et stable
        quelque soit le cas de figure (simple/multi node(s)). Le backend
        NCCL est spécifique pour le multi-GPU et GLOO spécifique au
        multi-CPU. Voir la documentation PyTorch pour les autres backend
        possible.
    seed: int (=42)
        Seed à destination du DistributedSampler afin de garantir que tous
        les processes aient la même seed pour le mélange (sinon les processes
        pourraient avoir des observations commune dans une eproch).
    master_class: Optional[Callable]
        Classe mère que l'on souhaite faire hérité. Si cette variable est
        a None une recherce de maching sera exécutée sur les classes de types
        de base de DSTK.

    Notes
    -----
    Il est important de bien initialiser PyTorch afin que tous les processes
    soit inialiser avec les mêmes poids aléatoires, sinon l'apprentissage
    sera inconsistant.

    >>> from dstk.utils import set_seed
    >>> from dstk.pytorch import auto_init_distributed
    >>> 
    >>> set_seed(42)
    >>> model, data = auto_init_distributed(model, dataset)
    >>> [...]
    """
    local_rank = init_distributed(
        dist_url=dist_url,
        backend=backend
    )
    if local_rank is None:
        warn(
            "Distribution des ressources impossible. Pocédure standard local "
            "utilisé."
        )
        train_data = DataLoader(train_dataset, **kwargs_train_dataloader)
        if eval_dataset:
            eval_data = DataLoader(eval_dataset, **kwargs_eval_dataloader)
            return model, train_data, eval_data
        return model, train_data

    model = model.cuda()
    model = SyncBatchNorm.convert_sync_batchnorm(model)
    # model = overload_distributed_data_parallel(model, master_class)(
    #     module=model,
    #     device_ids=[local_rank]
    # )
    model = overload_distributed_data_parallel(model)(
        module=model,
        device_ids=[local_rank]
    )
    shuffle = None
    drop_last = None
    if 'shuffle' in kwargs_train_dataloader:
        shuffle = kwargs_train_dataloader['shuffle']
        del kwargs_train_dataloader['shuffle']
    if 'drop_last' in kwargs_train_dataloader:
        drop_last = kwargs_train_dataloader['drop_last']
        del kwargs_train_dataloader['drop_last']
    train_sampler = DistributedSampler(
        dataset=train_dataset,
        shuffle=shuffle,
        drop_last=drop_last,
        seed=seed
    )
    train_data = DataLoader(
        dataset=train_dataset,
        sampler=train_sampler,
        shuffle=False,
        drop_last=False,
        **kwargs_train_dataloader
    )
    if eval_dataset:
        shuffle = None
        drop_last = None
        if 'shuffle' in kwargs_eval_dataloader:
            shuffle = kwargs_eval_dataloader['shuffle']
            del kwargs_eval_dataloader['shuffle']
        if 'drop_last' in kwargs_eval_dataloader:
            drop_last = kwargs_eval_dataloader['drop_last']
            del kwargs_eval_dataloader['drop_last']
        eval_sample = DistributedSampler(
            dataset=eval_dataset,
            shuffle=shuffle,
            drop_last=drop_last,
            seed=seed
        )
        eval_data = DataLoader(
            dataset=eval_dataset,
            sampler=eval_sample,
            shuffle=False,
            drop_last=False,
            **kwargs_eval_dataloader
        )
        return model, train_data, eval_data
    return model, train_data
