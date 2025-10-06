# Content generation with constraints
# Module: phases/phase_4_generation.md
# Part of PD-SMIS v5.1 Modular Framework

---

## PHASE 4: CONTEXTUAL GENERATION WITH PERFORMANCE FOCUS

### 4A: PERFORMANCE-DRIVEN STRUCTURE

```javascript
OPTIMIZED_STRUCTURE = {
  "TITLE": {
    content: role_title_with_key_differentiator(),
    engagement: strategic_emoji_if_appropriate(),
    optimization: keyword_for_searchability()
  },
  
  "HOOK": {
    // Dynamically determined based on bottleneck analysis
    if (low_application_rate) {
      lead_with: most_compelling_differentiator();
    } else if (low_screening_rate) {
      lead_with: clearest_role_definition();
    } else {
      lead_with: strongest_value_proposition();
    }
  },
  
  "OPPORTUNITY": {
    // Frame based on what evidence shows matters
    structure: evidence_based_not_template_based()
  },
  
  "RESPONSIBILITIES": {
    // Original safeguards maintained
    content: only_from_role_scope(),
    context: project_environment_as_context_only(),
    phrasing: action_oriented_you_will_statements()
  },
  
  "REQUIREMENTS": {
    // Calibrated based on bottleneck analysis
    if (screening_rate_issue) {
      clearly_separate: must_haves_vs_nice_to_haves();
      realistic_calibration: market_appropriate_expectations();
    }
  },
  
  "PROJECT_CONTEXT": {
    // Original safeguards maintained
    content: only_project_environment_facts(),
    framing: never_as_responsibilities()
  },
  
  "VALUE_PROPOSITION": {
    // Enhanced based on competitive analysis
    differentiation: what_makes_us_unique(),
    benefits: comprehensive_but_relevant()
  },
  
  "CALL_TO_ACTION": {
    // Optimized based on conversion goals
    friction_reduction: minimize_barrier_to_apply(),
    self_selection: help_right_people_identify()
  },
  
  // Ad-specific structure (when applicable)
  "AD_INTRO_STRUCTURE": {
    if (ad_campaign_active) {
      opening_hook: {
        characters_1_150: mobile_optimized_complete_thought(),
        attention_grabber: role_or_company_highlight()
      },
      
      body_content: {
        characters_151_450: expand_on_opportunity(),
        value_props: 2_3_key_differentiators(),
        credibility: brief_achievement_or_scale()
      },
      
      closing: {
        characters_450_600: clear_next_step(),
        cta_button: aligned_with_objective()
      }
    }
  }
}
```

### 4A.2: TIER-CONSTRAINED LANGUAGE SELECTION

```javascript
function GENERATE_WITH_CONSTRAINTS(fact) {
  tier = fact.tier_locked;
  
  // Generate appropriate language based on tier level
  // Higher tiers = more definitive claims
  // Lower tiers = more associative claims
  
  if (generated_claim_strength > source_claim_strength) {
    BLOCK("Cannot escalate precision beyond source");
  }
  
  return SELECT_APPROPRIATE_LANGUAGE_FOR_TIER();
}
```

### 4A.3: CROSS-DOMAIN RESPONSIBILITY FILTER

```javascript
function FILTER_RESPONSIBILITIES_BY_DOMAIN() {
  for (potential_responsibility from PROJECT_ENVIRONMENT) {
    if (!DOMAIN_EXTRACTION.COMPATIBILITY_MATRIX.compare(
        ROLE_DOMAIN, 
        PROJECT_DOMAINS[potential_responsibility])) {
      
      BLOCK_AS_DIRECT_RESPONSIBILITY();
      ALLOW_AS_CONTEXTUAL_REFERENCE_ONLY();
    }
  }
}
```

### 4A.5: MANDATORY SEMANTIC DIFF VALIDATION

```javascript
function SEMANTIC_DIFF_GATE(source_facts, generated_content) {
  // ENHANCED WITH TIER ENFORCEMENT
  
  EXTRACT_ALL_FACTUAL_CLAIMS(generated_content).forEach(claim => {
    source_mapping = TRACE_TO_SOURCE(claim);
    
    if (!source_mapping) {
      BLOCK_OUTPUT("Unattributable claim detected");
    }
    
    // TIER VIOLATION CHECK
    claim_tier = DETECT_PRECISION_TIER(claim.language_used);
    source_tier = source_mapping.assigned_tier;
    
    if (claim_tier < source_tier) { // Lower number = higher precision
      BLOCK_OUTPUT(`TIER VIOLATION:
        Source: "${source_mapping.original_text}" [TIER ${source_tier}]
        Generated: "${claim.text}" [TIER ${claim_tier}]
        
        ILLEGAL ESCALATION DETECTED`);
    }
  });
  
  return ALLOW_OUTPUT;
}

// Make this gate non-bypassable
PIPELINE_ENFORCEMENT = {
  generated_content = GENERATE();
  validated_content = SEMANTIC_DIFF_GATE(sources, generated_content);
  // Output blocked until validation passes
  return validated_content || REGENERATE_WITH_CONSTRAINTS();
}
```