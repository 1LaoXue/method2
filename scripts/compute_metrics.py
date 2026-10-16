"""Compute micro-accuracy and difficulty-balanced accuracy from complete records."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP, getcontext
from pathlib import Path


STRATA = ("low", "medium", "high")
GROUP_FIELDS = (
    "protocol_id",
    "split_id",
    "run_id",
    "model_id",
    "method_id",
    "condition_id",
    "pass_index",
    "sensitivity_setting_id",
)
REQUIRED_RESULT_FIELDS = set(GROUP_FIELDS) | {
    "episode_id",
    "question_id",
    "ground_truth",
    "final_answer",
    "final_correct",
    "metric_stratum_reference_id",
    "metric_stratum",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_jsonl(path: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    with path.open(encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            require(isinstance(value, dict), f"JSONL line {line_number} is not an object")
            records.append(value)
    require(bool(records), "result JSONL is empty")
    return records


def question_key(row: dict[str, object]) -> tuple[str, str]:
    return str(row["episode_id"]), str(row["question_id"])


def expected_test_keys(path: Path) -> set[tuple[str, str]]:
    rows = load_csv(path)
    keys = {
        (row["episode_id"], row["question_id"])
        for row in rows
        if row["split"] == "test"
    }
    require(len(keys) == 585, f"expected 585 test IDs, found {len(keys)}")
    return keys


def load_assignments(
    path: Path, expected_keys: set[tuple[str, str]]
) -> tuple[str, dict[tuple[str, str], str], dict[str, int]]:
    rows = load_csv(path)
    required = {
        "reference_assignment_id",
        "protocol_id",
        "split_id",
        "episode_id",
        "question_id",
        "difficulty_score",
        "difficulty_stratum",
    }
    require(bool(rows), "difficulty assignment CSV is empty")
    require(required <= set(rows[0]), f"difficulty CSV missing {sorted(required - set(rows[0]))}")
    ids = {row["reference_assignment_id"] for row in rows}
    require(len(ids) == 1, "difficulty CSV must contain one reference_assignment_id")
    reference_id = next(iter(ids))
    assignments: dict[tuple[str, str], str] = {}
    counts = {stratum: 0 for stratum in STRATA}
    for row in rows:
        key = (row["episode_id"], row["question_id"])
        require(key not in assignments, f"duplicate difficulty assignment for {key}")
        require(row["protocol_id"] == "muma-tom-main-qsplit-v1", f"wrong protocol for {key}")
        require(row["split_id"] == "muma-tom-main-qsplit-v1/test", f"wrong split for {key}")
        score = Decimal(row["difficulty_score"])
        require(Decimal(0) <= score <= Decimal(1), f"difficulty score out of range for {key}")
        expected_stratum = "low" if score < Decimal("0.30") else "medium" if score < Decimal("0.60") else "high"
        require(row["difficulty_stratum"] == expected_stratum, f"threshold mismatch for {key}")
        assignments[key] = expected_stratum
        counts[expected_stratum] += 1
    require(set(assignments) == expected_keys, "difficulty assignment IDs do not exactly cover the 585-question test split")
    require(all(counts[stratum] > 0 for stratum in STRATA), "difficulty assignment contains an empty stratum")
    return reference_id, assignments, counts


def decimal_ratio(numerator: int, denominator: int) -> Decimal:
    return Decimal(numerator) / Decimal(denominator)


def decimal_text(value: Decimal) -> str:
    return format(value, ".15f").rstrip("0").rstrip(".")


def render_percent(value: Decimal, decimals: int) -> str:
    quantum = Decimal(1).scaleb(-decimals)
    return f"{(value * 100).quantize(quantum, rounding=ROUND_HALF_UP):.{decimals}f}%"


def aggregate(
    records: list[dict[str, object]],
    assignments: dict[tuple[str, str], str],
    reference_id: str,
) -> list[dict[str, object]]:
    groups: dict[tuple[str, ...], list[dict[str, object]]] = defaultdict(list)
    for index, record in enumerate(records, start=1):
        missing = REQUIRED_RESULT_FIELDS - set(record)
        require(not missing, f"result record {index} missing {sorted(missing)}")
        group_key = tuple(str(record[field]) for field in GROUP_FIELDS)
        groups[group_key].append(record)

    summaries: list[dict[str, object]] = []
    expected_keys = set(assignments)
    for group_key in sorted(groups):
        group_records = groups[group_key]
        by_question: dict[tuple[str, str], dict[str, object]] = {}
        correct_by_stratum = {stratum: 0 for stratum in STRATA}
        total_by_stratum = {stratum: 0 for stratum in STRATA}
        for record in group_records:
            key = question_key(record)
            require(key not in by_question, f"duplicate result in group {group_key} for {key}")
            by_question[key] = record
            require(record["metric_stratum_reference_id"] == reference_id, f"wrong difficulty reference for {key}")
            stratum = assignments.get(key)
            require(stratum is not None, f"result key not in difficulty assignment: {key}")
            require(record["metric_stratum"] == stratum, f"result stratum mismatch for {key}")
            ground_truth = str(record["ground_truth"])
            final_answer = str(record["final_answer"])
            require(ground_truth in "ABCDE" and len(ground_truth) == 1, f"invalid ground truth for {key}")
            require(final_answer in {"A", "B", "C", "D", "E", "INVALID"}, f"invalid final answer for {key}")
            expected_correct = final_answer == ground_truth
            require(isinstance(record["final_correct"], bool), f"final_correct is not boolean for {key}")
            require(record["final_correct"] is expected_correct, f"final_correct mismatch for {key}")
            total_by_stratum[stratum] += 1
            correct_by_stratum[stratum] += int(expected_correct)
        require(set(by_question) == expected_keys, f"group {group_key} does not exactly cover all 585 assigned IDs")

        micro_correct = sum(correct_by_stratum.values())
        micro_total = sum(total_by_stratum.values())
        micro = decimal_ratio(micro_correct, micro_total)
        stratum_accuracy = {
            stratum: decimal_ratio(correct_by_stratum[stratum], total_by_stratum[stratum])
            for stratum in STRATA
        }
        db_accuracy = sum(stratum_accuracy.values(), Decimal(0)) / Decimal(3)
        summaries.append(
            {
                "group": dict(zip(GROUP_FIELDS, group_key)),
                "reference_assignment_id": reference_id,
                "n_low": total_by_stratum["low"],
                "n_medium": total_by_stratum["medium"],
                "n_high": total_by_stratum["high"],
                "correct_low": correct_by_stratum["low"],
                "correct_medium": correct_by_stratum["medium"],
                "correct_high": correct_by_stratum["high"],
                "stratum_accuracy": {key: decimal_text(value) for key, value in stratum_accuracy.items()},
                "difficulty_balanced_accuracy_exact": "(correct_low/n_low + correct_medium/n_medium + correct_high/n_high) / 3",
                "unrounded_difficulty_balanced_accuracy": decimal_text(db_accuracy),
                "integer_micro_correct": micro_correct,
                "integer_micro_total": micro_total,
                "unrounded_micro_accuracy": decimal_text(micro),
                "rendered": {
                    "table_4_percent": render_percent(db_accuracy, 2),
                    "table_6_percent": render_percent(db_accuracy, 2),
                    "table_7_percent": render_percent(db_accuracy, 1),
                },
            }
        )
    return summaries


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--difficulty-assignments", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--test-split", type=Path, default=root / "splits" / "main_question_split_v1.csv")
    return parser.parse_args()


def main() -> None:
    getcontext().prec = 40
    args = parse_args()
    results_path = args.results.resolve()
    assignment_path = args.difficulty_assignments.resolve()
    expected_keys = expected_test_keys(args.test_split.resolve())
    reference_id, assignments, assignment_counts = load_assignments(assignment_path, expected_keys)
    summaries = aggregate(load_jsonl(results_path), assignments, reference_id)
    output = {
        "schema_version": "1.0",
        "metric_definition": "configs/metrics.json",
        "results_input": {"path": str(args.results), "sha256": sha256(results_path)},
        "difficulty_assignment_input": {"path": str(args.difficulty_assignments), "sha256": sha256(assignment_path)},
        "reference_assignment_id": reference_id,
        "assignment_counts": assignment_counts,
        "group_count": len(summaries),
        "groups": summaries,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"metric groups: {len(summaries)}")


if __name__ == "__main__":
    main()
