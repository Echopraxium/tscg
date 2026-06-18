#!/usr/bin/env python3
"""
TSCG LittleBigBrain – Comparative Benchmark with Cross-Validation
"""

import sys
from pathlib import Path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

import argparse
import numpy as np
from scipy import stats
import torch
from sklearn.model_selection import KFold
from sentence_transformers import SentenceTransformer

from src.models import StandardLLM, TSCGLLM
from src.trainer import train_model, compute_delta
from src.auto_learning import AutoLearningCycle
from tests.test_api_client import TscgAPIClient

# Charger l'encodeur une fois
try:
    _embedder = SentenceTransformer('all-MiniLM-L6-v2')
    EMBEDDING_DIM = 384
    print("✅ SentenceTransformer loaded (embedding dim = 384)")
except Exception as e:
    print(f"⚠️  Could not load sentence transformer: {e}. Falling back to random vectors (20 dim).")
    _embedder = None
    EMBEDDING_DIM = 20

def get_embedding(text: str) -> np.ndarray:
    if _embedder is None or not text:
        return np.random.randn(EMBEDDING_DIM).astype(np.float32)
    return _embedder.encode(text, convert_to_numpy=True).astype(np.float32)

def prepare_data(poclets_list):
    X = []
    y = []
    for p in poclets_list:
        text = p.get('comment', p.get('label', ''))
        if not text:
            text = p.get('label', '')
        embedding = get_embedding(text)
        X.append(torch.tensor(embedding).float())
        target = np.array([
            float(p.get('A', 0.0)), float(p.get('S', 0.0)), float(p.get('F', 0.0)),
            float(p.get('It', 0.0)), float(p.get('D', 0.0)),
            float(p.get('R', 0.0)), float(p.get('E', 0.0)), float(p.get('V', 0.0)),
            float(p.get('O', 0.0)), float(p.get('Im', 0.0))
        ], dtype=np.float32)
        y.append(torch.tensor(target).float())
    return X, y

def evaluate_model_on_fold(model, train_X, train_y, test_X, test_y, api, cycles=3):
    train_data = [(x.unsqueeze(0), y.unsqueeze(0)) for x, y in zip(train_X, train_y)]
    train_model(model, train_data, epochs=30, verbose=False)
    deltas_test = []
    for x, y_true in zip(test_X, test_y):
        x_in = x.unsqueeze(0)
        asfid, revoi = model.predict(x_in)
        delta = compute_delta(asfid, revoi)
        deltas_test.append(delta)
    init_delta = np.mean(deltas_test)
    if cycles > 0:
        auto = AutoLearningCycle(model, api, train_data.copy(), "tscg", threshold=0.15, input_dim=EMBEDDING_DIM)
        auto.run_cycles(n_cycles=cycles, candidates_per_cycle=5, epochs_per_retrain=15)
    deltas_test = []
    for x, y_true in zip(test_X, test_y):
        x_in = x.unsqueeze(0)
        asfid, revoi = model.predict(x_in)
        delta = compute_delta(asfid, revoi)
        deltas_test.append(delta)
    final_delta = np.mean(deltas_test)
    return init_delta, final_delta

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--folds", type=int, default=5, help="Number of folds for cross-validation")
    parser.add_argument("--runs", type=int, default=None, help="Alias for --folds (compatibility)")
    parser.add_argument("--cycles", type=int, default=3, help="Auto-learning cycles per fold")
    parser.add_argument("--epochs", type=int, default=30, help="Initial training epochs")
    args = parser.parse_args()

    # Compatibility: if --runs is provided, use it as folds
    if args.runs is not None:
        args.folds = args.runs

    print("="*70)
    print("TSCG LittleBigBrain – Benchmark with Cross-Validation")
    print("="*70)

    api = TscgAPIClient(host=args.host, port=args.port, m0_dir="")
    if not api.is_running():
        print(f"❌ API server not reachable at {api.base_url}")
        return

    print("✅ Connected to TSCG ontology API")
    poclets_data = api.get_poclets_with_scores()
    if not poclets_data:
        print("❌ No poclets found.")
        return
    print(f"📦 {len(poclets_data)} poclets loaded")

    X_all, y_all = prepare_data(poclets_data)
    kf = KFold(n_splits=args.folds, shuffle=True, random_state=42)

    std_init_deltas = []
    std_final_deltas = []
    tscg_init_deltas = []
    tscg_final_deltas = []

    fold = 1
    for train_idx, test_idx in kf.split(X_all):
        print(f"\n🏁 Fold {fold}/{args.folds}")
        train_X = [X_all[i] for i in train_idx]
        train_y = [y_all[i] for i in train_idx]
        test_X = [X_all[i] for i in test_idx]
        test_y = [y_all[i] for i in test_idx]

        # Standard LLM
        model_std = StandardLLM(input_dim=EMBEDDING_DIM)
        init_std, final_std = evaluate_model_on_fold(
            model_std, train_X, train_y, test_X, test_y, api, cycles=args.cycles
        )
        std_init_deltas.append(init_std)
        std_final_deltas.append(final_std)
        print(f"  Standard – initial δ: {init_std:.4f}  final δ: {final_std:.4f}")

        # TSCG LLM
        model_tscg = TSCGLLM(input_dim=EMBEDDING_DIM)
        init_tscg, final_tscg = evaluate_model_on_fold(
            model_tscg, train_X, train_y, test_X, test_y, api, cycles=args.cycles
        )
        tscg_init_deltas.append(init_tscg)
        tscg_final_deltas.append(final_tscg)
        print(f"  TSCG     – initial δ: {init_tscg:.4f}  final δ: {final_tscg:.4f}")

        fold += 1

    print("\n" + "="*70)
    print("📊 CROSS-VALIDATION RESULTS (final δ only)")
    print("="*70)
    print(f"Standard LLM final δ: mean = {np.mean(std_final_deltas):.4f} ± {np.std(std_final_deltas):.4f}")
    print(f"TSCG LLM final δ:     mean = {np.mean(tscg_final_deltas):.4f} ± {np.std(tscg_final_deltas):.4f}")

    t_stat, p_value = stats.ttest_rel(std_final_deltas, tscg_final_deltas)
    print(f"\nPaired t-test (folds): t = {t_stat:.4f}, p = {p_value:.4f}")
    if p_value < 0.05:
        print("✅ REJECT H0 – TSCG provides statistically significant improvement.")
    else:
        print("❌ CANNOT REJECT H0 – No significant difference detected.")

    w_stat, p_w = stats.wilcoxon(std_final_deltas, tscg_final_deltas, alternative='two-sided')
    print(f"Wilcoxon signed-rank test: W = {w_stat:.1f}, p = {p_w:.4f}")
    if p_w < 0.05:
        print("✅ REJECT H0 (Wilcoxon) – TSCG improves.")
    else:
        print("❌ CANNOT REJECT H0 (Wilcoxon) – No significant difference.")

    print("\n🏁 Benchmark finished.")

if __name__ == "__main__":
    main()