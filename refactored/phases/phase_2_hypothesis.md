# KPI-based bottleneck analysis and hypothesis generation
# Module: phases/phase_2_hypothesis.md
# Part of PD-SMIS v5.1 Modular Framework

---

## PHASE 2: INTELLIGENT HYPOTHESIS GENERATION

### 2A: BOTTLENECK ANALYSIS ENGINE 

```javascript
function DIAGNOSE_PERFORMANCE_GAPS() {
  // Don't use templates - analyze THIS specific situation
  
  for (each KPI with significant gap) {
    // Generate multiple competing hypotheses
    hypotheses = [];
    
    // Hypothesis Type 1: Content Misalignment
    if (gap in application_rate) {
      analyze: {
        - Does title match actual role?
        - Are we competing for wrong talent pool?
        - Is compensation competitive but hidden?
        - Are requirements realistic for market?
      }
    }
    
    // Hypothesis Type 2: Expectation Mismatch
    if (gap in screening_rate) {
      analyze: {
        - Do requirements match what's actually needed?
        - Are nice-to-haves presented as must-haves?
        - Is seniority level clearly communicated?
        - Are we attracting adjacent but wrong skillsets?
      }
    }
    
    // Hypothesis Type 3: Communication Failures
    examine: {
      - Clarity of role scope
      - Specificity of technical requirements
      - Cultural fit indicators
      - Growth opportunity visibility
    }
    
    // Hypothesis Type 4: Market Dynamics
    consider: {
      - Competitive landscape for this role
      - Supply/demand for these skills
      - Geographic constraints
      - Industry perception issues
    }
    
    // Hypothesis Type 5: Ad Campaign Issues (if applicable)
    if (ad_campaign_active) {
      if (ctr_declining || ctr_low) {
        analyze: {
          - Is ad copy addressing right pain points?
          - Does intro text match job posting tone?
          - Is audience too broad or narrow?
          - Are we using optimal ad format?
          - Is mobile experience optimized?
          - Are visual elements effective?
        }
      }
      
      if (audience_size_suboptimal) {
        analyze: {
          - Which targeting parameters limit reach?
          - Can we expand through related job titles?
          - Should we adjust geographic boundaries?
          - Are exclusions too restrictive?
          - Can we leverage interest groups?
          - Should we test broader parameters?
        }
      }
    }
    
    // NEW: Iteration-Aware Analysis
    if (iteration_number > 1) {
      ITERATION_AWARE_ANALYSIS = {
        performance_trend: {
          if (kpis_declining_from_baseline) {
            recognition: "Our changes made things worse",
            action: FUNDAMENTAL_STRATEGY_PIVOT(),
            reference: DISPLAY_ORIGINAL_FOR_CONTEXT()
          },
          if (kpis_improving_but_slowly) {
            recognition: "Right direction, needs acceleration",
            action: AMPLIFY_WORKING_ELEMENTS()
          },
          if (kpis_plateaued) {
            recognition: "Reached local maximum with current approach",
            action: EXPLORE_ORTHOGONAL_STRATEGIES()
          }
        },
        
        hypothesis_evolution: {
          avoid_repeated_mistakes: {
            check: LEARNING_ACCUMULATOR.refuted_hypotheses,
            ensure: "Never retry proven failures"
          },
          
          build_on_successes: {
            check: LEARNING_ACCUMULATOR.confirmed_insights,
            action: "Double down on proven winners"
          },
          
          explore_new_territories: {
            if (strategy_exhaustion > 70%) {
              consider: [
                "Radical format changes",
                "Completely different value props",
                "Alternative audience segments",
                "Inverse of current approach"
              ]
            }
          }
        }
      }
    }
    
    // Generate custom hypotheses based on patterns
    return context_specific_theories_not_generic_assumptions();
  }
}
```

### 2B: EVIDENCE GATHERING PROTOCOL

```javascript
function VALIDATE_HYPOTHESES() {
  for (each hypothesis) {
    evidence_needed = determine_what_would_prove_or_disprove();
    
    // Look for evidence in original posting
    posting_analysis = {
      word_count_by_section: measure_emphasis(),
      requirement_complexity: count_mandatory_skills(),
      jargon_density: assess_accessibility(),
      value_proposition_strength: evaluate_compelling_factors()
    };
    
    // Look for evidence in ad campaign (if active)
    if (ad_campaign_active) {
      ad_analysis = {
        copy_posting_alignment: semantic_similarity_score(),
        audience_posting_fit: overlap_percentage(),
        creative_performance: engagement_by_element(),
        timing_analysis: performance_by_day_hour()
      };
    }
    
    // Look for evidence in iteration history (if available)
    if (iteration_number > 1) {
      historical_evidence = {
        what_worked_before: successful_changes_log(),
        what_failed_before: unsuccessful_attempts_log(),
        patterns_observed: recurring_themes(),
        seasonal_factors: temporal_correlations()
      };
    }
    
    // Compare to successful postings
    comparative_analysis = {
      what_high_performers_do_differently: identify_patterns(),
      language_differences: semantic_comparison(),
      structure_variations: format_analysis(),
      emphasis_shifts: priority_differences()
    };
    
    // Market intelligence
    competitive_intelligence = {
      what_others_offer: scan_similar_roles(),
      how_others_communicate: analyze_messaging(),
      where_we_stand: position_assessment(),
      market_saturation: assess_competition_density()
    };
    
    "ENHANCEMENT_HYPOTHESIS_GENERATION": {
      // Visual enhancements emerge from evidence, not prescription
      
      if (evidence_shows("low_engagement_metrics")) {
        generate_hypothesis: {
          "Visual anchoring might improve scan patterns",
          test_method: "Analyze top performers in this category",
          success_metric: "Specific KPI improvement"
        };
      }
      
      if (evidence_shows("cognitive_overload_in_original")) {
        generate_hypothesis: {
          "Visual breaks might improve comprehension",
          test_method: "Section markers and emphasis tools",
          success_metric: "Application→Screening improvement"
        };
      }
      
      // Key: Hypotheses emerge from THIS posting's problems, not generic rules
    }

    return evidence_based_conclusions_not_assumptions();
  }
}
```