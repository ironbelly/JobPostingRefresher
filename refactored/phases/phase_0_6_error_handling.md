# Error Handling Protocols for PD-SMIS Framework
# Module: phases/phase_0_6_error_handling.md
# Part of PD-SMIS v5.1 Modular Framework

---

## PHASE 0.6: ERROR HANDLING PROTOCOLS

```javascript
ERROR_HANDLERS = {
  ambiguous_claims: {
    detection: () => semantic_ambiguity_score() > 0.7,
    resolution: [
      attempt_contextual_disambiguation(),
      apply_conservative_interpretation(),
      flag_for_review_with_specific_question()
    ],
    fallback: assign_lowest_applicable_tier(),
    logging: "Ambiguous claim resolved conservatively to prevent escalation"
  },

  missing_data: {
    critical_missing: {
      fields: ['job_posting', 'role_title'],
      action: 'ABORT_WITH_ERROR',
      message: "Cannot proceed without job posting and role title"
    },
    partial_missing: {
      kpis: {
        action: use_available_subset_with_warnings(),
        warning: "Proceeding with partial KPI data - projections may be limited"
      },
      ad_data: {
        action: proceed_without_ad_optimization(),
        note: "Ad campaign optimization skipped - no ad data provided"
      },
      context: {
        action: use_defaults_with_documentation(),
        defaults: {
          iteration_number: 1,
          previous_versions: [],
          learning_history: []
        }
      }
    },
    logging: document_all_assumptions()
  },

  conflicting_sources: {
    detection: () => semantic_contradiction_detected(),
    resolution: {
      priority_order: [
        'job_posting',      // Highest priority - actual role description
        'project_description', // Second - project context
        'company_info',     // Third - company attributes
        'user_feedback'     // Fourth - subjective input
      ],
      action: [
        prioritize_by_source_hierarchy(),
        document_conflict_in_output_notes(),
        flag_high_confidence_conflicts_for_review()
      ]
    },
    documentation: "Source conflict resolved using priority hierarchy"
  },

  tier_violation_attempt: {
    detection: () => precision_level_exceeds_evidence(),
    immediate_action: 'BLOCK_AND_ROLLBACK',
    resolution: [
      revert_to_evidence_supported_tier(),
      log_violation_attempt_with_context(),
      flag_for_adversarial_review()
    ],
    severity: 'CRITICAL'
  },

  hallucination_risk: {
    detection: () => claim_lacks_source_attribution(),
    immediate_action: 'BLOCK_GENERATION',
    resolution: [
      remove_unattributed_claim(),
      search_for_supporting_evidence(),
      if_no_evidence_found_then_exclude()
    ],
    severity: 'CRITICAL'
  },

  performance_degradation: {
    detection: () => processing_time_exceeds_threshold(),
    thresholds: {
      warning: 30000,  // 30 seconds
      critical: 60000  // 60 seconds
    },
    resolution: [
      switch_to_optimized_mode(),
      reduce_validation_rounds_to_minimum(),
      cache_intermediate_results()
    ],
    maintain: "All critical validations must still run"
  },

  iteration_data_corruption: {
    detection: () => iteration_context_validation_fails(),
    resolution: [
      attempt_recovery_from_backup(),
      if_recovery_fails_then_reset_to_baseline(),
      log_corruption_event_with_diagnostics()
    ],
    fallback: start_fresh_iteration_with_warning()
  }
}

// Error severity classification
ERROR_SEVERITY = {
  CRITICAL: {
    // Must abort immediately
    examples: ['tier_violation', 'hallucination', 'missing_critical_data'],
    action: 'ABORT_PIPELINE',
    notification: 'IMMEDIATE'
  },
  HIGH: {
    // Can proceed with warnings
    examples: ['ambiguous_claims', 'conflicting_sources'],
    action: 'PROCEED_WITH_WARNINGS',
    notification: 'IN_OUTPUT'
  },
  MEDIUM: {
    // Handle gracefully
    examples: ['missing_optional_data', 'performance_degradation'],
    action: 'APPLY_FALLBACK',
    notification: 'LOG_ONLY'
  },
  LOW: {
    // Monitor only
    examples: ['cache_miss', 'redundant_validation'],
    action: 'CONTINUE',
    notification: 'METRICS_ONLY'
  }
}

// Integration with existing pipeline
function integrateErrorHandling(pipeline) {
  return {
    ...pipeline,

    beforePhase: (phase) => {
      checkPreConditions(phase);
      validateInputCompleteness(phase);
    },

    duringPhase: (phase, data) => {
      try {
        const result = phase.execute(data);
        validatePhaseOutput(result);
        return result;
      } catch (error) {
        return handlePhaseError(error, phase, data);
      }
    },

    afterPhase: (phase, result) => {
      logPhaseCompletion(phase, result);
      updateErrorMetrics(phase);
    },

    onCriticalError: (error) => {
      preserveWorkInProgress();
      generateErrorReport(error);
      suggestRemediation(error);
      throw error; // Propagate to stop pipeline
    }
  };
}

// Validation helper functions
function semantic_ambiguity_score(claim) {
  // Returns 0-1 score based on:
  // - Presence of qualifying words ("possibly", "might", "could")
  // - Multiple interpretations possible
  // - Conflicting context clues
  return calculateAmbiguityScore(claim);
}

function semantic_contradiction_detected(sources) {
  // Checks if sources contain contradictory information
  // Example: Job posting says "5 years" but project says "3 years"
  return detectContradictions(sources);
}

function precision_level_exceeds_evidence(claim, evidence) {
  // Verifies claim tier matches evidence tier
  // Cannot claim Tier 1 (shipped) with Tier 3 evidence (worked on)
  return claimTier(claim) > evidenceTier(evidence);
}

function claim_lacks_source_attribution(claim) {
  // Every claim must trace to specific source
  return !hasValidSourceAttribution(claim);
}
```

## ERROR RECOVERY STRATEGIES

```javascript
RECOVERY_STRATEGIES = {
  validation_failure: {
    max_retries: 3,
    backoff_strategy: 'exponential',
    between_retries: [
      regenerate_with_stricter_constraints(),
      reduce_optimization_aggressiveness(),
      fallback_to_minimal_changes()
    ]
  },

  data_inconsistency: {
    resolution_order: [
      attempt_automated_resolution(),
      request_user_clarification(),
      use_conservative_defaults()
    ]
  },

  performance_timeout: {
    graceful_degradation: [
      disable_non_critical_optimizations(),
      reduce_validation_depth(),
      cache_expensive_operations()
    ],
    maintain_critical: [
      'tier_enforcement',
      'source_attribution',
      'adversarial_validation'
    ]
  }
}
```

## TESTING REQUIREMENTS

```python
def test_error_handler_integration():
    """Verify error handlers integrate without breaking existing flow"""

    # Test 1: Handlers don't interfere with normal flow
    normal_input = load_test_case('complete_valid_input.json')
    result_without_handlers = process_v50(normal_input)
    result_with_handlers = process_v51(normal_input)
    assert result_with_handlers.output == result_without_handlers.output

    # Test 2: Handlers activate on ambiguous input
    ambiguous_input = load_test_case('ambiguous_claims.json')
    result = process_v51(ambiguous_input)
    assert 'Ambiguous claim resolved conservatively' in result.warnings

    # Test 3: Critical missing data blocks execution
    missing_critical = load_test_case('missing_job_posting.json')
    with pytest.raises(CriticalDataMissing):
        process_v51(missing_critical)

    # Test 4: Tier violations are caught and blocked
    tier_violation = load_test_case('tier_escalation_attempt.json')
    result = process_v51(tier_violation)
    assert result.tier_violations_blocked > 0

    # Test 5: Conflicts resolved by priority
    conflicting = load_test_case('conflicting_sources.json')
    result = process_v51(conflicting)
    assert result.conflict_resolution_applied == True

    return "ALL_TESTS_PASS"
```