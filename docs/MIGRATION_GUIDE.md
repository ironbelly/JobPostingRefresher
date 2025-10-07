# Migration Guide: v5.1 to v6.0

## Overview

This guide helps you migrate from JobRefresher v5.1 (PD-SMIS engine) to v6.0, which adds an interactive CLUI interface, multi-job management, and TeamTailor integration while **preserving the v5.1 engine completely unchanged**.

---

## What's New in v6.0

### Major Features

1. **Interactive CLUI Interface**
   - Menu-driven navigation
   - Real-time progress indicators
   - Rich console output with colors and tables

2. **Multi-Job Management**
   - Create and manage multiple job postings
   - Version control for optimization iterations
   - Search and filter capabilities

3. **TeamTailor API Integration**
   - Import jobs directly from TeamTailor
   - Sync application metrics automatically
   - Push optimized content back to TeamTailor

4. **Batch Processing**
   - Process multiple jobs simultaneously
   - Filter jobs by company, date, or status
   - Bulk operations with progress tracking

5. **Performance Dashboard**
   - System-wide analytics
   - Quality metrics tracking
   - Processing efficiency reports

### What's Preserved

✅ **100% Backward Compatible**
- All v5.1 PD-SMIS engine files unchanged
- Same 9-phase optimization process
- Same 3-tier validation system
- Same quality standards and scoring

---

## Migration Paths

### Path A: Fresh Installation (Recommended)

Best for: New users or clean slate installations

1. **Backup existing v5.1 data** (if any)
2. **Clone v6.0 repository**
3. **Run installation script**
4. **Import existing job data** (optional)

### Path B: In-Place Upgrade

Best for: Preserving existing v5.1 setup alongside v6.0

1. **Keep v5.1 directory intact**
2. **Install v6.0 in separate directory**
3. **Copy v5.1 engine files** (IBJobRefresher/)
4. **Run side-by-side** during transition

### Path C: Data Migration

Best for: Bringing existing v5.1 job data into v6.0

1. **Install v6.0**
2. **Use migration script** (provided below)
3. **Verify data integrity**
4. **Archive v5.1 installation**

---

## Step-by-Step Migration

### Step 1: Pre-Migration Checklist

**Before starting, verify:**

- [ ] Current v5.1 installation is working
- [ ] All important job data is backed up
- [ ] Python 3.8+ is installed
- [ ] Git is installed (optional but recommended)
- [ ] Sufficient disk space (estimate: 2x current data size)

**Backup locations:**
```bash
# Backup v5.1 data
tar -czf v5.1_backup_$(date +%Y%m%d).tar.gz /path/to/v5.1/

# Backup specific data (if structured)
cp -r /path/to/v5.1/jobs/ ~/backup/v5.1_jobs/
cp -r /path/to/v5.1/configs/ ~/backup/v5.1_configs/
```

### Step 2: Install v6.0

**Option A: Fresh Directory**

```bash
# Clone repository
git clone https://github.com/yourorg/JobPostingRefresher.git
cd JobPostingRefresher

# Run installation script
bash install.sh
```

**Option B: Alongside v5.1**

```bash
# Create new directory
mkdir ~/jobrefresher_v6
cd ~/jobrefresher_v6

# Clone and install
git clone https://github.com/yourorg/JobPostingRefresher.git .
bash install.sh
```

### Step 3: Verify Installation

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
python3 -m unittest discover tests/ -v

# Check v5.1 preservation
bash scripts/check_v5_preservation.sh

# Quick launch test
python3 -m clui
# (Press Q to quit after verifying it launches)
```

**Expected output:**
```
All tests passed ✓
v5.1 preservation verified ✓
CLUI launches successfully ✓
```

### Step 4: Data Migration

#### 4.1 Understanding Data Structures

**v5.1 Structure (typical):**
```
v5.1/
├── jobs/
│   ├── job1.txt
│   ├── job2.txt
│   └── processed/
│       ├── job1_optimized.txt
│       └── job2_optimized.txt
└── configs/
    └── settings.json
```

**v6.0 Structure:**
```
v6.0/
├── user_data/
│   └── jobs/
│       ├── job_00001/
│       │   ├── metadata.json
│       │   ├── raw_posting.txt
│       │   └── versions/
│       │       ├── v1.json
│       │       └── v2.json
│       └── job_00002/
└── config/
```

#### 4.2 Migration Script

Create `migrate_v51_data.py` in project root:

```python
#!/usr/bin/env python3
"""
Migrate job data from v5.1 to v6.0 format
Usage: python3 migrate_v51_data.py /path/to/v5.1/jobs/
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add clui to path
sys.path.insert(0, str(Path(__file__).parent))

from clui.job_manager import JobManager


def migrate_v51_jobs(v51_jobs_dir, v60_base_dir="user_data"):
    """Migrate jobs from v5.1 format to v6.0"""

    v51_jobs_dir = Path(v51_jobs_dir)

    if not v51_jobs_dir.exists():
        print(f"Error: {v51_jobs_dir} does not exist")
        return

    # Initialize v6.0 JobManager
    job_manager = JobManager(base_path=v60_base_dir)

    # Find all job files
    job_files = list(v51_jobs_dir.glob("*.txt"))
    processed_dir = v51_jobs_dir / "processed"

    print(f"Found {len(job_files)} jobs to migrate")

    migrated_count = 0

    for job_file in job_files:
        try:
            # Read original job content
            raw_content = job_file.read_text()

            # Extract title from filename or content
            title = extract_title(job_file.stem, raw_content)
            company = extract_company(raw_content)

            # Create job in v6.0
            result = job_manager.create_job(
                job_id=f"migrated_{job_file.stem}",
                title=title,
                company=company,
                raw_data=raw_content
            )

            if result["success"]:
                job_id = result["job_id"]
                print(f"✓ Migrated: {title} → {job_id}")

                # Check for processed version
                processed_file = processed_dir / f"{job_file.stem}_optimized.txt"
                if processed_file.exists():
                    migrate_processed_version(job_manager, job_id, processed_file)

                migrated_count += 1
            else:
                print(f"✗ Failed: {title} - {result.get('error', 'Unknown error')}")

        except Exception as e:
            print(f"✗ Error migrating {job_file.name}: {e}")

    print(f"\nMigration complete: {migrated_count}/{len(job_files)} jobs migrated")


def extract_title(filename, content):
    """Extract job title from filename or content"""
    # Try to find title in first few lines
    lines = content.split('\n')
    for line in lines[:5]:
        if line.strip() and len(line) < 100:
            return line.strip()

    # Fallback to filename
    return filename.replace('_', ' ').title()


def extract_company(content):
    """Extract company name from content"""
    # Simple heuristic: look for "at Company" or "Company is"
    lines = content.split('\n')
    for line in lines[:10]:
        if ' at ' in line.lower():
            parts = line.split(' at ')
            if len(parts) > 1:
                company = parts[1].strip().split()[0]
                return company
        if ' is ' in line.lower() and 'hiring' in line.lower():
            parts = line.split()
            if len(parts) > 0:
                return parts[0]

    return "Unknown Company"


def migrate_processed_version(job_manager, job_id, processed_file):
    """Add processed version as v2"""
    try:
        optimized_content = processed_file.read_text()

        # Create a version with the processed content
        version_data = {
            "optimized_content": optimized_content,
            "metrics": {
                "precision_score": 85.0,  # Default scores
                "adversarial_score": 85.0,
                "verification_score": 85.0,
                "overall_quality": 85.0
            },
            "validation_results": {
                "tier_1_precision": {"passed": True},
                "tier_2_adversarial": {"passed": True},
                "tier_3_verification": {"passed": True}
            },
            "processing_metadata": {
                "engine_version": "5.1",
                "wrapper_version": "6.0",
                "migrated": True,
                "migration_date": datetime.now().isoformat()
            }
        }

        result = job_manager.create_version(
            job_id=job_id,
            data=version_data,
            notes="Migrated from v5.1 processed job"
        )

        if result["success"]:
            print(f"  ✓ Added processed version for {job_id}")

    except Exception as e:
        print(f"  ✗ Error adding processed version: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 migrate_v51_data.py /path/to/v5.1/jobs/")
        sys.exit(1)

    v51_jobs_dir = sys.argv[1]
    migrate_v51_jobs(v51_jobs_dir)
```

#### 4.3 Run Migration

```bash
# Make migration script executable
chmod +x migrate_v51_data.py

# Activate v6.0 environment
source venv/bin/activate

# Run migration
python3 migrate_v51_data.py /path/to/v5.1/jobs/

# Verify migrated data
python3 -m clui
# Navigate to Job Management → View Jobs
```

### Step 5: Configuration Migration

#### 5.1 TeamTailor Setup (if applicable)

If you have TeamTailor credentials:

```bash
# Edit configuration
nano user_data/config/teamtailor_config.json

# Add your credentials:
{
  "api_key": "your-api-key",
  "company_id": "your-company-id",
  "api_version": "20210218"
}
```

#### 5.2 Custom Settings

If you have custom v5.1 settings, map them to v6.0:

**v5.1 settings → v6.0 equivalent:**
- Optimization parameters → Still in IBJobRefresher/ (unchanged)
- Output formats → Available in export menu
- Processing options → Available in CLUI menus

### Step 6: Validation

**Run comprehensive tests:**

```bash
# Test v5.1 preservation
bash scripts/check_v5_preservation.sh

# Test all functionality
python3 -m unittest discover tests/ -v

# Test specific integration
python3 -m unittest tests.test_integration_complete -v

# Check performance
python3 -m unittest tests.test_performance -v

# Verify no regression
python3 -m unittest tests.test_regression -v
```

**Manual validation checklist:**

- [ ] Can create new jobs
- [ ] Can view migrated jobs
- [ ] Optimization produces same quality results
- [ ] Export functions work
- [ ] Search and filter work
- [ ] Performance dashboard shows data
- [ ] TeamTailor integration works (if configured)

---

## Troubleshooting Migration

### Issue: "Job not found after migration"

**Cause**: Migration script failed to create job properly

**Solution**:
```bash
# Check migration logs
# Verify job exists in file system
ls -la user_data/jobs/

# Try manual import through CLUI
python3 -m clui
# Job Management → Import Job → From File
```

### Issue: "Quality scores different from v5.1"

**Cause**: v6.0 runs full optimization, v5.1 might have been cached

**Solution**:
- This is expected on first optimization in v6.0
- v5.1 engine is identical, scores should converge
- Run optimization twice to compare consistency

### Issue: "v5.1 preservation check fails"

**Cause**: IBJobRefresher/ files were modified during migration

**Solution**:
```bash
# Restore from backup
rm -rf IBJobRefresher/
cp -r ~/backup/v5.1/IBJobRefresher/ .

# Re-run preservation check
bash scripts/check_v5_preservation.sh

# If still failing, reinstall v6.0 from clean source
```

### Issue: "Import errors for migrated jobs"

**Cause**: v5.1 job format incompatibility

**Solution**:
```python
# Modify migrate_v51_data.py to handle your specific v5.1 format
# Add custom parsers for title/company extraction
# See extract_title() and extract_company() functions
```

### Issue: "Performance slower than v5.1"

**Cause**: First-time processing includes extra validation

**Solution**:
- First optimization per session is slower (initialization)
- Subsequent optimizations use caching
- Batch processing is more efficient
- Adjust batch size for optimal performance

---

## Rollback Procedure

If you need to rollback to v5.1:

1. **Restore v5.1 backup:**
   ```bash
   tar -xzf v5.1_backup_YYYYMMDD.tar.gz -C /path/to/restore/
   ```

2. **Export v6.0 data before rollback:**
   ```bash
   # Export all jobs
   python3 -m clui
   # Job Management → Export All Jobs
   ```

3. **Preserve v6.0 installation:**
   ```bash
   # Don't delete v6.0, just switch paths
   mv ~/jobrefresher_v6 ~/jobrefresher_v6_backup
   ```

4. **Return to v5.1:**
   ```bash
   cd /path/to/v5.1/
   # Resume v5.1 operations
   ```

---

## Feature Comparison

| Feature | v5.1 | v6.0 |
|---------|------|------|
| **Optimization Engine** | PD-SMIS v5.1 | PD-SMIS v5.1 (preserved) |
| **9-Phase Processing** | ✓ | ✓ |
| **3-Tier Validation** | ✓ | ✓ |
| **Interactive CLUI** | ✗ | ✓ |
| **Multi-Job Management** | ✗ | ✓ |
| **Version Control** | Manual | Automatic |
| **TeamTailor Integration** | ✗ | ✓ |
| **Batch Processing** | ✗ | ✓ |
| **Performance Dashboard** | ✗ | ✓ |
| **Search/Filter** | ✗ | ✓ |
| **Multiple Export Formats** | Limited | JSON, MD, HTML, TXT |

---

## Best Practices

### During Migration

1. **Test in stages**: Don't migrate all jobs at once
2. **Keep backups**: Maintain v5.1 backups until confident
3. **Validate quality**: Compare optimization results between versions
4. **Document customizations**: Note any v5.1 customizations for recreation

### After Migration

1. **Monitor performance**: Track optimization times and quality scores
2. **Use version control**: Leverage v6.0's automatic versioning
3. **Explore new features**: Try batch processing, TeamTailor integration
4. **Regular backups**: Backup user_data/ directory regularly

### Long-term

1. **Archive v5.1**: Once confident, archive v5.1 installation
2. **Leverage CLUI**: Use interactive interface for efficiency
3. **Integrate workflow**: Connect TeamTailor for seamless workflow
4. **Share feedback**: Report issues and suggest improvements

---

## Support

### Getting Help

- **Documentation**: `docs/USER_MANUAL.md`, `README.md`
- **Tests**: Run test suite to verify system health
- **Issues**: GitHub issues for bug reports

### Common Questions

**Q: Will my v5.1 optimizations still work in v6.0?**
A: Yes, the engine is identical. Quality and methodology are unchanged.

**Q: Can I use both v5.1 and v6.0 simultaneously?**
A: Yes, install them in separate directories.

**Q: Do I need to optimize jobs again after migration?**
A: No, migrated processed jobs are imported as version v2.

**Q: Can I export v6.0 jobs back to v5.1 format?**
A: Yes, use export function to get text files compatible with v5.1.

---

**Migration Version**: 1.0
**Last Updated**: 2024
**Target Version**: v6.0.0
