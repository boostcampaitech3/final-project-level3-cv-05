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

    logger = WandbLogger(project="project name", entity="wandb id", name='running name')
    
    """ 
    [ Checkpoint Callback ]

    filepath: 체크포인트 저장위치와 이름 형식을 지정
    verbose: 체크포인트 저장 결과를 출력
    save_last: 마지막 체크포인트를 저장
    save_top_k: 최대 몇 개의 체크포인트를 저장할지 지정(save_last에 의해 저장되는 체크포인트는 제외)
    monitor: 어떤 metric을 기준으로 체크포인트를 저장할지 지정
    ['train_loss', 'train_accuracy', 'val_loss', 'val_accuracy', 'epoch', 'step']
    mode: 지정한 metric의 어떤 기준(ex. min, max)으로 체크포인트를 저장할지 지정
    """   
    callbacks = pl.callbacks.ModelCheckpoint(filename='{epoch}_{val_accuracy:.4f}',save_top_k=2, monitor='val_accuracy', mode='max')

    trainer = pl.Trainer(
        logger=logger,
        callbacks=callbacks,
        max_epochs=cfg.epoch,
        **cfg.trainer
    )
    trainer.fit(model, datamodule=datamodule)


if __name__ == "__main__":
    main()
