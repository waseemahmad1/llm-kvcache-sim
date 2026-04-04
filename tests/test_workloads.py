from simulator.workload import (
    generate_default_workloads,
    generate_long_context_workload,
    generate_multiturn_workload,
    generate_short_prompt_workload,
)


def test_short_workload_is_deterministic() -> None:
    t1 = generate_short_prompt_workload(num_requests=100, seed=11)
    t2 = generate_short_prompt_workload(num_requests=100, seed=11)
    assert t1 == t2
    assert len(t1) == 100


def test_long_context_workload_sanity() -> None:
    trace = generate_long_context_workload(num_requests=250, seed=5)
    assert len(trace) == 250
    assert any(k.startswith("long_anchor_") for k in trace)
    assert any(k.startswith("long_block_") for k in trace)


def test_multiturn_workload_sanity() -> None:
    trace = generate_multiturn_workload(num_turns=3, turn_length=20, seed=9)
    assert len(trace) == 60
    assert any(k.startswith("system_block_") for k in trace)
    assert any(k.startswith("turn_1_block_") for k in trace)


def test_default_workloads_have_expected_keys() -> None:
    workloads = generate_default_workloads(seed=0)
    assert set(workloads) == {"short_prompt", "long_context", "multiturn"}
    assert all(len(trace) > 0 for trace in workloads.values())
