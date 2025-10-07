#!/bin/bash
# Final validation script for JobRefresher v6.0
# Comprehensive pre-release validation

set -e  # Exit on error

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Validation results
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   JobRefresher v6.0 Final Validation ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Function: Print status message
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

# Function: Print success message
print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
    ((PASSED_CHECKS++))
}

# Function: Print error message
print_error() {
    echo -e "${RED}[✗]${NC} $1"
    ((FAILED_CHECKS++))
}

# Function: Print warning message
print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
    ((WARNING_CHECKS++))
}

# Function: Run check
run_check() {
    ((TOTAL_CHECKS++))
}

# Change to project directory
cd "$PROJECT_DIR"

echo "Validating project: $PROJECT_DIR"
echo "Timestamp: $(date)"
echo ""

# ========================================
# 1. CRITICAL: v5.1 Preservation
# ========================================

print_status "=== v5.1 Preservation Validation ==="
echo ""

run_check
print_status "Checking v5.1 engine files..."

if [ ! -f "scripts/check_v5_preservation.sh" ]; then
    print_error "Preservation check script missing"
else
    if bash scripts/check_v5_preservation.sh > /dev/null 2>&1; then
        print_success "v5.1 engine preservation verified"
    else
        print_error "v5.1 engine has been modified - CRITICAL FAILURE"
        echo ""
        echo "Run: bash scripts/check_v5_preservation.sh"
        exit 1
    fi
fi

echo ""

# ========================================
# 2. Directory Structure
# ========================================

print_status "=== Directory Structure Validation ==="
echo ""

# Check critical directories
CRITICAL_DIRS=(
    "IBJobRefresher"
    "IBJobRefresher/phases"
    "IBJobRefresher/validation"
    "IBJobRefresher/safeguards"
    "IBJobRefresher/components"
    "clui"
    "tests"
    "tests/unit"
    "docs"
    "scripts"
    "user_data"
    "user_data/jobs"
    "user_data/config"
)

for dir in "${CRITICAL_DIRS[@]}"; do
    run_check
    if [ -d "$dir" ]; then
        print_success "Directory exists: $dir"
    else
        print_error "Missing critical directory: $dir"
    fi
done

echo ""

# ========================================
# 3. Critical Files
# ========================================

print_status "=== Critical Files Validation ==="
echo ""

# Check critical files
CRITICAL_FILES=(
    "README.md"
    "CHANGELOG.md"
    "install.sh"
    "clui/__init__.py"
    "clui/__main__.py"
    "clui/jbr.py"
    "clui/job_manager.py"
    "clui/pd_smis_engine.py"
    "clui/teamtailor_client.py"
    "tests/run_ci_tests.sh"
    "tests/check_coverage.sh"
    "scripts/check_v5_preservation.sh"
    "scripts/cleanup.sh"
    "scripts/final_validation.sh"
    "docs/USER_MANUAL.md"
    "docs/MIGRATION_GUIDE.md"
    "docs/QUICK_REFERENCE.md"
    "docs/RELEASE_CHECKLIST.md"
)

for file in "${CRITICAL_FILES[@]}"; do
    run_check
    if [ -f "$file" ]; then
        print_success "File exists: $file"
    else
        print_error "Missing critical file: $file"
    fi
done

echo ""

# ========================================
# 4. v5.1 Engine Files
# ========================================

print_status "=== v5.1 Engine Files Validation ==="
echo ""

V51_FILES=(
    "IBJobRefresher/orchestrator.md"
    "IBJobRefresher/phases/phase_0_collection.md"
    "IBJobRefresher/phases/phase_0_5_iteration.md"
    "IBJobRefresher/phases/phase_0_6_error_handling.md"
    "IBJobRefresher/phases/phase_1_extraction.md"
    "IBJobRefresher/phases/phase_2_hypothesis.md"
    "IBJobRefresher/phases/phase_3_optimization.md"
    "IBJobRefresher/phases/phase_4_generation.md"
    "IBJobRefresher/phases/phase_6_learning.md"
    "IBJobRefresher/phases/phase_7_iteration.md"
    "IBJobRefresher/validation/adversarial_validation.md"
    "IBJobRefresher/validation/precision_tiers.md"
    "IBJobRefresher/validation/validation_orchestrator.md"
    "IBJobRefresher/validation/verification_suite.md"
    "IBJobRefresher/safeguards/critical_safeguards.md"
    "IBJobRefresher/components/output_format.md"
)

V51_MISSING=0

for file in "${V51_FILES[@]}"; do
    run_check
    if [ -f "$file" ]; then
        print_success "v5.1 file: $file"
    else
        print_error "Missing v5.1 file: $file"
        ((V51_MISSING++))
    fi
done

if [ $V51_MISSING -gt 0 ]; then
    print_error "Missing $V51_MISSING v5.1 engine files - CRITICAL"
fi

echo ""

# ========================================
# 5. Python Syntax Check
# ========================================

print_status "=== Python Syntax Validation ==="
echo ""

PYTHON_FILES=$(find clui tests -name "*.py" 2>/dev/null)
SYNTAX_ERRORS=0

for file in $PYTHON_FILES; do
    run_check
    if python3 -m py_compile "$file" 2>/dev/null; then
        print_success "Syntax valid: $file"
    else
        print_error "Syntax error: $file"
        ((SYNTAX_ERRORS++))
    fi
done

if [ $SYNTAX_ERRORS -gt 0 ]; then
    print_error "Found $SYNTAX_ERRORS Python syntax errors"
fi

echo ""

# ========================================
# 6. Executable Scripts
# ========================================

print_status "=== Executable Scripts Validation ==="
echo ""

EXECUTABLE_SCRIPTS=(
    "install.sh"
    "tests/run_ci_tests.sh"
    "tests/check_coverage.sh"
    "scripts/check_v5_preservation.sh"
    "scripts/cleanup.sh"
    "scripts/final_validation.sh"
)

for script in "${EXECUTABLE_SCRIPTS[@]}"; do
    run_check
    if [ -x "$script" ]; then
        print_success "Executable: $script"
    else
        print_warning "Not executable: $script (run: chmod +x $script)"
    fi
done

echo ""

# ========================================
# 7. Test Suite
# ========================================

print_status "=== Test Suite Validation ==="
echo ""

run_check
print_status "Running complete test suite..."

if python3 -m unittest discover tests/ -v > /tmp/test_output.txt 2>&1; then
    TEST_COUNT=$(grep -c "test_" /tmp/test_output.txt || echo "0")
    print_success "All tests passed ($TEST_COUNT tests)"
else
    print_error "Test suite has failures"
    echo ""
    echo "Failed tests:"
    tail -20 /tmp/test_output.txt
    echo ""
fi

# Check test counts
run_check
UNIT_TESTS=$(find tests/unit -name "test_*.py" 2>/dev/null | wc -l)
if [ "$UNIT_TESTS" -gt 0 ]; then
    print_success "Unit tests found: $UNIT_TESTS files"
else
    print_warning "No unit tests found"
fi

run_check
if [ -f "tests/test_v5_preservation_final.py" ]; then
    print_success "v5.1 preservation tests present"
else
    print_error "v5.1 preservation tests missing"
fi

run_check
if [ -f "tests/test_integration_complete.py" ]; then
    print_success "Integration tests present"
else
    print_error "Integration tests missing"
fi

run_check
if [ -f "tests/test_performance.py" ]; then
    print_success "Performance tests present"
else
    print_error "Performance tests missing"
fi

run_check
if [ -f "tests/test_regression.py" ]; then
    print_success "Regression tests present"
else
    print_error "Regression tests missing"
fi

echo ""

# ========================================
# 8. Documentation Completeness
# ========================================

print_status "=== Documentation Validation ==="
echo ""

# Check README.md content
run_check
if grep -q "JobRefresher v6.0" README.md; then
    print_success "README contains v6.0 content"
else
    print_warning "README may need v6.0 updates"
fi

# Check CHANGELOG
run_check
if [ -f "CHANGELOG.md" ] && grep -q "\[6.0.0\]" CHANGELOG.md; then
    print_success "CHANGELOG contains v6.0 entry"
else
    print_warning "CHANGELOG may need v6.0 entry"
fi

# Check documentation files
run_check
USER_MANUAL_SIZE=$(wc -l < "docs/USER_MANUAL.md" 2>/dev/null || echo "0")
if [ "$USER_MANUAL_SIZE" -gt 100 ]; then
    print_success "USER_MANUAL.md is comprehensive ($USER_MANUAL_SIZE lines)"
else
    print_warning "USER_MANUAL.md may be incomplete"
fi

run_check
MIGRATION_SIZE=$(wc -l < "docs/MIGRATION_GUIDE.md" 2>/dev/null || echo "0")
if [ "$MIGRATION_SIZE" -gt 100 ]; then
    print_success "MIGRATION_GUIDE.md is comprehensive ($MIGRATION_SIZE lines)"
else
    print_warning "MIGRATION_GUIDE.md may be incomplete"
fi

echo ""

# ========================================
# 9. Git Status
# ========================================

print_status "=== Git Status Validation ==="
echo ""

if command -v git &> /dev/null; then
    run_check
    if git rev-parse --git-dir > /dev/null 2>&1; then
        print_success "Git repository detected"

        # Check for uncommitted changes
        run_check
        if [ -z "$(git status --porcelain)" ]; then
            print_success "No uncommitted changes"
        else
            print_warning "Uncommitted changes detected"
            git status --short
        fi

        # Check current branch
        run_check
        CURRENT_BRANCH=$(git branch --show-current)
        print_success "Current branch: $CURRENT_BRANCH"
    else
        print_warning "Not a git repository"
    fi
else
    print_warning "Git not installed"
fi

echo ""

# ========================================
# 10. Python Version
# ========================================

print_status "=== Python Version Validation ==="
echo ""

run_check
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)

    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        print_success "Python $PYTHON_VERSION (≥3.8 required)"
    else
        print_error "Python $PYTHON_VERSION too old (need 3.8+)"
    fi
else
    print_error "Python 3 not found"
fi

echo ""

# ========================================
# 11. Dependencies
# ========================================

print_status "=== Dependencies Validation ==="
echo ""

# Check if virtual environment exists
run_check
if [ -d "venv" ]; then
    print_success "Virtual environment exists"

    # Check if dependencies are installed (in venv)
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate

        run_check
        if python3 -c "import rich" 2>/dev/null; then
            print_success "Dependency installed: rich"
        else
            print_error "Missing dependency: rich"
        fi

        run_check
        if python3 -c "import prompt_toolkit" 2>/dev/null; then
            print_success "Dependency installed: prompt_toolkit"
        else
            print_error "Missing dependency: prompt_toolkit"
        fi

        run_check
        if python3 -c "import requests" 2>/dev/null; then
            print_success "Dependency installed: requests"
        else
            print_error "Missing dependency: requests"
        fi

        deactivate
    fi
else
    print_warning "Virtual environment not found (run install.sh)"
fi

echo ""

# ========================================
# 12. File Permissions
# ========================================

print_status "=== File Permissions Validation ==="
echo ""

run_check
if [ -w "user_data/jobs" ]; then
    print_success "Job directory writable"
else
    print_error "Job directory not writable"
fi

run_check
if [ -w "user_data/config" ]; then
    print_success "Config directory writable"
else
    print_error "Config directory not writable"
fi

echo ""

# ========================================
# Summary
# ========================================

echo ""
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Validation Summary                  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""
echo "Total Checks:    $TOTAL_CHECKS"
echo -e "${GREEN}Passed:          $PASSED_CHECKS${NC}"
echo -e "${RED}Failed:          $FAILED_CHECKS${NC}"
echo -e "${YELLOW}Warnings:        $WARNING_CHECKS${NC}"
echo ""

# Calculate pass rate
PASS_RATE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
echo "Pass Rate:       $PASS_RATE%"
echo ""

# Determine validation result
if [ $FAILED_CHECKS -eq 0 ]; then
    if [ $WARNING_CHECKS -eq 0 ]; then
        echo -e "${GREEN}✓ VALIDATION PASSED - Ready for release!${NC}"
        EXIT_CODE=0
    else
        echo -e "${YELLOW}⚠ VALIDATION PASSED WITH WARNINGS - Review warnings before release${NC}"
        EXIT_CODE=0
    fi
else
    echo -e "${RED}✗ VALIDATION FAILED - Fix errors before release${NC}"
    EXIT_CODE=1
fi

echo ""
echo "Next steps:"
if [ $FAILED_CHECKS -eq 0 ]; then
    echo "  1. Review RELEASE_CHECKLIST.md"
    echo "  2. Create git tag: git tag v6.0.0"
    echo "  3. Push to repository: git push --tags"
    echo "  4. Create GitHub release"
else
    echo "  1. Fix failed checks above"
    echo "  2. Re-run validation: bash scripts/final_validation.sh"
    echo "  3. Run tests: python3 -m unittest discover tests/ -v"
fi

echo ""

exit $EXIT_CODE
