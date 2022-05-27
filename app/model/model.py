from typing import List

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torchmetrics
from munch import Munch
from pytorch_lightning import LightningModule
from timm import create_model

from loss import create_criterion


class BackboneBlock(nn.Module):
    def __init__(self, backbone, output_feature: int = 1024, pretrained: bool = True):
        super(BackboneBlock, self).__init__()
        self.feature = create_model(backbone, num_classes=output_feature, pretrained=pretrained)

    def forward(self, x):
        return self.feature(x)


class MlpBlock(nn.Module):
    def __init__(self, input_channel, output_channel, depth):
        super(MlpBlock, self).__init__()
        layers = self.build_layers(input_channel, output_channel, depth)
        self.feature = nn.Sequential(*layers)

    def forward(self, x):
        return self.feature(x)

    def build_layers(self, input_channel: int, output_channel: int, depth: int) -> List[nn.Module]:
        """
        :param input_channel: input size of first layer
        :param output_channel: output size of last layer
        :param depth: number of layers
        :return: [nn.Module] * depth
        """
        layers = [nn.Linear(input_channel, 1024)]
        for i in range(depth - 2):
            layers.append(nn.Linear(1024, 1024))
        layers.append(nn.Linear(1024, output_channel))
        return layers


class PostOCRModel(nn.Module):
    def __init__(self,
                 backbone: str,
                 input_feature: int,
                 backbone_out_feature: int,
                 mlp_out_feature: int,
                 num_classes: int,
                 depth: int):
        super(PostOCRModel, self).__init__()
        self.cnn_feature = BackboneBlock(backbone, backbone_out_feature)
        self.mlp_feature = MlpBlock(input_feature, mlp_out_feature, depth)
        self.classifier = MlpBlock(backbone_out_feature + mlp_out_feature, num_classes, depth)
        self.accuracy = torchmetrics.Accuracy()

    def forward(self, x, tab):
        """
        :param x: image inputs (batch_size, 3, height, weight)
        :param tab: tabular inputs (batch_size, input_feature_size)
        :return: (batch_size, labels)
        """
        x_feature = self.cnn_feature(x)
        tab_feature = self.mlp_feature(tab)
        feature = torch.concat((x_feature, tab_feature), 1)
        output = self.classifier(feature)
        return output


class PostOCRLearner(LightningModule):
    def __init__(self, cfg: Munch):
        super(PostOCRLearner, self).__init__()
        self.cfg = cfg
        self.feature = PostOCRModel(**cfg.Model)
        self._criterion = create_criterion(cfg.Loss)
        self.learning_rate = self.cfg.learning_rate
        self.accuracy = torchmetrics.Accuracy()

    def forward(self, x, tabs):
        return self.feature(x, tabs)

    def training_step(self, batch, batch_idx):
        preds, loss, acc, labels = self.__share_step(batch, 'train')
        self.log("train_loss", loss)
        self.log("train_accuracy", acc)
        return {"loss": loss, "pred": preds.detach(), 'labels': labels.detach()}

    def validation_step(self, batch, batch_idx):
        preds, loss, acc, labels = self.__share_step(batch, 'val')
        self.log("val_loss", loss)
        self.log("val_accuracy", acc)
        return {"loss": loss, "pred": preds, 'labels': labels}

    def __share_step(self, batch, mode):
        x, tabs, y = batch
        pred = self.feature(x, tabs)
        loss = self._criterion(pred, y)
        acc = self.accuracy(pred, y)
        return pred, loss, acc, y

    # def training_epoch_end(self, outputs):
    #     pass
    #
    # def validation_epoch_end(self, outputs):
    #     pass
    #
    # def __cal_metrics(self, outputs, mode) -> None:
    #     pass

    def configure_optimizers(self):
        optimizer = eval(self.cfg.optim['name'])(
            self.parameters(), lr=self.learning_rate)
        scheduler = eval(self.cfg.sche['name'])(
            optimizer,
            **self.cfg.sche['params']
        )
        return [optimizer], [scheduler]
