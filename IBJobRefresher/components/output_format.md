# Output Structure and Formatting
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
