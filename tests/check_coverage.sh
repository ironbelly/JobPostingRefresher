#!/bin/bash
# Test coverage checker

echo "======================================"
echo "Test Coverage Analysis"
echo "======================================"

# Check if coverage is installed
if ! python3 -m coverage --version > /dev/null 2>&1; then
    echo "Installing coverage..."
    pip3 install coverage > /dev/null 2>&1
fi

# Run coverage on all tests
echo "Running tests with coverage..."
python3 -m coverage run -m unittest discover tests/ -v

# Generate report
echo ""
echo "Coverage Report:"
echo "======================================"
python3 -m coverage report --include="clui/*" -m

# Generate HTML report
python3 -m coverage html --include="clui/*"

echo ""
echo "======================================"
echo "HTML report generated in htmlcov/index.html"
echo "======================================"
