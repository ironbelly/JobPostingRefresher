#!/bin/bash
# CI/CD test runner for v6.0
# Run this before any commit or deployment

set -e  # Exit on error

echo "======================================"
echo "JobRefresher v6.0 CI/CD Test Runner"
echo "======================================"

# 1. Check Python environment
echo "Checking Python environment..."
python3 --version

# 2. CRITICAL: v5.1 Preservation Check
echo ""
echo "CRITICAL: Checking v5.1 preservation..."
bash scripts/check_v5_preservation.sh
if [ $? -ne 0 ]; then
    echo "❌ CRITICAL FAILURE: v5.1 has been modified!"
    exit 1
fi
echo "✅ v5.1 preserved"

# 3. Run unit tests
echo ""
echo "Running unit tests..."
python3 -m unittest tests.unit.test_job_manager -v
python3 -m unittest tests.unit.test_teamtailor_client -v
python3 -m unittest tests.unit.test_pd_smis_engine -v
python3 -m unittest tests.unit.test_clui_core -v

# 4. Run preservation tests
echo ""
echo "Running preservation tests..."
python3 -m unittest tests.test_v5_preservation_final -v

# 5. Run integration tests
echo ""
echo "Running integration tests..."
python3 -m unittest tests.test_integration_complete -v

# 6. Run regression tests
echo ""
echo "Running regression tests..."
python3 -m unittest tests.test_regression -v

# 7. Run performance tests
echo ""
echo "Running performance tests..."
python3 -m unittest tests.test_performance -v

echo ""
echo "======================================"
echo "✅ CI/CD Tests Complete"
echo "======================================"
