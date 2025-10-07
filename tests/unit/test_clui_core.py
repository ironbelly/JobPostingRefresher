"""
Unit tests for CLUI Core
Tests interactive interface components
"""

import os
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from clui.jbr import JobRefresherCLUI


class TestCLUICore(unittest.TestCase):
    """Test suite for CLUI core functionality"""

    def setUp(self):
        """Initialize CLUI instance"""
        self.clui = JobRefresherCLUI()

    def test_initialization(self):
        """Test CLUI initialization"""
        self.assertIsNotNone(self.clui)
        self.assertIsNotNone(self.clui.job_manager)
        self.assertIsNotNone(self.clui.teamtailor_client)
        self.assertIsNotNone(self.clui.pd_smis_engine)
        self.assertEqual(self.clui.breadcrumbs, ["Main Menu"])
        self.assertTrue(self.clui.running)

    def test_breadcrumbs_initial_state(self):
        """Test initial breadcrumb state"""
        self.assertEqual(len(self.clui.breadcrumbs), 1)
        self.assertEqual(self.clui.breadcrumbs[0], "Main Menu")

    def test_breadcrumbs_navigation(self):
        """Test breadcrumb navigation tracking"""
        self.clui.breadcrumbs = ["Main Menu", "Job Management"]
        self.assertEqual(len(self.clui.breadcrumbs), 2)
        self.assertEqual(self.clui.breadcrumbs[-1], "Job Management")

    def test_show_message_without_rich(self):
        """Test message display without Rich library"""
        # Temporarily disable Rich
        original_console = self.clui.console
        self.clui.console = None

        # Test various message styles
        try:
            self.clui.show_message("Test message", "success")
            self.clui.show_message("Test error", "error")
            self.clui.show_message("Test warning", "warning")
            self.clui.show_message("Test info", "info")
        except Exception as e:
            self.fail(f"show_message raised exception: {e}")
        finally:
            self.clui.console = original_console

    @patch('builtins.input', return_value='test input')
    def test_get_input_basic(self, mock_input):
        """Test basic input retrieval"""
        # Without Rich
        original_console = self.clui.console
        self.clui.console = None

        result = self.clui.get_input("Test prompt")
        self.assertEqual(result, "test input")

        self.clui.console = original_console

    @patch('builtins.input', return_value='')
    def test_get_input_with_default(self, mock_input):
        """Test input with default value"""
        original_console = self.clui.console
        self.clui.console = None

        result = self.clui.get_input("Test prompt", default="default_value")
        self.assertEqual(result, "default_value")

        self.clui.console = original_console

    @patch('builtins.input', return_value='y')
    def test_get_confirmation_yes(self, mock_input):
        """Test confirmation with yes response"""
        original_console = self.clui.console
        self.clui.console = None

        result = self.clui.get_confirmation("Confirm?")
        self.assertTrue(result)

        self.clui.console = original_console

    @patch('builtins.input', return_value='n')
    def test_get_confirmation_no(self, mock_input):
        """Test confirmation with no response"""
        original_console = self.clui.console
        self.clui.console = None

        result = self.clui.get_confirmation("Confirm?")
        self.assertFalse(result)

        self.clui.console = original_console

    @patch('builtins.input', return_value='')
    def test_get_confirmation_default(self, mock_input):
        """Test confirmation with default value"""
        original_console = self.clui.console
        self.clui.console = None

        # Default True
        result = self.clui.get_confirmation("Confirm?", default=True)
        self.assertTrue(result)

        # Default False
        result = self.clui.get_confirmation("Confirm?", default=False)
        self.assertFalse(result)

        self.clui.console = original_console

    def test_display_menu_without_rich(self):
        """Test menu display without Rich library"""
        original_console = self.clui.console
        self.clui.console = None

        options = [
            ("1", "Option One"),
            ("2", "Option Two"),
            ("q", "Quit")
        ]

        try:
            self.clui.display_menu("Test Menu", options)
        except Exception as e:
            self.fail(f"display_menu raised exception: {e}")
        finally:
            self.clui.console = original_console

    def test_components_accessible(self):
        """Test that all major components are accessible"""
        # Job Manager
        self.assertTrue(hasattr(self.clui.job_manager, 'create_job'))
        self.assertTrue(hasattr(self.clui.job_manager, 'list_jobs'))
        self.assertTrue(hasattr(self.clui.job_manager, 'get_job_data'))

        # TeamTailor Client
        self.assertTrue(hasattr(self.clui.teamtailor_client, 'get_status'))
        self.assertTrue(hasattr(self.clui.teamtailor_client, 'fetch_job'))

        # PD-SMIS Engine
        self.assertTrue(hasattr(self.clui.pd_smis_engine, 'process_job'))
        self.assertTrue(hasattr(self.clui.pd_smis_engine, 'get_engine_info'))

    def test_component_integration(self):
        """Test that components work together"""
        import tempfile
        import shutil

        # Create temporary directory for job manager
        temp_dir = tempfile.mkdtemp()

        try:
            from clui.job_manager import JobManager
            test_job_manager = JobManager(base_path=temp_dir)

            # Create a job
            result = test_job_manager.create_job(
                "test_001",
                "Test Job",
                "TestCo",
                "Test content"
            )

            self.assertTrue(result["success"])

            # Process it through engine
            job_data = test_job_manager.get_job_data("test_001")
            engine_result = self.clui.pd_smis_engine.process_job({
                "job_id": "test_001",
                "title": job_data["metadata"]["title"],
                "company": job_data["metadata"]["company"],
                "raw_content": job_data["raw_content"]
            })

            self.assertTrue(engine_result["success"])

        finally:
            shutil.rmtree(temp_dir)

    def test_clear_screen(self):
        """Test clear screen functionality"""
        try:
            self.clui.clear_screen()
        except Exception as e:
            self.fail(f"clear_screen raised exception: {e}")

    def test_display_header(self):
        """Test header display"""
        try:
            self.clui.display_header()
        except Exception as e:
            self.fail(f"display_header raised exception: {e}")

    def test_display_breadcrumbs(self):
        """Test breadcrumb display"""
        self.clui.breadcrumbs = ["Main Menu", "Job Management", "Create Job"]

        try:
            self.clui.display_breadcrumbs()
        except Exception as e:
            self.fail(f"display_breadcrumbs raised exception: {e}")


class TestCLUIWithoutRich(unittest.TestCase):
    """Test CLUI functionality when Rich library is not available"""

    @patch('clui.jbr.RICH_AVAILABLE', False)
    def test_initialization_without_rich(self):
        """Test CLUI works without Rich library"""
        clui = JobRefresherCLUI()
        self.assertIsNone(clui.console)
        self.assertIsNotNone(clui.job_manager)

    @patch('clui.jbr.RICH_AVAILABLE', False)
    def test_all_display_methods_without_rich(self):
        """Test all display methods work without Rich"""
        clui = JobRefresherCLUI()

        try:
            clui.display_header()
            clui.display_breadcrumbs()
            clui.display_menu("Test", [("1", "Option")])
            clui.show_message("Test", "success")
        except Exception as e:
            self.fail(f"Display methods raised exception without Rich: {e}")


if __name__ == '__main__':
    unittest.main()
