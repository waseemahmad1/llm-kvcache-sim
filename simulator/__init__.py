"""KV-cache simulator package."""

from simulator.cache import CacheEntry, KVCacheSimulator
from simulator.policies import FIFOPolicy, LRUPolicy
from simulator.runner import SimulationResult, run_trace
from simulator.workload import (
    generate_default_workloads,
    generate_long_context_workload,
    generate_multiturn_workload,
    generate_short_prompt_workload,
)

__all__ = [
    "CacheEntry",
    "FIFOPolicy",
    "KVCacheSimulator",
    "LRUPolicy",
    "SimulationResult",
    "generate_default_workloads",
    "generate_long_context_workload",
    "generate_multiturn_workload",
    "generate_short_prompt_workload",
    "run_trace",
]
