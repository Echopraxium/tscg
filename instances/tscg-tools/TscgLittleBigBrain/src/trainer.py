import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import List, Tuple, Dict, Callable
from .models import StandardLLM, TSCGLLM

def train_model(model, train_data: List[Tuple[torch.Tensor, torch.Tensor]],
                epochs: int = 30, lr: float = 0.001, verbose: bool = False) -> float:
    if not train_data:
        print("  Warning: empty training data, skipping training.")
        return 0.0

    # Filtrage simple : juste vérifier que les tenseurs existent
    valid_data = []
    for x, target in train_data:
        if x is None or target is None:
            continue
        if not isinstance(x, torch.Tensor) or not isinstance(target, torch.Tensor):
            continue
        if x.numel() == 0 or target.numel() == 0:
            continue
        valid_data.append((x, target))

    if not valid_data:
        print("  Warning: no valid training samples after filtering, skipping training.")
        return 0.0

    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    for epoch in range(epochs):
        total_loss = 0.0
        for x, target in valid_data:
            optimizer.zero_grad()
            if isinstance(model, StandardLLM):
                pred = model(x)
                loss = criterion(pred.squeeze(), target.squeeze())
            else:
                a_pred, r_pred = model(x)
                loss = criterion(a_pred.squeeze(), target[:,:5].squeeze()) + \
                       criterion(r_pred.squeeze(), target[:,5:].squeeze())
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        avg_loss = total_loss / len(valid_data)
        if verbose and (epoch+1) % 10 == 0:
            print(f"  Epoch {epoch+1}/{epochs}, loss={avg_loss:.4f}")
    return avg_loss

def evaluate_on_test(model, test_poclets: List[Dict], input_generator: Callable, delta_func: Callable) -> float:
    if not test_poclets:
        return 0.0
    deltas = []
    for poc in test_poclets:
        x = input_generator(poc)
        asfid, revoi = model.predict(x)
        deltas.append(delta_func(asfid, revoi))
    return np.mean(deltas)

def compute_delta(asfid: np.ndarray, revoi: np.ndarray) -> float:
    mean_asfid = np.mean(asfid)
    mean_revoi = np.mean(revoi)
    return abs(mean_asfid - mean_revoi) / np.sqrt(2)