"""Validate the package; update checksums only when explicitly requested."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TYPES = ("belief", "social-goal", "goal-belief")
RESULT_KEY = [
    "protocol_id",
    "run_id",
    "model_id",
    "method_id",
    "condition_id",
    "pass_index",
    "sensitivity_setting_id",
    "episode_id",
    "question_id",
]
CONFIDENCE_SOURCE_FIELDS = (
    "source_publication",
    "source_task",
    "source_scenario_id",
    "source_stimulus_path_or_url",
    "source_type_id",
    "observation_sequence_id",
)


def load_csv(name: str) -> list[dict[str, str]]:
    with (ROOT / "splits" / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON root must be an object: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair(row: dict[str, str]) -> tuple[str, str]:
    return row["episode_id"], row["question_id"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_splits(require_completed_evidence: bool) -> None:
    source = load_csv("question_index.csv")
    episode_index = load_csv("episode_index.csv")
    main = load_csv("main_question_split_v1.csv")
    episodes = load_csv("episode_disjoint_episodes_v1.csv")
    episode_questions = load_csv("episode_disjoint_questions_v1.csv")
    repeat = load_csv("repeated_run_subset_550_v1.csv")
    human = load_csv("human_reference_subset_100_v1.csv")
    confidence = load_csv("confidence_consistency_scenarios_v1.csv")

    require(len(source) == len({pair(row) for row in source}) == 900, "source index uniqueness")
    require(len(episode_index) == len({row["episode_id"] for row in episode_index}) == 225, "source episode index uniqueness")
    require(len(main) == len({pair(row) for row in main}) == 900, "main split uniqueness")
    require(len(episodes) == len({row["episode_id"] for row in episodes}) == 225, "episode uniqueness")
    require(len(episode_questions) == len({pair(row) for row in episode_questions}) == 900, "episode-question uniqueness")
    require(Counter(row["split"] for row in main) == {"memory": 225, "validation": 90, "test": 585}, "main counts")
    require(Counter(row["split"] for row in episodes) == {"memory": 56, "validation": 23, "test": 146}, "episode counts")
    require(Counter(row["split"] for row in episode_questions) == {"memory": 224, "validation": 92, "test": 584}, "episode-question counts")

    source_by_key = {pair(row): row for row in source}
    require(set(source_by_key) == {pair(row) for row in main}, "main split/source membership")
    require(set(source_by_key) == {pair(row) for row in episode_questions}, "episode split/source membership")
    require(all(row["question_type"] == source_by_key[pair(row)]["paper_question_type"] for row in main), "main question-type mapping")
    require(Counter(row["paper_question_type"] for row in source) == {question_type: 300 for question_type in TYPES}, "source per-type counts")
    require(all(row["correct_option"] in {"A", "B", "C", "D", "E"} for row in source), "source answer labels")
    require(all(int(row["question_count"]) == 4 for row in episode_index), "episode index question counts")

    for split, expected in {
        "memory": {"belief": 75, "social-goal": 75, "goal-belief": 75},
        "validation": {"belief": 30, "social-goal": 30, "goal-belief": 30},
        "test": {"belief": 195, "social-goal": 195, "goal-belief": 195},
    }.items():
        require(Counter(row["question_type"] for row in main if row["split"] == split) == expected, f"main per-type counts for {split}")

    episode_sets = {
        split: {row["episode_id"] for row in episodes if row["split"] == split}
        for split in ("memory", "validation", "test")
    }
    require(not (episode_sets["memory"] & episode_sets["validation"]), "memory/validation episode overlap")
    require(not (episode_sets["memory"] & episode_sets["test"]), "memory/test episode overlap")
    require(not (episode_sets["validation"] & episode_sets["test"]), "validation/test episode overlap")

    main_test = {pair(row) for row in main if row["split"] == "test"}
    for rows, size, name in ((repeat, 550, "repeat"), (human, 100, "human")):
        keys = {pair(row) for row in rows}
        require(len(rows) == len(keys) == size, f"{name} subset uniqueness")
        require(keys <= main_test, f"{name} subset membership")

    require({row["protocol_id"] for row in main} == {"muma-tom-main-qsplit-v1"}, "main protocol ID")
    require({row["protocol_id"] for row in episodes} == {"muma-tom-episode-disjoint-v1"}, "episode protocol ID")
    require({row["subset_id"] for row in repeat} == {"muma-tom-repeat550-v1"}, "repeat subset ID")
    require({row["subset_id"] for row in human} == {"muma-tom-human100-v1"}, "human subset ID")
    require(len(confidence) == len({row["scenario_id"] for row in confidence}) == 20, "confidence scenario uniqueness")
    require(Counter(row["task"] for row in confidence) == {"online_goal_inference": 6, "desire_inference": 7, "belief_inference": 7}, "confidence scenario counts")
    require({row["protocol_id"] for row in confidence} == {"controlled-confidence-consistency-v1"}, "confidence protocol ID")
    for row in confidence:
        require(row["mapping_status"] in {"RESOLVED", "UNRESOLVED_SOURCE_MAPPING"}, f"invalid mapping status for {row['scenario_id']}")
        require(all(row.get(field, "").strip() for field in CONFIDENCE_SOURCE_FIELDS), f"missing mapping field for {row['scenario_id']}")
        if require_completed_evidence:
            require(row["mapping_status"] == "RESOLVED", f"completed evidence has unresolved scenario {row['scenario_id']}")
            require(all(not row[field].startswith("UNRESOLVED") for field in CONFIDENCE_SOURCE_FIELDS), f"completed evidence has placeholder mapping for {row['scenario_id']}")


def validate_json_and_references() -> None:
    config_dir = ROOT / "configs"
    prompt_dir = ROOT / "prompts"
    json_paths = (
        sorted(config_dir.rglob("*.json"))
        + sorted(prompt_dir.rglob("*.json"))
        + [
            ROOT / "splits" / "split_registry_v1.json",
            ROOT / "splits" / "split_schema_v1.json",
            ROOT / "splits" / "dataset_source_manifest.json",
        ]
    )
    for path in json_paths:
        load_json(path)

    common = load_json(config_dir / "common.json")
    registry = load_json(ROOT / "splits" / "split_registry_v1.json")
    source_manifest = load_json(ROOT / "splits" / "dataset_source_manifest.json")
    require(registry["source_index_file"] == "question_index.csv", "source index filename")
    require(sha256(ROOT / "splits" / "question_index.csv") == registry["source_index_sha256"], "source index checksum")
    require(sha256(ROOT / "splits" / "question_index.csv") == source_manifest["canonical_question_index"]["sha256"], "source manifest question checksum")
    require(sha256(ROOT / "splits" / "episode_index.csv") == source_manifest["canonical_episode_index"]["sha256"], "source manifest episode checksum")
    for seed_name in ("main_question_split", "episode_disjoint_split", "repeated_run_subset", "human_reference_subset"):
        require(common["seeds"][seed_name] == registry["randomization"]["seeds"][seed_name], f"{seed_name} seed mismatch")
    for filename, metadata in registry["files"].items():
        require(sha256(ROOT / "splits" / filename) == metadata["sha256"], f"split checksum mismatch for {filename}")

    experiment_manifest = load_json(config_dir / "experiment_manifest.json")
    for filename in experiment_manifest["supporting_configs"]:
        require((config_dir / filename).is_file(), f"missing supporting config {filename}")
    for item in experiment_manifest["experiments"]:
        experiment_path = config_dir / item["file"]
        require(experiment_path.is_file(), f"missing config {item['file']}")
        experiment = load_json(experiment_path)
        for field in (
            "assignments",
            "episode_assignments",
            "question_assignments",
            "subset_assignments",
            "scenario_assignments",
            "initial_memory_build_config",
            "observation_schema",
        ):
            if field in experiment:
                referenced = (config_dir / experiment[field]).resolve()
                require(ROOT.resolve() in referenced.parents, f"reference escapes package in {item['file']}: {field}")
                require(referenced.is_file(), f"missing referenced input in {item['file']}: {field}")

    main_memory = load_json(config_dir / "initial_memory_build.json")
    episode_memory = load_json(config_dir / "episode_disjoint_initial_memory_build.json")
    episode_experiment = load_json(config_dir / "episode_disjoint.json")
    require(main_memory["source_split_id"] == "muma-tom-main-qsplit-v1/memory" and main_memory["expected_questions"] == 225, "main memory initialization")
    require(episode_memory["source_split_id"] == "muma-tom-episode-disjoint-v1/memory", "episode memory split")
    require(episode_memory["source_assignments"] == "../splits/episode_disjoint_questions_v1.csv", "episode memory assignment file")
    require(episode_memory["expected_questions"] == 224 and episode_memory["expected_episodes"] == 56, "episode memory counts")
    require(episode_experiment["initial_memory_build_config"] == "episode_disjoint_initial_memory_build.json", "episode experiment memory config")
    require(episode_experiment["initial_memory_snapshot"] == episode_memory["snapshot"]["output"], "episode memory snapshot mismatch")

    metrics = load_json(config_dir / "metrics.json")
    require((config_dir / metrics["difficulty_assignment_schema"]).is_file(), "missing difficulty assignment schema")
    require((config_dir / metrics["aggregation_entrypoint"]).resolve().is_file(), "missing metric aggregation entrypoint")
    metric_ids = set(metrics["metrics"])
    difficulty_reference_ids = set(metrics["difficulty_references"])
    for item in experiment_manifest["experiments"]:
        experiment = load_json(config_dir / item["file"])
        for key in ("accuracy_metric_id", "per_model_accuracy_metric_id", "per_run_accuracy_metric_id"):
            if key in experiment:
                require(experiment[key] in metric_ids, f"unknown metric in {item['file']}: {experiment[key]}")
        if experiment.get("accuracy_metric_id") == "difficulty_balanced_accuracy":
            require(experiment.get("difficulty_reference_id") in difficulty_reference_ids, f"missing difficulty reference in {item['file']}")
    for filename in ("budget_matched.json", "computational_cost.json", "sensitivity.json"):
        experiment = load_json(config_dir / filename)
        require(experiment["accuracy_metric_id"] == "difficulty_balanced_accuracy", f"DB-Acc. metric mismatch in {filename}")
        require(experiment["difficulty_reference_id"] == "muma-tom-gpt35-main-test-difficulty-v1", f"DB-Acc. reference mismatch in {filename}")
    oracle = load_json(config_dir / "oracle_feedback.json")
    require(oracle["accuracy_metric_id"] == "difficulty_balanced_accuracy", "oracle DB-Acc. metric")
    require(oracle["difficulty_assignment_frozen_before_pass"] == 1, "oracle difficulty freeze point")
    require(oracle["reuse_same_difficulty_assignment_across_conditions_and_passes"] is True, "oracle difficulty reuse")

    sensitivity = load_json(config_dir / "sensitivity.json")
    settings = sensitivity["settings"]
    require(len(settings) == sensitivity["expected_setting_count"] == 9, "sensitivity setting count")
    require(len({item["setting_id"] for item in settings}) == 9, "sensitivity setting IDs")
    default = settings[0]
    require(default["setting_id"] == "default" and default["changed_parameter"] == "NONE", "sensitivity default")
    parameters = ("theta", "T_succ", "low_medium_boundary", "medium_high_boundary")
    for setting in settings[1:]:
        changed = setting["changed_parameter"]
        require(changed in parameters, f"unknown sensitivity parameter {changed}")
        require(sum(setting[name] != default[name] for name in parameters) == 1, f"setting is not one-factor-at-a-time: {setting['setting_id']}")
        require(setting[changed] != default[changed], f"declared parameter did not change: {setting['setting_id']}")
    require("successful_case_threshold" in common["debate"]["maximum_rounds_formula"], "round formula does not reference T_succ parameter")
    count_definition = common["debate"]["successful_case_count_definition"]
    require("before truncation" in count_definition and "at-most-15" in count_definition, "N_succ counting stage is ambiguous")

    routing = load_json(config_dir / "model_routing.json")
    require((config_dir / routing["provider_lookup"]).is_file(), "missing provider lookup")
    require(common["decoding"]["synthesizer_seed"] == routing["routes"]["synthesizer_agent"]["seed"] == "run_seed_plus_2", "synthesizer seed conflict")
    require(routing["routes"]["logical_agent"]["seed"] == "run_seed", "logical seed")
    require(routing["routes"]["innovative_agent"]["seed"] == "run_seed_plus_1", "innovative seed")

    result_schema = load_json(config_dir / "result_record_schema.json")
    run_schema = load_json(config_dir / "run_manifest_schema.json")
    require(result_schema["unique_record_key"] == RESULT_KEY, "result record unique key")
    require(common["evaluation"]["result_record_key"] == RESULT_KEY, "common result record key")
    require(run_schema["required_fields"]["result_record_key"], "run manifest record key declaration")

    human = load_json(config_dir / "human_reference.json")
    require(human["abstention_encoding"] == "ABSTAIN", "human abstention encoding")
    require(human["reference_accuracy"]["participant_formula"] == "correct_answered / answered", "human accuracy denominator")
    require(human["agreement"]["missing_response_policy"] == "complete_case_questions_only", "human kappa missing-data policy")
    require(human["agreement"]["confidence_interval"]["resamples"] == 10000, "human kappa bootstrap count")
    require((config_dir / human["aggregation_entrypoint"]).resolve().is_file(), "missing human aggregation entrypoint")

    confidence_config = load_json(config_dir / "confidence_consistency.json")
    require((config_dir / confidence_config["observation_schema"]).is_file(), "missing confidence observation schema")
    require((config_dir / confidence_config["aggregation_entrypoint"]).resolve().is_file(), "missing confidence aggregation entrypoint")

    prompt_manifest = load_json(prompt_dir / "prompt_manifest.json")
    for item in prompt_manifest["templates"]:
        require((prompt_dir / item["file"]).is_file(), f"missing prompt {item['file']}")
    prompt_files = {item["file"] for item in prompt_manifest["templates"]}
    for key, filename in common["prompts"].items():
        if key not in {"directory", "manifest"}:
            require(filename in prompt_files, f"common config prompt missing from manifest: {filename}")
    media = load_json(config_dir / "media_preprocessing.json")
    for field in ("system_prompt", "user_message"):
        require((config_dir / media[field]).resolve().is_file(), f"missing media prompt: {field}")

    resolved_manifest = load_json(config_dir / "resolved" / "resolved_manifest.json")
    require(len(resolved_manifest["resolved_configs"]) == len(experiment_manifest["experiments"]) == 14, "resolved config count")
    for item in resolved_manifest["resolved_configs"]:
        path = config_dir / item["file"]
        require(path.is_file(), f"missing resolved config {item['file']}")
        require(sha256(path) == item["sha256"], f"resolved config checksum mismatch {item['file']}")
        resolved = load_json(path)
        require(resolved["profile_type"] == "frozen_reproducibility_protocol", "resolved profile type")
        require(len(resolved["prompt_templates"]) == len(prompt_manifest["templates"]), "resolved prompt count")
        require(all(prompt["content"].strip() for prompt in resolved["prompt_templates"]), "empty embedded prompt")
        active_memory = resolved["active_initial_memory_build"]
        if item["source"] == "episode_disjoint.json":
            require(active_memory["config_id"] == episode_memory["config_id"] and active_memory["expected_questions"] == 224, "resolved episode memory conflict")
        else:
            require(active_memory["config_id"] == main_memory["config_id"] and active_memory["expected_questions"] == 225, f"resolved main memory conflict in {item['source']}")

    release_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in [ROOT / "README.md", ROOT / "MANUSCRIPT_ARTIFACT_CROSSWALK.md", ROOT / "CODE_RELEASE_REPRODUCIBILITY.md"]
        + sorted(config_dir.rglob("*.json"))
        + sorted(prompt_dir.rglob("*"))
        + sorted((ROOT / "splits").rglob("*"))
        + sorted((ROOT / "scripts").rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    )
    require(not re.search(r"\b2026101[5-9]\b", release_text), "date-like legacy seed remains")
    require(not re.search(r"[A-Za-z]:\\\\", release_text), "absolute Windows path remains in release package")


def checksum_paths() -> list[Path]:
    paths = [
        ROOT / "README.md",
        ROOT / "MANUSCRIPT_ARTIFACT_CROSSWALK.md",
        ROOT / "CODE_RELEASE_REPRODUCIBILITY.md",
        ROOT / "build_specification.py",
        ROOT / "validate_release.py",
    ]
    for directory in (ROOT / "splits", ROOT / "configs", ROOT / "prompts", ROOT / "scripts"):
        paths.extend(path for path in directory.rglob("*") if path.is_file() and "__pycache__" not in path.parts)
    return sorted(set(paths), key=lambda path: path.relative_to(ROOT).as_posix())


def validate_completed_evidence() -> None:
    config_dir = ROOT / "configs"
    metrics = load_json(config_dir / "metrics.json")
    required_paths = [
        ROOT / reference["assignment_output"]
        for reference in metrics["difficulty_references"].values()
    ]
    for filename in (
        "budget_matched.json",
        "computational_cost.json",
        "sensitivity.json",
        "oracle_feedback.json",
    ):
        config = load_json(config_dir / filename)
        required_paths.extend((ROOT / config["output_jsonl"], ROOT / config["summary_json"]))
    human = load_json(config_dir / "human_reference.json")
    required_paths.extend(
        (
            ROOT / human["responses_csv"],
            ROOT / human["participant_summary_csv"],
            ROOT / human["summary_json"],
        )
    )
    confidence = load_json(config_dir / "confidence_consistency.json")
    required_paths.extend(
        (
            ROOT / confidence["raw_observations_csv"],
            ROOT / confidence["summary_json"],
        )
    )
    for path in required_paths:
        require(path.is_file(), f"missing completed evidence file: {path.relative_to(ROOT).as_posix()}")


def write_checksum_manifest() -> None:
    manifest = {
        "schema_version": "1.0",
        "algorithm": "SHA-256",
        "files": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in checksum_paths()
        ],
    }
    (ROOT / "release_checksums.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify_checksum_manifest() -> None:
    manifest_path = ROOT / "release_checksums.json"
    require(manifest_path.is_file(), "missing release_checksums.json")
    manifest = load_json(manifest_path)
    require(manifest.get("algorithm") == "SHA-256", "checksum algorithm")
    records = manifest.get("files", [])
    require(isinstance(records, list), "checksum files must be a list")
    recorded = {item["path"]: item for item in records}
    require(len(recorded) == len(records), "duplicate checksum manifest paths")
    actual_paths = checksum_paths()
    actual_relative = {path.relative_to(ROOT).as_posix() for path in actual_paths}
    require(set(recorded) == actual_relative, f"checksum manifest file set mismatch: recorded={len(recorded)}, actual={len(actual_relative)}")
    for path in actual_paths:
        relative = path.relative_to(ROOT).as_posix()
        item = recorded[relative]
        require(item["bytes"] == path.stat().st_size, f"checksum byte-size mismatch for {relative}")
        require(item["sha256"] == sha256(path), f"checksum mismatch for {relative}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-checksums", action="store_true", help="regenerate release_checksums.json after validating package structure")
    parser.add_argument("--require-completed-evidence", action="store_true", help="require resolved stimulus mappings and all raw/summary files needed for audited manuscript results")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate_splits(args.require_completed_evidence)
    validate_json_and_references()
    if args.require_completed_evidence:
        validate_completed_evidence()
    if args.write_checksums:
        write_checksum_manifest()
    verify_checksum_manifest()
    mode = "checksums updated" if args.write_checksums else "read-only"
    print(f"release validation: PASS ({mode})")


if __name__ == "__main__":
    main()
