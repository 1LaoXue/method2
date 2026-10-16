"""Compute participant accuracy and complete-case Fleiss' kappa."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from decimal import Decimal, getcontext
from pathlib import Path


LABELS = ("A", "B", "C", "D", "E")
PARTICIPANTS = tuple(f"P{i:02d}" for i in range(1, 7))
REQUIRED_FIELDS = {
    "participant_id",
    "presentation_order",
    "episode_id",
    "question_id",
    "response",
    "ground_truth",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def decimal_text(value: Decimal) -> str:
    return format(value, ".15f").rstrip("0").rstrip(".")


def fleiss_kappa(items: list[list[str]]) -> float | None:
    if len(items) < 2:
        return None
    n = len(items[0])
    require(n == 6 and all(len(item) == n for item in items), "complete-case item does not contain six ratings")
    counts = [Counter(item) for item in items]
    observed = sum((sum(count[label] ** 2 for label in LABELS) - n) / (n * (n - 1)) for count in counts) / len(counts)
    category_proportions = {
        label: sum(count[label] for count in counts) / (len(counts) * n)
        for label in LABELS
    }
    expected = sum(value * value for value in category_proportions.values())
    denominator = 1.0 - expected
    if abs(denominator) < 1e-15:
        return None
    return (observed - expected) / denominator


def quantile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def bootstrap_kappa(items: list[list[str]], resamples: int, seed: int) -> tuple[float, float]:
    rng = random.Random(seed)
    values: list[float] = []
    attempts = 0
    max_attempts = resamples * 100
    while len(values) < resamples and attempts < max_attempts:
        attempts += 1
        sample = [items[rng.randrange(len(items))] for _ in items]
        value = fleiss_kappa(sample)
        if value is not None and math.isfinite(value):
            values.append(value)
    require(len(values) == resamples, "could not obtain the configured number of nondegenerate bootstrap replicates")
    return quantile(values, 0.025), quantile(values, 0.975)


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--responses", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--participant-output", type=Path, required=True)
    parser.add_argument("--subset", type=Path, default=root / "splits" / "human_reference_subset_100_v1.csv")
    parser.add_argument("--question-index", type=Path, default=root / "splits" / "question_index.csv")
    parser.add_argument("--bootstrap-resamples", type=int, default=10000)
    parser.add_argument("--bootstrap-seed", type=int, default=84726111)
    return parser.parse_args()


def main() -> None:
    getcontext().prec = 40
    args = parse_args()
    response_path = args.responses.resolve()
    rows = read_csv(response_path)
    require(bool(rows), "response CSV is empty")
    require(REQUIRED_FIELDS <= set(rows[0]), f"response CSV missing {sorted(REQUIRED_FIELDS - set(rows[0]))}")
    subset_rows = read_csv(args.subset.resolve())
    subset_keys = {(row["episode_id"], row["question_id"]) for row in subset_rows}
    require(len(subset_keys) == 100, "human subset must contain 100 unique question IDs")
    index_rows = read_csv(args.question_index.resolve())
    truth_by_key = {(row["episode_id"], row["question_id"]): row["correct_option"] for row in index_rows}

    by_participant: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_question: dict[tuple[str, str], dict[str, str]] = defaultdict(dict)
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        participant = row["participant_id"]
        key = (row["episode_id"], row["question_id"])
        record_key = (participant, *key)
        require(participant in PARTICIPANTS, f"unexpected participant ID {participant}")
        require(key in subset_keys, f"response outside fixed subset: {key}")
        require(record_key not in seen, f"duplicate response: {record_key}")
        seen.add(record_key)
        require(row["response"] in {*LABELS, "ABSTAIN"}, f"invalid response for {record_key}")
        require(row["ground_truth"] == truth_by_key[key], f"ground truth mismatch for {record_key}")
        by_participant[participant].append(row)
        by_question[key][participant] = row["response"]

    require(set(by_participant) == set(PARTICIPANTS), "responses must contain P01 through P06")
    participant_summaries: list[dict[str, object]] = []
    accuracy_values: list[Decimal] = []
    for participant in PARTICIPANTS:
        participant_rows = by_participant[participant]
        keys = {(row["episode_id"], row["question_id"]) for row in participant_rows}
        orders = {int(row["presentation_order"]) for row in participant_rows}
        require(keys == subset_keys, f"{participant} does not cover the fixed 100-question subset")
        require(orders == set(range(1, 101)), f"{participant} presentation_order must be 1 through 100")
        abstained = sum(row["response"] == "ABSTAIN" for row in participant_rows)
        answered = 100 - abstained
        require(answered > 0, f"{participant} has zero answered questions")
        correct = sum(row["response"] == row["ground_truth"] for row in participant_rows)
        accuracy = Decimal(correct) / Decimal(answered)
        accuracy_values.append(accuracy)
        participant_summaries.append(
            {
                "participant_id": participant,
                "assigned": 100,
                "answered": answered,
                "abstained": abstained,
                "correct_answered": correct,
                "accuracy": decimal_text(accuracy),
            }
        )

    complete_items = [
        [responses[participant] for participant in PARTICIPANTS]
        for key, responses in sorted(by_question.items())
        if set(responses) == set(PARTICIPANTS)
        and all(responses[participant] in LABELS for participant in PARTICIPANTS)
    ]
    kappa = fleiss_kappa(complete_items)
    require(kappa is not None, "Fleiss' kappa is undefined for the complete-case responses")
    ci_low, ci_high = bootstrap_kappa(complete_items, args.bootstrap_resamples, args.bootstrap_seed)
    mean_accuracy = sum(accuracy_values, Decimal(0)) / Decimal(6)

    args.participant_output.parent.mkdir(parents=True, exist_ok=True)
    with args.participant_output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(participant_summaries[0]))
        writer.writeheader()
        writer.writerows(participant_summaries)

    summary = {
        "schema_version": "1.0",
        "responses_input": {"path": str(args.responses), "sha256": sha256(response_path)},
        "participant_accuracy_definition": "correct_answered/answered",
        "group_accuracy_definition": "unweighted mean of six participant accuracies",
        "participants": participant_summaries,
        "mean_individual_accuracy": decimal_text(mean_accuracy),
        "fleiss_kappa": kappa,
        "kappa_complete_case_questions": len(complete_items),
        "kappa_excluded_questions_with_abstention": 100 - len(complete_items),
        "kappa_missing_response_policy": "complete_case_questions_only",
        "kappa_95_percentile_bootstrap_ci": [ci_low, ci_high],
        "bootstrap_resamples": args.bootstrap_resamples,
        "bootstrap_seed": args.bootstrap_seed,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"mean individual accuracy: {decimal_text(mean_accuracy)}")
    print(f"complete-case questions: {len(complete_items)}")


if __name__ == "__main__":
    main()
