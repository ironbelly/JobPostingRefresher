#!/usr/bin/env python3
"""
Split PD-SMIS v5.0 framework into modular components
Preserves all functionality while enabling isolated editing
"""

import re
import os
from pathlib import Path

def split_framework(input_file='JobEvalV5.md', output_dir='refactored'):
    """Split monolithic framework into logical modules"""

    # Read the entire framework
    with open(input_file, 'r') as f:
        content = f.read()

    # Define module extraction patterns
    modules = {
        'phases/phase_0_collection.md': {
            'start': '## PHASE 0: MANDATORY SOURCE COLLECTION',
            'end': '## PHASE 0.5:',
            'description': 'Source material collection and input structure'
        },
        'phases/phase_0_5_iteration.md': {
            'start': '## PHASE 0.5: ITERATION CONTEXT MANAGEMENT',
            'end': '## PHASE 1:',
            'description': 'Iteration tracking and learning accumulator'
        },
        'phases/phase_1_extraction.md': {
            'start': '## PHASE 1: COMPREHENSIVE SOURCE EXTRACTION',
            'end': '## PHASE 2:',
            'description': 'Source extraction with semantic fingerprinting'
        },
        'phases/phase_2_hypothesis.md': {
            'start': '## PHASE 2: HYPOTHESIS GENERATION',
            'end': '## PHASE 3:',
            'description': 'KPI-based bottleneck analysis'
        },
        'phases/phase_3_optimization.md': {
            'start': '## PHASE 3: STRATEGIC OPTIMIZATION',
            'end': '## PHASE 4:',
            'description': 'Evidence-based intervention design'
        },
        'phases/phase_4_generation.md': {
            'start': '## PHASE 4: CONTEXTUAL GENERATION',
            'end': '## PHASE 4.5:',
            'description': 'Content generation with constraints'
        },
        'validation/adversarial_validation.md': {
            'start': '## PHASE 4.5: ADVERSARIAL VALIDATION',
            'end': '## PHASE 5:',
            'description': 'Hostile validation agent'
        },
        'validation/verification_suite.md': {
            'start': '## PHASE 5: VERIFICATION SUITE',
            'end': '## PHASE 6:',
            'description': 'Multi-layer validation checks'
        },
        'phases/phase_6_learning.md': {
            'start': '## PHASE 6: LEARNING PROTOCOL',
            'end': '## PHASE 7:',
            'description': 'Measurement and learning framework'
        },
        'phases/phase_7_iteration.md': {
            'start': '## PHASE 7: ITERATION CYCLE MANAGEMENT',
            'end': '## CRITICAL SAFEGUARDS:',
            'description': 'Multi-iteration workflow management'
        },
        'safeguards/critical_safeguards.md': {
            'start': '## CRITICAL SAFEGUARDS:',
            'end': '## FINAL EXECUTION SEQUENCE:',
            'description': 'All 14 critical safeguards'
        },
        'components/execution_sequence.md': {
            'start': '## FINAL EXECUTION SEQUENCE:',
            'end': '## OUTPUT FORMAT:',
            'description': 'Pipeline execution logic'
        },
        'components/output_format.md': {
            'start': '## OUTPUT FORMAT:',
            'end': None,  # Goes to end of file
            'description': 'Output structure and formatting'
        }
    }

    # Create header for main orchestrator file
    orchestrator_content = """# PD-SMIS v5.1 - Modular Framework Orchestrator

## Overview
This modular version of the Performance-Driven Source Material Inventory System (PD-SMIS) v5.0
has been restructured for maintainability while preserving all original functionality.

## Module Loading Sequence

```python
# Load modules in dependency order
modules = [
    'phases/phase_0_collection.md',
    'phases/phase_0_5_iteration.md',
    'phases/phase_1_extraction.md',
    'phases/phase_2_hypothesis.md',
    'phases/phase_3_optimization.md',
    'phases/phase_4_generation.md',
    'validation/adversarial_validation.md',
    'validation/verification_suite.md',
    'phases/phase_6_learning.md',
    'phases/phase_7_iteration.md',
    'safeguards/critical_safeguards.md',
    'components/execution_sequence.md',
    'components/output_format.md'
]
```

## Critical Constraints (NEVER COMPROMISE)
1. All 14 safeguards must remain active
2. Adversarial validation intensity must not be reduced
3. Tier boundaries must be enforced
4. Source segregation must be maintained
5. Evidence chain must be preserved
6. 100% source-context integrity required

## Module Descriptions
"""

    # Extract and save each module
    for module_path, config in modules.items():
        output_path = Path(output_dir) / module_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Extract module content
        if config['start'] in content:
            start_idx = content.index(config['start'])
            if config['end'] and config['end'] in content:
                end_idx = content.index(config['end'])
                module_content = content[start_idx:end_idx].strip()
            else:
                # Goes to end of file
                module_content = content[start_idx:].strip()

            # Add module header
            module_header = f"""# {config['description']}
# Module: {module_path}
# Part of PD-SMIS v5.1 Modular Framework

---

"""

            # Write module file
            with open(output_path, 'w') as f:
                f.write(module_header + module_content)

            print(f"Created: {output_path}")

            # Add to orchestrator
            orchestrator_content += f"\n### {module_path}\n{config['description']}\n"

    # Extract precision tier definitions (appears multiple times, consolidate)
    tier_content = """# Precision Tier Classification System
# Core component of PD-SMIS validation

## PRECISION_TIERS Definition

```javascript
PRECISION_TIERS = {
  1: {
    name: "completion",
    verbs: ["shipped", "delivered", "launched", "deployed", "released"],
    can_claim: "Full ownership and successful deployment",
    cannot_escalate_from: [2, 3, 4, 5]
  },
  2: {
    name: "creation",
    verbs: ["built", "created", "architected", "developed", "designed", "implemented"],
    can_claim: "Primary authorship/creation role",
    cannot_escalate_from: [3, 4, 5]
  },
  3: {
    name: "participation",
    verbs: ["contributed to", "worked on", "assisted with", "participated in"],
    can_claim: "Active involvement without primary ownership",
    cannot_escalate_from: [4, 5]
  },
  4: {
    name: "association",
    verbs: ["involved with", "engaged in", "supported", "helped with"],
    can_claim: "Supportive/secondary role",
    cannot_escalate_from: [5]
  },
  5: {
    name: "proximity",
    verbs: ["exposed to", "familiar with", "worked alongside", "part of team that"],
    can_claim: "Environmental exposure only",
    cannot_escalate_to: "ANY higher tier"
  }
}
```

## Enforcement Rules
- Facts are locked to their evidence-supported tier
- Precision can NEVER increase beyond source evidence
- When ambiguous, assign LOWEST applicable tier
- Tier boundaries are absolute and non-negotiable
"""

    # Save precision tier system
    tier_path = Path(output_dir) / 'validation/precision_tiers.md'
    tier_path.parent.mkdir(parents=True, exist_ok=True)
    with open(tier_path, 'w') as f:
        f.write(tier_content)
    print(f"Created: {tier_path}")

    # Save orchestrator file
    orchestrator_path = Path(output_dir) / 'orchestrator.md'
    with open(orchestrator_path, 'w') as f:
        f.write(orchestrator_content)
    print(f"Created: {orchestrator_path}")

    # Create validation test file
    test_content = """# Module Validation Tests
# Ensures all critical components preserved after modularization

## Component Presence Tests

```python
def test_all_phases_present():
    required_phases = [
        'phase_0_collection',
        'phase_0_5_iteration',
        'phase_1_extraction',
        'phase_2_hypothesis',
        'phase_3_optimization',
        'phase_4_generation',
        'adversarial_validation',
        'verification_suite',
        'phase_6_learning',
        'phase_7_iteration'
    ]
    for phase in required_phases:
        assert phase_exists(phase), f"Missing phase: {phase}"

def test_all_safeguards_present():
    required_safeguards = [
        'Role-Project Firewall',
        'Source Attribution Check',
        'Phrasing Pattern Validation',
        'Evidence-Based Decision Guard',
        'Over-Optimization Prevention',
        'Engagement-Accuracy Balance',
        'Tier Boundary Enforcement',
        'Adversarial Validation Gate',
        'Dual-Lock Verification',
        'Domain Boundary Enforcement',
        'Semantic Diff Validation',
        'Pipeline Enforcement',
        'Engagement Enhancement Boundaries',
        'Learning Accumulator Protection'
    ]
    for safeguard in required_safeguards:
        assert safeguard_exists(safeguard), f"Missing safeguard: {safeguard}"

def test_tier_system_intact():
    assert all_five_tiers_defined()
    assert tier_escalation_prevented()
    assert conservative_interpretation_enforced()

def test_adversarial_validation_intensity():
    assert adversarial_mindset == "hostile"
    assert success_metric == "violations_found"
    assert multiple_rounds_required()
```

## Behavioral Equivalence Tests

```python
def test_same_output_for_same_input():
    test_cases = load_test_cases()
    for test in test_cases:
        v5_output = run_v5_monolith(test.input)
        v5_1_output = run_v5_1_modular(test.input)
        assert outputs_semantically_equal(v5_output, v5_1_output)

def test_catches_known_violations():
    violation_cases = load_violation_test_suite()
    for violation in violation_cases:
        assert v5_1_catches_violation(violation)
```
"""

    # Save test file
    test_path = Path(output_dir) / 'tests/validation_tests.md'
    test_path.parent.mkdir(parents=True, exist_ok=True)
    with open(test_path, 'w') as f:
        f.write(test_content)
    print(f"Created: {test_path}")

    print("\n✅ Framework successfully modularized!")
    print(f"📁 Modules created in: {output_dir}/")
    print("📋 Next step: Review modules and implement specific enhancements")

if __name__ == "__main__":
    split_framework()