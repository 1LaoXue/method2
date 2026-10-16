# Complete Reproducibility Protocol

Protocol profile: `frozen_reproducibility_protocol`.

## Dataset and identifiers

| Field | Fixed value |
|---|---|
| Dataset | MuMA-ToM |
| Episodes | 225 |
| Raw videos | 1,030 |
| Questions | 900 |
| Questions per episode | 4 |
| Question types | belief, social-goal, goal-belief |
| Questions per type | 300 |
| Composite question ID | `(episode_id, question_id)` |
| Canonical question index | `splits/question_index.csv` |
| Canonical episode index | `splits/episode_index.csv` |
| Source-index SHA-256 | `2e81b1d5865c5ae279790ec627c9b1b16d7f45441e542b71c7783e90ba1d021a` |

### Fixed randomization

| Operation | Seed |
|---|---:|
| Main question split | 73194217 |
| Episode-disjoint split | 18465031 |
| Repeated-run subset | 59280463 |
| Human-reference subset | 31847029 |
| Paired/bootstrap resampling | 84726111 |
| Non-debate API calls | 90472131 |
| Five run seeds | 35719823, 68245109, 11472863, 94026571, 52680347 |

Randomization uses `Python random.Random(seed).shuffle`. Input records are first sorted by numeric `episode_id` and numeric `question_id`. Question types are processed in the order `belief`, `social-goal`, `goal-belief`.

### Complete assignment files

| File | Rows | SHA-256 |
|---|---:|---|
| `splits/question_index.csv` | 900 | `2e81b1d5865c5ae279790ec627c9b1b16d7f45441e542b71c7783e90ba1d021a` |
| `splits/episode_index.csv` | 225 | `dd163a447008a669af995e6c5ef7f2bd6fcce0fecdbfa1014032dc7cac49ea0e` |
| `splits/main_question_split_v1.csv` | 900 | `47c6a0c737ca0f763e4bef06bd41ec2e78e746bd4554f90442cc53d3e8a93279` |
| `splits/episode_disjoint_episodes_v1.csv` | 225 | `cb1b52af593ced893760e239b4fa2457b36e4af091e853b235ed3e177412ab5a` |
| `splits/episode_disjoint_questions_v1.csv` | 900 | `99086ba34a8316d88b3f07a6eb2cedc006844dc92fcf09980fcd211efe3e8844` |
| `splits/repeated_run_subset_550_v1.csv` | 550 | `5e7ccd4469b062427ff7aeb75306bb0d567b3c423157ad7705cf45593a4c1fe5` |
| `splits/human_reference_subset_100_v1.csv` | 100 | `42003074605fce115944366609b5f07a68ce93af9891bc9a0bf5b2e8c8be4c59` |
| `splits/confidence_consistency_scenarios_v1.csv` | 20 | `a97ba042cce7a73d218df4894b73553238c702b448c5ee1c0c9adfed05a80116` |

Every MuMA-ToM assignment row contains the original `episode_id`, original within-episode `question_id`, question type, protocol ID, split ID, and split name.

### Main question-level protocol

Protocol ID: `muma-tom-main-qsplit-v1`.

| Split | Belief | Social goal | Goal belief | Total |
|---|---:|---:|---:|---:|
| Memory | 75 | 75 | 75 | 225 |
| Validation | 30 | 30 | 30 | 90 |
| Test | 195 | 195 | 195 | 585 |

### Episode-disjoint protocol

Protocol ID: `muma-tom-episode-disjoint-v1`.

| Split | Episodes | Belief | Social goal | Goal belief | Questions |
|---|---:|---:|---:|---:|---:|
| Memory | 56 | 74 | 74 | 76 | 224 |
| Validation | 23 | 30 | 30 | 32 | 92 |
| Test | 146 | 196 | 196 | 192 | 584 |

Episode assignment is performed before memory construction. The memory, validation, and test episode intersections are empty.

### Fixed subsets

| Subset ID | Belief | Social goal | Goal belief | Total | Parent split |
|---|---:|---:|---:|---:|---|
| `muma-tom-repeat550-v1` | 184 | 183 | 183 | 550 | `muma-tom-main-qsplit-v1/test` |
| `muma-tom-human100-v1` | 34 | 33 | 33 | 100 | `muma-tom-main-qsplit-v1/test` |
| Overlap between fixed subsets | - | - | - | 97 | - |

### Confidence-consistency scenario IDs

| Order | Scenario ID | Task | Selection | Mapping | Source scenario |
|---:|---|---|---|---|---|
| 1 | `baker-online-goal-01` | `online_goal_inference` | `all_scenarios` | `RESOLVED` | `online_goal1` |
| 2 | `baker-online-goal-02` | `online_goal_inference` | `all_scenarios` | `RESOLVED` | `online_goal2` |
| 3 | `baker-online-goal-03` | `online_goal_inference` | `all_scenarios` | `RESOLVED` | `online_goal3` |
| 4 | `baker-online-goal-04` | `online_goal_inference` | `all_scenarios` | `RESOLVED` | `online_goal4` |
| 5 | `baker-online-goal-05` | `online_goal_inference` | `all_scenarios` | `RESOLVED` | `online_goal5` |
| 6 | `baker-online-goal-06` | `online_goal_inference` | `all_scenarios` | `RESOLVED` | `online_goal6` |
| 7 | `baker-desire-type-01` | `desire_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck1` |
| 8 | `baker-desire-type-02` | `desire_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck2` |
| 9 | `baker-desire-type-03` | `desire_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck5` |
| 10 | `baker-desire-type-04` | `desire_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck16` |
| 11 | `baker-desire-type-05` | `desire_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck18` |
| 12 | `baker-desire-type-06` | `desire_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck55` |
| 13 | `baker-desire-type-07` | `desire_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck56` |
| 14 | `baker-belief-type-01` | `belief_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck1` |
| 15 | `baker-belief-type-02` | `belief_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck2` |
| 16 | `baker-belief-type-03` | `belief_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck5` |
| 17 | `baker-belief-type-04` | `belief_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck16` |
| 18 | `baker-belief-type-05` | `belief_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck18` |
| 19 | `baker-belief-type-06` | `belief_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck55` |
| 20 | `baker-belief-type-07` | `belief_inference` | `one_representative_per_type` | `RESOLVED` | `food_truck56` |

## Execution environment

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-environment-v1",
  "profile_type": "frozen_reproducibility_protocol",
  "operating_system": "Ubuntu 22.04.5 LTS",
  "architecture": "x86_64",
  "python": "3.11.9",
  "timezone": "UTC",
  "locale": "C.UTF-8",
  "packages": {
    "numpy": "1.26.4",
    "pandas": "2.2.2",
    "scipy": "1.13.1",
    "openai": "1.51.2",
    "google-generativeai": "0.8.3",
    "httpx": "0.27.2",
    "pydantic": "2.9.2",
    "tenacity": "9.0.0",
    "tiktoken": "0.8.0",
    "opencv-python-headless": "4.10.0.84"
  },
  "api_key_environment_variables": {
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "dashscope": "DASHSCOPE_API_KEY",
    "together": "TOGETHER_API_KEY"
  },
  "network": {
    "connect_timeout_seconds": 30,
    "read_timeout_seconds": 120,
    "max_connections": 1
  },
  "numeric": {
    "float_storage": "IEEE-754 float64",
    "json_float_precision": 10,
    "csv_encoding": "UTF-8",
    "line_ending": "LF"
  }
}
```

## Provider endpoints and model aliases

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-provider-endpoints-v1",
  "providers": {
    "openai": {
      "base_url": "https://api.openai.com/v1",
      "api_key_environment_variable": "OPENAI_API_KEY",
      "models": [
        "gpt-5",
        "gpt-4o-2024-11-20",
        "gpt-3.5-turbo-0125",
        "o4-mini"
      ]
    },
    "google_gemini_openai_compatible": {
      "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
      "api_key_environment_variable": "GEMINI_API_KEY",
      "models": [
        "gemini-2.5-pro-preview-05-06",
        "gemini-2.5-flash"
      ]
    },
    "deepseek": {
      "base_url": "https://api.deepseek.com/v1",
      "api_key_environment_variable": "DEEPSEEK_API_KEY",
      "models": [
        "DeepSeek-V3.1"
      ]
    },
    "dashscope_openai_compatible": {
      "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "api_key_environment_variable": "DASHSCOPE_API_KEY",
      "models": [
        "Qwen3-VL-32B-Instruct"
      ]
    },
    "together_openai_compatible": {
      "base_url": "https://api.together.xyz/v1",
      "api_key_environment_variable": "TOGETHER_API_KEY",
      "models": [
        "Meta-Llama-3.2-90B-Vision-Instruct"
      ]
    }
  },
  "alias_resolution": {
    "record_requested_model": true,
    "record_provider_resolved_model": true,
    "record_request_timestamp_utc": true,
    "record_provider_request_id": true
  }
}
```

## Media preprocessing

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-media-preprocessing-v1",
  "profile_type": "frozen_reproducibility_protocol",
  "input_preference": [
    "provider_native_video",
    "ordered_uniform_frames"
  ],
  "native_video": {
    "enabled_when_supported": true,
    "include_audio": true,
    "clip_start_seconds": 0.0,
    "clip_end": "full_video"
  },
  "frame_fallback": {
    "decoder": "OpenCV VideoCapture",
    "sampling": "uniform_over_full_duration",
    "frames_per_second": 1.0,
    "minimum_frames": 8,
    "maximum_frames": 32,
    "always_include_first_frame": true,
    "always_include_last_frame": true,
    "duplicate_timestamp_policy": "keep_first",
    "ordering": "timestamp_ascending",
    "color_space": "RGB",
    "resize": {
      "longest_side_pixels": 768,
      "allow_upscale": false
    },
    "encoding": {
      "format": "JPEG",
      "quality": 90
    }
  },
  "text_context": {
    "include_dataset_description": true,
    "include_dialogue_transcript": true,
    "include_target_person_name": true,
    "include_answer_options_during_visual_extraction": false
  },
  "visual_parser": "gemini-2.5-pro-preview-05-06",
  "system_prompt": "../prompts/visual_action_extraction.txt",
  "user_message": "../prompts/visual_request_user_message.txt",
  "temperature": 0.0,
  "seed": 90472131,
  "max_tokens": 1000,
  "cache_key": "sha256(video_bytes || rendered_prompt || model_id || config_id)"
}
```

## Model routing and API behavior

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-model-routing-v1",
  "provider_lookup": "provider_endpoints.json",
  "seed_resolution": {
    "precedence": "route_seed_overrides_common_decoding_role_seed",
    "logical_agent": "run_seed",
    "innovative_agent": "run_seed_plus_1",
    "synthesizer_agent": "run_seed_plus_2"
  },
  "routes": {
    "visual_action_extraction": {
      "model": "gemini-2.5-pro-preview-05-06",
      "provider": "google_gemini_openai_compatible",
      "temperature": 0.0,
      "seed": 90472131
    },
    "person_action_utterance_parsing": {
      "model": "gpt-4o-2024-11-20",
      "temperature": 0.0,
      "seed": 90472131
    },
    "initial_state_extraction": {
      "model": "gpt-4o-2024-11-20",
      "temperature": 0.0,
      "seed": 90472131
    },
    "latent_hypothesis_generation": {
      "model": "experiment_core_reasoner",
      "temperature": 0.0,
      "seed": 90472131
    },
    "utterance_likelihood": {
      "model": "experiment_core_reasoner",
      "temperature": 0.0,
      "seed": 90472131,
      "request_token_logprobs": true
    },
    "action_likelihood": {
      "model": "experiment_core_reasoner",
      "temperature": 0.0,
      "seed": 90472131,
      "request_token_logprobs": true
    },
    "bounded_score_fallback": {
      "model": "experiment_core_reasoner",
      "temperature": 0.0,
      "seed": 90472131,
      "response_format": "json_object"
    },
    "question_type_classification": {
      "model": "experiment_core_reasoner",
      "temperature": 0.0,
      "seed": 90472131
    },
    "short_context_summary": {
      "model": "experiment_core_reasoner",
      "temperature": 0.0,
      "seed": 90472131
    },
    "reasoning_summary": {
      "model": "experiment_core_reasoner",
      "temperature": 0.0,
      "seed": 90472131,
      "response_format": "json_object"
    },
    "retrieval_pattern_summary": {
      "model": "experiment_core_reasoner",
      "temperature": 0.0,
      "seed": 90472131
    },
    "invalid_format_repair": {
      "model": "same_model_as_failed_stage",
      "temperature": 0.0,
      "seed": 90472131
    },
    "logical_agent": {
      "model": "experiment_core_reasoner",
      "provider": "lookup_by_resolved_model_id",
      "temperature": 0.3,
      "seed": "run_seed"
    },
    "innovative_agent": {
      "model": "experiment_core_reasoner",
      "provider": "lookup_by_resolved_model_id",
      "temperature": 0.3,
      "seed": "run_seed_plus_1"
    },
    "synthesizer_agent": {
      "model": "experiment_core_reasoner",
      "provider": "lookup_by_resolved_model_id",
      "temperature": 0.1,
      "seed": "run_seed_plus_2"
    }
  },
  "all_routes": {
    "max_tokens": 1000,
    "timeout_seconds": 120,
    "max_retries": 3,
    "retry_on": [
      "timeout",
      "rate_limit",
      "server_error",
      "invalid_format"
    ],
    "retry_backoff_seconds": [
      2,
      4,
      8
    ]
  }
}
```

## Evaluation metrics and aggregation

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-evaluation-metrics-v1",
  "difficulty_assignment_schema": "difficulty_assignment_schema.json",
  "aggregation_entrypoint": "../scripts/compute_metrics.py",
  "metrics": {
    "micro_accuracy": {
      "display_name": "Micro-Acc.",
      "formula": "sum_i I(prediction_i == ground_truth_i) / N",
      "numerator": "integer number of correct predictions",
      "denominator": "all assigned questions, including INVALID and failed predictions",
      "aggregation_unit": "question"
    },
    "difficulty_balanced_accuracy": {
      "display_name": "DB-Acc.",
      "formula": "(1/3) * sum_{h in {low,medium,high}} (correct_h / n_h)",
      "strata": [
        "low",
        "medium",
        "high"
      ],
      "stratum_weights": {
        "low": "1/3",
        "medium": "1/3",
        "high": "1/3"
      },
      "difficulty_thresholds": {
        "low": "D < 0.30",
        "medium": "0.30 <= D < 0.60",
        "high": "D >= 0.60"
      },
      "empty_stratum_policy": "invalid_run_do_not_report",
      "assignment_policy": "compute_once_from_the_declared_frozen_reference_state_then_reuse_unchanged_within_the_comparison",
      "not_equivalent_to": "support-weighted_stratum_accuracy_or_integer_correct_count_divided_by_585",
      "audit_requirements": [
        "reference_assignment_id",
        "reference_assignment_sha256",
        "n_low",
        "n_medium",
        "n_high",
        "correct_low",
        "correct_medium",
        "correct_high",
        "unrounded_difficulty_balanced_accuracy",
        "integer_micro_correct",
        "integer_micro_total",
        "unrounded_micro_accuracy"
      ]
    }
  },
  "difficulty_references": {
    "muma-tom-gpt35-main-test-difficulty-v1": {
      "protocol_id": "muma-tom-main-qsplit-v1",
      "split_id": "muma-tom-main-qsplit-v1/test",
      "questions": 585,
      "core_reasoner": "gpt-3.5-turbo-0125",
      "memory_state": "initial_memory_snapshot_frozen_before_test",
      "score_configuration": "common.json/difficulty",
      "processing_order": [
        "episode_id_ascending",
        "question_id_ascending"
      ],
      "used_by": [
        "budget_matched.json",
        "computational_cost.json",
        "sensitivity.json"
      ],
      "assignment_output": "outputs/metrics/muma-tom-gpt35-main-test-difficulty-v1.csv"
    },
    "muma-tom-gpt4o-oracle-prepass-difficulty-v1": {
      "protocol_id": "muma-tom-main-qsplit-v1",
      "split_id": "muma-tom-main-qsplit-v1/test",
      "questions": 585,
      "core_reasoner": "gpt-4o-2024-11-20",
      "memory_state": "initial_memory_snapshot_frozen_before_oracle_pass_1",
      "score_configuration": "common.json/difficulty",
      "processing_order": [
        "episode_id_ascending",
        "question_id_ascending"
      ],
      "reuse": "same_assignment_for_both_conditions_and_all_five_passes",
      "used_by": [
        "oracle_feedback.json"
      ],
      "assignment_output": "outputs/metrics/muma-tom-gpt4o-oracle-prepass-difficulty-v1.csv"
    }
  },
  "reporting": {
    "store_unrounded_values": true,
    "rounding_mode": "decimal_ROUND_HALF_UP",
    "table_4_decimals": 2,
    "table_6_decimals": 2,
    "table_7_decimals": 1,
    "table_rendering": {
      "table_4_budget_matched": {
        "metric_id": "difficulty_balanced_accuracy",
        "percent_decimals": 2
      },
      "table_6_computational_cost": {
        "metric_id": "difficulty_balanced_accuracy",
        "percent_decimals": 2
      },
      "table_7_oracle_feedback": {
        "metric_id": "difficulty_balanced_accuracy",
        "percent_decimals": 1
      }
    },
    "report_micro_accuracy_alongside_db_accuracy_in_machine_readable_summary": true
  },
  "completed_evidence_requirements": {
    "difficulty_assignment": "exactly 585 unique main-test question keys with nonempty low, medium, and high strata",
    "result_group": "exactly one record for every assignment key within each method/model/run/condition/pass/sensitivity group",
    "audit_output": "integer counts for every stratum, exact count fractions, unrounded decimal values, rendered table values, and SHA-256 hashes of both inputs"
  }
}
```

### Difficulty assignment input schema

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-difficulty-assignment-schema-v1",
  "format": "CSV UTF-8 with header",
  "unique_key": [
    "reference_assignment_id",
    "episode_id",
    "question_id"
  ],
  "required_fields": {
    "reference_assignment_id": "string matching configs/metrics.json",
    "protocol_id": "muma-tom-main-qsplit-v1",
    "split_id": "muma-tom-main-qsplit-v1/test",
    "episode_id": "dataset episode identifier",
    "question_id": "question identifier within episode",
    "difficulty_score": "float in [0,1] computed from the frozen reference state",
    "difficulty_stratum": "low|medium|high"
  },
  "threshold_consistency": {
    "low": "difficulty_score < 0.30",
    "medium": "0.30 <= difficulty_score < 0.60",
    "high": "difficulty_score >= 0.60"
  },
  "coverage": {
    "expected_questions": 585,
    "expected_question_keys_from": "../splits/main_question_split_v1.csv where split == test",
    "missing_keys_allowed": false,
    "extra_keys_allowed": false,
    "duplicate_keys_allowed": false,
    "empty_strata_allowed": false
  }
}
```

### Confidence observation input schema

```json
{
  "schema_version": "1.0",
  "config_id": "controlled-confidence-observation-schema-v1",
  "format": "CSV UTF-8 with header",
  "unique_key": [
    "scenario_id",
    "observation_sequence_id",
    "timepoint_index",
    "model_id"
  ],
  "required_fields": {
    "protocol_id": "controlled-confidence-consistency-v1",
    "scenario_id": "must resolve through confidence_consistency_scenarios_v1.csv",
    "observation_sequence_id": "must equal the mapped sequence ID",
    "task": "online_goal_inference|desire_inference|belief_inference",
    "timepoint_index": "positive integer unique within scenario/model sequence",
    "model_id": "full_framework|gpt-4o-2024-11-20|o4-mini|gemini-2.5-flash",
    "model_score": "finite float in [0,1]",
    "human_rating": "finite float on the original task-specific scale",
    "human_rating_scale_min": "finite float smaller than human_rating_scale_max",
    "human_rating_scale_max": "finite float larger than human_rating_scale_min"
  },
  "mapping_requirement": "Every scenario row must have mapping_status RESOLVED and non-placeholder source publication, source task, source scenario ID, stimulus location, source type ID, and observation sequence ID before aggregation.",
  "correlation_unit": "all sequential observations pooled within task and model",
  "bootstrap_unit": "scenario cluster with every timepoint retained when a scenario is resampled"
}
```

## Deterministic execution order

1. Load the selected assignment file, verify its protocol and split IDs, and sort records by numeric `episode_id` and numeric `question_id` unless an experiment supplies an explicit `selection_order`.
2. Build the initial task-partitioned memory only from the declared memory split, apply the validation-only calibration, serialize the initial memory manifest, and freeze that snapshot before test inference.
3. For each assigned test question, obtain the configured visual/text context, classify the question type, construct option hypotheses, evaluate utterance and action likelihoods, normalize the option scores, and select the baseline answer.
4. Restrict retrieval to the classified question-type partition. Retrieve the configured top five records for trigger and difficulty statistics, applying similarity tie breaks by ascending episode ID and question ID.
5. Compute the trigger statistics and difficulty score from the frozen pre-prediction state. Apply trigger rules in ascending priority order and activate debate only when the matched rule returns `debate` and its confidence is strictly greater than `theta=0.60`.
6. If debate is not activated, set the final answer equal to the baseline answer. If debate is activated, scan at most 15 guidance candidates, retain at most three qualifying cases, determine the maximum round budget from the frozen difficulty level and successful-case rule, and execute logical agent, innovative agent, then synthesizer in every round.
7. Parse `Final Answer: [A-E]` after every synthesis. Stop after two consecutive identical valid synthesized answers or at the maximum round budget. If no valid synthesized answer remains, use the declared majority-vote fallback and alphabetical tie break; otherwise record `INVALID` as incorrect.
8. Write one result record before any test label or correctness signal can update memory. Standard offline runs never update memory from test outcomes; oracle-feedback runs reveal the label only after the prediction record is complete and then apply the declared update schedule.
9. Compute the experiment's declared accuracy metric from complete result records, retain failed and invalid predictions in denominators, store unrounded summaries and integer audit counts, and apply the declared decimal rounding only when rendering a manuscript table.

## Option scoring

For `M` options, the prior is uniform: `P(H_k)=1/M`.

```text
pi = exp(logp_likely - logsumexp(logp_likely, logp_unlikely))
s_k = log P(H_k) + sum_(t,i) log pi(b_i^t | D^(0:t-1), s^0, H_k)
p_k = exp(s_k - logsumexp(s_1,...,s_M))
```

Token probabilities are clipped to `[1e-6, 1-1e-6]`. Missing or unstable token log probabilities invoke `bounded_score_fallback.txt`; the returned score is used only for within-request relative ranking. An invalid binary response is retried once with `invalid_format_repair.txt`, then evaluated with the bounded fallback.

## Memory implementation

```json
{
  "partitions": [
    "belief",
    "social-goal",
    "goal-belief"
  ],
  "initialization_source": "memory_split_only",
  "embedding": {
    "method": "deterministic_signed_feature_hashing",
    "dimension": 1536,
    "fields": [
      "question",
      "options",
      "short_context_summary"
    ],
    "lowercase": true,
    "tokenizer_regex": "(?u)\\b\\w+\\b",
    "ngrams": [
      1,
      2
    ],
    "hash_function": "SHA-256",
    "hash_seed": 63841277,
    "index_bytes": "digest[0:8]_big_endian_mod_1536",
    "sign_rule": "positive_if_digest_byte_8_is_even_else_negative",
    "normalization": "L2",
    "similarity": "cosine",
    "zero_vector_similarity": 0.0,
    "similarity_tie_break": [
      "episode_id_ascending",
      "question_id_ascending"
    ]
  },
  "capacity_per_partition": 500,
  "trigger_retrieval_k": 5,
  "difficulty_retrieval_k": 5,
  "guidance_candidate_scan_limit": 15,
  "guidance_case_limit": 3,
  "guidance_filter": "correct == true and validity_score > 0.7",
  "entry_fields": [
    "memory_id",
    "episode_id",
    "question_id",
    "question_type",
    "question",
    "options",
    "short_context_summary",
    "ground_truth",
    "baseline_option_distribution",
    "trigger_decision",
    "difficulty_score",
    "difficulty_level",
    "maximum_rounds",
    "actual_rounds",
    "final_answer",
    "correct",
    "reasoning_summary",
    "validity_score",
    "access_count",
    "last_access_utc"
  ],
  "memory_id_format": "{question_type}:{episode_id}:{question_id}",
  "new_entry_validity": {
    "correct": 0.9,
    "incorrect": 0.3
  },
  "validity_update": {
    "useful": "min(1.0,e+0.1)",
    "not_useful": "max(0.1,e-0.05)"
  },
  "pruning_score": "0.5*e+0.3*log(1+access_count)-0.2*log(1+age_days)",
  "age_clock": "UTC_midnight_frozen_at_run_start",
  "standard_test_update": "disabled"
}
```

### Main-protocol initial memory construction

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-initial-memory-build-v1",
  "common": "common.json",
  "source_split_id": "muma-tom-main-qsplit-v1/memory",
  "source_assignments": "../splits/main_question_split_v1.csv",
  "expected_questions": 225,
  "processing_order": [
    "question_type_order",
    "episode_id_ascending",
    "question_id_ascending"
  ],
  "question_type_order": [
    "belief",
    "social-goal",
    "goal-belief"
  ],
  "entry_creation": {
    "run_baseline_and_debate_pipeline": true,
    "store_ground_truth_after_prediction": true,
    "store_reasoning_summary_not_raw_chain_of_thought": true,
    "correct_entry_validity": 0.9,
    "incorrect_entry_validity": 0.3
  },
  "validity_maintenance": {
    "evaluation_unit": "completed_run",
    "retrieved_and_selected_as_guidance_and_final_correct": "useful",
    "retrieved_and_selected_as_guidance_and_final_incorrect": "not_useful",
    "retrieved_but_not_selected_as_guidance": "no_change",
    "useful_update": "min(1.0,e+0.1)",
    "not_useful_update": "max(0.1,e-0.05)"
  },
  "snapshot": {
    "output": "outputs/memory/main_initial_memory.jsonl",
    "metadata_output": "outputs/memory/main_initial_memory_manifest.json",
    "sort_order": [
      "partition",
      "episode_id",
      "question_id"
    ],
    "checksum": "SHA-256"
  }
}
```

### Episode-disjoint initial memory construction

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-episode-disjoint-initial-memory-build-v1",
  "common": "common.json",
  "source_split_id": "muma-tom-episode-disjoint-v1/memory",
  "source_assignments": "../splits/episode_disjoint_questions_v1.csv",
  "expected_questions": 224,
  "expected_episodes": 56,
  "require_zero_episode_overlap_with": [
    "muma-tom-episode-disjoint-v1/validation",
    "muma-tom-episode-disjoint-v1/test"
  ],
  "processing_order": [
    "question_type_order",
    "episode_id_ascending",
    "question_id_ascending"
  ],
  "question_type_order": [
    "belief",
    "social-goal",
    "goal-belief"
  ],
  "entry_creation": {
    "run_baseline_and_debate_pipeline": true,
    "store_ground_truth_after_prediction": true,
    "store_reasoning_summary_not_raw_chain_of_thought": true,
    "correct_entry_validity": 0.9,
    "incorrect_entry_validity": 0.3
  },
  "validity_maintenance": {
    "evaluation_unit": "completed_run",
    "retrieved_and_selected_as_guidance_and_final_correct": "useful",
    "retrieved_and_selected_as_guidance_and_final_incorrect": "not_useful",
    "retrieved_but_not_selected_as_guidance": "no_change",
    "useful_update": "min(1.0,e+0.1)",
    "not_useful_update": "max(0.1,e-0.05)"
  },
  "snapshot": {
    "output": "outputs/memory/episode_disjoint_initial_memory.jsonl",
    "metadata_output": "outputs/memory/episode_disjoint_initial_memory_manifest.json",
    "sort_order": [
      "partition",
      "episode_id",
      "question_id"
    ],
    "checksum": "SHA-256"
  }
}
```

## Retrieval statistics and trigger

```json
{
  "statistics_scope": "all_type_matched_retrieved_memories",
  "epsilon": 1e-12,
  "feature_formulas": {
    "R_debate": "sum(d_k)/(N_ret+epsilon)",
    "R_succ": "sum(d_k*f_k)/(sum(d_k)+epsilon)",
    "R_correct": "sum(d_k*(1-b_k)*f_k)/(sum(d_k)+epsilon)",
    "R_harm": "sum(d_k*b_k*(1-f_k))/(sum(d_k)+epsilon)",
    "R_quick": "sum(d_k*tau_k)/(sum(d_k)+epsilon)",
    "mean_similarity": "sum(sim_k)/(N_ret+epsilon)"
  },
  "theta_0": 0.65,
  "alpha": 0.25,
  "validation_correct_trigger_decisions": 63,
  "validation_decisions": 90,
  "validation_trigger_accuracy": 0.7,
  "theta_formula": "theta_0-alpha*(validation_trigger_accuracy-0.5)",
  "test_theta": 0.6,
  "comparison": "strict_greater_than",
  "rules": [
    {
      "priority": 1,
      "condition": "N_ret < 2",
      "decision": "debate",
      "confidence": 0.7
    },
    {
      "priority": 2,
      "condition": "R_succ > 0.80 and N_ret >= 3 and normalized_entropy < 0.80",
      "decision": "no_debate",
      "confidence": "R_succ"
    },
    {
      "priority": 3,
      "condition": "R_correct > 2*R_harm",
      "decision": "debate",
      "confidence": "min(1,R_correct-R_harm+0.50)"
    },
    {
      "priority": 4,
      "condition": "p_max < 0.40 or normalized_entropy > 0.80 or top_two_ratio < 1.50 or mean_similarity < 0.20 or D >= 0.60",
      "decision": "debate",
      "confidence": 0.65
    },
    {
      "priority": 5,
      "condition": "otherwise",
      "decision": "no_debate",
      "confidence": 0.5
    }
  ],
  "final_decision": "matched_decision == debate and confidence > test_theta"
}
```

## Difficulty and debate-depth control

```json
{
  "formula": "0.4*(1-p_max)+0.3*normalized_entropy+0.2*(1-N_mem/5)+0.1*(question_length_words/100)",
  "weights": {
    "one_minus_p_max": 0.4,
    "normalized_entropy": 0.3,
    "memory_unavailability": 0.2,
    "question_length": 0.1
  },
  "memory_normalizer": 5,
  "question_length_normalizer_words": 100,
  "question_length_counting": "Unicode regex word tokens after whitespace normalization",
  "normalized_entropy": "-sum(p_j*log(p_j))/log(M)",
  "entropy_zero_term": "0*log(0)=0",
  "top_two_ratio": "p_max/max(p_second,1e-12)",
  "clip_components_and_final_score": [
    0.0,
    1.0
  ],
  "bands": {
    "low": "D < 0.30",
    "medium": "0.30 <= D < 0.60",
    "high": "D >= 0.60"
  }
}
```

```json
{
  "base_rounds": {
    "low": 3,
    "medium": 5,
    "high": 8
  },
  "minimum_rounds": 2,
  "successful_case_threshold": 3,
  "round_reduction_beta": 1,
  "successful_case_count_definition": "N_succ is the number of cases satisfying correct == true and validity_score > 0.7 among the at-most-15 type-matched candidates scanned before truncation to the at-most-3 cases inserted into the prompt",
  "maximum_rounds_formula": "max(minimum_rounds,base_rounds-round_reduction_beta*I[N_succ>=successful_case_threshold])",
  "early_stop_stable_rounds": 2,
  "early_stop_signal": "unchanged_parsed_synthesizer_answer",
  "round_schedule": [
    "logical_agent",
    "innovative_agent",
    "synthesizer_agent"
  ],
  "first_round_context": [
    "multimodal_background",
    "question",
    "options",
    "baseline_distribution",
    "up_to_three_high_validity_memories",
    "retrieval_pattern_summary"
  ],
  "later_round_context": [
    "first_round_context",
    "complete_previous_debate_messages"
  ],
  "answer_pattern": "Final Answer: [A-E]",
  "fallback": "majority_vote_over_last_valid_agent_answers",
  "fallback_tie_break": "alphabetical_option_order",
  "invalid_final_answer": "incorrect_and_retained_in_denominator"
}
```

## Evaluation modes

Standard evaluation constructs memory only from the memory split, uses validation only for hyperparameter selection and trigger calibration, freezes the memory snapshot before the test split, and never exposes test labels or correctness before final prediction. Ordinary results use `micro_accuracy` unless an experiment configuration explicitly selects `difficulty_balanced_accuracy`.

Oracle-feedback evaluation uses five ordered passes of the 585-question test split. A label is revealed only after its prediction completes. The oracle condition updates memory immediately after that completed prediction; the frozen control never updates memory. Its DB-Acc. difficulty assignment is generated before pass 1 and reused unchanged across both conditions and all passes.

## Complete experiment configurations

Each block below is the experiment-specific portion. The corresponding `configs/resolved/*.json` file additionally embeds every common parameter, support configuration, prompt body, split statistic, and checksum.

### `main.json`

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-main-evaluation-v1",
  "protocol_id": "muma-tom-main-qsplit-v1",
  "assignments": "../splits/main_question_split_v1.csv",
  "memory_split_id": "muma-tom-main-qsplit-v1/memory",
  "validation_split_id": "muma-tom-main-qsplit-v1/validation",
  "evaluation_split_id": "muma-tom-main-qsplit-v1/test",
  "expected_counts": {
    "memory": 225,
    "validation": 90,
    "test": 585
  },
  "expected_per_type": {
    "memory": 75,
    "validation": 30,
    "test": 195
  },
  "run_id": "main-gpt4o-run-01",
  "run_seed": 35719823,
  "core_reasoner": "gpt-4o-2024-11-20",
  "visual_parser": "gemini-2.5-pro-preview-05-06",
  "evaluation_mode": "frozen_memory_offline",
  "accuracy_metric_id": "micro_accuracy",
  "memory_updates_during_test": false,
  "output_jsonl": "outputs/main/gpt4o_full_framework_run01.jsonl",
  "summary_json": "outputs/main/gpt4o_full_framework_run01_summary.json"
}
```

### `episode_disjoint.json`

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-episode-disjoint-evaluation-v1",
  "protocol_id": "muma-tom-episode-disjoint-v1",
  "episode_assignments": "../splits/episode_disjoint_episodes_v1.csv",
  "question_assignments": "../splits/episode_disjoint_questions_v1.csv",
  "initial_memory_build_config": "episode_disjoint_initial_memory_build.json",
  "memory_split_id": "muma-tom-episode-disjoint-v1/memory",
  "validation_split_id": "muma-tom-episode-disjoint-v1/validation",
  "evaluation_split_id": "muma-tom-episode-disjoint-v1/test",
  "expected_episode_counts": {
    "memory": 56,
    "validation": 23,
    "test": 146
  },
  "expected_question_counts": {
    "memory": 224,
    "validation": 92,
    "test": 584
  },
  "run_id": "episode-disjoint-gpt4o-run-01",
  "run_seed": 35719823,
  "core_reasoner": "gpt-4o-2024-11-20",
  "visual_parser": "gemini-2.5-pro-preview-05-06",
  "evaluation_mode": "frozen_memory_offline",
  "accuracy_metric_id": "micro_accuracy",
  "require_episode_intersection_size": 0,
  "initial_memory_snapshot": "outputs/memory/episode_disjoint_initial_memory.jsonl",
  "initial_memory_manifest": "outputs/memory/episode_disjoint_initial_memory_manifest.json",
  "paired_comparisons": [
    "single_pass_multimodal",
    "debate_without_memory",
    "fixed_round_debate",
    "without_memory_partitioning"
  ],
  "multiple_comparison_method": "Holm-Bonferroni",
  "output_jsonl": "outputs/episode_disjoint/all_methods_run01.jsonl",
  "summary_json": "outputs/episode_disjoint/paired_statistics.json"
}
```

### `backbone_comparison.json`

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-backbone-comparison-v1",
  "protocol_id": "muma-tom-main-qsplit-v1",
  "evaluation_split_id": "muma-tom-main-qsplit-v1/test",
  "questions": 585,
  "run_id": "backbone-comparison-run-01",
  "run_seed": 35719823,
  "visual_parser": "gemini-2.5-pro-preview-05-06",
  "core_reasoners": [
    "gpt-5",
    "gpt-4o-2024-11-20",
    "DeepSeek-V3.1",
    "Qwen3-VL-32B-Instruct",
    "Meta-Llama-3.2-90B-Vision-Instruct"
  ],
  "methods": [
    "Shi_et_al_single_pass_multimodal",
    "single_model_variant",
    "BIP-ALM",
    "full_framework"
  ],
  "memory_mode": "frozen_memory_offline",
  "per_model_accuracy_metric_id": "micro_accuracy",
  "aggregation": [
    "per_model_micro_accuracy",
    "unweighted_mean_over_five_core_reasoner_micro_accuracies"
  ],
  "output_jsonl": "outputs/backbone_comparison/all_models_all_methods.jsonl",
  "summary_json": "outputs/backbone_comparison/accuracy_summary.json",
  "figure_output": "outputs/backbone_comparison/model_comparison.pdf"
}
```

### `modality_decoupling.json`

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-modality-decoupling-v1",
  "protocol_id": "muma-tom-main-qsplit-v1",
  "evaluation_split_id": "muma-tom-main-qsplit-v1/test",
  "questions": 585,
  "run_id": "modality-decoupling-run-01",
  "run_seed": 35719823,
  "core_reasoners": [
    "gpt-5",
    "gpt-4o-2024-11-20",
    "DeepSeek-V3.1",
    "Qwen3-VL-32B-Instruct",
    "Meta-Llama-3.2-90B-Vision-Instruct"
  ],
  "conditions": [
    {
      "condition_id": "text_only_single_pass",
      "text_description": true,
      "video_derived_cues": false,
      "reasoning": "single_pass"
    },
    {
      "condition_id": "video_cues_only_single_pass",
      "text_description": false,
      "video_derived_cues": true,
      "reasoning": "single_pass"
    },
    {
      "condition_id": "text_video_single_pass",
      "text_description": true,
      "video_derived_cues": true,
      "reasoning": "single_pass"
    },
    {
      "condition_id": "text_video_full_framework",
      "text_description": true,
      "video_derived_cues": true,
      "reasoning": "memory_adaptive_debate"
    }
  ],
  "per_model_accuracy_metric_id": "micro_accuracy",
  "aggregation": "unweighted_mean_over_five_core_reasoner_micro_accuracies",
  "output_jsonl": "outputs/modality_decoupling/all_conditions.jsonl",
  "summary_json": "outputs/modality_decoupling/table_summary.json"
}
```

### `debate_statistics.json`

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-debate-statistics-v1",
  "protocol_id": "muma-tom-main-qsplit-v1",
  "evaluation_split_id": "muma-tom-main-qsplit-v1/test",
  "questions": 585,
  "run_id": "debate-statistics-run-01",
  "run_seed": 35719823,
  "core_reasoners": [
    "gpt-5",
    "gpt-4o-2024-11-20",
    "DeepSeek-V3.1",
    "Qwen3-VL-32B-Instruct",
    "Meta-Llama-3.2-90B-Vision-Instruct"
  ],
  "metrics": {
    "R_debate": {
      "numerator": "triggered_questions",
      "denominator": "all_test_questions"
    },
    "R_succ": {
      "numerator": "triggered_and_final_correct",
      "denominator": "triggered_questions"
    },
    "R_correct": {
      "numerator": "triggered_baseline_wrong_final_correct",
      "denominator": "triggered_questions"
    },
    "R_harm": {
      "numerator": "triggered_baseline_correct_final_wrong",
      "denominator": "triggered_questions"
    },
    "early_termination_rate": {
      "numerator": "triggered_and_terminated_before_max_rounds",
      "denominator": "triggered_questions"
    }
  },
  "confidence_intervals": {
    "model": "gpt-4o-2024-11-20",
    "method": "Wilson",
    "confidence_level": 0.95
  },
  "breakdowns": [
    "difficulty",
    "question_type",
    "core_reasoner"
  ],
  "input_jsonl": "outputs/backbone_comparison/all_models_all_methods.jsonl",
  "summary_json": "outputs/debate_statistics/metrics_and_wilson_intervals.json"
}
```

### `ablation.json`

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-ablation-v1",
  "protocol_id": "muma-tom-main-qsplit-v1",
  "evaluation_split_id": "muma-tom-main-qsplit-v1/test",
  "questions": 585,
  "run_id": "ablation-run-01",
  "run_seed": 35719823,
  "core_reasoners": [
    "gpt-5",
    "gpt-4o-2024-11-20",
    "DeepSeek-V3.1",
    "Qwen3-VL-32B-Instruct",
    "Meta-Llama-3.2-90B-Vision-Instruct"
  ],
  "conditions": [
    {
      "condition_id": "no_debate",
      "memory": false,
      "debate": false
    },
    {
      "condition_id": "debate_without_memory",
      "memory": false,
      "debate": true,
      "round_control": "adaptive"
    },
    {
      "condition_id": "fixed_3_round_debate",
      "memory": true,
      "debate": true,
      "rounds": 3,
      "early_termination": false
    },
    {
      "condition_id": "fixed_5_round_debate",
      "memory": true,
      "debate": true,
      "rounds": 5,
      "early_termination": false
    },
    {
      "condition_id": "fixed_8_round_debate",
      "memory": true,
      "debate": true,
      "rounds": 8,
      "early_termination": false
    },
    {
      "condition_id": "without_memory_partitioning",
      "memory": true,
      "memory_partitions": 1,
      "debate": true,
      "round_control": "adaptive"
    },
    {
      "condition_id": "full_framework",
      "memory": true,
      "memory_partitions": 3,
      "debate": true,
      "round_control": "adaptive",
      "early_termination": true
    }
  ],
  "per_model_accuracy_metric_id": "micro_accuracy",
  "aggregation": "unweighted_mean_over_five_core_reasoner_micro_accuracies",
  "output_jsonl": "outputs/ablation/all_conditions.jsonl",
  "summary_json": "outputs/ablation/accuracy_summary.json",
  "figure_output": "outputs/ablation/accuracy_comparison_7conditions.pdf"
}
```

### `budget_matched.json`

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-budget-matched-v1",
  "protocol_id": "muma-tom-main-qsplit-v1",
  "evaluation_split_id": "muma-tom-main-qsplit-v1/test",
  "questions": 585,
  "run_id": "budget-matched-run-01",
  "run_seed": 35719823,
  "core_reasoner": "gpt-3.5-turbo-0125",
  "visual_parser": "gemini-2.5-pro-preview-05-06",
  "exclude_visual_parsing_tokens": true,
  "reference_method": "full_framework",
  "reference_budget_ratio": 1.0,
  "methods": [
    "single_pass_reasoning",
    "self_consistency",
    "majority_voting",
    "RAG_without_debate",
    "memory_only_without_debate",
    "debate_without_memory",
    "full_framework"
  ],
  "multi_call_target_token_range": [
    16280,
    17680
  ],
  "accuracy_metric_id": "difficulty_balanced_accuracy",
  "difficulty_reference_id": "muma-tom-gpt35-main-test-difficulty-v1",
  "reported_metrics": [
    "difficulty_balanced_accuracy",
    "micro_accuracy",
    "average_reasoning_tokens",
    "budget_ratio",
    "average_api_calls"
  ],
  "output_jsonl": "outputs/budget_matched/all_methods.jsonl",
  "summary_json": "outputs/budget_matched/table_summary.json"
}
```

### `repeated_runs.json`

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-repeated-runs-v1",
  "protocol_id": "muma-tom-main-qsplit-v1",
  "evaluation_split_id": "muma-tom-main-qsplit-v1/test",
  "subset_id": "muma-tom-repeat550-v1",
  "subset_assignments": "../splits/repeated_run_subset_550_v1.csv",
  "questions_per_run": 550,
  "runs": 5,
  "run_seeds": [
    35719823,
    68245109,
    11472863,
    94026571,
    52680347
  ],
  "run_ids": [
    "repeat-run-01",
    "repeat-run-02",
    "repeat-run-03",
    "repeat-run-04",
    "repeat-run-05"
  ],
  "core_reasoner": "gpt-3.5-turbo-0125",
  "visual_parser": "gemini-2.5-pro-preview-05-06",
  "methods": [
    "single_pass_reasoning",
    "Shi_et_al_baseline",
    "debate_without_memory",
    "full_framework"
  ],
  "same_ordered_question_ids_for_all_methods_and_runs": true,
  "memory_mode": "frozen_memory_offline",
  "per_run_accuracy_metric_id": "micro_accuracy",
  "run_summary": [
    "mean_accuracy",
    "sample_standard_deviation_accuracy"
  ],
  "output_pattern": "outputs/repeated_runs/{method_id}/{run_id}.jsonl",
  "summary_json": "outputs/repeated_runs/five_run_summary.json"
}
```

### `paired_statistics.json`

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-paired-statistics-v1",
  "subset_id": "muma-tom-repeat550-v1",
  "questions": 550,
  "runs": 5,
  "run_id": "paired-statistics-v1",
  "prediction_aggregation": "majority_vote_per_question",
  "valid_labels": [
    "A",
    "B",
    "C",
    "D",
    "E"
  ],
  "vote_tie_break": "alphabetical_option_order",
  "invalid_prediction": "incorrect_and_retained_in_denominator",
  "bootstrap": {
    "unit": "paired_question_id",
    "resamples": 5000,
    "confidence_level": 0.95,
    "interval": "percentile",
    "seed": 84726111
  },
  "mcnemar": {
    "continuity_correction": true,
    "formula": "(|n01-n10|-1)^2/(n01+n10)"
  },
  "multiple_comparisons": {
    "method": "Holm-Bonferroni",
    "family_size": 3,
    "comparisons": [
      "full_framework_vs_single_pass",
      "full_framework_vs_Shi_et_al",
      "full_framework_vs_debate_without_memory"
    ]
  },
  "input_pattern": "outputs/repeated_runs/{method_id}/{run_id}.jsonl",
  "output_json": "outputs/repeated_runs/paired_statistics.json"
}
```

### `computational_cost.json`

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-computational-cost-v1",
  "protocol_id": "muma-tom-main-qsplit-v1",
  "evaluation_split_id": "muma-tom-main-qsplit-v1/test",
  "questions": 585,
  "run_id": "computational-cost-run-01",
  "run_seed": 35719823,
  "core_reasoner": "gpt-3.5-turbo-0125",
  "visual_parser": "gemini-2.5-pro-preview-05-06",
  "exclude_visual_parsing_cost": true,
  "relative_cost_reference": "always_debate_8_rounds",
  "strategies": [
    {
      "strategy_id": "single_pass_reasoning",
      "debate_trigger": false
    },
    {
      "strategy_id": "always_debate_3_rounds",
      "debate_trigger": "always",
      "rounds": 3,
      "early_termination": false
    },
    {
      "strategy_id": "always_debate_5_rounds",
      "debate_trigger": "always",
      "rounds": 5,
      "early_termination": false
    },
    {
      "strategy_id": "always_debate_8_rounds",
      "debate_trigger": "always",
      "rounds": 8,
      "early_termination": false
    },
    {
      "strategy_id": "fixed_8_round_debate",
      "debate_trigger": "adaptive",
      "rounds": 8,
      "early_termination": false
    },
    {
      "strategy_id": "early_termination_only",
      "debate_trigger": "always",
      "maximum_rounds": 8,
      "early_termination": true
    },
    {
      "strategy_id": "full_framework",
      "debate_trigger": "adaptive",
      "round_control": "adaptive",
      "early_termination": true
    }
  ],
  "accuracy_metric_id": "difficulty_balanced_accuracy",
  "difficulty_reference_id": "muma-tom-gpt35-main-test-difficulty-v1",
  "reported_metrics": [
    "difficulty_balanced_accuracy",
    "micro_accuracy",
    "average_reasoning_tokens",
    "average_api_calls",
    "relative_api_cost"
  ],
  "output_jsonl": "outputs/computational_cost/all_strategies.jsonl",
  "summary_json": "outputs/computational_cost/table_summary.json"
}
```

### `sensitivity.json`

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-sensitivity-v1",
  "protocol_id": "muma-tom-main-qsplit-v1",
  "evaluation_split_id": "muma-tom-main-qsplit-v1/test",
  "questions": 585,
  "run_id": "sensitivity-run-01",
  "run_seed": 35719823,
  "core_reasoner": "gpt-3.5-turbo-0125",
  "design": "one_factor_at_a_time",
  "default": {
    "theta": 0.6,
    "T_succ": 3,
    "low_medium_boundary": 0.3,
    "medium_high_boundary": 0.6
  },
  "variations": {
    "theta": [
      0.55,
      0.6,
      0.65
    ],
    "T_succ": [
      2,
      3,
      4
    ],
    "low_medium_boundary": [
      0.25,
      0.3,
      0.35
    ],
    "medium_high_boundary": [
      0.55,
      0.6,
      0.65
    ]
  },
  "settings": [
    {
      "setting_id": "default",
      "changed_parameter": "NONE",
      "theta": 0.6,
      "T_succ": 3,
      "low_medium_boundary": 0.3,
      "medium_high_boundary": 0.6
    },
    {
      "setting_id": "theta_0p55",
      "changed_parameter": "theta",
      "theta": 0.55,
      "T_succ": 3,
      "low_medium_boundary": 0.3,
      "medium_high_boundary": 0.6
    },
    {
      "setting_id": "theta_0p65",
      "changed_parameter": "theta",
      "theta": 0.65,
      "T_succ": 3,
      "low_medium_boundary": 0.3,
      "medium_high_boundary": 0.6
    },
    {
      "setting_id": "T_succ_2",
      "changed_parameter": "T_succ",
      "theta": 0.6,
      "T_succ": 2,
      "low_medium_boundary": 0.3,
      "medium_high_boundary": 0.6
    },
    {
      "setting_id": "T_succ_4",
      "changed_parameter": "T_succ",
      "theta": 0.6,
      "T_succ": 4,
      "low_medium_boundary": 0.3,
      "medium_high_boundary": 0.6
    },
    {
      "setting_id": "low_medium_0p25",
      "changed_parameter": "low_medium_boundary",
      "theta": 0.6,
      "T_succ": 3,
      "low_medium_boundary": 0.25,
      "medium_high_boundary": 0.6
    },
    {
      "setting_id": "low_medium_0p35",
      "changed_parameter": "low_medium_boundary",
      "theta": 0.6,
      "T_succ": 3,
      "low_medium_boundary": 0.35,
      "medium_high_boundary": 0.6
    },
    {
      "setting_id": "medium_high_0p55",
      "changed_parameter": "medium_high_boundary",
      "theta": 0.6,
      "T_succ": 3,
      "low_medium_boundary": 0.3,
      "medium_high_boundary": 0.55
    },
    {
      "setting_id": "medium_high_0p65",
      "changed_parameter": "medium_high_boundary",
      "theta": 0.6,
      "T_succ": 3,
      "low_medium_boundary": 0.3,
      "medium_high_boundary": 0.65
    }
  ],
  "expected_setting_count": 9,
  "unchanged_parameter_policy": "every field other than changed_parameter equals the default setting",
  "successful_case_count_definition": "qualifying successful cases in the at-most-15 pre-truncation guidance candidate pool; counting occurs before the prompt insertion cap of three",
  "fixed_uncertainty_trigger_cutoff": "D >= 0.60",
  "trigger_comparison": "confidence > theta",
  "accuracy_metric_id": "difficulty_balanced_accuracy",
  "difficulty_reference_id": "muma-tom-gpt35-main-test-difficulty-v1",
  "reported_metrics": [
    "difficulty_balanced_accuracy",
    "micro_accuracy",
    "average_reasoning_tokens"
  ],
  "required_result_groups": "one complete 585-question group for each sensitivity_setting_id",
  "output_jsonl": "outputs/sensitivity/all_variations.jsonl",
  "summary_json": "outputs/sensitivity/ofat_summary.json"
}
```

### `oracle_feedback.json`

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-oracle-feedback-v1",
  "protocol_id": "muma-tom-main-qsplit-v1",
  "evaluation_split_id": "muma-tom-main-qsplit-v1/test",
  "questions_per_pass": 585,
  "passes": 5,
  "run_id": "oracle-feedback-run-01",
  "run_seed": 35719823,
  "core_reasoner": "gpt-4o-2024-11-20",
  "conditions": [
    "frozen_memory_control",
    "oracle_feedback"
  ],
  "initial_memory_source": "muma-tom-main-qsplit-v1/memory",
  "validation_use": "hyperparameter_selection_only",
  "question_order": [
    "episode_id_ascending",
    "question_id_ascending"
  ],
  "label_reveal": "after_prediction_completion",
  "oracle_update_schedule": "after_each_completed_prediction",
  "frozen_control_update_schedule": "disabled",
  "accuracy_metric_id": "difficulty_balanced_accuracy",
  "difficulty_reference_id": "muma-tom-gpt4o-oracle-prepass-difficulty-v1",
  "difficulty_assignment_frozen_before_pass": 1,
  "reuse_same_difficulty_assignment_across_conditions_and_passes": true,
  "reported_metrics": [
    "difficulty_balanced_accuracy",
    "micro_accuracy"
  ],
  "reported_separately_from_standard_offline_accuracy": true,
  "output_jsonl": "outputs/oracle_feedback/all_passes_both_conditions.jsonl",
  "summary_json": "outputs/oracle_feedback/pass_summary.json"
}
```

### `human_reference.json`

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-human-reference-v1",
  "protocol_id": "muma-tom-main-qsplit-v1",
  "evaluation_split_id": "muma-tom-main-qsplit-v1/test",
  "subset_id": "muma-tom-human100-v1",
  "subset_assignments": "../splits/human_reference_subset_100_v1.csv",
  "questions": 100,
  "participants": 6,
  "run_id": "human-reference-v1",
  "presentation_order": "randomized_per_participant",
  "participant_order_seeds": [
    26371049,
    77532061,
    42168937,
    90614253,
    14857309,
    65480127
  ],
  "abstention_encoding": "ABSTAIN",
  "response_labels": [
    "A",
    "B",
    "C",
    "D",
    "E",
    "ABSTAIN"
  ],
  "reference_accuracy": {
    "participant_formula": "correct_answered / answered",
    "answered_formula": "assigned_questions - abstained",
    "group_formula": "unweighted arithmetic mean of the six participant accuracies",
    "participant_weight": "1/6",
    "zero_answered_policy": "invalid_input"
  },
  "agreement": {
    "statistic": "Fleiss_kappa",
    "missing_response_policy": "complete_case_questions_only",
    "complete_case_definition": "all six participants supplied A-E; any question containing ABSTAIN is excluded from kappa only",
    "rating_categories": [
      "A",
      "B",
      "C",
      "D",
      "E"
    ],
    "minimum_complete_case_questions": 2,
    "confidence_interval": {
      "method": "question_level_nonparametric_percentile_bootstrap",
      "resamples": 10000,
      "seed": 84726111,
      "confidence_level": 0.95,
      "quantile_definition": "linear interpolation at (n-1)*p",
      "degenerate_replicate_policy": "discard_and_redraw_until_resamples_valid_or_100_times_resamples_attempts"
    }
  },
  "response_csv_schema": {
    "unique_key": [
      "participant_id",
      "episode_id",
      "question_id"
    ],
    "required_fields": {
      "participant_id": "P01 through P06 pseudonym",
      "presentation_order": "integer 1 through 100 unique within participant",
      "episode_id": "dataset episode identifier",
      "question_id": "question identifier within episode",
      "response": "A|B|C|D|E|ABSTAIN",
      "ground_truth": "A|B|C|D|E"
    },
    "required_rows": 600,
    "question_membership": "exactly the 100 keys in subset_assignments for every participant"
  },
  "participant_summary_csv_schema": {
    "required_fields": [
      "participant_id",
      "assigned",
      "answered",
      "abstained",
      "correct_answered",
      "accuracy"
    ],
    "required_rows": 6
  },
  "majority_vote_use": "agreement_label_only",
  "responses_csv": "outputs/human_reference/responses.csv",
  "participant_summary_csv": "outputs/human_reference/participant_summary.csv",
  "aggregation_entrypoint": "../scripts/compute_human_reference.py",
  "summary_json": "outputs/human_reference/accuracy_and_agreement.json"
}
```

### `confidence_consistency.json`

```json
{
  "schema_version": "1.0",
  "config_id": "controlled-confidence-consistency-v1",
  "dataset_source": "Baker_food_truck_tasks",
  "source_implementation": {
    "repository": "https://github.com/SCAI-JHU/AutoToM",
    "commit": "3f569b7ab1d0ee2702ab43ebdc724679d5fc5231",
    "online_goal_source_keys": [
      "1",
      "2",
      "3",
      "4",
      "5",
      "6"
    ],
    "food_truck_source_keys": [
      "1",
      "2",
      "5",
      "16",
      "18",
      "55",
      "56"
    ],
    "food_truck_reuse": "the same seven source stimuli are analyzed once for desire scores and once for belief scores"
  },
  "protocol_id": "controlled-confidence-consistency-v1",
  "scenario_assignments": "../splits/confidence_consistency_scenarios_v1.csv",
  "observation_schema": "confidence_observation_schema.json",
  "tasks": {
    "online_goal_inference": {
      "scenarios": 6,
      "selection": "all"
    },
    "desire_inference": {
      "scenarios": 7,
      "selection": "one_representative_per_type"
    },
    "belief_inference": {
      "scenarios": 7,
      "selection": "one_representative_per_type"
    }
  },
  "total_scenarios": 20,
  "run_id": "confidence-consistency-run-01",
  "run_seed": 35719823,
  "memory_bank": "empty",
  "debate_control": "difficulty_only",
  "human_rating_scale": "retain_original_task_specific_scale",
  "correlation": "Pearson_per_task",
  "bootstrap": {
    "unit": "scenario_cluster",
    "preserve_sequential_observations": true,
    "resamples": 5000,
    "confidence_level": 0.95,
    "seed": 84726111
  },
  "models": [
    "full_framework",
    "gpt-4o-2024-11-20",
    "o4-mini",
    "gemini-2.5-flash"
  ],
  "raw_observations_csv": "outputs/confidence_consistency/sequential_observations.csv",
  "aggregation_entrypoint": "../scripts/compute_confidence_consistency.py",
  "summary_json": "outputs/confidence_consistency/correlations_and_clustered_intervals.json",
  "figure_output": "outputs/confidence_consistency/human_alignment.pdf"
}
```

## Per-question result record

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-result-record-schema-v1",
  "format": "JSON Lines UTF-8",
  "one_record_per": "unique_record_key",
  "unique_record_key": [
    "protocol_id",
    "run_id",
    "model_id",
    "method_id",
    "condition_id",
    "pass_index",
    "sensitivity_setting_id",
    "episode_id",
    "question_id"
  ],
  "required_fields": {
    "protocol_id": "string",
    "split_id": "string",
    "run_id": "string",
    "run_seed": "integer",
    "model_id": "string",
    "method_id": "string",
    "condition_id": "string|NOT_APPLICABLE",
    "pass_index": "positive_integer|NOT_APPLICABLE",
    "sensitivity_setting_id": "string|NOT_APPLICABLE",
    "episode_id": "string",
    "question_id": "string",
    "question_type": "belief|social-goal|goal-belief",
    "ground_truth": "A|B|C|D|E",
    "baseline_option_scores": "object label->float",
    "baseline_answer": "A|B|C|D|E",
    "trigger_rule_priority": "integer",
    "trigger_decision": "boolean",
    "trigger_confidence": "float",
    "difficulty_score": "float",
    "difficulty_level": "low|medium|high",
    "metric_stratum_reference_id": "string|NOT_APPLICABLE",
    "metric_stratum": "low|medium|high|NOT_APPLICABLE",
    "maximum_rounds": "integer",
    "actual_rounds": "integer",
    "early_termination": "boolean",
    "final_answer": "A|B|C|D|E|INVALID",
    "baseline_correct": "boolean",
    "final_correct": "boolean",
    "prompt_tokens": "integer",
    "completion_tokens": "integer",
    "api_calls": "integer",
    "retrieved_memory_ids": "array[string]",
    "wall_time_seconds": "float"
  },
  "applicability_rules": {
    "oracle_feedback": "condition_id is frozen_memory_control or oracle_feedback; pass_index is 1 through 5; sensitivity_setting_id is NOT_APPLICABLE",
    "sensitivity": "condition_id and pass_index are NOT_APPLICABLE; sensitivity_setting_id is one of the nine IDs in sensitivity.json",
    "all_other_experiments": "condition_id, pass_index, and sensitivity_setting_id are NOT_APPLICABLE",
    "difficulty_balanced_accuracy": "metric_stratum_reference_id and metric_stratum must identify the frozen assignment used for aggregation",
    "micro_accuracy_only": "metric_stratum_reference_id and metric_stratum are NOT_APPLICABLE"
  },
  "optional_fields": {
    "provider_request_id": "string",
    "retry_count": "integer",
    "seed_supported": "boolean",
    "score_source": "token_logprobs|bounded_fallback",
    "parser_fallback_used": "boolean",
    "error_code": "string"
  },
  "invalid_final_answer_policy": "store_INVALID_set_final_correct_false_retain_denominator"
}
```

## Run manifest

```json
{
  "schema_version": "1.0",
  "config_id": "muma-tom-run-manifest-schema-v1",
  "required_fields": {
    "run_id": "string",
    "started_at_utc": "ISO-8601 string",
    "finished_at_utc": "ISO-8601 string",
    "git_commit": "40-character SHA-1",
    "config_files": "array[{path,sha256}]",
    "split_files": "array[{path,sha256}]",
    "prompt_files": "array[{path,sha256}]",
    "metric_config_file": "{path,sha256}",
    "accuracy_metric_id": "string",
    "result_record_key": "array[string] equal to result_record_schema.json/unique_record_key",
    "condition_ids": "array[string] including NOT_APPLICABLE when unused",
    "pass_indices": "array[positive_integer]|[NOT_APPLICABLE]",
    "sensitivity_setting_ids": "array[string] including NOT_APPLICABLE when unused",
    "metric_reference_assignment": "{id,path,sha256}|NOT_APPLICABLE",
    "model_routes": "object stage->{requested_model,resolved_model,provider}",
    "run_seed": "integer",
    "seed_support": "object stage->boolean",
    "environment": "environment.json contents and SHA-256",
    "question_count": "integer",
    "completed_question_count": "integer",
    "failed_question_count": "integer",
    "output_jsonl": "path",
    "output_sha256": "string",
    "metric_summary_json": "path",
    "metric_summary_sha256": "string"
  },
  "failure_policy": {
    "continue_after_question_failure": true,
    "write_failure_record": true,
    "exclude_failed_question_from_denominator": false,
    "failed_question_final_answer": "INVALID"
  }
}
```

## Statistical procedures

- Five runs use the same ordered 550-question subset and the five fixed run seeds.
- Run summaries report mean accuracy and sample standard deviation (`ddof=1`).
- Five predictions per method/question are aggregated by majority vote for paired inference.
- Vote ties select the alphabetically earliest valid option.
- Invalid predictions remain in the denominator and are scored incorrect.
- Paired bootstrap uses 5,000 question-level resamples, seed `84726111`, and percentile 95% intervals.
- McNemar uses `(|n01-n10|-1)^2/(n01+n10)`.
- Three repeated-run comparisons use Holm-Bonferroni correction.
- The episode-disjoint family contains four paired comparisons and uses Holm-Bonferroni correction.
- Confidence-consistency intervals use 5,000 scenario-clustered resamples and preserve every sequential observation from a sampled scenario.

## Statistical entry points

```text
python scripts/compute_metrics.py --results <results.jsonl> --difficulty-assignments <difficulty.csv> --output <summary.json>
python scripts/compute_human_reference.py --responses <responses.csv> --output <summary.json> --participant-output <participants.csv>
python scripts/compute_confidence_consistency.py --observations <observations.csv> --output <summary.json>
```

Each command validates exact key coverage before writing a summary. The confidence command additionally requires every scenario-to-source mapping to be resolved.

## Complete prompt templates

### `person_action_utterance_parsing.txt`

Stage: `multimodal_parsing`. Origin: `adapted_from_manuscript_appendix`.

```text
You are a social scenario understanding expert. Extract the chronological actions and utterances of the specified person from the supplied context.

Rules:
1. Retain only actions performed by {{target_person}}.
2. Replace ambiguous pronouns with explicit objects or locations when the context supports the replacement.
3. Preserve chronological order.
4. Return an empty list when no valid action or utterance is present.
5. Do not add explanations.

Context:
{{context}}

Target person:
{{target_person}}

Return exactly:
Actions: ['action one', ...]
Utterances: ['utterance one', ...]
```

### `initial_state_extraction.txt`

Stage: `initial_state`. Origin: `adapted_from_manuscript_appendix`.

```text
You are a scene analyst. Infer the environmental state before any listed action occurred. Focus on object placements implied by actions such as grab, put, open, and close. Do not infer facts unsupported by the action sequence.

Actions:
{{actions}}

Return only statements in this form, one per line:
There is a [object] [location].
```

### `latent_hypothesis_generation.txt`

Stage: `hypothesis_generation`. Origin: `adapted_from_manuscript_appendix`.

```text
You are a theory-of-mind reasoner. For every answer option, construct one hypothesis H = <b(s), g_i, b(g_j)> containing:
- the target agent's belief about the environment state;
- the target agent's social goal or attitude toward the other agent's actions;
- what the target agent believes the other agent's physical goal to be.

Context:
{{context}}

Question:
{{question}}

Options:
{{options}}

Return exactly one semicolon-delimited hypothesis per option:
A: <belief; social goal; belief about other agent's goal>
B: <belief; social goal; belief about other agent's goal>
Continue through the final supplied option.
```

### `visual_action_extraction.txt`

Stage: `visual_action_extraction`. Origin: `adapted_from_manuscript_appendix`.

```text
You are a visual behavior interpreter. Summarize only the actions performed by {{target_person}} using these action types: walk to, grab from, open, close, and put. Infer room-level locations only when supported by the visual evidence or scene description. Use consistent object names and preserve chronological order. Do not add explanations.

Scene description:
{{scene_description}}

Target person:
{{target_person}}

Return exactly:
Actions: ['action1', 'action2', ...]
```

### `visual_request_user_message.txt`

Stage: `visual_request`. Origin: `generated_for_code_release`.

```text
Analyze the attached video or ordered frames for the following request.

Target person:
{{target_person}}

Additional scene information:
{{scene_description}}

Media attachment identifier:
{{media_attachment_id}}
```

### `utterance_likelihood.txt`

Stage: `utterance_likelihood`. Origin: `adapted_from_manuscript_appendix`.

```text
You are a mental-state simulator. Judge whether the target agent would generate the observed utterance under the supplied hypothesis and preceding context.

Decision rules:
1. Check whether the utterance is consistent with the target agent's belief about the physical state.
2. Under a helping or cooperative social goal, accurate belief-consistent information is more likely than misleading information.
3. Under a hindering or deceptive social goal, strategically misleading information can be likely even when it conflicts with the target agent's private belief.
4. Use the preceding utterance only as conversational context; do not replace the target agent's hypothesized belief with the counterpart's statement.
5. Judge the supplied utterance, not an alternative utterance.

Hypothesis H:
{{hypothesis}}

Initial state:
{{initial_state}}

Previous interaction history:
{{history}}

Counterpart's preceding utterance:
{{counterpart_utterance}}

Target utterance:
{{target_utterance}}

Return exactly one option:
A) Likely
B) Unlikely
```

### `action_likelihood.txt`

Stage: `action_likelihood`. Origin: `generated_from_manuscript_method`.

```text
You are a mental-state simulator. Judge whether the target agent would perform the observed action under the supplied hypothesis, initial state, and prior interaction history.

Decision rules:
1. Check physical feasibility from the initial state and prior actions.
2. Check whether the action advances the target agent's hypothesized physical or social goal.
3. Check consistency with what the target agent believes, rather than with privileged ground truth.
4. Account for helping, hindering, and deceptive intentions when they are present in the hypothesis.
5. Judge the supplied action, not a more optimal alternative.

Hypothesis H:
{{hypothesis}}

Initial state:
{{initial_state}}

Previous interaction history:
{{history}}

Target action:
{{target_action}}

Return exactly one option:
A) Likely
B) Unlikely
```

### `bounded_score_fallback.txt`

Stage: `likelihood_fallback`. Origin: `generated_from_manuscript_method`.

```text
Estimate the relative compatibility of the observation with the supplied hypothesis when token log probabilities are unavailable. The score is used only to rank answer options within this request and is not a calibrated probability.

Hypothesis H:
{{hypothesis}}

Initial state:
{{initial_state}}

Previous interaction history:
{{history}}

Observation type:
{{observation_type}}

Observation:
{{observation}}

Scoring anchors:
- 0.00: incompatible with the hypothesis or physically impossible.
- 0.25: weakly compatible but contradicted by important evidence.
- 0.50: ambiguous or approximately neutral.
- 0.75: strongly compatible with minor uncertainty.
- 1.00: directly expected under the hypothesis.

Return only valid JSON with one decimal number in [0, 1] and no surrounding text:
{"score": 0.000000}
```

### `question_type_classification.txt`

Stage: `question_type_classification`. Origin: `generated_from_manuscript_method`.

```text
Classify the question into exactly one MuMA-ToM reasoning type.

Definitions:
- belief: infer an agent's belief about the physical state.
- social-goal: infer whether an agent intends to help, hinder, cooperate, or mislead.
- goal-belief: infer one agent's belief about another agent's physical goal.

Question:
{{question}}

Options:
{{options}}

Return exactly one label:
belief
social-goal
goal-belief

Tie rule: choose the type corresponding to the deepest mental-state relation explicitly requested by the question; `goal-belief` takes priority over `social-goal`, which takes priority over `belief`.
```

### `short_context_summary.txt`

Stage: `memory_retrieval_summary`. Origin: `generated_from_manuscript_method`.

```text
Summarize the supplied multimodal interaction context for similarity retrieval. Preserve the agents, object locations, actions, utterances, and belief-relevant state changes. Do not answer the multiple-choice question. Use at most 100 words.

Context:
{{context}}

Return only the summary.
```

### `logical_agent.txt`

Stage: `debate_logical_agent`. Origin: `adapted_from_manuscript_appendix`.

```text
You are a detail-oriented analyst specializing in logical reasoning and structured problem decomposition.

For the current question:
1. Reconstruct the relevant physical state transitions in chronological order.
2. Separate each agent's private belief from the observable world state.
3. Identify the target agent, the requested mental-state level, and the relevant social or physical goal.
4. Test every answer option against the reconstructed state and agent beliefs.
5. Identify contradictions, unsupported assumptions, and misleading utterances.
6. Use retrieved memory cases only as supporting precedents; never copy their labels to the current question.
7. Prefer the option supported by the current multimodal evidence when memory and current evidence disagree.

Provide a concise evidence-based analysis. End with exactly one line:
Final Answer: [A-E]
```

### `innovative_agent.txt`

Stage: `debate_innovative_agent`. Origin: `adapted_from_manuscript_appendix`.

```text
You are an innovative analyst.

For the current question:
1. Identify the leading interpretation and construct at least one plausible alternative.
2. Test for deception, helping, hindering, mistaken belief, and nested goal-belief explanations.
3. Look for an observation that distinguishes the alternatives.
4. Challenge assumptions imported from similar memory cases.
5. Reject creative interpretations that conflict with the supplied evidence or action chronology.
6. Compare all answer options before selecting one.

Provide a concise alternative analysis. End with exactly one line:
Final Answer: [A-E]
```

### `synthesizer_agent.txt`

Stage: `debate_synthesizer`. Origin: `adapted_from_manuscript_appendix`.

```text
You are an integration specialist.

For the current question:
1. Extract the concrete evidence used by each agent.
2. Resolve disagreements using the observed action chronology, utterances, initial state, and the target agent's information access.
3. Give priority to current evidence over retrieved examples.
4. Do not decide by agent identity, writing style, confidence wording, or response length.
5. Check the selected option against every other option.
6. Return one option even when evidence is incomplete; use the option with the fewest unsupported assumptions.

Provide a concise synthesis. End with exactly one line:
Final Answer: [A-E]
```

### `debate_round_user_message.txt`

Stage: `debate_dynamic_context`. Origin: `generated_from_manuscript_method`.

```text
Multimodal background:
{{background_info}}

Question type:
{{question_type}}

Question:
{{question}}

Options:
{{options}}

Baseline option distribution:
{{option_distribution}}

Baseline answer:
{{baseline_answer}}

Retrieved high-validity cases:
{{retrieved_cases}}

Debate history through the previous round:
{{debate_history}}

Current round:
{{round_index}} of {{maximum_rounds}}
```

### `synthesizer_user_message.txt`

Stage: `synthesizer_dynamic_context`. Origin: `generated_from_manuscript_method`.

```text
Multimodal background:
{{background_info}}

Question:
{{question}}

Options:
{{options}}

Logical-agent analysis:
{{logical_analysis}}

Innovative-agent analysis:
{{innovative_analysis}}

Previous synthesized answers:
{{previous_synthesized_answers}}

Return the integrated analysis and exactly one final line:
Final Answer: [A-E]
```

### `reasoning_summary.txt`

Stage: `memory_reasoning_summary`. Origin: `generated_from_manuscript_method`.

```text
Create a compact memory-bank summary of the completed prediction. Do not include private chain-of-thought or unsupported speculation.

Question type:
{{question_type}}

Question:
{{question}}

Observed evidence:
{{background_info}}

Baseline answer and score distribution:
{{baseline_answer}}
{{option_distribution}}

Final answer:
{{final_answer}}

Correctness:
{{correctness}}

Return valid JSON with these fields:
{"key_evidence": ["..."], "belief_state": "...", "social_or_physical_goal": "...", "correction_summary": "...", "final_answer": "A"}
```

### `retrieval_pattern_summary.txt`

Stage: `memory_pattern_summary`. Origin: `generated_from_manuscript_method`.

```text
Summarize the retrieved-memory statistics for debate guidance without changing any numeric value.

Retrieved count: {{N_ret}}
Debate rate: {{R_debate}}
Debate success rate: {{R_succ}}
Correction rate: {{R_correct}}
Harm rate: {{R_harm}}
Quick convergence rate: {{R_quick}}
Mean similarity: {{mean_similarity}}

Return exactly two sentences. The first sentence states whether prior debate was generally beneficial, harmful, or inconclusive. The second states whether the retrieved evidence is sufficient and similar enough to guide the current case.
```

### `invalid_format_repair.txt`

Stage: `format_repair`. Origin: `generated_for_code_release`.

```text
Reformat the supplied model output without changing its substantive choice.

Original output:
{{original_output}}

Required output schema:
{{required_schema}}

Rules:
1. Preserve a clearly stated answer or score when one exists.
2. Do not invent an answer when the original output contains no recoverable choice.
3. Return only the required schema with no explanation.
4. If no value can be recovered, return the schema's INVALID value.
```

## Integrity and validation

`validate_release.py` validates source-index membership, unique IDs, exact counts, question-type balance, episode disjointness, active memory initialization, subset membership, protocol IDs, JSON syntax, prompt/config/metric references, fixed seeds, split hashes, resolved configuration count, package-relative paths, and the checksum manifest. Its default mode is read-only.

Use `python validate_release.py --write-checksums` only after an intentional package update. Then run `python validate_release.py` to perform a read-only verification. `release_checksums.json` records SHA-256 for every release file except the checksum manifest itself.
