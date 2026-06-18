#!/usr/bin/env python3
"""
TSCG LittleBigBrain – Comparative Benchmark
"""

import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

import argparse
import random
import numpy as np
from scipy import stats
import torch

from src.models import StandardLLM, TSCGLLM
from src.trainer import train_model, evaluate_on_test, compute_delta
from src.auto_learning import AutoLearningCycle
from tests.test_api_client import TscgAPIClient


def prepare_training_data(poclets_list):
    data = []
    for p in poclets_list:
        target = np.array([
            float(p.get('A', 0.0)), float(p.get('S', 0.0)), float(p.get('F', 0.0)),
            float(p.get('It', 0.0)), float(p.get('D', 0.0)),
            float(p.get('R', 0.0)), float(p.get('E', 0.0)), float(p.get('V', 0.0)),
            float(p.get('O', 0.0)), float(p.get('Im', 0.0))
        ], dtype=np.float32)
        label = p.get('label', '')
        rng = np.random.RandomState(hash(label) % 2**32)
        input_vec = torch.tensor(rng.randn(1, 20)).float()
        target_tensor = torch.tensor(target).float().unsqueeze(0)
        data.append((input_vec, target_tensor))
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--cycles", type=int, default=3)
    args = parser.parse_args()

    print("=" * 70)
    print("TSCG LittleBigBrain – Benchmark")
    print("=" * 70)

    # Chemin vers le dossier "instances" à la racine du dépôt tscg
    # Depuis tests/test_benchmark.py, remonter 4 niveaux : tests -> TscgLittleBigBrain -> tscg-tools -> instances
    instances_root = Path(__file__).parent.parent.parent.parent
    if not instances_root.exists() or instances_root.name != "instances":
        # Fallback : si le nom n'est pas "instances", on essaie de le trouver
        instances_root = Path(__file__).parent.parent.parent.parent / "instances"
    if instances_root.exists():
        m0_paths = str(instances_root)
        print(f"📁 Loading M0 instances from: {instances_root}")
    else:
        print(f"⚠️  Instances directory not found at {instances_root}")
        m0_paths = ""

    api = TscgAPIClient(host=args.host, port=args.port, m0_dir=m0_paths)
    if not api.is_running():
        print(f"❌ API server not reachable at {api.base_url}")
        return

    print("✅ Connected to TSCG ontology API")
    poclets_data = api.get_poclets_with_scores()
    if not poclets_data:
        print("❌ No poclets found.")
        return
    print(f"📦 {len(poclets_data)} poclets loaded")

    random.shuffle(poclets_data)
    split = int(0.8 * len(poclets_data))
    train_poclets = poclets_data[:split]
    test_poclets = poclets_data[split:]

    train_data = prepare_training_data(train_poclets)

    results = {"standard": {"deltas": []}, "tscg": {"deltas": []}}

    for run in range(args.runs):
        print(f"\n🏁 Run {run+1}/{args.runs}")

        # Standard LLM
        model_std = StandardLLM()
        train_model(model_std, train_data, epochs=args.epochs)
        init_delta_std = evaluate_on_test(model_std, test_poclets, lambda p: torch.randn(1,20), compute_delta)
        print(f"  Standard – initial δ: {init_delta_std:.4f}")
        auto_std = AutoLearningCycle(model_std, api, train_data.copy(), "standard", threshold=0.15)
        auto_std.run_cycles(n_cycles=args.cycles, candidates_per_cycle=5, epochs_per_retrain=15)
        final_delta_std = evaluate_on_test(model_std, test_poclets, lambda p: torch.randn(1,20), compute_delta)
        print(f"  Standard – final δ:   {final_delta_std:.4f}")

        # TSCG LLM
        model_tscg = TSCGLLM()
        train_model(model_tscg, train_data, epochs=args.epochs)
        init_delta_tscg = evaluate_on_test(model_tscg, test_poclets, lambda p: torch.randn(1,20), compute_delta)
        print(f"  TSCG     – initial δ: {init_delta_tscg:.4f}")
        auto_tscg = AutoLearningCycle(model_tscg, api, train_data.copy(), "tscg", threshold=0.15)
        auto_tscg.run_cycles(n_cycles=args.cycles, candidates_per_cycle=5, epochs_per_retrain=15)
        final_delta_tscg = evaluate_on_test(model_tscg, test_poclets, lambda p: torch.randn(1,20), compute_delta)
        print(f"  TSCG     – final δ:   {final_delta_tscg:.4f}")

        results["standard"]["deltas"].append({"init": init_delta_std, "final": final_delta_std})
        results["tscg"]["deltas"].append({"init": init_delta_tscg, "final": final_delta_tscg})

    std_improvements = [d["init"] - d["final"] for d in results["standard"]["deltas"]]
    tscg_improvements = [d["init"] - d["final"] for d in results["tscg"]["deltas"]]
    std_final = [d["final"] for d in results["standard"]["deltas"]]
    tscg_final = [d["final"] for d in results["tscg"]["deltas"]]

    print("\n" + "="*70)
    print("📊 FINAL RESULTS")
    print("="*70)
    print(f"Improvement (initial - final):")
    print(f"  Standard: {np.mean(std_improvements):.4f} ± {np.std(std_improvements):.4f}")
    print(f"  TSCG:     {np.mean(tscg_improvements):.4f} ± {np.std(tscg_improvements):.4f}")
    print(f"\nFinal δ after recursive cycles:")
    print(f"  Standard: {np.mean(std_final):.4f} ± {np.std(std_final):.4f}")
    print(f"  TSCG:     {np.mean(tscg_final):.4f} ± {np.std(tscg_final):.4f}")

    t_stat, p_value = stats.ttest_ind(tscg_final, std_final)
    print(f"\nt-test on final δ: t = {t_stat:.4f}, p = {p_value:.4f}")
    if p_value < 0.05:
        print("✅ REJECT H0 – TSCG provides statistically significant improvement.")
    else:
        print("❌ CANNOT REJECT H0 – No significant difference detected.")

    print("\n🏁 Benchmark finished.")


if __name__ == "__main__":
    main()