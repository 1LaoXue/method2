"""Generate deterministic MuMA-ToM reproducibility split manifests."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path


TYPES = ("belief", "social-goal", "goal-belief")
SPLITS = ("memory", "validation", "test")
PROVENANCE = "release_assignment_v1"
PROTOCOL_IDS = {
    "main": "muma-tom-main-qsplit-v1",
    "episode": "muma-tom-episode-disjoint-v1",
    "repeat": "muma-tom-repeat550-v1",
    "human": "muma-tom-human100-v1",
    "confidence": "controlled-confidence-consistency-v1",
}
SEEDS = {
    "main_question_split": 73194217,
    "episode_disjoint_split": 18465031,
    "repeated_run_subset": 59280463,
    "human_reference_subset": 31847029,
}


def numeric(value: str) -> int:
    return int(value)


def question_key(row: dict[str, str]) -> tuple[str, str]:
    return row["episode_id"], row["question_id"]


def question_sort(row: dict[str, str]) -> tuple[int, int]:
    return numeric(row["episode_id"]), numeric(row["question_id"])


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def type_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    counts = Counter(row["paper_question_type"] for row in rows)
    return {question_type: counts[question_type] for question_type in TYPES}


def stratified_subset(
    rows: list[dict[str, str]], counts: dict[str, int], seed: int
) -> list[dict[str, str]]:
    rng = random.Random(seed)
    selected: list[dict[str, str]] = []
    for question_type in TYPES:
        pool = sorted(
            (row for row in rows if row["paper_question_type"] == question_type),
            key=question_sort,
        )
        rng.shuffle(pool)
        selected.extend(pool[: counts[question_type]])
    return selected


def main_allocation(rows: list[dict[str, str]]) -> dict[tuple[str, str], str]:
    rng = random.Random(SEEDS["main_question_split"])
    assignment: dict[tuple[str, str], str] = {}
    for question_type in TYPES:
        pool = sorted(
            (row for row in rows if row["paper_question_type"] == question_type),
            key=question_sort,
        )
        rng.shuffle(pool)
        for index, row in enumerate(pool):
            split = "memory" if index < 75 else "validation" if index < 105 else "test"
            assignment[question_key(row)] = split
    return assignment


def episode_allocation(
    rows: list[dict[str, str]],
) -> tuple[dict[str, str], dict[str, list[dict[str, str]]]]:
    by_episode: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_episode[row["episode_id"]].append(row)

    patterns: dict[tuple[int, int, int], list[str]] = defaultdict(list)
    for episode_id, episode_rows in by_episode.items():
        counts = Counter(row["paper_question_type"] for row in episode_rows)
        patterns[tuple(counts[t] for t in TYPES)].append(episode_id)
    expected_patterns = {(2, 2, 0): 150, (0, 0, 4): 75}
    if {pattern: len(ids) for pattern, ids in patterns.items()} != expected_patterns:
        raise ValueError("Unexpected episode/question-type composition")

    rng = random.Random(SEEDS["episode_disjoint_split"])
    assignment: dict[str, str] = {}
    for pattern, memory_count, validation_count in (
        ((2, 2, 0), 37, 15),
        ((0, 0, 4), 19, 8),
    ):
        episode_ids = sorted(patterns[pattern], key=numeric)
        rng.shuffle(episode_ids)
        for index, episode_id in enumerate(episode_ids):
            split = (
                "memory"
                if index < memory_count
                else "validation"
                if index < memory_count + validation_count
                else "test"
            )
            assignment[episode_id] = split
    return assignment, by_episode


def split_summary(
    rows: list[dict[str, str]], assignment: dict[tuple[str, str], str]
) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for split in SPLITS:
        selected = [row for row in rows if assignment[question_key(row)] == split]
        result[split] = {"questions": len(selected), "per_type": type_counts(selected)}
    return result


def validate(
    rows: list[dict[str, str]],
    main_split: dict[tuple[str, str], str],
    episode_split: dict[str, str],
    subset_550: list[dict[str, str]],
    subset_100: list[dict[str, str]],
) -> None:
    source_keys = {question_key(row) for row in rows}
    if len(rows) != 900 or len(source_keys) != 900:
        raise ValueError("Expected 900 unique questions")
    if len({row["episode_id"] for row in rows}) != 225:
        raise ValueError("Expected 225 unique episodes")
    if type_counts(rows) != {question_type: 300 for question_type in TYPES}:
        raise ValueError("Expected 300 questions per type")
    if Counter(main_split.values()) != {"memory": 225, "validation": 90, "test": 585}:
        raise ValueError("Main split count mismatch")
    if Counter(episode_split.values()) != {"memory": 56, "validation": 23, "test": 146}:
        raise ValueError("Episode split count mismatch")
    episode_question_counts = Counter(episode_split[row["episode_id"]] for row in rows)
    if episode_question_counts != {"memory": 224, "validation": 92, "test": 584}:
        raise ValueError("Episode-disjoint question count mismatch")
    test_keys = {key for key, split in main_split.items() if split == "test"}
    for subset, expected_size in ((subset_550, 550), (subset_100, 100)):
        keys = {question_key(row) for row in subset}
        if len(subset) != expected_size or len(keys) != expected_size or not keys <= test_keys:
            raise ValueError(f"Invalid subset of size {expected_size}")


def build(source: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = sorted(list(csv.DictReader(handle)), key=question_sort)

    main_split = main_allocation(rows)
    episode_split, by_episode = episode_allocation(rows)
    test_rows = [row for row in rows if main_split[question_key(row)] == "test"]
    subset_550 = stratified_subset(
        test_rows, dict(zip(TYPES, (184, 183, 183))), SEEDS["repeated_run_subset"]
    )
    subset_100 = stratified_subset(
        test_rows, dict(zip(TYPES, (34, 33, 33))), SEEDS["human_reference_subset"]
    )
    validate(rows, main_split, episode_split, subset_550, subset_100)

    main_rows = []
    episode_question_rows = []
    for row in rows:
        key = question_key(row)
        split = main_split[key]
        main_rows.append(
            {
                "provenance": PROVENANCE,
                "protocol_id": PROTOCOL_IDS["main"],
                "split_id": f'{PROTOCOL_IDS["main"]}/{split}',
                "episode_id": row["episode_id"],
                "question_id": row["question_id"],
                "question_type": row["paper_question_type"],
                "split": split,
            }
        )
        ed_split = episode_split[row["episode_id"]]
        episode_question_rows.append(
            {
                "provenance": PROVENANCE,
                "protocol_id": PROTOCOL_IDS["episode"],
                "split_id": f'{PROTOCOL_IDS["episode"]}/{ed_split}',
                "episode_id": row["episode_id"],
                "question_id": row["question_id"],
                "question_type": row["paper_question_type"],
                "split": ed_split,
            }
        )

    common_fields = [
        "provenance",
        "protocol_id",
        "split_id",
        "episode_id",
        "question_id",
        "question_type",
        "split",
    ]
    write_csv(output_dir / "main_question_split_v1.csv", common_fields, main_rows)
    write_csv(
        output_dir / "episode_disjoint_questions_v1.csv",
        common_fields,
        episode_question_rows,
    )

    episode_rows = [
        {
            "provenance": PROVENANCE,
            "protocol_id": PROTOCOL_IDS["episode"],
            "split_id": f'{PROTOCOL_IDS["episode"]}/{episode_split[episode_id]}',
            "episode_id": episode_id,
            "split": episode_split[episode_id],
            "question_count": len(by_episode[episode_id]),
        }
        for episode_id in sorted(by_episode, key=numeric)
    ]
    write_csv(
        output_dir / "episode_disjoint_episodes_v1.csv",
        ["provenance", "protocol_id", "split_id", "episode_id", "split", "question_count"],
        episode_rows,
    )

    def subset_rows(
        subset: list[dict[str, str]], subset_id: str
    ) -> list[dict[str, object]]:
        return [
            {
                "provenance": PROVENANCE,
                "subset_id": subset_id,
                "parent_split_id": f'{PROTOCOL_IDS["main"]}/test',
                "selection_order": index,
                "episode_id": row["episode_id"],
                "question_id": row["question_id"],
                "question_type": row["paper_question_type"],
            }
            for index, row in enumerate(subset, start=1)
        ]

    subset_fields = [
        "provenance",
        "subset_id",
        "parent_split_id",
        "selection_order",
        "episode_id",
        "question_id",
        "question_type",
    ]
    write_csv(
        output_dir / "repeated_run_subset_550_v1.csv",
        subset_fields,
        subset_rows(subset_550, PROTOCOL_IDS["repeat"]),
    )
    write_csv(
        output_dir / "human_reference_subset_100_v1.csv",
        subset_fields,
        subset_rows(subset_100, PROTOCOL_IDS["human"]),
    )

    confidence_rows: list[dict[str, object]] = []
    selection_order = 1
    source_commit = "3f569b7ab1d0ee2702ab43ebdc724679d5fc5231"
    online_source = f"https://github.com/SCAI-JHU/AutoToM/blob/{source_commit}/experiment_2/online_goal_inference/eval_AutoToM.py"
    food_source = f"https://github.com/SCAI-JHU/AutoToM/blob/{source_commit}/experiment_2/food_truck_scenarios/eval_AutoToM.py"
    confidence_specs = (
        (
            "online_goal_inference",
            "baker-online-goal",
            tuple(str(index) for index in range(1, 7)),
            "all_scenarios",
            "Baker_et_al_2009_goal_inference_adapted_by_AutoToM",
            "online_goal",
            online_source,
        ),
        (
            "desire_inference",
            "baker-desire-type",
            ("1", "2", "5", "16", "18", "55", "56"),
            "one_representative_per_type",
            "Baker_et_al_2017_food_truck_adapted_by_AutoToM",
            "food_truck_desire",
            food_source,
        ),
        (
            "belief_inference",
            "baker-belief-type",
            ("1", "2", "5", "16", "18", "55", "56"),
            "one_representative_per_type",
            "Baker_et_al_2017_food_truck_adapted_by_AutoToM",
            "food_truck_belief",
            food_source,
        ),
    )
    for task, prefix, source_ids, rule, publication, source_task, source_path in confidence_specs:
        for type_index, source_id in enumerate(source_ids, start=1):
            confidence_rows.append(
                {
                    "provenance": "release_scenario_key_v1",
                    "protocol_id": PROTOCOL_IDS["confidence"],
                    "scenario_id": f"{prefix}-{type_index:02d}",
                    "task": task,
                    "scenario_type_index": type_index,
                    "selection_order": selection_order,
                    "selection_rule": rule,
                    "mapping_status": "RESOLVED",
                    "source_publication": publication,
                    "source_task": source_task,
                    "source_scenario_id": f"{'online_goal' if task == 'online_goal_inference' else 'food_truck'}{source_id}",
                    "source_stimulus_path_or_url": source_path,
                    "source_type_id": (
                        "NOT_APPLICABLE"
                        if task == "online_goal_inference"
                        else f"food_truck_source_key_{source_id}"
                    ),
                    "observation_sequence_id": f"{source_task}-{source_id}",
                }
            )
            selection_order += 1
    write_csv(
        output_dir / "confidence_consistency_scenarios_v1.csv",
        [
            "provenance",
            "protocol_id",
            "scenario_id",
            "task",
            "scenario_type_index",
            "selection_order",
            "selection_rule",
            "mapping_status",
            "source_publication",
            "source_task",
            "source_scenario_id",
            "source_stimulus_path_or_url",
            "source_type_id",
            "observation_sequence_id",
        ],
        confidence_rows,
    )

    generated_files = [
        "main_question_split_v1.csv",
        "episode_disjoint_episodes_v1.csv",
        "episode_disjoint_questions_v1.csv",
        "repeated_run_subset_550_v1.csv",
        "human_reference_subset_100_v1.csv",
        "confidence_consistency_scenarios_v1.csv",
    ]
    episode_question_assignment = {
        question_key(row): episode_split[row["episode_id"]] for row in rows
    }
    registry = {
        "schema_version": "1.0",
        "dataset": "MuMA-ToM",
        "source_index_file": "question_index.csv",
        "source_index_sha256": sha256(source),
        "provenance": {
            "profile_type": "frozen_reproducibility_protocol",
            "assignment_origin": "deterministic_release_assignment_from_canonical_dataset_index",
        },
        "randomization": {
            "implementation": "Python random.Random(seed).shuffle",
            "initial_order": "numeric episode_id then numeric question_id",
            "question_type_order": list(TYPES),
            "seeds": SEEDS,
        },
        "protocols": {
            PROTOCOL_IDS["main"]: {
                "allocation_unit": "question",
                "episode_disjoint": False,
                "assignments_file": "main_question_split_v1.csv",
                "counts": split_summary(rows, main_split),
            },
            PROTOCOL_IDS["episode"]: {
                "allocation_unit": "episode",
                "episode_disjoint": True,
                "episode_assignments_file": "episode_disjoint_episodes_v1.csv",
                "question_assignments_file": "episode_disjoint_questions_v1.csv",
                "episode_counts": {
                    split: Counter(episode_split.values())[split] for split in SPLITS
                },
                "counts": split_summary(rows, episode_question_assignment),
            },
        },
        "subsets": {
            PROTOCOL_IDS["repeat"]: {
                "parent_split_id": f'{PROTOCOL_IDS["main"]}/test',
                "assignments_file": "repeated_run_subset_550_v1.csv",
                "questions": 550,
                "per_type": type_counts(subset_550),
            },
            PROTOCOL_IDS["human"]: {
                "parent_split_id": f'{PROTOCOL_IDS["main"]}/test',
                "assignments_file": "human_reference_subset_100_v1.csv",
                "questions": 100,
                "per_type": type_counts(subset_100),
            },
        },
        "controlled_scenarios": {
            PROTOCOL_IDS["confidence"]: {
                "assignments_file": "confidence_consistency_scenarios_v1.csv",
                "total_scenarios": 20,
                "per_task": {
                    "online_goal_inference": 6,
                    "desire_inference": 7,
                    "belief_inference": 7,
                },
            }
        },
        "subset_overlap_questions": len(
            {question_key(row) for row in subset_550}
            & {question_key(row) for row in subset_100}
        ),
        "files": {
            name: {"sha256": sha256(output_dir / name)} for name in generated_files
        },
    }
    write_json(output_dir / "split_registry_v1.json", registry)
    print(json.dumps(registry, ensure_ascii=False, indent=2))


def parse_args() -> argparse.Namespace:
    default_source = Path(__file__).resolve().parent / "question_index.csv"
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=default_source)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    build(args.source.resolve(), args.output_dir.resolve())
