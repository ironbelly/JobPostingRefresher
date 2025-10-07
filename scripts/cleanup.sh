#!/bin/bash
# Project cleanup script for JobRefresher v6.0
# Removes temporary files, old logs, and build artifacts

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

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   JobRefresher v6.0 Cleanup          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Function: Print status message
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

# Function: Print success message
print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

# Function: Print warning message
print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Function: Get directory size
get_dir_size() {
    if [ -d "$1" ]; then
        du -sh "$1" 2>/dev/null | cut -f1
    else
        echo "0"
    fi
}

# Function: Count files in directory
count_files() {
    if [ -d "$1" ]; then
        find "$1" -type f 2>/dev/null | wc -l
    else
        echo "0"
    fi
}

# Change to project directory
cd "$PROJECT_DIR"

echo "Project directory: $PROJECT_DIR"
echo ""

# Display current disk usage
print_status "Analyzing project disk usage..."
echo ""
echo "Current sizes:"
echo "  user_data/     $(get_dir_size user_data)"
echo "  .pytest_cache/ $(get_dir_size .pytest_cache)"
echo "  __pycache__/   $(get_dir_size clui/__pycache__)"
echo "  .coverage      $(get_dir_size .coverage)"
echo ""

# Ask for confirmation
read -p "Proceed with cleanup? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled"
    exit 0
fi
echo ""

# Cleanup categories
REMOVED_COUNT=0
TOTAL_SIZE_BEFORE=$(du -sb . 2>/dev/null | cut -f1)

# 1. Python cache files
print_status "Removing Python cache files..."
PYCACHE_COUNT=0

# Find and remove __pycache__ directories
while IFS= read -r -d '' dir; do
    rm -rf "$dir"
    ((PYCACHE_COUNT++))
done < <(find . -type d -name "__pycache__" -print0 2>/dev/null)

# Find and remove .pyc files
PYC_COUNT=$(find . -type f -name "*.pyc" 2>/dev/null | wc -l)
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Find and remove .pyo files
PYO_COUNT=$(find . -type f -name "*.pyo" 2>/dev/null | wc -l)
find . -type f -name "*.pyo" -delete 2>/dev/null || true

REMOVED_COUNT=$((REMOVED_COUNT + PYCACHE_COUNT + PYC_COUNT + PYO_COUNT))
print_success "Removed $PYCACHE_COUNT __pycache__ directories, $PYC_COUNT .pyc files, $PYO_COUNT .pyo files"

# 2. Test artifacts
print_status "Removing test artifacts..."
TEST_ARTIFACTS=0

# Remove pytest cache
if [ -d ".pytest_cache" ]; then
    rm -rf .pytest_cache
    ((TEST_ARTIFACTS++))
    print_success "Removed .pytest_cache/"
fi

# Remove coverage files
if [ -f ".coverage" ]; then
    rm -f .coverage
    ((TEST_ARTIFACTS++))
fi

if [ -d "htmlcov" ]; then
    rm -rf htmlcov
    ((TEST_ARTIFACTS++))
fi

if [ -d ".coverage.*" ]; then
    rm -rf .coverage.*
    ((TEST_ARTIFACTS++))
fi

REMOVED_COUNT=$((REMOVED_COUNT + TEST_ARTIFACTS))
if [ $TEST_ARTIFACTS -gt 0 ]; then
    print_success "Removed $TEST_ARTIFACTS test artifact items"
fi

# 3. Temporary files
print_status "Removing temporary files..."
TEMP_COUNT=0

# Remove common temp patterns
find . -type f -name "*.tmp" -delete 2>/dev/null && ((TEMP_COUNT+=1)) || true
find . -type f -name "*.temp" -delete 2>/dev/null && ((TEMP_COUNT+=1)) || true
find . -type f -name "*~" -delete 2>/dev/null && ((TEMP_COUNT+=1)) || true
find . -type f -name ".DS_Store" -delete 2>/dev/null && ((TEMP_COUNT+=1)) || true

# Remove temp directories
if [ -d "tmp" ]; then
    rm -rf tmp
    ((TEMP_COUNT++))
fi

if [ -d "temp" ]; then
    rm -rf temp
    ((TEMP_COUNT++))
fi

REMOVED_COUNT=$((REMOVED_COUNT + TEMP_COUNT))
if [ $TEMP_COUNT -gt 0 ]; then
    print_success "Removed $TEMP_COUNT temporary items"
fi

# 4. Build artifacts
print_status "Removing build artifacts..."
BUILD_COUNT=0

if [ -d "build" ]; then
    rm -rf build
    ((BUILD_COUNT++))
fi

if [ -d "dist" ]; then
    rm -rf dist
    ((BUILD_COUNT++))
fi

if [ -d "*.egg-info" ]; then
    rm -rf *.egg-info
    ((BUILD_COUNT++))
fi

REMOVED_COUNT=$((REMOVED_COUNT + BUILD_COUNT))
if [ $BUILD_COUNT -gt 0 ]; then
    print_success "Removed $BUILD_COUNT build artifact items"
fi

# 5. Log files (optional)
print_status "Checking log files..."
LOG_SIZE=$(get_dir_size user_data/logs 2>/dev/null)
LOG_COUNT=$(count_files user_data/logs 2>/dev/null)

if [ -d "user_data/logs" ] && [ "$LOG_COUNT" -gt 0 ]; then
    print_warning "Found $LOG_COUNT log files ($LOG_SIZE)"
    read -p "Remove old log files? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Keep only last 7 days of logs
        find user_data/logs -type f -mtime +7 -delete 2>/dev/null || true
        NEW_LOG_COUNT=$(count_files user_data/logs 2>/dev/null)
        DELETED_LOGS=$((LOG_COUNT - NEW_LOG_COUNT))
        print_success "Removed $DELETED_LOGS old log files (kept last 7 days)"
        REMOVED_COUNT=$((REMOVED_COUNT + DELETED_LOGS))
    fi
fi

# 6. Old exports (optional)
print_status "Checking export files..."
EXPORT_COUNT=0

if [ -d "user_data/jobs" ]; then
    # Count all export files
    EXPORT_COUNT=$(find user_data/jobs -type d -name "exports" -exec find {} -type f \; 2>/dev/null | wc -l)

    if [ "$EXPORT_COUNT" -gt 0 ]; then
        print_warning "Found $EXPORT_COUNT export files"
        read -p "Remove old exports (>30 days)? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Remove exports older than 30 days
            find user_data/jobs -type d -name "exports" -exec find {} -type f -mtime +30 -delete \; 2>/dev/null || true
            NEW_EXPORT_COUNT=$(find user_data/jobs -type d -name "exports" -exec find {} -type f \; 2>/dev/null | wc -l)
            DELETED_EXPORTS=$((EXPORT_COUNT - NEW_EXPORT_COUNT))
            print_success "Removed $DELETED_EXPORTS old export files"
            REMOVED_COUNT=$((REMOVED_COUNT + DELETED_EXPORTS))
        fi
    fi
fi

# 7. Empty directories
print_status "Removing empty directories..."
EMPTY_DIRS=$(find . -type d -empty 2>/dev/null | wc -l)

if [ "$EMPTY_DIRS" -gt 0 ]; then
    find . -type d -empty -delete 2>/dev/null || true
    print_success "Removed $EMPTY_DIRS empty directories"
    REMOVED_COUNT=$((REMOVED_COUNT + EMPTY_DIRS))
fi

# Calculate space saved
TOTAL_SIZE_AFTER=$(du -sb . 2>/dev/null | cut -f1)
SPACE_SAVED=$((TOTAL_SIZE_BEFORE - TOTAL_SIZE_AFTER))
SPACE_SAVED_MB=$((SPACE_SAVED / 1024 / 1024))

# Summary
echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Cleanup Complete!                   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "Summary:"
echo "  Items removed:  $REMOVED_COUNT"
echo "  Space saved:    ${SPACE_SAVED_MB}MB"
echo ""
echo "Updated sizes:"
echo "  user_data/     $(get_dir_size user_data)"
echo "  Total project: $(get_dir_size .)"
echo ""

# Verify critical files still exist
print_status "Verifying project integrity..."

CRITICAL_MISSING=0

# Check critical directories
for dir in "clui" "IBJobRefresher" "tests" "docs"; do
    if [ ! -d "$dir" ]; then
        print_warning "Critical directory missing: $dir"
        ((CRITICAL_MISSING++))
    fi
done

# Check critical files
for file in "README.md" "CHANGELOG.md" "install.sh"; do
    if [ ! -f "$file" ]; then
        print_warning "Critical file missing: $file"
        ((CRITICAL_MISSING++))
    fi
done

if [ $CRITICAL_MISSING -eq 0 ]; then
    print_success "Project integrity verified"
else
    print_warning "$CRITICAL_MISSING critical items missing - project may be damaged"
fi

echo ""
echo "Next steps:"
echo "  - Run tests: python3 -m unittest discover tests/ -v"
echo "  - Verify v5.1: bash scripts/check_v5_preservation.sh"
echo "  - Launch app: python3 -m clui"
echo ""

exit 0
