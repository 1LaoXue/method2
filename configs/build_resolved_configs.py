"""Build self-contained experiment configurations with no unresolved references."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


CONFIG_DIR = Path(__file__).resolve().parent
ROOT = CONFIG_DIR.parent
PROMPT_DIR = ROOT / "prompts"
SPLIT_DIR = ROOT / "splits"
OUTPUT_DIR = CONFIG_DIR / "resolved"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prompt_bundle() -> list[dict[str, object]]:
    manifest = load_json(PROMPT_DIR / "prompt_manifest.json")
    bundle = []
    for item in manifest["templates"]:
        path = PROMPT_DIR / item["file"]
        bundle.append(
            {
                **item,
                "sha256": sha256(path),
                "content": path.read_text(encoding="utf-8"),
            }
        )
    return bundle


def split_bundle(registry: dict, experiment: dict) -> dict:
    bundle: dict[str, object] = {
        "source_index_sha256": registry["source_index_sha256"],
        "randomization": registry["randomization"],
    }
    protocol_id = experiment.get("protocol_id")
    if protocol_id in registry["protocols"]:
        bundle["protocol"] = {
            "protocol_id": protocol_id,
            **registry["protocols"][protocol_id],
        }
    subset_id = experiment.get("subset_id")
    if subset_id in registry["subsets"]:
        bundle["subset"] = {"subset_id": subset_id, **registry["subsets"][subset_id]}
    if experiment.get("config_id") == "controlled-confidence-consistency-v1":
        scenario_file = SPLIT_DIR / "confidence_consistency_scenarios_v1.csv"
        with scenario_file.open(encoding="utf-8", newline="") as handle:
            scenarios = list(csv.DictReader(handle))
        bundle["controlled_scenarios"] = {
            "file": scenario_file.name,
            "sha256": sha256(scenario_file),
            "records": scenarios,
        }
    files = {}
    for field in (
        "assignments",
        "episode_assignments",
        "question_assignments",
        "subset_assignments",
        "scenario_assignments",
    ):
        value = experiment.get(field)
        if isinstance(value, str):
            path = (CONFIG_DIR / value).resolve()
            if path.is_file():
                files[field] = {
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": sha256(path),
                }
    if files:
        bundle["files"] = files
    return bundle


def build() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    common = load_json(CONFIG_DIR / "common.json")
    registry = load_json(SPLIT_DIR / "split_registry_v1.json")
    supporting = {
        "environment": load_json(CONFIG_DIR / "environment.json"),
        "provider_endpoints": load_json(CONFIG_DIR / "provider_endpoints.json"),
        "media_preprocessing": load_json(CONFIG_DIR / "media_preprocessing.json"),
        "model_routing": load_json(CONFIG_DIR / "model_routing.json"),
        "metrics": load_json(CONFIG_DIR / "metrics.json"),
        "difficulty_assignment_schema": load_json(CONFIG_DIR / "difficulty_assignment_schema.json"),
        "confidence_observation_schema": load_json(CONFIG_DIR / "confidence_observation_schema.json"),
        "result_record_schema": load_json(CONFIG_DIR / "result_record_schema.json"),
        "run_manifest_schema": load_json(CONFIG_DIR / "run_manifest_schema.json"),
    }
    main_initial_memory = load_json(CONFIG_DIR / "initial_memory_build.json")
    episode_initial_memory = load_json(
        CONFIG_DIR / "episode_disjoint_initial_memory_build.json"
    )
    prompts = prompt_bundle()
    experiment_manifest = load_json(CONFIG_DIR / "experiment_manifest.json")
    output_records = []
    for entry in experiment_manifest["experiments"]:
        source_path = CONFIG_DIR / entry["file"]
        experiment = load_json(source_path)
        experiment.pop("common", None)
        initial_memory = (
            episode_initial_memory
            if entry["file"] == "episode_disjoint.json"
            else main_initial_memory
        )
        resolved = {
            "schema_version": "1.0",
            "profile_type": "frozen_reproducibility_protocol",
            "resolved_config_id": f'{experiment["config_id"]}-resolved',
            "dataset_and_splits": split_bundle(registry, experiment),
            "common_algorithm_configuration": common,
            "supporting_configuration": supporting,
            "active_initial_memory_build": initial_memory,
            "prompt_templates": prompts,
            "experiment": experiment,
            "declared_output": entry["output"],
        }
        output_path = OUTPUT_DIR / entry["file"]
        output_path.write_text(
            json.dumps(resolved, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        output_records.append(
            {
                "file": output_path.relative_to(CONFIG_DIR).as_posix(),
                "source": entry["file"],
                "bytes": output_path.stat().st_size,
                "sha256": sha256(output_path),
            }
        )
    manifest = {
        "schema_version": "1.0",
        "profile_type": "frozen_reproducibility_protocol",
        "resolved_configs": output_records,
    }
    (OUTPUT_DIR / "resolved_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"resolved configurations: {len(output_records)}")


if __name__ == "__main__":
    build()
