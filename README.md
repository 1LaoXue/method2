# Reproducibility Release Package

This directory is the single entry point for the reproducibility materials accompanying the manuscript. All paths below are relative to this directory; no file outside this directory is required to inspect or regenerate the released specifications.

## Package map

| Path | Purpose |
|---|---|
| `CODE_RELEASE_REPRODUCIBILITY.md` | Fully expanded, human-readable protocol containing all fixed parameters and prompt bodies. |
| `MANUSCRIPT_ARTIFACT_CROSSWALK.md` | Direct mapping from each manuscript result to its configuration, assignments, metric, and output. |
| `configs/` | Machine-readable common, experiment, metric, environment, provider, routing, schema, and resolved configurations. |
| `prompts/` | Complete prompt templates and their manifest. |
| `scripts/` | Executable metric, human-reference, and confidence-consistency aggregation programs with exact input contracts. |
| `splits/question_index.csv` | Canonical 900-question source index used to generate every released split. |
| `splits/episode_index.csv` | Canonical 225-episode inventory. |
| `splits/*split*.csv` | Exact question- and episode-level assignments and fixed evaluation subsets. |
| `splits/generate_splits.py` | Deterministic split generator. |
| `build_specification.py` | Regenerates the expanded Markdown protocol from the machine-readable files. |
| `validate_release.py` | Read-only validation of identifiers, counts, references, metrics, hashes, and package self-containment by default. |
| `release_checksums.json` | SHA-256 manifest for every released file except the manifest itself. |

## Accuracy terminology

`micro_accuracy` is the integer correct count divided by the evaluated question count. `difficulty_balanced_accuracy` (`DB-Acc.`) is the unweighted macro-average of the low-, medium-, and high-difficulty stratum accuracies. Tables 4, 6, and 7 use `DB-Acc.`; their difficulty strata are generated once from the specified frozen reference state and reused for every method or pass in the corresponding comparison. The exact formulas, assignment IDs, rounding rules, and required audit fields are in `configs/metrics.json`.

`scripts/compute_metrics.py` refuses to aggregate unless each result group and its frozen difficulty file cover exactly the same 585 test IDs, with no duplicate, missing, extra, or empty-stratum records. It writes the three stratum denominators and correct counts, unrounded DB-Acc., integer micro correct/total, and table-specific rendered values.

## Evidence inputs

| Claim | Required raw evidence | Aggregator |
|---|---|---|
| Tables 4 and 6 | Complete per-question JSONL plus `muma-tom-gpt35-main-test-difficulty-v1.csv` | `scripts/compute_metrics.py` |
| Table 7 | Complete two-condition, five-pass JSONL plus `muma-tom-gpt4o-oracle-prepass-difficulty-v1.csv` | `scripts/compute_metrics.py` |
| Human accuracy and Fleiss' kappa | 600-row participant response CSV | `scripts/compute_human_reference.py` |
| Confidence consistency | Resolved 20-scenario source map plus sequential observation CSV | `scripts/compute_confidence_consistency.py` |

No summary is accepted as completed evidence unless its raw inputs, SHA-256 hashes, exact key coverage, and audit counts pass the corresponding aggregator.

## Deterministic rebuild

Run the following commands from this directory in order:

```text
python splits/generate_splits.py
python configs/build_resolved_configs.py
python build_specification.py
python validate_release.py --write-checksums
python validate_release.py
```

The checksum-writing option is used only after intentional package changes. The final command is read-only and must print `release validation: PASS (read-only)`. Generated `configs/resolved/*.json`, `CODE_RELEASE_REPRODUCIBILITY.md`, and `release_checksums.json` are committed so that reviewers can inspect the package without running the build.

## Completion gate

Run `python validate_release.py --require-completed-evidence` before declaring the reported-result evidence complete. This stricter mode rejects unresolved scenario mappings and requires the frozen difficulty files, audited result JSONL files, human responses, confidence observations, participant summaries, and metric summaries at their declared paths. Every executed experiment must retain its per-question JSONL or response CSV, aggregation summary, run manifest, and input hashes.
