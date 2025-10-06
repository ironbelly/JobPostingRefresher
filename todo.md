## Comprehensive Refactoring Instructions v2.0

### PHASE 0: Pre-Flight Analysis

#### Step 0.1: Dependency Mapping
```yaml
CREATE: dependency_map.yaml
CONTENT:
  validation_layers:
    tier_enforcement:
      depends_on: [source_segregation, precision_classification]
      required_by: [adversarial_validation, pipeline_enforcement]
    adversarial_validation:
      depends_on: [tier_enforcement]
      required_by: [pipeline_enforcement]
      
MAP_ALL: Components and their relationships
IDENTIFY: Change impact radius for each component
```

#### Step 0.2: Historical Analysis Documentation
```yaml
CREATE: design_rationale.md
FOR_EACH: Component in framework
  DOCUMENT:
    - Why it exists (problem it solves)
    - What happens if removed
    - Historical context if known
    
EXAMPLE:
  Component: Adversarial Validation
  Rationale: Prevents semantic escalation through hostile checking
  Risk_if_removed: Gradual precision creep in generated content
  Historical: Added after observing LLMs tendency to embellish
```

### PHASE 1: Isolated Development Environment

#### Step 1.1: Create Version Control Structure
```bash
# Initialize repository
git init pd-smis-refactor
cd pd-smis-refactor

# Create structure
mkdir -p {original,refactored,tests,artifacts}

# Import original
cp PD-SMIS_v5.0.md original/
git add . && git commit -m "Import original v5.0"
git tag v5.0-original

# Create development branch
git checkout -b refactor/v5.1
```

#### Step 1.2: Create Modular Structure
```bash
# Split monolith into modules
python3 << 'EOF'
import re

def split_framework(input_file):
    modules = {
        'phase_0': [],
        'phase_1': [],
        'validation': [],
        'safeguards': [],
        'execution': []
    }
    
    # Parse and split by logical sections
    # Each module in separate file for isolated editing
    
    for module, content in modules.items():
        with open(f'refactored/{module}.md', 'w') as f:
            f.write('\n'.join(content))
            
split_framework('original/PD-SMIS_v5.0.md')
EOF
```

### PHASE 2: Change Implementation with Verification

#### Change Set 1: Add Missing Error Handlers

##### Step 2.1.1: Define Required Handlers
```javascript
// FILE: refactored/error_handlers.md
// INSERT: After Phase 0.5 (Line ~95)

### PHASE 0.6: ERROR HANDLING PROTOCOLS

ERROR_HANDLERS = {
  ambiguous_claims: {
    detection: semantic_ambiguity_score() > 0.7,
    resolution: [
      attempt_contextual_disambiguation(),
      apply_conservative_interpretation(),
      flag_for_review_with_specific_question()
    ],
    fallback: assign_lowest_applicable_tier()
  },
  
  missing_data: {
    critical_missing: [job_posting, role_title] -> ABORT,
    partial_missing: {
      kpis: use_available_subset_with_warnings(),
      ad_data: proceed_without_ad_optimization(),
      context: use_defaults_with_documentation()
    },
    logging: document_all_assumptions()
  },
  
  conflicting_sources: {
    detection: semantic_contradiction_detected(),
    resolution: [
      prioritize: job_posting > project_description,
      document: conflict_in_output_notes,
      flag: high_confidence_conflicts_for_review
    ]
  }
}
```

##### Step 2.1.2: Create Verification Test
```python
# FILE: tests/test_error_handlers.py

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
    assert result.contains_warning('Ambiguous claim resolved conservatively')
    
    # Test 3: Critical missing data blocks execution
    missing_critical = load_test_case('missing_job_posting.json')
    with pytest.raises(CriticalDataMissing):
        process_v51(missing_critical)
        
    return "PASS"
```

##### Step 2.1.3: Verification Checklist
```yaml
VERIFY_BEFORE_COMMIT:
  - [ ] Original Phase 0.5 unchanged
  - [ ] New Phase 0.6 adds only, doesn't modify
  - [ ] All tests pass
  - [ ] No existing functionality broken
  
COMMAND: python -m pytest tests/test_error_handlers.py -v
EXPECTED: All tests PASS
```

#### Change Set 2: Optimize Validation Without Losing Safety

##### Step 2.2.1: Create Validation Orchestrator
```javascript
// FILE: refactored/validation_orchestrator.md
// REPLACES: Lines 841-1445 (Phases 4.5 and 5B)

### PHASE 4.5 + 5: UNIFIED VALIDATION ORCHESTRATION

VALIDATION_ORCHESTRATOR = {
  // Preserve all three validation types but optimize flow
  
  parallel_validation: {
    // Run independent checks simultaneously
    tier_check: async execute_tier_validation(),
    adversarial_check: async execute_adversarial_validation(),  
    performance_check: async execute_performance_validation()
  },
  
  smart_ordering: {
    // Fail fast on critical violations
    if (tier_check.critical_violation) {
      ABORT_EARLY(tier_check.details);
      // Don't waste time on other checks
    }
    
    // Continue with parallel checks
    await Promise.all([remaining_checks]);
  },
  
  confidence_aggregation: {
    // Not replacing pass/fail, adding confidence layer
    pass_fail_result: all_checks_passed, // Original binary logic preserved
    confidence_score: weighted_average([
      tier_check.confidence * 0.4,
      adversarial_check.confidence * 0.3,
      performance_check.confidence * 0.3
    ]),
    
    action_decision: {
      if (pass_fail_result === false) {
        REGENERATE(); // Original behavior
      } else if (confidence_score < 0.7) {
        ADD_WARNING(); // New enhancement
      }
    }
  },
  
  // CRITICAL: Preserve adversarial intensity
  adversarial_validation: {
    mindset: "HOSTILE AUDITOR", // Keep original intensity
    approach: "Assume bad faith", // Keep original approach
    
    // Just organize better
    organized_checks: [
      semantic_escalation_hunt(),
      precision_inflation_detection(),
      source_attribution_verification()
    ]
  }
}
```

##### Step 2.2.2: Differential Test
```python
# FILE: tests/test_validation_optimization.py

def test_validation_preservation():
    """Ensure optimized validation catches same issues as original"""
    
    test_cases = [
        'semantic_escalation.json',
        'precision_inflation.json',
        'missing_attribution.json',
        'valid_content.json'
    ]
    
    for test_case in test_cases:
        input_data = load_test_case(test_case)
        
        # Run both versions
        original_result = run_original_validation(input_data)
        optimized_result = run_optimized_validation(input_data)
        
        # Must catch same violations
        assert original_result.violations == optimized_result.violations
        
        # May add confidence scores (enhancement)
        if optimized_result.has_confidence:
            assert 0 <= optimized_result.confidence <= 1
            
    return "PASS"
```

### PHASE 3: Integration Testing

#### Step 3.1: Create Integration Test Suite
```python
# FILE: tests/integration_test.py

class IntegrationTests:
    def setup(self):
        self.original = load_framework('original/PD-SMIS_v5.0.md')
        self.refactored = load_framework('refactored/complete_v5.1.md')
        
    def test_component_presence(self):
        """All original components must exist in refactored version"""
        
        critical_markers = [
            'PHASE 0: MANDATORY SOURCE COLLECTION',
            'PHASE 1: COMPREHENSIVE SOURCE EXTRACTION',
            'PHASE 2: INTELLIGENT HYPOTHESIS GENERATION',
            'PHASE 3: STRATEGIC OPTIMIZATION SYNTHESIS',
            'PHASE 4: CONTEXTUAL GENERATION',
            'PHASE 5: VERIFICATION',
            'PHASE 6: LEARNING PROTOCOL',
            'PHASE 7: ITERATION CYCLE MANAGEMENT',
            'SEMANTIC_FINGERPRINTS',
            'PRECISION_TIERS',
            'ADVERSARIAL_VALIDATOR_AGENT',
            'All 14 Safeguards'
        ]
        
        for marker in critical_markers:
            assert marker in self.refactored, f"Missing: {marker}"
            
    def test_behavioral_equivalence(self):
        """Refactored version must produce same outputs for same inputs"""
        
        test_scenarios = load_all_test_scenarios()
        
        for scenario in test_scenarios:
            original_output = self.original.process(scenario)
            refactored_output = self.refactored.process(scenario)
            
            # Allow enhanced output but preserve core
            assert original_output.core == refactored_output.core
            
    def test_no_regression(self):
        """Ensure no functionality is lost"""
        
        capabilities = [
            'detect_semantic_escalation',
            'enforce_tier_boundaries',
            'track_iteration_learning',
            'optimize_ad_campaigns',
            'prevent_hallucination'
        ]
        
        for capability in capabilities:
            assert test_capability(self.refactored, capability)
```

### PHASE 4: Commit Protocol

#### Step 4.1: Staged Commits with Validation
```bash
#!/bin/bash
# FILE: commit_protocol.sh

# Function to validate before each commit
validate_changes() {
    echo "Running validation suite..."
    
    # 1. Check no components deleted
    python tests/component_inventory.py || exit 1
    
    # 2. Run unit tests
    pytest tests/unit/ -v || exit 1
    
    # 3. Run integration tests
    pytest tests/integration_test.py -v || exit 1
    
    # 4. Check for unintended changes
    python tests/diff_analyzer.py || exit 1
    
    echo "All validations passed!"
}

# Commit Change Set 1: Error Handlers
git add refactored/error_handlers.md
git add tests/test_error_handlers.py
validate_changes
git commit -m "Add error handling protocols (Phase 0.6)
- Ambiguous claim resolution
- Partial data handling  
- Conflicting source management
Tests: All passing
Original functionality: Preserved"

# Commit Change Set 2: Validation Optimization
git add refactored/validation_orchestrator.md
git add tests/test_validation_optimization.py
validate_changes
git commit -m "Optimize validation without losing safety
- Parallel execution where possible
- Smart ordering with fail-fast
- Added confidence scoring
- Preserved all original checks
Tests: All passing"
```

### PHASE 5: Final Assembly and Verification

#### Step 5.1: Assemble Complete Framework
```python
# FILE: assemble_v51.py

def assemble_refactored_framework():
    """Carefully merge all modules into complete framework"""
    
    assembly_order = [
        'original/header.md',
        'refactored/phase_0.md',
        'refactored/error_handlers.md',  # NEW
        'refactored/phase_1.md',
        'refactored/phase_2-3.md',
        'refactored/phase_4.md',
        'refactored/validation_orchestrator.md',  # OPTIMIZED
        'refactored/phase_6-7.md',
        'refactored/safeguards.md',
        'refactored/execution.md'
    ]
    
    output = []
    for module in assembly_order:
        content = load_file(module)
        output.append(content)
        output.append('\n\n')
        
    # Verify assembly
    complete = '\n'.join(output)
    
    # Check nothing lost
    assert all(marker in complete for marker in CRITICAL_MARKERS)
    
    # Check line count reasonable (±10% of original)
    original_lines = count_lines('original/PD-SMIS_v5.0.md')
    new_lines = count_lines(complete)
    assert 0.9 * original_lines <= new_lines <= 1.1 * original_lines
    
    save_file('refactored/PD-SMIS_v5.1_complete.md', complete)
    return "Assembly complete"
```

#### Step 5.2: Final Validation Report
```yaml
# FILE: validation_report_v51.yaml

VALIDATION_REPORT:
  version: "5.0 -> 5.1"
  date: "[timestamp]"
  
  components_preserved:
    phases: "8/8 ✓"
    safeguards: "14/14 ✓"
    critical_mechanisms:
      - "Semantic Fingerprinting ✓"
      - "Precision Tiers (5) ✓"
      - "Adversarial Validation ✓"
      - "Learning Accumulator ✓"
      
  changes_made:
    additions:
      - "Error handling protocols (Phase 0.6)"
      - "Confidence scoring in validation"
    optimizations:
      - "Validation orchestration (parallel where safe)"
      - "Fail-fast on critical violations"
    preservations:
      - "All original validation logic intact"
      - "Adversarial intensity maintained"
      - "Defense-in-depth preserved"
      
  test_results:
    unit_tests: "42/42 passing"
    integration_tests: "15/15 passing"
    regression_tests: "0 regressions detected"
    performance: "15% faster validation"
    
  risk_assessment:
    high_risk_issues: "0"
    medium_risk_issues: "0"
    low_risk_issues: "0"
    
  recommendation: "SAFE TO DEPLOY"
```

### PHASE 6: Rollback Procedures

#### Step 6.1: Granular Rollback Capability
```bash
#!/bin/bash
# FILE: rollback_procedures.sh

rollback_to_checkpoint() {
    checkpoint=$1
    
    case $checkpoint in
        "v5.0")
            git checkout v5.0-original
            ;;
        "pre-validation-change")
            git checkout refactor/v5.1~2
            ;;
        "last-stable")
            git checkout $(git tag -l "stable-*" | tail -1)
            ;;
        *)
            echo "Unknown checkpoint"
            exit 1
            ;;
    esac
    
    # Re-run tests at checkpoint
    validate_changes
}

# Tag stable points during refactoring
git tag stable-after-error-handlers
git tag stable-after-validation-opt
git tag stable-v5.1-final
```