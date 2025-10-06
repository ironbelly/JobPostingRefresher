#!/usr/bin/env python3
"""
Fix missing module extractions from PD-SMIS v5.0 framework
"""

import re
from pathlib import Path

def extract_missing_modules():
    """Extract the missing modules with correct headers"""

    # Read the entire framework
    with open('JobEvalV5.md', 'r') as f:
        content = f.read()

    # Extract Phase 2 (was missing)
    if '## PHASE 2:' in content:
        start_idx = content.index('## PHASE 2:')
        end_idx = content.index('## PHASE 3:')
        phase_2_content = content[start_idx:end_idx].strip()

        phase_2_header = """# KPI-based bottleneck analysis and hypothesis generation
# Module: phases/phase_2_hypothesis.md
# Part of PD-SMIS v5.1 Modular Framework

---

"""
        output_path = Path('refactored/phases/phase_2_hypothesis.md')
        with open(output_path, 'w') as f:
            f.write(phase_2_header + phase_2_content)
        print(f"Created: {output_path}")

    # Extract Phase 5 (was missing - verification suite)
    if '## PHASE 5:' in content:
        start_idx = content.index('## PHASE 5:')
        end_idx = content.index('## PHASE 6:')
        phase_5_content = content[start_idx:end_idx].strip()

        phase_5_header = """# Multi-layer verification and validation suite
# Module: validation/verification_suite.md
# Part of PD-SMIS v5.1 Modular Framework

---

"""
        output_path = Path('refactored/validation/verification_suite.md')
        with open(output_path, 'w') as f:
            f.write(phase_5_header + phase_5_content)
        print(f"Created: {output_path}")

    # Extract Critical Safeguards
    if '## CRITICAL SAFEGUARDS' in content:
        start_idx = content.index('## CRITICAL SAFEGUARDS')
        # Find the end - look for next major section or end of file
        try:
            # Try to find FINAL EXECUTION or OUTPUT FORMAT
            if '## FINAL EXECUTION' in content[start_idx:]:
                end_idx = start_idx + content[start_idx:].index('## FINAL EXECUTION')
            elif '## OUTPUT FORMAT' in content[start_idx:]:
                end_idx = start_idx + content[start_idx:].index('## OUTPUT FORMAT')
            else:
                # Goes to end of file
                end_idx = len(content)
        except:
            end_idx = len(content)

        safeguards_content = content[start_idx:end_idx].strip()

        safeguards_header = """# All 14 Critical Safeguards for PD-SMIS Framework
# Module: safeguards/critical_safeguards.md
# Part of PD-SMIS v5.1 Modular Framework

---

"""
        output_path = Path('refactored/safeguards/critical_safeguards.md')
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(safeguards_header + safeguards_content)
        print(f"Created: {output_path}")

    # Check for execution sequence and output format
    if '## FINAL EXECUTION' in content or 'FINAL_VALIDATION_GATE' in content:
        # Look for final execution logic
        execution_content = """# Pipeline Execution Logic
# Module: components/execution_sequence.md
# Part of PD-SMIS v5.1 Modular Framework

---

## FINAL EXECUTION SEQUENCE

```javascript
function executePipeline(input) {
  // Phase 0: Collect inputs
  const sources = collectSources(input);

  // Phase 0.5: Load iteration context
  const context = loadIterationContext(sources);

  // Phase 1: Extract with semantic fingerprinting
  const extracted = extractWithFingerprinting(sources);

  // Phase 2: Generate hypotheses
  const hypotheses = generateHypotheses(extracted, context.kpis);

  // Phase 3: Design optimization strategy
  const strategy = designOptimization(hypotheses, extracted);

  // Phase 4: Generate content
  const generated = generateContent(strategy, extracted);

  // Phase 4.5: Adversarial validation
  const adversarialResult = runAdversarialValidation(generated);
  if (!adversarialResult.passed) {
    throw new Error("Adversarial validation failed: " + adversarialResult.violations);
  }

  // Phase 5: Multi-layer verification
  const verificationResult = runVerificationSuite(generated);
  if (!verificationResult.passed) {
    throw new Error("Verification failed: " + verificationResult.failures);
  }

  // Phase 6: Learning protocol
  const learnings = extractLearnings(generated, context);

  // Phase 7: Prepare for next iteration
  const iterationPackage = prepareIteration(generated, learnings);

  return {
    optimizedPosting: generated,
    learnings: learnings,
    nextIteration: iterationPackage
  };
}

// All safeguards active throughout pipeline
const ACTIVE_SAFEGUARDS = [
  'roleProjectFirewall',
  'sourceAttribution',
  'phrasingValidation',
  'evidenceBasedDecisions',
  'overOptimizationPrevention',
  'engagementAccuracyBalance',
  'tierBoundaryEnforcement',
  'adversarialValidation',
  'dualLockVerification',
  'domainBoundaryEnforcement',
  'semanticDiffValidation',
  'pipelineEnforcement',
  'engagementBoundaries',
  'learningAccumulatorProtection'
];
```
"""
        output_path = Path('refactored/components/execution_sequence.md')
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(execution_content)
        print(f"Created: {output_path}")

    # Create output format module
    output_format_content = """# Output Structure and Formatting
# Module: components/output_format.md
# Part of PD-SMIS v5.1 Modular Framework

---

## OUTPUT FORMAT

### Standard Job Posting Output

```markdown
[OPTIMIZED JOB TITLE]
{Evidence-based title optimized for search and clarity}

[OPTIMIZED JOB POSTING]
{Full posting with all optimizations applied}
- Maintains 100% source accuracy
- Tier-appropriate language
- KPI-targeted improvements

[SEMANTIC VALIDATION REPORT]
✅ All facts traced to source
✅ No tier escalations detected
✅ Domain boundaries maintained
✅ Adversarial validation passed

[KPI IMPROVEMENT PROJECTIONS]
Based on applied optimizations:
- Visit/Application: +X% expected
- Application/Screening: +Y% expected
- [Additional metrics]

[ITERATION LEARNINGS]
- What worked: {specific elements}
- What didn't work: {specific elements}
- Recommended next test: {hypothesis}
```

### LinkedIn Ad Campaign Output (if applicable)

```markdown
[OPTIMIZED AD INTRO]
{Hook optimized for target audience}

[AD TARGETING REFINEMENTS]
- Refined job titles: []
- Refined skills: []
- Refined interests: []

[EXPECTED AD PERFORMANCE]
- CTR improvement: +X%
- CPC reduction: -Y%
- Conversion improvement: +Z%
```

### Validation Evidence Package

```javascript
VALIDATION_EVIDENCE = {
  source_attribution: {
    total_claims: n,
    verified_claims: n,
    unattributed_claims: 0
  },
  tier_compliance: {
    tier_1_facts: n,
    tier_2_facts: n,
    tier_3_facts: n,
    tier_4_facts: n,
    tier_5_facts: n,
    escalation_attempts: 0,
    escalations_blocked: 0
  },
  adversarial_rounds: {
    total_rounds: n,
    violations_found: [],
    violations_fixed: [],
    final_status: "PASSED"
  },
  performance_metrics: {
    processing_time: "Xs",
    validation_time: "Ys",
    total_tokens: n
  }
}
```

### Error Output Format

```markdown
[ERROR TYPE]
{Specific error classification}

[VIOLATION DETAILS]
- What was attempted: {description}
- Why it failed: {reason}
- Source reference: {line/section}

[REMEDIATION]
- Required fix: {specific action}
- Validation that will check: {validator}

[CANNOT PROCEED UNTIL]
{Specific conditions that must be met}
```
"""

    output_path = Path('refactored/components/output_format.md')
    with open(output_path, 'w') as f:
        f.write(output_format_content)
    print(f"Created: {output_path}")

    print("\n✅ Missing modules extracted successfully!")

if __name__ == "__main__":
    extract_missing_modules()