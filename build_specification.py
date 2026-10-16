"""Build the factual reproducibility specification from release artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONFIG_DIR = ROOT / "configs"
PROMPT_DIR = ROOT / "prompts"
SPLIT_DIR = ROOT / "splits"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def json_block(value: object) -> list[str]:
    return ["```json", json.dumps(value, ensure_ascii=False, indent=2), "```", ""]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build() -> None:
    registry = load_json(SPLIT_DIR / "split_registry_v1.json")
    common = load_json(CONFIG_DIR / "common.json")
    environment = load_json(CONFIG_DIR / "environment.json")
    providers = load_json(CONFIG_DIR / "provider_endpoints.json")
    media = load_json(CONFIG_DIR / "media_preprocessing.json")
    routing = load_json(CONFIG_DIR / "model_routing.json")
    metrics = load_json(CONFIG_DIR / "metrics.json")
    initial_memory = load_json(CONFIG_DIR / "initial_memory_build.json")
    episode_initial_memory = load_json(CONFIG_DIR / "episode_disjoint_initial_memory_build.json")
    difficulty_schema = load_json(CONFIG_DIR / "difficulty_assignment_schema.json")
    confidence_schema = load_json(CONFIG_DIR / "confidence_observation_schema.json")
    result_schema = load_json(CONFIG_DIR / "result_record_schema.json")
    run_schema = load_json(CONFIG_DIR / "run_manifest_schema.json")
    experiment_manifest = load_json(CONFIG_DIR / "experiment_manifest.json")
    prompt_manifest = load_json(PROMPT_DIR / "prompt_manifest.json")
    confidence_rows = read_csv(SPLIT_DIR / "confidence_consistency_scenarios_v1.csv")

    lines = [
        "# Complete Reproducibility Protocol",
        "",
        "Protocol profile: `frozen_reproducibility_protocol`.",
        "",
        "## Dataset and identifiers",
        "",
        "| Field | Fixed value |",
        "|---|---|",
        "| Dataset | MuMA-ToM |",
        "| Episodes | 225 |",
        "| Raw videos | 1,030 |",
        "| Questions | 900 |",
        "| Questions per episode | 4 |",
        "| Question types | belief, social-goal, goal-belief |",
        "| Questions per type | 300 |",
        "| Composite question ID | `(episode_id, question_id)` |",
        "| Canonical question index | `splits/question_index.csv` |",
        "| Canonical episode index | `splits/episode_index.csv` |",
        f"| Source-index SHA-256 | `{registry['source_index_sha256']}` |",
        "",
        "### Fixed randomization",
        "",
        "| Operation | Seed |",
        "|---|---:|",
        f"| Main question split | {common['seeds']['main_question_split']} |",
        f"| Episode-disjoint split | {common['seeds']['episode_disjoint_split']} |",
        f"| Repeated-run subset | {common['seeds']['repeated_run_subset']} |",
        f"| Human-reference subset | {common['seeds']['human_reference_subset']} |",
        f"| Paired/bootstrap resampling | {common['seeds']['paired_bootstrap']} |",
        f"| Non-debate API calls | {common['seeds']['non_debate_api']} |",
        f"| Five run seeds | {', '.join(str(x) for x in common['seeds']['run_seeds'])} |",
        "",
        "Randomization uses `Python random.Random(seed).shuffle`. Input records are first sorted by numeric `episode_id` and numeric `question_id`. Question types are processed in the order `belief`, `social-goal`, `goal-belief`.",
        "",
        "### Complete assignment files",
        "",
        "| File | Rows | SHA-256 |",
        "|---|---:|---|",
    ]
    row_counts = {
        "question_index.csv": 900,
        "episode_index.csv": 225,
        "main_question_split_v1.csv": 900,
        "episode_disjoint_episodes_v1.csv": 225,
        "episode_disjoint_questions_v1.csv": 900,
        "repeated_run_subset_550_v1.csv": 550,
        "human_reference_subset_100_v1.csv": 100,
        "confidence_consistency_scenarios_v1.csv": 20,
    }
    source_files = {
        "question_index.csv": {"sha256": registry["source_index_sha256"]},
        "episode_index.csv": {
            "sha256": load_json(SPLIT_DIR / "dataset_source_manifest.json")["canonical_episode_index"]["sha256"]
        },
    }
    for filename, metadata in {**source_files, **registry["files"]}.items():
        lines.append(f"| `splits/{filename}` | {row_counts[filename]} | `{metadata['sha256']}` |")
    lines.extend(
        [
            "",
            "Every MuMA-ToM assignment row contains the original `episode_id`, original within-episode `question_id`, question type, protocol ID, split ID, and split name.",
            "",
            "### Main question-level protocol",
            "",
            "Protocol ID: `muma-tom-main-qsplit-v1`.",
            "",
            "| Split | Belief | Social goal | Goal belief | Total |",
            "|---|---:|---:|---:|---:|",
            "| Memory | 75 | 75 | 75 | 225 |",
            "| Validation | 30 | 30 | 30 | 90 |",
            "| Test | 195 | 195 | 195 | 585 |",
            "",
            "### Episode-disjoint protocol",
            "",
            "Protocol ID: `muma-tom-episode-disjoint-v1`.",
            "",
            "| Split | Episodes | Belief | Social goal | Goal belief | Questions |",
            "|---|---:|---:|---:|---:|---:|",
            "| Memory | 56 | 74 | 74 | 76 | 224 |",
            "| Validation | 23 | 30 | 30 | 32 | 92 |",
            "| Test | 146 | 196 | 196 | 192 | 584 |",
            "",
            "Episode assignment is performed before memory construction. The memory, validation, and test episode intersections are empty.",
            "",
            "### Fixed subsets",
            "",
            "| Subset ID | Belief | Social goal | Goal belief | Total | Parent split |",
            "|---|---:|---:|---:|---:|---|",
            "| `muma-tom-repeat550-v1` | 184 | 183 | 183 | 550 | `muma-tom-main-qsplit-v1/test` |",
            "| `muma-tom-human100-v1` | 34 | 33 | 33 | 100 | `muma-tom-main-qsplit-v1/test` |",
            f"| Overlap between fixed subsets | - | - | - | {registry['subset_overlap_questions']} | - |",
            "",
            "### Confidence-consistency scenario IDs",
            "",
            "| Order | Scenario ID | Task | Selection | Mapping | Source scenario |",
            "|---:|---|---|---|---|---|",
        ]
    )
    for row in confidence_rows:
        lines.append(
            f"| {row['selection_order']} | `{row['scenario_id']}` | `{row['task']}` | `{row['selection_rule']}` | `{row['mapping_status']}` | `{row['source_scenario_id']}` |"
        )

    lines.extend(["", "## Execution environment", ""])
    lines.extend(json_block(environment))
    lines.extend(["## Provider endpoints and model aliases", ""])
    lines.extend(json_block(providers))
    lines.extend(["## Media preprocessing", ""])
    lines.extend(json_block(media))
    lines.extend(["## Model routing and API behavior", ""])
    lines.extend(json_block(routing))

    lines.extend(["## Evaluation metrics and aggregation", ""])
    lines.extend(json_block(metrics))
    lines.extend(["### Difficulty assignment input schema", ""])
    lines.extend(json_block(difficulty_schema))
    lines.extend(["### Confidence observation input schema", ""])
    lines.extend(json_block(confidence_schema))

    lines.extend(
        [
            "## Deterministic execution order",
            "",
            "1. Load the selected assignment file, verify its protocol and split IDs, and sort records by numeric `episode_id` and numeric `question_id` unless an experiment supplies an explicit `selection_order`.",
            "2. Build the initial task-partitioned memory only from the declared memory split, apply the validation-only calibration, serialize the initial memory manifest, and freeze that snapshot before test inference.",
            "3. For each assigned test question, obtain the configured visual/text context, classify the question type, construct option hypotheses, evaluate utterance and action likelihoods, normalize the option scores, and select the baseline answer.",
            "4. Restrict retrieval to the classified question-type partition. Retrieve the configured top five records for trigger and difficulty statistics, applying similarity tie breaks by ascending episode ID and question ID.",
            "5. Compute the trigger statistics and difficulty score from the frozen pre-prediction state. Apply trigger rules in ascending priority order and activate debate only when the matched rule returns `debate` and its confidence is strictly greater than `theta=0.60`.",
            "6. If debate is not activated, set the final answer equal to the baseline answer. If debate is activated, scan at most 15 guidance candidates, retain at most three qualifying cases, determine the maximum round budget from the frozen difficulty level and successful-case rule, and execute logical agent, innovative agent, then synthesizer in every round.",
            "7. Parse `Final Answer: [A-E]` after every synthesis. Stop after two consecutive identical valid synthesized answers or at the maximum round budget. If no valid synthesized answer remains, use the declared majority-vote fallback and alphabetical tie break; otherwise record `INVALID` as incorrect.",
            "8. Write one result record before any test label or correctness signal can update memory. Standard offline runs never update memory from test outcomes; oracle-feedback runs reveal the label only after the prediction record is complete and then apply the declared update schedule.",
            "9. Compute the experiment's declared accuracy metric from complete result records, retain failed and invalid predictions in denominators, store unrounded summaries and integer audit counts, and apply the declared decimal rounding only when rendering a manuscript table.",
            "",
        ]
    )

    lines.extend(
        [
            "## Option scoring",
            "",
            "For `M` options, the prior is uniform: `P(H_k)=1/M`.",
            "",
            "```text",
            "pi = exp(logp_likely - logsumexp(logp_likely, logp_unlikely))",
            "s_k = log P(H_k) + sum_(t,i) log pi(b_i^t | D^(0:t-1), s^0, H_k)",
            "p_k = exp(s_k - logsumexp(s_1,...,s_M))",
            "```",
            "",
            "Token probabilities are clipped to `[1e-6, 1-1e-6]`. Missing or unstable token log probabilities invoke `bounded_score_fallback.txt`; the returned score is used only for within-request relative ranking. An invalid binary response is retried once with `invalid_format_repair.txt`, then evaluated with the bounded fallback.",
            "",
            "## Memory implementation",
            "",
        ]
    )
    lines.extend(json_block(common["memory"]))
    lines.extend(["### Main-protocol initial memory construction", ""])
    lines.extend(json_block(initial_memory))
    lines.extend(["### Episode-disjoint initial memory construction", ""])
    lines.extend(json_block(episode_initial_memory))

    lines.extend(["## Retrieval statistics and trigger", ""])
    lines.extend(json_block(common["trigger"]))
    lines.extend(["## Difficulty and debate-depth control", ""])
    lines.extend(json_block(common["difficulty"]))
    lines.extend(json_block(common["debate"]))

    lines.extend(
        [
            "## Evaluation modes",
            "",
            "Standard evaluation constructs memory only from the memory split, uses validation only for hyperparameter selection and trigger calibration, freezes the memory snapshot before the test split, and never exposes test labels or correctness before final prediction. Ordinary results use `micro_accuracy` unless an experiment configuration explicitly selects `difficulty_balanced_accuracy`.",
            "",
            "Oracle-feedback evaluation uses five ordered passes of the 585-question test split. A label is revealed only after its prediction completes. The oracle condition updates memory immediately after that completed prediction; the frozen control never updates memory. Its DB-Acc. difficulty assignment is generated before pass 1 and reused unchanged across both conditions and all passes.",
            "",
            "## Complete experiment configurations",
            "",
            "Each block below is the experiment-specific portion. The corresponding `configs/resolved/*.json` file additionally embeds every common parameter, support configuration, prompt body, split statistic, and checksum.",
            "",
        ]
    )
    for entry in experiment_manifest["experiments"]:
        experiment = load_json(CONFIG_DIR / entry["file"])
        experiment.pop("common", None)
        lines.extend([f"### `{entry['file']}`", ""])
        lines.extend(json_block(experiment))

    lines.extend(["## Per-question result record", ""])
    lines.extend(json_block(result_schema))
    lines.extend(["## Run manifest", ""])
    lines.extend(json_block(run_schema))

    lines.extend(
        [
            "## Statistical procedures",
            "",
            "- Five runs use the same ordered 550-question subset and the five fixed run seeds.",
            "- Run summaries report mean accuracy and sample standard deviation (`ddof=1`).",
            "- Five predictions per method/question are aggregated by majority vote for paired inference.",
            "- Vote ties select the alphabetically earliest valid option.",
            "- Invalid predictions remain in the denominator and are scored incorrect.",
            "- Paired bootstrap uses 5,000 question-level resamples, seed `84726111`, and percentile 95% intervals.",
            "- McNemar uses `(|n01-n10|-1)^2/(n01+n10)`.",
            "- Three repeated-run comparisons use Holm-Bonferroni correction.",
            "- The episode-disjoint family contains four paired comparisons and uses Holm-Bonferroni correction.",
            "- Confidence-consistency intervals use 5,000 scenario-clustered resamples and preserve every sequential observation from a sampled scenario.",
            "",
            "## Statistical entry points",
            "",
            "```text",
            "python scripts/compute_metrics.py --results <results.jsonl> --difficulty-assignments <difficulty.csv> --output <summary.json>",
            "python scripts/compute_human_reference.py --responses <responses.csv> --output <summary.json> --participant-output <participants.csv>",
            "python scripts/compute_confidence_consistency.py --observations <observations.csv> --output <summary.json>",
            "```",
            "",
            "Each command validates exact key coverage before writing a summary. The confidence command additionally requires every scenario-to-source mapping to be resolved.",
            "",
            "## Complete prompt templates",
            "",
        ]
    )
    for item in prompt_manifest["templates"]:
        content = (PROMPT_DIR / item["file"]).read_text(encoding="utf-8").rstrip()
        lines.extend(
            [
                f"### `{item['file']}`",
                "",
                f"Stage: `{item['stage']}`. Origin: `{item['origin']}`.",
                "",
                "```text",
                content,
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Integrity and validation",
            "",
            "`validate_release.py` validates source-index membership, unique IDs, exact counts, question-type balance, episode disjointness, active memory initialization, subset membership, protocol IDs, JSON syntax, prompt/config/metric references, fixed seeds, split hashes, resolved configuration count, package-relative paths, and the checksum manifest. Its default mode is read-only.",
            "",
            "Use `python validate_release.py --write-checksums` only after an intentional package update. Then run `python validate_release.py` to perform a read-only verification. `release_checksums.json` records SHA-256 for every release file except the checksum manifest itself.",
            "",
        ]
    )
    (ROOT / "CODE_RELEASE_REPRODUCIBILITY.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


if __name__ == "__main__":
    build()
