"""Compute per-task confidence correlations with scenario-clustered intervals."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from collections import defaultdict
from pathlib import Path


REQUIRED_FIELDS = {
    "protocol_id",
    "scenario_id",
    "observation_sequence_id",
    "task",
    "timepoint_index",
    "model_id",
    "model_score",
    "human_rating",
    "human_rating_scale_min",
    "human_rating_scale_max",
}
SOURCE_FIELDS = (
    "source_publication",
    "source_task",
    "source_scenario_id",
    "source_stimulus_path_or_url",
    "source_type_id",
    "observation_sequence_id",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pearson(pairs: list[tuple[float, float]]) -> float | None:
    if len(pairs) < 2:
        return None
    xs = [pair[0] for pair in pairs]
    ys = [pair[1] for pair in pairs]
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    covariance = sum((x - mean_x) * (y - mean_y) for x, y in pairs)
    sum_x = sum((x - mean_x) ** 2 for x in xs)
    sum_y = sum((y - mean_y) ** 2 for y in ys)
    denominator = math.sqrt(sum_x * sum_y)
    if denominator == 0:
        return None
    return covariance / denominator


def quantile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def clustered_interval(
    by_scenario: dict[str, list[tuple[float, float]]], resamples: int, rng: random.Random
) -> tuple[float, float]:
    scenario_ids = sorted(by_scenario)
    require(len(scenario_ids) >= 2, "clustered bootstrap requires at least two scenarios")
    values: list[float] = []
    attempts = 0
    while len(values) < resamples and attempts < resamples * 100:
        attempts += 1
        pairs: list[tuple[float, float]] = []
        for _ in scenario_ids:
            pairs.extend(by_scenario[rng.choice(scenario_ids)])
        value = pearson(pairs)
        if value is not None and math.isfinite(value):
            values.append(value)
    require(len(values) == resamples, "could not obtain all nondegenerate bootstrap replicates")
    return quantile(values, 0.025), quantile(values, 0.975)


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--observations", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scenario-map", type=Path, default=root / "splits" / "confidence_consistency_scenarios_v1.csv")
    parser.add_argument("--bootstrap-resamples", type=int, default=5000)
    parser.add_argument("--bootstrap-seed", type=int, default=84726111)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    observation_path = args.observations.resolve()
    mapping_path = args.scenario_map.resolve()
    mapping_rows = read_csv(mapping_path)
    require(len(mapping_rows) == 20, "scenario map must contain 20 rows")
    mapping: dict[str, dict[str, str]] = {}
    for row in mapping_rows:
        scenario_id = row["scenario_id"]
        require(scenario_id not in mapping, f"duplicate scenario mapping {scenario_id}")
        require(row.get("mapping_status") == "RESOLVED", f"source mapping is unresolved for {scenario_id}")
        for field in SOURCE_FIELDS:
            value = row.get(field, "").strip()
            require(value and not value.startswith("UNRESOLVED"), f"missing {field} for {scenario_id}")
        mapping[scenario_id] = row

    rows = read_csv(observation_path)
    require(bool(rows), "observation CSV is empty")
    require(REQUIRED_FIELDS <= set(rows[0]), f"observation CSV missing {sorted(REQUIRED_FIELDS - set(rows[0]))}")
    seen: set[tuple[str, str, int, str]] = set()
    grouped: dict[tuple[str, str], dict[str, list[tuple[float, float]]]] = defaultdict(lambda: defaultdict(list))
    human_by_timepoint: dict[tuple[str, int], tuple[float, float, float]] = {}
    for row in rows:
        scenario_id = row["scenario_id"]
        require(scenario_id in mapping, f"unknown scenario ID {scenario_id}")
        mapped = mapping[scenario_id]
        require(row["protocol_id"] == "controlled-confidence-consistency-v1", f"wrong protocol for {scenario_id}")
        require(row["task"] == mapped["task"], f"task mismatch for {scenario_id}")
        require(row["observation_sequence_id"] == mapped["observation_sequence_id"], f"sequence mismatch for {scenario_id}")
        timepoint = int(row["timepoint_index"])
        require(timepoint > 0, f"nonpositive timepoint for {scenario_id}")
        key = (scenario_id, row["observation_sequence_id"], timepoint, row["model_id"])
        require(key not in seen, f"duplicate observation {key}")
        seen.add(key)
        model_score = float(row["model_score"])
        human_rating = float(row["human_rating"])
        scale_min = float(row["human_rating_scale_min"])
        scale_max = float(row["human_rating_scale_max"])
        require(all(math.isfinite(value) for value in (model_score, human_rating, scale_min, scale_max)), f"nonfinite value for {key}")
        require(0.0 <= model_score <= 1.0, f"model score outside [0,1] for {key}")
        require(scale_min < scale_max and scale_min <= human_rating <= scale_max, f"invalid human scale/rating for {key}")
        human_key = (scenario_id, timepoint)
        human_value = (human_rating, scale_min, scale_max)
        if human_key in human_by_timepoint:
            require(human_by_timepoint[human_key] == human_value, f"human rating differs across models for {human_key}")
        else:
            human_by_timepoint[human_key] = human_value
        grouped[(row["task"], row["model_id"])][scenario_id].append((model_score, human_rating))

    rng = random.Random(args.bootstrap_seed)
    summaries: list[dict[str, object]] = []
    expected_scenarios_by_task: dict[str, set[str]] = defaultdict(set)
    for scenario_id, row in mapping.items():
        expected_scenarios_by_task[row["task"]].add(scenario_id)
    for (task, model_id), by_scenario in sorted(grouped.items()):
        require(set(by_scenario) == expected_scenarios_by_task[task], f"{task}/{model_id} does not cover every mapped scenario")
        for scenario_id, pairs_for_scenario in by_scenario.items():
            require(len(pairs_for_scenario) >= 2, f"{task}/{model_id}/{scenario_id} has fewer than two timepoints")
        pairs = [pair for scenario_id in sorted(by_scenario) for pair in by_scenario[scenario_id]]
        value = pearson(pairs)
        require(value is not None, f"Pearson correlation is undefined for {task}/{model_id}")
        ci_low, ci_high = clustered_interval(by_scenario, args.bootstrap_resamples, rng)
        summaries.append(
            {
                "task": task,
                "model_id": model_id,
                "scenario_clusters": len(by_scenario),
                "sequential_observations": len(pairs),
                "pearson_r": value,
                "scenario_clustered_95_percentile_bootstrap_ci": [ci_low, ci_high],
            }
        )

    output = {
        "schema_version": "1.0",
        "observations_input": {"path": str(args.observations), "sha256": sha256(observation_path)},
        "scenario_map_input": {"path": str(args.scenario_map), "sha256": sha256(mapping_path)},
        "bootstrap_resamples": args.bootstrap_resamples,
        "bootstrap_seed": args.bootstrap_seed,
        "results": summaries,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"confidence correlation groups: {len(summaries)}")


if __name__ == "__main__":
    main()
