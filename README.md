# kvcache-sim

A lightweight Python simulator for studying KV-cache behavior under LLM-like inference workloads.

This project models token-block cache accesses (not real model tensors/heads) and compares basic eviction policies.

## Features

- Fixed-capacity KV-cache simulator (capacity in blocks)
- Eviction policies:
  - LRU
  - FIFO
- Synthetic LLM-like workloads:
  - short prompts
  - long-context generation
  - multi-turn conversations
- Metrics:
  - cache hit rate
  - miss rate
  - recomputation cost (default miss cost = 1)
- Experiment scripts for CSV outputs and matplotlib visualizations
- Lightweight pytest suite

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
    metrics.py
    runner.py
  experiments/
    exp_policy_compare.py
    exp_cache_size_sweep.py
  tests/
    test_cache.py
    test_policies.py
    test_workloads.py
  results/
    figures/
    data/
```

## Setup

1. Create and activate a virtual environment (optional but recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Run

Run one simulation from the CLI entrypoint:

```bash
python3 main.py --workload short_prompt --policy lru --capacity 128
```

## Run Tests

```bash
python3 -m pytest -q
```

## Run Experiments

Policy comparison across default workloads:

```bash
python3 experiments/exp_policy_compare.py
```

Cache size sweep:

```bash
python3 experiments/exp_cache_size_sweep.py
```

## Outputs

- CSV files are saved to `results/data/`
- Figures are saved to `results/figures/`

Expected output files:

- `results/data/policy_compare.csv`
- `results/data/cache_size_sweep.csv`
- `results/figures/policy_compare_hit_rate.png`
- `results/figures/policy_compare_recompute_cost.png`
- `results/figures/cache_size_sweep_hit_rate.png`

## Notes

- Deterministic random seeds are used by default for reproducibility.
- Misses add recomputation cost by default (`cost=1` per miss).
- This is a simulator only; it does not run real LLM inference.
