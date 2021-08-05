import os

import torch
import torch.nn as nn
from torch.nn.functional import relu

from project_files.constants import GAMMA, LEARNING_RATE


class Model(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()

        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = relu(self.layer1(x))
        x = self.layer2(x)

        return x

    def save(self, filename='model.pth'):
        print(filename)
        torch.save(self.state_dict(), filename)


class Trainer:
    def __init__(self, model):
        self.model = model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over):
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)
            game_over = (game_over, )

        # get predicted values with current state
        pred = self.model(state)

        # newQ = Reward + y * max(next_predicted)
        target = pred.clone()
        for idx in range(len(game_over)):
            q_new = reward[idx]

            if not game_over[idx]:
                q_new = reward[idx] + GAMMA * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action).item()] = q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()
