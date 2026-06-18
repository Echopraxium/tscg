import torch
import torch.nn as nn
import numpy as np
from typing import Tuple

class StandardLLM(nn.Module):
    def __init__(self, input_dim: int = 20, hidden_dim: int = 64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 10),
            nn.Sigmoid()
        )
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)
    def predict(self, x: torch.Tensor) -> Tuple[np.ndarray, np.ndarray]:
        out = self.forward(x).detach().cpu().numpy().squeeze()
        return out[:5], out[5:]

class TSCGLLM(nn.Module):
    def __init__(self, input_dim: int = 20, hidden_dim: int = 64):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        self.territory_head = nn.Linear(hidden_dim, 5)
        self.map_head = nn.Linear(hidden_dim, 5)
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        h = self.encoder(x)
        return torch.sigmoid(self.territory_head(h)), torch.sigmoid(self.map_head(h))
    def predict(self, x: torch.Tensor) -> Tuple[np.ndarray, np.ndarray]:
        a, r = self.forward(x)
        return a.detach().cpu().numpy().squeeze(), r.detach().cpu().numpy().squeeze()