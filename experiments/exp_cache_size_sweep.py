"""Sweep cache sizes and compare policies on one workload."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "results" / ".mplconfig"))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from simulator.runner import run_trace
from simulator.workload import generate_long_context_workload


def main() -> None:
    data_dir = ROOT / "results" / "data"
    fig_dir = ROOT / "results" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    capacities = [32, 64, 128, 256, 512]
    policies = ["lru", "fifo"]
    workload_name = "long_context"
    trace = generate_long_context_workload(seed=2026)

    rows = []
    for cap in capacities:
        for policy in policies:
            result = run_trace(
                trace=trace,
                policy_name=policy,
                capacity=cap,
                workload_name=workload_name,
            )
            rows.append(result.to_dict())

    df = pd.DataFrame(rows).sort_values(["policy", "capacity"])
    csv_path = data_dir / "cache_size_sweep.csv"
    df.to_csv(csv_path, index=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    for policy in policies:
        sub = df[df["policy"] == policy]
        ax.plot(sub["capacity"], sub["hit_rate"], marker="o", label=policy.upper())

    ax.set_title(f"Hit Rate vs Cache Size ({workload_name})")
    ax.set_xlabel("Cache Capacity (blocks)")
    ax.set_ylabel("Hit Rate")
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.25)
    ax.legend()
    plt.tight_layout()
    fig_path = fig_dir / "cache_size_sweep_hit_rate.png"
    plt.savefig(fig_path, dpi=150)
    plt.close()

    print("Saved:", csv_path)
    print("Saved:", fig_path)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
