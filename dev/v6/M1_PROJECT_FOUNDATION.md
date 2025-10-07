# Milestone 1: Project Foundation

## Purpose
Establish the core project structure, preserve v5.1 engine integrity, and set up development environment with strict separation between new and existing code.

**Success Criteria:**
- Complete directory structure created
- v5.1 engine copied and checksums recorded
- Python environment configured
- Git repository initialized with proper .gitignore

## Dependencies
- None (this is the foundation milestone)

## Start Procedure

### Pre-flight Checks
```bash
# 1. Verify we're in the correct directory
pwd  # Should show /config/workspace/JobPostingRefresher

# 2. Check if v5.1 engine exists
ls -la IBJobRefresher/  # Should show existing v5.1 files

# 3. Verify Python version
python --version  # Should be 3.8+

# 4. Check git status
git status  # Ensure clean working directory
```

### Initialize Milestone
```bash
# Create milestone tracking
touch /dev/v6/M1.IN_PROGRESS
echo "Started: $(date)" >> /dev/v6/execution_log.md
```

## Tasks

### Task 1.1: Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: v5.1 baseline"
```

### Task 1.2: Create Complete Directory Structure
```bash
# Core directories
mkdir -p config
mkdir -p clui
mkdir -p tests
mkdir -p user_data/config
mkdir -p user_data/jobs

# Documentation and examples
mkdir -p docs
mkdir -p examples
```

### Task 1.3: Create Comprehensive .gitignore
Create `.gitignore` with:
```gitignore
# User data - NEVER commit
/user_data/
user_data/**

# Configuration with secrets
config/teamtailor_config.json
*.secret
*.key
*_credentials.json

# Environment
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Logs and temp
*.log
logs/
tmp/
temp/
*.tmp
*.bak

# Testing
.coverage
htmlcov/
.pytest_cache/
```

### Task 1.4: Preserve v5.1 Engine with Checksums
```bash
# IF v5.1 doesn't exist in IBJobRefresher, copy it
# Otherwise, just record checksums

# Record checksums for preservation verification
find IBJobRefresher -name "*.md" -exec md5sum {} \; > dev/v6/v5_baseline_checksums.txt

# Create preservation marker
echo "V5.1 ENGINE PRESERVED - DO NOT MODIFY" > IBJobRefresher/DO_NOT_MODIFY.txt
```

### Task 1.5: Setup Python Environment
Create `requirements.txt`:
```
rich>=13.0.0
prompt-toolkit>=3.0.0
requests>=2.28.0
python-dateutil>=2.8.0
colorama>=0.4.0
pytest>=7.0.0
pytest-cov>=4.0.0
```

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Task 1.6: Create Configuration Templates
Create `config/teamtailor_config.json.example`:
```json
{
  "api_key": "YOUR_API_KEY_HERE",
  "company_id": "YOUR_COMPANY_ID_HERE",
  "api_version": "20210218",
  "_comment": "Copy this file to user_data/config/teamtailor_config.json and add your credentials"
}
```

### Task 1.7: Create Project Documentation Structure
Create `README.md`:
```markdown
# JobRefresher v6.0

AI-powered job posting optimization system with interactive CLI interface.

## Quick Start
1. Copy `config/teamtailor_config.json.example` to `user_data/config/teamtailor_config.json`
2. Add your TeamTailor API credentials
3. Run: `python clui/jbr.py`

## Directory Structure
- `/IBJobRefresher/` - Core v5.1 engine (DO NOT MODIFY)
- `/clui/` - New CLI interface code
- `/user_data/` - Your jobs and configuration (git-ignored)
- `/tests/` - Validation and preservation tests
```

### Task 1.8: Initialize User Data Structure
```bash
# Create example job structure (for testing)
mkdir -p user_data/jobs/example_job_001
echo '{"job_id": "example_001", "created_date": "'$(date -I)'"}' > user_data/jobs/example_job_001/metadata.json
echo "v1" > user_data/jobs/example_job_001/current_version.txt
mkdir -p user_data/jobs/example_job_001/v1

# Create README for user_data
cat > user_data/README.md << 'EOF'
# User Data Directory

This directory contains your personal data:
- `/config/` - Your API credentials and settings
- `/jobs/` - Your job postings and optimization history

This directory is git-ignored and never committed.
To backup: `tar -czf backup_$(date +%Y%m%d).tar.gz user_data/`
EOF
```

### Task 1.9: Create Development Utilities
Create `dev/v6/check_preservation.sh`:
```bash
#!/bin/bash
# Quick script to verify v5.1 preservation

echo "Checking v5.1 preservation..."
if [ -f "dev/v6/v5_baseline_checksums.txt" ]; then
    find IBJobRefresher -name "*.md" -exec md5sum {} \; > /tmp/current_checksums.txt
    if diff dev/v6/v5_baseline_checksums.txt /tmp/current_checksums.txt > /dev/null; then
        echo "✅ v5.1 files intact"
    else
        echo "❌ WARNING: v5.1 files modified!"
        diff dev/v6/v5_baseline_checksums.txt /tmp/current_checksums.txt
        exit 1
    fi
else
    echo "⚠️  No baseline checksums found"
fi
```

```bash
chmod +x dev/v6/check_preservation.sh
```

### Task 1.10: Final Structure Verification and Commit
```bash
# Verify structure
tree -L 2 -d

# Run preservation check
./dev/v6/check_preservation.sh

# Commit foundation
git add .
git commit -m "M1 Complete: Project foundation established"
```

## Validation Tests

### V1.1: Directory Structure Test
```bash
# All required directories exist
for dir in clui tests user_data/config user_data/jobs docs examples; do
    [ -d "$dir" ] && echo "✅ $dir exists" || echo "❌ $dir missing"
done
```

### V1.2: Git Configuration Test
```bash
# .gitignore properly excludes user_data
echo "test" > user_data/test.txt
git status | grep -q "user_data/test.txt" && echo "❌ user_data not ignored" || echo "✅ user_data ignored"
rm user_data/test.txt
```

### V1.3: Python Environment Test
```python
# test_environment.py
import rich
import prompt_toolkit
import requests
print("✅ All core dependencies importable")
```

### V1.4: v5.1 Preservation Test
```bash
./dev/v6/check_preservation.sh
```

### V1.5: Configuration Template Test
```bash
# Template exists and is valid JSON
python -c "import json; json.load(open('config/teamtailor_config.json.example'))" && echo "✅ Config template valid"
```

## Completion Procedure

### Final Validation
```bash
# Run all validation tests
echo "Running final validation..."
python test_environment.py
./dev/v6/check_preservation.sh

# Check git status is clean
git status
```

### Mark Complete
```bash
# Mark milestone complete
mv /dev/v6/M1.IN_PROGRESS /dev/v6/M1.COMPLETE
echo "Completed: $(date)" >> /dev/v6/execution_log.md
echo "✅ Milestone 1: Project Foundation COMPLETE"
```

### Handoff Notes
- v5.1 engine preserved with checksums in `dev/v6/v5_baseline_checksums.txt`
- Python environment ready in `venv/`
- User data structure initialized
- Ready for Milestone 2: Data Layer

## Rollback Plan

If this milestone fails or needs to be undone:

```bash
# 1. Deactivate Python environment
deactivate

# 2. Remove created directories (preserve v5.1)
rm -rf clui tests user_data docs examples venv

# 3. Reset git to initial commit
git reset --hard HEAD~1

# 4. Remove milestone marker
rm -f /dev/v6/M1.COMPLETE /dev/v6/M1.IN_PROGRESS

# 5. Note in execution log
echo "ROLLED BACK M1: $(date)" >> /dev/v6/execution_log.md
```