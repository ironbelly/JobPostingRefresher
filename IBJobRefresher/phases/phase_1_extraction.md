# Source extraction with semantic fingerprinting
# Module: phases/phase_1_extraction.md
# Part of PD-SMIS v5.1 Modular Framework

---

## PHASE 1: COMPREHENSIVE SOURCE EXTRACTION & ANALYSIS

### 1A: SOURCE-SEGREGATED Fact Inventory 

```javascript
SOURCE_SEGREGATED_FACTS = {
  // ROLE-SPECIFIC FACTS (from job posting ONLY)
  "ROLE_SCOPE": {
    "job_title": extract_from_job_posting(),
    "responsibilities": extract_from_job_posting_responsibilities(),
    "required_skills": extract_from_job_posting_requirements(),
    "preferred_skills": extract_from_job_posting_nice_to_haves(),
    "years_required": extract_from_job_posting(),
    "seniority_level": extract_from_job_posting(),
    // USAGE: Can become "You will..." statements
    // FORBIDDEN: Cannot describe project features
  },
  
  // PROJECT CONTEXT (from project description ONLY)
  "PROJECT_ENVIRONMENT": {
    "project_type": extract_from_project_description(),
    "game_features": extract_from_project_description(),
    "technical_architecture": extract_from_project_description(),
    "target_audience": extract_from_project_description(),
    // USAGE: Can describe "the environment you'll work in"
    // FORBIDDEN: Cannot become "You will build..." statements
  },
  
  // COMPANY CONTEXT (from company info)
  "COMPANY_ATTRIBUTES": {
    "company_name": extract_exact(),
    "team_size": extract_exact(),
    "previous_titles": extract_exact(),
    "team_backgrounds": extract_exact(),
    "location": extract_exact(),
    "remote_policy": extract_exact(),
    "benefits_listed": extract_exact(),
    "salary_details": extract_exact(),
    // USAGE: Can describe company/team/benefits
    // FORBIDDEN: Cannot become responsibilities
  },

SEMANTIC_FINGERPRINTS = {
  for (each extracted_fact) {
    create_immutable_record: {
      "original_text": exact_source_string(),
      "semantic_core": extract_factual_claim_without_modifiers(),
      "precision_level": identify_specificity_markers(),
      // "300+ projects" → core: "300+ projects", precision: "approximate_participation"
      // NOT allowed to become "shipped" (changes precision to "completion")
    },
  },
},

// Add to Phase 5B verification:
function SEMANTIC_PRESERVATION_CHECK(generated_content) {
  for (each fact_in_output) {
    source_fingerprint = find_matching_semantic_core();
    if (precision_level_increased(output, source_fingerprint)) {
      REJECT("Cannot increase precision beyond source");
      // "worked on" cannot become "shipped"
      // "participated" cannot become "led"  
      // "knowledge" cannot become "expertise"
    },
  },
},
}
```

### 1A.5: PRECISION TIER CLASSIFICATION

```javascript
PRECISION_TIERS = {
  TIER_1_DEFINITIVE: "Claims of complete ownership, final delivery, or achieved outcomes",
  TIER_2_CONSTRUCTIVE: "Claims of building, creating, or primary contribution",
  TIER_3_COLLABORATIVE: "Claims of participation, assistance, or shared involvement",
  TIER_4_ASSOCIATIVE: "Claims of exposure, familiarity, or peripheral connection",
  TIER_5_ENVIRONMENTAL: "Claims about context, surroundings, or indirect relationship"
}

CLASSIFY_ALL_FACTS = {
  for (each fact) {
    tier = analyze_claim_strength(fact);
    // Assess: Does source claim completion? Creation? Participation? Association? Context?
    if (!tier) tier = 4; // Default to associative if unclear
    fact.tier_locked = tier;
    fact.allowed_language = generate_appropriate_verbs_for_tier(tier);
    // Can only use language at same or lower precision than source
  }
}

if (!all_facts_classified) BLOCK("Classification incomplete");
```

### 1B: ENGAGEMENT ELEMENTS EXTRACTION 

```javascript
ENGAGEMENT_INVENTORY = {
  "VISUAL_ELEMENTS": {
    "emojis_used": extract_all_emojis_with_positions(),
    "formatting_patterns": identify_visual_hierarchy(),
    "section_structure": map_content_flow(),
    "attention_anchors": find_eye_catching_elements()
  },
  
  "LINGUISTIC_PATTERNS": {
    "hook_strategy": analyze_opening_approach(),
    "power_words": extract_high_impact_vocabulary(),
    "tone_markers": identify_voice_characteristics(),
    "call_to_action": examine_closing_strategy()
  }
}
```

### 1B.2: DOMAIN EXTRACTION ENGINE

```javascript
DOMAIN_EXTRACTION = {
  ROLE_DOMAIN: {
    technical_markers: extract_all_technologies_from_job_posting(),
    action_verbs: extract_all_technical_verbs_from_responsibilities(),
    scope_indicators: extract_all_system_types_mentioned()
  },
  
  PROJECT_DOMAINS: {
    for (each PROJECT_ENVIRONMENT.feature) {
      feature_domain = {
        technologies: extract_tech_stack(),
        system_layer: identify_architectural_layer(),
        technical_verbs: extract_action_requirements()
      }
    }
  },
  
  COMPATIBILITY_MATRIX: {
    compare: function(role_domain, feature_domain) {
      overlap_score = calculate_semantic_overlap();
      explicit_mention = job_posting_references_feature_type();
      return (overlap_score > 0.7 || explicit_mention);
    }
  }
}
```

### 1C: PERFORMANCE METRICS DEEP ANALYSIS 

```javascript
PERFORMANCE_INTELLIGENCE = {
  "KPI_DIAGNOSTICS": {
    "visit_to_application": {
      "rate": extract_percentage(),
      "trend": calculate_direction_of_change(),
      "gap_analysis": identify_optimization_opportunity(),
      "bottleneck_hypothesis": generate_initial_theories()
    },
    "application_to_screening": {
      "rate": extract_percentage(),
      "trend": calculate_direction_of_change(),
      "gap_analysis": assess_filtering_effectiveness(),
      "bottleneck_hypothesis": why_candidates_don_t_qualify()
    },
    "screening_to_interview": {
      "rate": extract_percentage(),
      "trend": calculate_direction_of_change(),
      "gap_analysis": evaluate_screening_criteria(),
      "bottleneck_hypothesis": what_causes_rejection()
    },
    "interview_to_offer": {
      "rate": extract_percentage(),
      "trend": calculate_direction_of_change(),
      "gap_analysis": assess_interview_process(),
      "bottleneck_hypothesis": why_no_offers_extended()
    }
  }
}
```

### 1D: AD CAMPAIGN INTELLIGENCE [NEW SECTION]

```javascript
AD_PERFORMANCE_ANALYSIS = {
  "AD_COPY_ANALYSIS": {
    character_count: measure_against_600_limit(),
    mobile_optimization: analyze_first_150_chars(),
    hook_effectiveness: evaluate_opening_impact(),
    cta_presence: identify_call_to_action(),
    value_prop_clarity: assess_benefit_communication(),
    emoji_usage: count_and_evaluate_visual_elements()
  },
  
  "AUDIENCE_ALIGNMENT": {
    size_analysis: {
      current_size: extract_audience_count(),
      size_adequacy: assess_reach_potential(),
      quality_score: assess_relevance_vs_reach(),
      expansion_potential: identify_growth_opportunities()
    },
    targeting_precision: {
      parameter_count: count_active_targeting_facets(),
      parameter_effectiveness: evaluate_each_criterion(),
      overlap_analysis: check_redundant_criteria(),
      exclusion_impact: measure_negative_targeting_effect()
    }
  },
  
  "PERFORMANCE_TRACKING": {
    ctr_performance: {
      current_rate: extract_ctr(),
      trend_direction: improving_or_declining(),
      optimization_potential: identify_improvement_areas()
    },
    cost_efficiency: {
      cpc_trend: track_cost_evolution(),
      cpm_analysis: evaluate_impression_costs(),
      roi_calculation: cost_vs_quality_of_applicants()
    },
    funnel_impact: {
      ad_to_application: measure_post_click_conversion(),
      quality_assessment: downstream_performance_tracking()
    }
  }
}
```