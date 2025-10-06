# Measurement and learning framework
# Module: phases/phase_6_learning.md
# Part of PD-SMIS v5.1 Modular Framework

---

## PHASE 6: LEARNING PROTOCOL

### 6A: MEASUREMENT FRAMEWORK 

```javascript
POST_IMPLEMENTATION_LEARNING = {
  "success_metrics": {
    define: specific_improvements_expected(),
    timeline: when_to_measure_impact(),
    threshold: what_constitutes_success()
  },
  
  "iteration_strategy": {
    if (metrics_improve_partially) {
      analyze: what_worked_what_didn_t();
      adjust: fine_tune_not_overhaul();
    },
    
    if (metrics_don_t_improve) {
      revisit: hypothesis_may_be_wrong();
      gather: more_evidence_needed();
    },
    
    if (metrics_get_worse) {
      rollback: preserve_original();
      investigate: unexpected_negative_effect();
      display: original_for_reference();
    }
  },
  
  "knowledge_capture": {
    document: what_we_learned_about_this_role_type();
    generalize: carefully_with_caveats();
    apply: to_future_similar_contexts_only();
  },
  
  // Ad-specific learning (if applicable)
  "ad_campaign_learning": {
    if (ad_campaign_active) {
      ctr_patterns: {
        document: which_hooks_performed_best(),
        analyze: audience_segment_responsiveness(),
        optimize: creative_element_impact()
      },
      
      audience_insights: {
        capture: high_converting_segments(),
        identify: unexpected_quality_sources(),
        refine: targeting_parameter_effectiveness()
      },
      
      cost_optimization: {
        track: quality_score_improvements(),
        measure: bid_strategy_effectiveness(),
        adjust: budget_allocation_patterns()
      }
    }
  },
  
  // NEW: Iteration learning
  "iteration_learning": {
    cumulative_insights: {
      aggregate: learnings_across_all_iterations(),
      identify: consistent_patterns(),
      document: role_specific_findings()
    },
    
    strategy_effectiveness: {
      rank: strategies_by_impact(),
      classify: quick_wins_vs_major_changes(),
      prioritize: future_testing_order()
    }
  }
}
```