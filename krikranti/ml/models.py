import torch
import torch.nn as nn
import torch.nn.functional as F


class ImageClassificationBase(nn.Module):
    def training_step(self, batch):
        images, labels = batch
        out = self(images)  # Generate predictions
        loss = F.cross_entropy(out, labels)  # Calculate loss
        return loss


def conv_block(in_channels, out_channels, pool=False):
    layers = [nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
              nn.BatchNorm2d(out_channels),
              nn.ReLU(inplace=True)]
    if pool: layers.append(nn.MaxPool2d(2))
    return nn.Sequential(*layers)


class ResNet9(ImageClassificationBase):
    def __init__(self, in_channels, num_classes):
        super().__init__()
        # Input : 3 * 32 * 32
        self.conv1 = conv_block(in_channels, 64)  # 64 * 32 * 32
        self.conv2 = conv_block(64, 128, pool=True)  # 128 * 16 * 16
        self.res1 = nn.Sequential(conv_block(128, 128),
                                  conv_block(128, 128))  # 128 * 16 * 16

        self.conv3 = conv_block(128, 256, pool=True)  # 256 * 8 * 8
        self.conv4 = conv_block(256, 512, pool=True)  #  512 * 4 * 4
        self.res2 = nn.Sequential(conv_block(512, 512),
                                  conv_block(512, 512))  # 512 * 4 *4

        self.classifier = nn.Sequential(nn.MaxPool2d(4),  # 512 * 1 * 1
                                        nn.Flatten(),  # 512
                                        nn.Dropout(0.2),
                                        nn.Linear(512, num_classes))

    def forward(self, xb):
        out = self.conv1(xb)
        out = self.conv2(out)
        out = self.res1(out) + out
        out = self.conv3(out)
        out = self.conv4(out)
        out = self.res2(out) + out
        out = self.classifier(out)
        return out
