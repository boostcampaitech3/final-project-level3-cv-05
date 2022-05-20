import torch
import numpy as np
import random
import pytorch_lightning as pl
from pytorch_lightning.loggers import WandbLogger
import argparse
import yaml
from munch import Munch

from model import PostOCRLearner
from dataset import PostOCRDataLoader


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='./config.yaml')
    args = parser.parse_args()
    return args


def config(args):
    with open(args.config, 'r') as f:
        cfg = yaml.safe_load(f)
    return Munch(cfg)


def seed_everything(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # if use multi-GPU
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)
    random.seed(seed)


def main():
    args = get_parser()
    cfg = config(args)
    datamodule = PostOCRDataLoader(cfg, **cfg.Dataset)
    model = PostOCRLearner(cfg)
    logger = None
    callbacks = None
    trainer = pl.Trainer(
        logger=logger,
        callbacks=callbacks,
        max_epochs=cfg.epoch,
        **cfg.trainer
    )
    trainer.fit(model, datamodule=datamodule)


if __name__ == "__main__":
    main()
