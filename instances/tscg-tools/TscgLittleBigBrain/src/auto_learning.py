import torch
import numpy as np
from typing import List, Tuple, Dict
from .trainer import train_model

class AutoLearningCycle:
    def __init__(self, model, api_client, train_data: List[Tuple[torch.Tensor, torch.Tensor]],
                 model_type: str, threshold: float = 0.15, input_dim: int = 384):
        self.model = model
        self.api = api_client
        self.train_data = train_data
        self.model_type = model_type
        self.threshold = threshold
        self.input_dim = input_dim

    def run_cycles(self, n_cycles: int = 5, candidates_per_cycle: int = 10, epochs_per_retrain: int = 20):
        for cycle in range(n_cycles):
            candidates = []
            for _ in range(candidates_per_cycle):
                x = torch.randn(1, self.input_dim)
                asfid, revoi = self.model.predict(x)
                candidate = {
                    "asfid": {k: float(asfid[i]) for i,k in enumerate(['A','S','F','It','D'])},
                    "revoi": {k: float(revoi[i]) for i,k in enumerate(['R','E','V','O','Im'])}
                }
                candidates.append(candidate)
            valid = []
            for cand in candidates:
                try:
                    val = self.api.validate_poclet(cand)
                    if val.get('delta', 1.0) < self.threshold:
                        valid.append(cand)
                except:
                    pass
            if not valid:
                print(f"  Cycle {cycle+1}: no valid candidates, stopping.")
                break
            for cand in valid:
                target = np.concatenate([
                    [cand['asfid'][k] for k in ['A','S','F','It','D']],
                    [cand['revoi'][k] for k in ['R','E','V','O','Im']]
                ])
                target_tensor = torch.tensor(target).float().unsqueeze(0)
                input_tensor = torch.randn(1, self.input_dim)
                self.train_data.append((input_tensor, target_tensor))
            if self.train_data:
                loss = train_model(self.model, self.train_data, epochs=epochs_per_retrain)
                print(f"  Cycle {cycle+1}: {len(valid)} valid, loss={loss:.4f}")
            else:
                print(f"  Cycle {cycle+1}: no training data, skipping retrain.")