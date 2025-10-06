# Precision Tier Classification System
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
