import sys
sys.path.append('..')
from utils import *

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class VnChessNNet(nn.Module):
    def __init__(self, game, args):
        #Game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        super(VnChessNNet, self).__init__()


    def Net_init(self):
        '''
        Init cnn of model
        '''
        self.conv1 = nn.Conv2d(1, self.args.num_channels, 3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(self.args.num_channels, self.args.num_channels, 3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(self.args.num_channels, self.args.num_channels, 3, stride=1)
        self.conv4 = nn.Conv2d(self.args.num_channels, self.args.num_channels, 3, stride=1)

        self.bn1 = nn.BatchNorm2d(self.args.num_channels)
        self.bn2 = nn.BatchNorm2d(self.args.num_channels)
        self.bn3 = nn.BatchNorm2d(self.args.num_channels)
        self.bn4 = nn.BatchNorm2d(self.args.num_channels)

        self.fc1 = nn.Linear(self.args.num_channels*(self.board_x-4)*(self.board_y-4), 1024)
        self.fc_bn1 = nn.BatchNorm1d(1024)

        self.fc2 = nn.Linear(1024, 512)
        self.fc_bn2 = nn.BatchNorm1d(512)

        self.fc3 = nn.Linear(512, self.action_size)

        self.fc4 = nn.Linear(512, 1)
    
    def forward(self, s):
        #state shape: (batch_size, board_x, board_y)

        s = s.view(-1, 1, self.board_x, self.board_y)
        #convert to (batch_size, channels, board_x, board_y)

        s = F.relu(self.bn1(self.conv1(s)))
        #(batch_size, num_channels, board_x, board_y)

        s = 

