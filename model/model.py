import torch
import torch.nn as nn
from timm import create_model


class BackboneBlock(nn.Module):
    def __init__(self, backbone, output_feature: int = 1024, pretrained: bool = True):
        super(BackboneBlock, self).__init__()
        self.feature = create_model(backbone, num_classes=output_feature, pretrained=pretrained)

    def forward(self, x):
        return self.feature(x)


class MlpBlock(nn.Module):
    def __init__(self, input_channel, output_channel, depth):
        super(MlpBlock, self).__init__()
        layers = self._build_layers(input_channel, output_channel, depth)
        self.feature = nn.Sequential(*layers)

    def forward(self, x):
        return self.feature(x)

    def _build_layers(self, input_channel, output_channel, depth) -> list:
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
                 output_feature: int,
                 depth: int):
        super(PostOCRModel, self).__init__()
        self.cnn_feature = BackboneBlock(backbone, backbone_out_feature)
        self.mlp_feature = MlpBlock(input_feature, mlp_out_feature, depth)
        self.classifier = MlpBlock(backbone_out_feature + mlp_out_feature, output_feature, depth)

    def forward(self, x, tab):
        """
        :param x: image inputs (batch_size, 3, height, weight)
        :param tab: tabular inputs (batch_size, input_feature_size)
        :return: (batch_size, labels)
        """
        x_feature = self.cnn_feature(x)
        tab_feature = self.mlp_feature(tab)
        feature = torch.concat((x_feature, tab_feature))
        output = self.classifier(feature)
        return output
