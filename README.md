# kvcache-sim

A lightweight Python simulator for studying KV-cache behavior under LLM-like inference workloads.

This repository now includes:
- 75% baseline: fixed-capacity cache + LRU/FIFO + synthetic workloads + plots.
- 100% extension: MOONCAKE-inspired shared global cache across concurrent requests.
- 125% extension: adaptive, cost-aware eviction under workload shift and memory pressure.

## Features

- Fixed-capacity cache simulator (capacity measured in blocks)
- Eviction policies:
  - FIFO
  - LRU
  - Adaptive cost-aware (shared-global mode)
- Workload types:
  - short prompt
  - multi-turn conversation
  - long context
  - concurrent multi-request shared-prefix stream
  - shifted concurrent stream (phase1 -> phase2)
- Metrics:
  - total accesses, hits, misses
  - hit rate, miss rate
  - recomputation cost
  - workload summaries (unique blocks, reuse ratio, etc.)
- Reproducible multi-seed evaluation (default 15 seeds in experiment scripts)

## Project Structure

```text
kvcache-sim/
  main.py
  requirements.txt
  README.md
  simulator/
    __init__.py
    cache.py
    policies.py
    workload.py
    runner.py
    global_workload.py
    global_cache.py
  experiments/
    exp_policy_compare.py
    exp_cache_size_sweep.py
    exp_shared_global_cache.py
    exp_shared_global_sensitivity.py
    exp_adaptive_controller.py
  tests/
    test_cache.py
    test_policies.py
    test_workloads.py
    test_runner.py
    test_global_workload.py
    test_global_cache.py
  results/
    data/
    figures/
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Tests

Run from the project root (`kvcache-sim/`):

```bash
python3 -m pytest -q
```

## Run Experiments

75% baseline experiments:

```bash
python3 experiments/exp_policy_compare.py
python3 experiments/exp_cache_size_sweep.py
```

100% shared global cache experiment:

```bash
python3 experiments/exp_shared_global_cache.py
```

100% robustness/sensitivity sweep (shared-prefix intensity + concurrency):

```bash
python3 experiments/exp_shared_global_sensitivity.py
```

125% adaptive controller experiment:

```bash
python3 experiments/exp_adaptive_controller.py
```

The adaptive experiment now evaluates robustness across:
- shift severities: `moderate`, `hard`
- capacities: `256`, `384`, `512`
- 15 seeds per setting

Adaptive policy behavior:
- pressure-aware admission control (limits low-value inserts during miss pressure)
- dynamic eviction weighting (becomes more recency-responsive under high miss rate)
- cost-aware retention of expensive/shared-prefix blocks when useful

## Reproducibility

- Synthetic generators are deterministic for a fixed seed.
- Experiment scripts use fixed seed ranges (15 seeds) and report mean/std.
- Running the same script with unchanged code yields identical outputs.

## Output Files

Experiment CSV files are saved under `results/data/` and figures under `results/figures/`.

Key outputs include:
- `policy_compare*.csv`, `cache_size_sweep*.csv`
- `shared_global_compare*.csv`
- `shared_global_sensitivity*.csv`
- `adaptive_controller*.csv`
- `*_summary*.csv`
- corresponding `*.png` figures

## Notes

- This is a simulator only; it does not run real LLM inference.
- Cache entries are modeled at token-block granularity.
- Recomputation cost is modeled per miss (cost may vary by block type in shared-global experiments).
