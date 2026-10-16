# Statistical Reproduction Entry Points

Run every command from the `details/` directory. Each program validates identifiers, coverage, duplicates, and input values before writing an output.

## Tables 4, 6, and 7

```text
python scripts/compute_metrics.py \
  --results outputs/budget_matched/all_methods.jsonl \
  --difficulty-assignments outputs/metrics/muma-tom-gpt35-main-test-difficulty-v1.csv \
  --output outputs/budget_matched/table_summary.json
```

Use the same command with the computational-cost JSONL for Table 6. For Table 7, use the oracle-feedback JSONL and `muma-tom-gpt4o-oracle-prepass-difficulty-v1.csv`. Every method/condition/pass/sensitivity group must contain exactly the same 585 question IDs as the frozen difficulty assignment. The output includes low/medium/high sample counts, integer correct counts, exact count fractions, unrounded DB-Acc., micro correct/total, and the one- or two-decimal rendered percentages.

Difficulty assignment CSV fields and thresholds are defined in `configs/difficulty_assignment_schema.json`. Per-question result fields and the composite uniqueness key are defined in `configs/result_record_schema.json`.

## Human Reference

```text
python scripts/compute_human_reference.py \
  --responses outputs/human_reference/responses.csv \
  --participant-output outputs/human_reference/participant_summary.csv \
  --output outputs/human_reference/accuracy_and_agreement.json
```

The input must contain 600 rows: the same fixed 100 questions for each of `P01` through `P06`. `ABSTAIN` is excluded from that participant's accuracy denominator. The reported reference is the equal-weight mean of six participant accuracies. Fleiss' kappa uses only questions answered A-E by all six participants; its interval is a 10,000-resample question bootstrap with seed `84726111`.

## Confidence Consistency

```text
python scripts/compute_confidence_consistency.py \
  --observations outputs/confidence_consistency/sequential_observations.csv \
  --output outputs/confidence_consistency/correlations_and_clustered_intervals.json
```

Before this command can run, all 20 rows in `splits/confidence_consistency_scenarios_v1.csv` must map to source publication/task/scenario/type/stimulus identifiers with `mapping_status=RESOLVED`. The program computes Pearson correlation separately for each task and model and obtains 95% percentile intervals by resampling scenario clusters while retaining every sequential observation.

## Experiment Runner Contract

The release does not substitute a mock LLM runner for provider execution. A conforming runner must load one resolved configuration, use its embedded prompts and route-level seeds, process exactly the declared IDs in order, and write one JSONL record matching `configs/result_record_schema.json` for every composite record key. It must then write a run manifest matching `configs/run_manifest_schema.json` and invoke the appropriate aggregation program above.
