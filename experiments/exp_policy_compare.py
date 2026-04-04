"""Compare LRU and FIFO across default workloads."""

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
from simulator.workload import generate_default_workloads


def main() -> None:
    data_dir = ROOT / "results" / "data"
    fig_dir = ROOT / "results" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    policies = ["lru", "fifo"]
    capacity = 128
    workloads = generate_default_workloads(seed=2026)

    rows = []
    for workload_name, trace in workloads.items():
        for policy in policies:
            result = run_trace(
                trace=trace,
                policy_name=policy,
                capacity=capacity,
                workload_name=workload_name,
            )
            rows.append(result.to_dict())

    df = pd.DataFrame(rows).sort_values(["workload", "policy"])
    csv_path = data_dir / "policy_compare.csv"
    df.to_csv(csv_path, index=False)

    hit_pivot = df.pivot(index="workload", columns="policy", values="hit_rate")
    ax = hit_pivot.plot(kind="bar", figsize=(8, 5))
    ax.set_title(f"Cache Hit Rate by Workload and Policy (capacity={capacity})")
    ax.set_ylabel("Hit Rate")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    fig_hit = fig_dir / "policy_compare_hit_rate.png"
    plt.savefig(fig_hit, dpi=150)
    plt.close()

    rec_pivot = df.pivot(index="workload", columns="policy", values="recomputation_cost")
    ax = rec_pivot.plot(kind="bar", figsize=(8, 5))
    ax.set_title(f"Recomputation Cost by Workload and Policy (capacity={capacity})")
    ax.set_ylabel("Recomputation Cost")
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    fig_rec = fig_dir / "policy_compare_recompute_cost.png"
    plt.savefig(fig_rec, dpi=150)
    plt.close()

    print("Saved:", csv_path)
    print("Saved:", fig_hit)
    print("Saved:", fig_rec)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
