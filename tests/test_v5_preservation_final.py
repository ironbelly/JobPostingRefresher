"""
CRITICAL: Final v5.1 preservation verification
This test MUST pass or the entire v6.0 is invalid
Run with: python3 -m unittest tests.test_v5_preservation_final -v
"""
import unittest
import hashlib
from pathlib import Path
import subprocess
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestV5PreservationFinal(unittest.TestCase):
    """Final comprehensive v5.1 preservation tests"""

    def test_no_modifications_to_ibjobrefresher(self):
        """CRITICAL: Verify zero modifications to IBJobRefresher directory"""
        # Check git status for any changes
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'IBJobRefresher/'],
            capture_output=True,
            text=True
        )

        modified_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        assert len(modified_files) == 0, f"CRITICAL: v5.1 files modified: {modified_files}"

    def test_all_critical_files_present(self):
        """Verify all critical v5.1 files exist"""
        critical_files = [
            "IBJobRefresher/orchestrator.md",
            "IBJobRefresher/phases/phase_0_collection.md",
            "IBJobRefresher/phases/phase_0_5_iteration.md",
            "IBJobRefresher/phases/phase_0_6_error_handling.md",
            "IBJobRefresher/phases/phase_1_extraction.md",
            "IBJobRefresher/phases/phase_2_hypothesis.md",
            "IBJobRefresher/phases/phase_3_optimization.md",
            "IBJobRefresher/phases/phase_4_generation.md",
            "IBJobRefresher/phases/phase_6_learning.md",
            "IBJobRefresher/phases/phase_7_iteration.md",
            "IBJobRefresher/validation/adversarial_validation.md",
            "IBJobRefresher/validation/precision_tiers.md",
            "IBJobRefresher/validation/validation_orchestrator.md",
            "IBJobRefresher/validation/verification_suite.md",
            "IBJobRefresher/safeguards/critical_safeguards.md",
            "IBJobRefresher/components/output_format.md"
        ]

        for file_path in critical_files:
            assert Path(file_path).exists(), f"Critical file missing: {file_path}"

    def test_checksum_verification(self):
        """Verify checksums match baseline"""
        baseline_file = Path("dev/v6/v5_baseline_checksums.txt")

        if not baseline_file.exists():
            self.skipTest("No baseline checksums found (run M1 first)")

        # Read baseline
        baseline = {}
        with open(baseline_file, 'r') as f:
            for line in f:
                if line.strip() and 'IBJobRefresher' in line:
                    parts = line.strip().split('  ')
                    if len(parts) == 2:
                        checksum, filepath = parts
                        baseline[filepath] = checksum

        # Verify each file
        for filepath, expected_checksum in baseline.items():
            if Path(filepath).exists():
                with open(filepath, 'rb') as f:
                    actual_checksum = hashlib.md5(f.read()).hexdigest()
                assert actual_checksum == expected_checksum, \
                    f"Checksum mismatch for {filepath}"

    def test_wrapper_doesnt_import_from_engine(self):
        """Verify wrapper doesn't import from IBJobRefresher"""
        wrapper_file = Path("clui/pd_smis_engine.py")

        if wrapper_file.exists():
            content = wrapper_file.read_text()

            # Check for actual import statements, not comments/docstrings
            import_lines = [line.strip() for line in content.split('\n')
                           if line.strip().startswith(('import ', 'from '))
                           and not line.strip().startswith('#')]

            # Filter out docstring content
            actual_imports = [line for line in import_lines
                             if not line.startswith('"""') and not line.startswith("'''")]

            # Should NOT contain any imports from IBJobRefresher
            ibjob_imports = [line for line in actual_imports
                            if 'IBJobRefresher' in line]

            assert len(ibjob_imports) == 0, \
                f"Found IBJobRefresher imports: {ibjob_imports}"
            print("✅ Wrapper correctly isolated from engine")

    def test_phase_sequence_preserved(self):
        """Verify phase execution sequence matches v5.1"""
        from clui.pd_smis_engine import PDSMISEngine

        engine = PDSMISEngine()
        phases = engine.get_phase_sequence()

        # Should have 9 phases as documented in v5.1
        assert len(phases) == 9, f"Expected 9 phases, got {len(phases)}"

        # Check for key phases
        assert "phase_0_collection" in phases
        assert "phase_1_extraction" in phases
        assert "phase_2_hypothesis" in phases
        assert "phase_3_optimization" in phases
        assert "phase_4_generation" in phases


if __name__ == "__main__":
    unittest.main()
