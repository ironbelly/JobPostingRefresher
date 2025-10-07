#!/bin/bash
# v5.1 PD-SMIS Engine Preservation Check
# This script verifies that no files in IBJobRefresher/ have been modified

echo "=================================="
echo "v5.1 PD-SMIS Preservation Check"
echo "=================================="
echo ""

# Check if baseline exists
if [ ! -f "dev/v6/v5_baseline_checksums.txt" ]; then
    echo "❌ ERROR: Baseline checksums file not found!"
    echo "   Expected: dev/v6/v5_baseline_checksums.txt"
    exit 1
fi

# Run checksum verification
echo "Checking v5.1 PD-SMIS engine preservation..."
echo ""

RESULT=$(md5sum -c dev/v6/v5_baseline_checksums.txt 2>&1)
FAILED=$(echo "$RESULT" | grep -i "failed")

if [ -n "$FAILED" ]; then
    echo "❌ v5.1 FILES MODIFIED!"
    echo ""
    echo "The following v5.1 files have been changed:"
    echo "$FAILED"
    echo ""
    echo "CRITICAL: v5.1 PD-SMIS engine must remain unchanged!"
    echo "Please restore the modified files immediately."
    exit 1
else
    echo "✅ v5.1 files intact - All checksums match!"
    echo ""
    FILE_COUNT=$(wc -l < dev/v6/v5_baseline_checksums.txt)
    echo "Verified $FILE_COUNT files in IBJobRefresher/"
    exit 0
fi
