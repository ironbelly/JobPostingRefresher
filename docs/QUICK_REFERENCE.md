# JobRefresher v6.0 Quick Reference

## Installation

```bash
# Clone repository
git clone https://github.com/yourorg/JobPostingRefresher.git
cd JobPostingRefresher

# Run installation
bash install.sh

# Activate environment
source venv/bin/activate

# Launch application
python3 -m clui
```

---

## Main Menu Structure

```
Main Menu
├── [1] Job Management
│   ├── Create New Job
│   ├── View Job Details
│   ├── Search Jobs
│   ├── Import Job
│   ├── Delete Job
│   ├── Compare Versions
│   └── Export Job
├── [2] Job Processing
│   ├── Optimize Single Job
│   ├── Batch Process Jobs
│   └── Performance Dashboard
├── [3] TeamTailor Integration
│   ├── Import Jobs
│   ├── Sync Metrics
│   └── Push Optimized Job
└── [Q] Quit
```

---

## Common Operations

### Create a Job
1. Main Menu → `[1]` Job Management
2. `[1]` Create New Job
3. Enter title, company, and raw posting content

### Optimize a Job
1. Main Menu → `[2]` Job Processing
2. `[1]` Optimize Single Job
3. Enter Job ID
4. Wait for 9-phase processing to complete

### View Job Details
1. Main Menu → `[1]` Job Management
2. `[2]` View Job Details
3. Enter Job ID

### Export a Job
1. Main Menu → `[1]` Job Management
2. `[7]` Export Job
3. Choose format: JSON, Markdown, HTML, or Text

### Compare Versions
1. Main Menu → `[1]` Job Management
2. `[6]` Compare Versions
3. Enter Job ID
4. Select two versions to compare

### Batch Process Jobs
1. Main Menu → `[2]` Job Processing
2. `[2]` Batch Process Jobs
3. Select filter criteria
4. Monitor progress

---

## Keyboard Shortcuts

### Navigation
| Key | Action |
|-----|--------|
| `1-9` | Select menu option |
| `Q` | Quit current menu |
| `B` | Go back to previous menu |
| `H` | Show help |

### During Processing
| Key | Action |
|-----|--------|
| `Ctrl+C` | Cancel operation |
| `P` | Pause processing |
| `R` | Resume processing |
| `S` | Show status |

---

## File Locations

```
JobPostingRefresher/
├── user_data/                  # User data (git-ignored)
│   ├── jobs/                  # Job storage
│   │   └── {job_id}/
│   │       ├── metadata.json
│   │       ├── raw_posting.txt
│   │       ├── versions/
│   │       │   ├── v1.json
│   │       │   ├── v2.json
│   │       │   └── v3.json
│   │       └── exports/
│   ├── config/                # Configuration
│   │   └── teamtailor_config.json
│   └── logs/                  # Application logs
├── IBJobRefresher/            # v5.1 engine (DO NOT MODIFY)
├── clui/                      # v6.0 CLUI components
├── tests/                     # Test suite
└── docs/                      # Documentation
```

---

## PD-SMIS Engine Phases

### Optimization Phases (9 Total)
```
Phase 0 - Collection & Analysis
Phase 0.5 - Iteration
Phase 0.6 - Error Handling
Phase 1 - Information Extraction
Phase 2 - Hypothesis Generation
Phase 3 - Optimization Strategy
Phase 4 - Content Generation
Phase 6 - Learning Integration
Phase 7 - Iterative Refinement
```

### Validation Tiers (3 Total)
```
Tier 1 - Precision Validation
Tier 2 - Adversarial Validation
Tier 3 - Verification Suite
```

---

## Configuration

### TeamTailor API Setup
```bash
# Edit configuration file
nano user_data/config/teamtailor_config.json

# Add credentials:
{
  "api_key": "your-api-key-here",
  "company_id": "your-company-id",
  "api_version": "20210218"
}
```

---

## Testing

```bash
# Run all tests
python3 -m unittest discover tests/ -v

# Run specific test category
python3 -m unittest tests.unit.test_job_manager -v
python3 -m unittest tests.test_integration_complete -v
python3 -m unittest tests.test_performance -v
python3 -m unittest tests.test_regression -v
python3 -m unittest tests.test_v5_preservation_final -v

# Run CI test suite
bash tests/run_ci_tests.sh

# Check test coverage
bash tests/check_coverage.sh

# Verify v5.1 preservation
bash scripts/check_v5_preservation.sh
```

---

## Job Data Structure

### Metadata (metadata.json)
```json
{
  "job_id": "job_12345",
  "title": "Senior Software Engineer",
  "company": "Acme Corp",
  "created_date": "2024-01-15T10:30:00",
  "status": "processed",
  "current_version": 2,
  "teamtailor_id": null
}
```

### Version Data (versions/v1.json)
```json
{
  "optimized_content": "Enhanced job posting...",
  "metrics": {
    "precision_score": 87.5,
    "adversarial_score": 92.0,
    "verification_score": 89.3,
    "overall_quality": 89.6
  },
  "validation_results": {
    "tier_1_precision": {"passed": true},
    "tier_2_adversarial": {"passed": true},
    "tier_3_verification": {"passed": true}
  },
  "processing_metadata": {
    "engine_version": "5.1",
    "wrapper_version": "6.0",
    "timestamp": "2024-01-15T10:35:42"
  }
}
```

---

## Common Commands

### Launch Application
```bash
# Method 1: Module
python3 -m clui

# Method 2: Direct
python3 clui/jbr.py

# Method 3: Launcher (after install)
./jobrefresher
```

### Manage Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Install dependencies manually
pip install rich prompt-toolkit requests
```

### Git Operations
```bash
# Check current state
git status
git branch

# Create feature branch
git checkout -b feature/your-feature

# View changes
git diff

# Commit changes
git add .
git commit -m "Description"
```

---

## Error Messages

### Common Errors & Solutions

**"Job not found"**
→ Verify Job ID, use search function

**"TeamTailor connection failed"**
→ Check API key in `user_data/config/teamtailor_config.json`

**"Optimization not available"**
→ Verify IBJobRefresher/ files exist, run `bash scripts/check_v5_preservation.sh`

**"Permission denied"**
→ Check file permissions, ensure user_data/ is writable

**"Module not found"**
→ Activate virtual environment: `source venv/bin/activate`

---

## Performance Benchmarks

| Operation | Expected Time |
|-----------|---------------|
| Create job | < 0.5s |
| List 50 jobs | < 1s |
| Retrieve job | < 0.1s |
| Optimize job | ~2 minutes |
| Create version | < 0.5s |
| Export (3 formats) | < 2s |
| Batch (10 jobs) | ~20 minutes |

---

## Troubleshooting Quick Checks

```bash
# Check Python version (need 3.8+)
python3 --version

# Verify v5.1 engine integrity
bash scripts/check_v5_preservation.sh

# Run all tests
python3 -m unittest discover tests/ -v

# Check disk space
df -h user_data/

# View recent logs
tail -n 50 user_data/logs/latest.log

# Clean up temporary files
bash scripts/cleanup.sh
```

---

## Quality Metrics

### Score Ranges
- **Precision Score**: 0-100% (Target: ≥80%)
- **Adversarial Score**: 0-100% (Target: ≥80%)
- **Verification Score**: 0-100% (Target: ≥80%)
- **Overall Quality**: Average of three scores

### Quality Indicators
```
90-100% - Excellent
80-89%  - Good
70-79%  - Acceptable
<70%    - Needs Review
```

---

## Export Formats

### JSON
- Complete data structure
- Machine-readable
- All metadata included

### Markdown
- Human-readable
- Formatted text
- Easy to share

### HTML
- Web-ready
- Styled presentation
- Printable format

### Text
- Plain text
- Simple format
- Universal compatibility

---

## Support Resources

### Documentation
- **User Manual**: `docs/USER_MANUAL.md`
- **Migration Guide**: `docs/MIGRATION_GUIDE.md`
- **README**: `README.md`
- **Changelog**: `CHANGELOG.md`

### Getting Help
- Run tests to diagnose issues
- Check error messages carefully
- Review documentation
- Check GitHub issues

---

## Tips & Best Practices

### Optimization
- Provide complete, detailed job postings
- Run optimization 2-3 times for best results
- Review optimized content before publishing

### Data Management
- Regular backups of `user_data/jobs/`
- Archive old jobs periodically
- Use version control for important jobs

### Performance
- Use batch processing for multiple jobs
- Clean up old exports regularly
- Monitor disk space usage

### TeamTailor
- Test with non-critical jobs first
- Sync metrics weekly for active jobs
- Keep API credentials secure

---

## Version Information

**Current Version**: 6.0.0
**Engine Version**: 5.1 (PD-SMIS)
**Python Required**: 3.8+
**License**: [Your License]

---

**Quick Reference Version**: 1.0
**Last Updated**: 2024
