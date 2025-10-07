#!/usr/bin/env python3
"""
JobRefresher CLUI (Command Line User Interface)
Interactive menu-driven interface for v6.0

Usage: python3 -m clui.jbr
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

# Try to import Rich library
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.layout import Layout
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  Warning: 'rich' library not available. Using basic text interface.")
    print("   Install with: pip install rich")

# Import our components
from clui.job_manager import JobManager
from clui.teamtailor_client import TeamTailorClient
from clui.pd_smis_engine import PDSMISEngine


class JobRefresherCLUI:
    """
    Interactive CLUI for JobRefresher v6.0

    Features:
    - Menu-driven navigation
    - Job management operations
    - Job processing with PD-SMIS engine
    - TeamTailor integration
    - Rich terminal UI (when available)
    """

    def __init__(self):
        """Initialize CLUI with components"""
        self.console = Console() if RICH_AVAILABLE else None
        self.job_manager = JobManager()
        self.teamtailor_client = TeamTailorClient()
        self.pd_smis_engine = PDSMISEngine()
        self.breadcrumbs = ["Main Menu"]
        self.running = True

        # Session statistics
        self.session_stats = {
            "jobs_created": 0,
            "jobs_processed": 0,
            "jobs_exported": 0,
            "jobs_imported": 0,
            "start_time": None
        }

        import datetime
        self.session_stats["start_time"] = datetime.datetime.now()

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')

    def display_header(self):
        """Display application header"""
        if RICH_AVAILABLE:
            header = Panel(
                "[bold cyan]JobRefresher v6.0[/bold cyan]\n"
                "[dim]PD-SMIS Engine Wrapper with Multi-Job Management[/dim]",
                box=box.DOUBLE,
                border_style="cyan"
            )
            self.console.print(header)
        else:
            print("\n" + "="*60)
            print("       JobRefresher v6.0")
            print("  PD-SMIS Engine Wrapper with Multi-Job Management")
            print("="*60)

    def display_breadcrumbs(self):
        """Display navigation breadcrumbs"""
        if RICH_AVAILABLE:
            breadcrumb_text = " > ".join(self.breadcrumbs)
            self.console.print(f"[dim]{breadcrumb_text}[/dim]\n")
        else:
            print(" > ".join(self.breadcrumbs))

    def display_menu(self, title: str, options: List[tuple]):
        """
        Display menu with options

        Args:
            title: Menu title
            options: List of (key, description) tuples
        """
        if RICH_AVAILABLE:
            self.console.print(f"\n[bold]{title}[/bold]\n")

            table = Table(show_header=False, box=box.SIMPLE)
            table.add_column("Key", style="cyan", width=6)
            table.add_column("Option", style="white")

            for key, description in options:
                table.add_row(f"[{key}]", description)

            self.console.print(table)
        else:
            print(f"\n{title}")
            print("-" * len(title))
            for key, description in options:
                print(f"  [{key}] {description}")

    def get_input(self, prompt: str, default: Optional[str] = None) -> str:
        """
        Get user input with prompt

        Args:
            prompt: Input prompt
            default: Default value

        Returns:
            User input string
        """
        if RICH_AVAILABLE:
            return Prompt.ask(prompt, default=default or "")
        else:
            if default:
                return input(f"{prompt} [{default}]: ") or default
            return input(f"{prompt}: ")

    def get_confirmation(self, prompt: str, default: bool = False) -> bool:
        """
        Get yes/no confirmation

        Args:
            prompt: Confirmation prompt
            default: Default value

        Returns:
            Boolean confirmation
        """
        if RICH_AVAILABLE:
            return Confirm.ask(prompt, default=default)
        else:
            default_str = "Y/n" if default else "y/N"
            response = input(f"{prompt} [{default_str}]: ").lower()
            if not response:
                return default
            return response in ['y', 'yes']

    def show_message(self, message: str, style: str = "white"):
        """
        Display a message to user

        Args:
            message: Message to display
            style: Message style (success, error, warning, info)
        """
        if RICH_AVAILABLE:
            style_map = {
                "success": "green",
                "error": "red",
                "warning": "yellow",
                "info": "cyan"
            }
            self.console.print(f"[{style_map.get(style, 'white')}]{message}[/{style_map.get(style, 'white')}]")
        else:
            prefix_map = {
                "success": "✅",
                "error": "❌",
                "warning": "⚠️",
                "info": "ℹ️"
            }
            prefix = prefix_map.get(style, "")
            print(f"{prefix} {message}")

    def pause(self):
        """Pause and wait for user input"""
        input("\nPress Enter to continue...")

    # ==================== Main Menu ====================

    def main_menu(self):
        """Display and handle main menu"""
        while self.running:
            self.clear_screen()
            self.display_header()
            self.breadcrumbs = ["Main Menu"]
            self.display_breadcrumbs()

            options = [
                ("1", "Job Management"),
                ("2", "Job Processing"),
                ("3", "TeamTailor Integration"),
                ("4", "System Status"),
                ("5", "Settings"),
                ("q", "Quit")
            ]

            self.display_menu("Main Menu", options)

            choice = self.get_input("\nSelect option").lower()

            if choice == "1":
                self.job_management_menu()
            elif choice == "2":
                self.job_processing_menu()
            elif choice == "3":
                self.teamtailor_menu()
            elif choice == "4":
                self.system_status()
            elif choice == "5":
                self.settings_menu()
            elif choice == "q":
                if self.get_confirmation("Are you sure you want to quit?"):
                    self.running = False
            else:
                self.show_message("Invalid option. Please try again.", "error")
                self.pause()

    # ==================== Job Management ====================

    def job_management_menu(self):
        """Job management submenu"""
        while True:
            self.clear_screen()
            self.display_header()
            self.breadcrumbs = ["Main Menu", "Job Management"]
            self.display_breadcrumbs()

            options = [
                ("1", "Create New Job"),
                ("2", "View All Jobs"),
                ("3", "View Job Details"),
                ("4", "Search Jobs"),
                ("5", "Delete Job"),
                ("b", "Back to Main Menu")
            ]

            self.display_menu("Job Management", options)

            choice = self.get_input("\nSelect option").lower()

            if choice == "1":
                self.create_job()
            elif choice == "2":
                self.view_all_jobs()
            elif choice == "3":
                self.view_job_details()
            elif choice == "4":
                self.search_jobs()
            elif choice == "5":
                self.delete_job()
            elif choice == "b":
                break
            else:
                self.show_message("Invalid option. Please try again.", "error")
                self.pause()

    def create_job(self):
        """Create a new job posting"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "Job Management", "Create Job"]
        self.display_breadcrumbs()

        self.show_message("\n=== Create New Job ===\n", "info")

        # Get job details
        job_id = self.get_input("Job ID (unique identifier)")
        if not job_id:
            self.show_message("Job ID is required", "error")
            self.pause()
            return

        title = self.get_input("Job Title")
        company = self.get_input("Company Name")

        self.show_message("\nEnter job description (end with empty line):", "info")
        raw_data_lines = []
        while True:
            line = input()
            if not line:
                break
            raw_data_lines.append(line)

        raw_data = "\n".join(raw_data_lines)

        # Optional metadata
        tags_input = self.get_input("Tags (comma-separated, optional)", "")
        tags = [t.strip() for t in tags_input.split(",")] if tags_input else []

        notes = self.get_input("Notes (optional)", "")

        # Create job
        metadata = {
            "tags": tags,
            "notes": notes,
            "source": "manual"
        }

        result = self.job_manager.create_job(job_id, title, company, raw_data, metadata)

        if result["success"]:
            self.session_stats["jobs_created"] += 1
            self.show_message(f"\n✅ Job '{job_id}' created successfully!", "success")
        else:
            self.show_message(f"\n❌ Error: {result['error']}", "error")

        self.pause()

    def view_all_jobs(self):
        """View all jobs in the system"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "Job Management", "View All Jobs"]
        self.display_breadcrumbs()

        jobs = self.job_manager.list_jobs()

        if not jobs:
            self.show_message("\nNo jobs found in the system.", "info")
            self.pause()
            return

        if RICH_AVAILABLE:
            table = Table(title=f"All Jobs ({len(jobs)} total)", box=box.ROUNDED)
            table.add_column("Job ID", style="cyan")
            table.add_column("Title", style="white")
            table.add_column("Company", style="yellow")
            table.add_column("Status", style="green")
            table.add_column("Created", style="dim")

            for job in jobs:
                created = job.get("created_at", "")[:10]  # Just the date
                table.add_row(
                    job.get("job_id", ""),
                    job.get("title", "")[:40],
                    job.get("company", ""),
                    job.get("status", ""),
                    created
                )

            self.console.print(table)
        else:
            print(f"\nAll Jobs ({len(jobs)} total):")
            print("-" * 80)
            for i, job in enumerate(jobs, 1):
                print(f"{i}. [{job.get('job_id', '')}] {job.get('title', '')} - {job.get('company', '')}")
                print(f"   Status: {job.get('status', '')} | Created: {job.get('created_at', '')[:10]}")

        self.pause()

    def view_job_details(self):
        """View detailed information about a specific job"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "Job Management", "Job Details"]
        self.display_breadcrumbs()

        job_id = self.get_input("\nEnter Job ID")

        if not job_id:
            self.show_message("Job ID is required", "error")
            self.pause()
            return

        job_data = self.job_manager.get_job_data(job_id)

        if not job_data["success"]:
            self.show_message(f"Error: {job_data['error']}", "error")
            self.pause()
            return

        # Display job details
        metadata = job_data["metadata"]

        if RICH_AVAILABLE:
            # Create info panel
            info_text = f"""[bold]Job ID:[/bold] {metadata.get('job_id', '')}
[bold]Title:[/bold] {metadata.get('title', '')}
[bold]Company:[/bold] {metadata.get('company', '')}
[bold]Status:[/bold] {metadata.get('status', '')}
[bold]Created:[/bold] {metadata.get('created_at', '')}
[bold]Updated:[/bold] {metadata.get('updated_at', '')}
[bold]Tags:[/bold] {', '.join(metadata.get('tags', []))}
[bold]Versions:[/bold] {len(metadata.get('versions', []))}"""

            panel = Panel(info_text, title="Job Details", border_style="cyan")
            self.console.print(panel)

            # Display raw content preview
            raw_preview = job_data.get("raw_content", "")[:200]
            self.console.print(f"\n[bold]Raw Content Preview:[/bold]")
            self.console.print(f"[dim]{raw_preview}...[/dim]")
        else:
            print("\n=== Job Details ===")
            print(f"Job ID: {metadata.get('job_id', '')}")
            print(f"Title: {metadata.get('title', '')}")
            print(f"Company: {metadata.get('company', '')}")
            print(f"Status: {metadata.get('status', '')}")
            print(f"Created: {metadata.get('created_at', '')}")
            print(f"Tags: {', '.join(metadata.get('tags', []))}")
            print(f"\nRaw Content Preview:")
            print(job_data.get("raw_content", "")[:200] + "...")

        self.pause()

    def search_jobs(self):
        """Search jobs by filters"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "Job Management", "Search Jobs"]
        self.display_breadcrumbs()

        self.show_message("\n=== Search Jobs ===\n", "info")

        # Get search filters
        status = self.get_input("Filter by status (raw/processed/all)", "all")
        company = self.get_input("Filter by company (leave empty for all)", "")
        tags_input = self.get_input("Filter by tags (comma-separated)", "")

        # Build filter
        filter_by = {}
        if status != "all":
            filter_by["status"] = status
        if company:
            filter_by["company"] = company
        if tags_input:
            filter_by["tags"] = [t.strip() for t in tags_input.split(",")]

        # Search
        jobs = self.job_manager.list_jobs(filter_by if filter_by else None)

        self.show_message(f"\nFound {len(jobs)} job(s)", "info")

        if jobs:
            for i, job in enumerate(jobs, 1):
                print(f"{i}. [{job.get('job_id')}] {job.get('title')} - {job.get('company')}")

        self.pause()

    def delete_job(self):
        """Delete a job"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "Job Management", "Delete Job"]
        self.display_breadcrumbs()

        job_id = self.get_input("\nEnter Job ID to delete")

        if not job_id:
            self.show_message("Job ID is required", "error")
            self.pause()
            return

        # Confirm deletion
        if not self.get_confirmation(f"Are you sure you want to delete job '{job_id}'? This cannot be undone."):
            self.show_message("Deletion cancelled", "info")
            self.pause()
            return

        result = self.job_manager.delete_job(job_id, confirm=True)

        if result["success"]:
            self.show_message(f"✅ Job '{job_id}' deleted successfully", "success")
        else:
            self.show_message(f"❌ Error: {result['error']}", "error")

        self.pause()

    # ==================== Job Processing ====================

    def job_processing_menu(self):
        """Job processing submenu"""
        while True:
            self.clear_screen()
            self.display_header()
            self.breadcrumbs = ["Main Menu", "Job Processing"]
            self.display_breadcrumbs()

            options = [
                ("1", "Process Single Job"),
                ("2", "Batch Process Jobs"),
                ("3", "View Processing Results"),
                ("4", "Compare Job Versions"),
                ("5", "Performance Dashboard"),
                ("6", "Export Job"),
                ("b", "Back to Main Menu")
            ]

            self.display_menu("Job Processing", options)

            choice = self.get_input("\nSelect option").lower()

            if choice == "1":
                self.process_single_job()
            elif choice == "2":
                self.batch_process_jobs()
            elif choice == "3":
                self.view_processing_results()
            elif choice == "4":
                self.compare_versions_menu()
            elif choice == "5":
                self.performance_dashboard()
            elif choice == "6":
                self.export_job()
            elif choice == "b":
                break
            else:
                self.show_message("Invalid option. Please try again.", "error")
                self.pause()

    def process_single_job(self):
        """Process a single job through PD-SMIS engine"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "Job Processing", "Process Job"]
        self.display_breadcrumbs()

        job_id = self.get_input("\nEnter Job ID to process")

        if not job_id:
            self.show_message("Job ID is required", "error")
            self.pause()
            return

        # Get job data
        job_data = self.job_manager.get_job_data(job_id)

        if not job_data["success"]:
            self.show_message(f"Error: {job_data['error']}", "error")
            self.pause()
            return

        self.show_message(f"\n🔄 Processing job '{job_id}' through PD-SMIS engine...", "info")

        # Process through engine
        try:
            result = self.pd_smis_engine.process_job({
                "job_id": job_id,
                "title": job_data["metadata"]["title"],
                "company": job_data["metadata"]["company"],
                "raw_content": job_data["raw_content"]
            })

            if result["success"]:
                # Save processed data
                self.job_manager.save_processed_job(job_id, result, create_version=True)

                # Update session stats
                self.session_stats["jobs_processed"] += 1

                self.show_message("\n✅ Job processed successfully!", "success")
                self.show_message(f"Overall Quality Score: {result['metrics']['overall_quality']:.2f}", "info")
                self.show_message(f"Precision Score: {result['metrics']['precision_score']:.2f}", "info")
                self.show_message(f"Iterations: {result['iterations']}", "info")
            else:
                self.show_message(f"\n❌ Processing failed: {result.get('error', 'Unknown error')}", "error")

        except Exception as e:
            self.show_message(f"\n❌ Error during processing: {str(e)}", "error")

        self.pause()

    def batch_process_jobs(self):
        """Process multiple jobs in batch"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "Job Processing", "Batch Process"]
        self.display_breadcrumbs()

        self.show_message("\n=== Batch Process Jobs ===\n", "info")

        # Get filter criteria
        status = self.get_input("Filter by status (raw/all)", "raw")
        company = self.get_input("Filter by company (leave empty for all)", "")

        # Build filter
        filter_by = {}
        if status != "all":
            filter_by["status"] = status
        if company:
            filter_by["company"] = company

        # Get jobs
        jobs = self.job_manager.list_jobs(filter_by if filter_by else None)

        if not jobs:
            self.show_message("No jobs found matching criteria", "warning")
            self.pause()
            return

        self.show_message(f"\nFound {len(jobs)} job(s) to process", "info")

        if not self.get_confirmation(f"Process all {len(jobs)} job(s)?"):
            self.show_message("Batch processing cancelled", "info")
            self.pause()
            return

        # Process jobs
        self.show_message("\n🔄 Processing jobs...\n", "info")

        processed = 0
        failed = 0

        for i, job in enumerate(jobs, 1):
            job_id = job["job_id"]
            self.show_message(f"[{i}/{len(jobs)}] Processing {job_id}...", "info")

            try:
                # Get full job data
                job_data = self.job_manager.get_job_data(job_id)

                if not job_data["success"]:
                    self.show_message(f"  ❌ Failed to load job: {job_data['error']}", "error")
                    failed += 1
                    continue

                # Process through engine
                result = self.pd_smis_engine.process_job({
                    "job_id": job_id,
                    "title": job_data["metadata"]["title"],
                    "company": job_data["metadata"]["company"],
                    "raw_content": job_data["raw_content"]
                })

                if result["success"]:
                    # Save processed data
                    self.job_manager.save_processed_job(job_id, result, create_version=True)
                    self.show_message(f"  ✅ Completed (Quality: {result['metrics']['overall_quality']:.2f})", "success")
                    processed += 1
                    self.session_stats["jobs_processed"] += 1
                else:
                    self.show_message(f"  ❌ Processing failed", "error")
                    failed += 1

            except Exception as e:
                self.show_message(f"  ❌ Error: {str(e)}", "error")
                failed += 1

        # Summary
        self.show_message(f"\n=== Batch Processing Complete ===", "info")
        self.show_message(f"Processed: {processed}", "success")
        self.show_message(f"Failed: {failed}", "error" if failed > 0 else "info")

        self.pause()

    def compare_versions_menu(self):
        """Compare different versions of a job"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "Job Processing", "Compare Versions"]
        self.display_breadcrumbs()

        job_id = self.get_input("\nEnter Job ID")

        if not job_id:
            self.show_message("Job ID is required", "error")
            self.pause()
            return

        # Get job data
        job_data = self.job_manager.get_job_data(job_id)

        if not job_data["success"]:
            self.show_message(f"Error: {job_data['error']}", "error")
            self.pause()
            return

        versions = job_data["metadata"].get("versions", [])

        if len(versions) < 2:
            self.show_message(f"Job has {len(versions)} version(s). Need at least 2 for comparison.", "warning")
            self.pause()
            return

        self.show_message(f"\nAvailable versions: {', '.join(versions)}", "info")

        # Display version comparison
        if RICH_AVAILABLE:
            from rich.table import Table

            table = Table(title=f"Version Comparison - {job_id}")
            table.add_column("Metric", style="cyan")

            for version_id in versions:
                table.add_column(version_id, style="white")

            # Load all versions
            version_data = {}
            for version_id in versions:
                version_file = Path(f"user_data/jobs/{job_id}/versions/{version_id}.json")
                if version_file.exists():
                    import json
                    with open(version_file, 'r') as f:
                        version_data[version_id] = json.load(f)

            # Compare metrics
            if version_data:
                # Quality scores
                row_data = ["Overall Quality"]
                for version_id in versions:
                    vdata = version_data.get(version_id, {}).get("data", {})
                    metrics = vdata.get("metrics", {})
                    score = metrics.get("overall_quality", 0)
                    row_data.append(f"{score:.2f}")
                table.add_row(*row_data)

                # Precision scores
                row_data = ["Precision Score"]
                for version_id in versions:
                    vdata = version_data.get(version_id, {}).get("data", {})
                    metrics = vdata.get("metrics", {})
                    score = metrics.get("precision_score", 0)
                    row_data.append(f"{score:.2f}")
                table.add_row(*row_data)

                # Iterations
                row_data = ["Iterations"]
                for version_id in versions:
                    vdata = version_data.get(version_id, {}).get("data", {})
                    iterations = vdata.get("iterations", 0)
                    row_data.append(str(iterations))
                table.add_row(*row_data)

            self.console.print(table)
        else:
            print("\n=== Version Comparison ===")
            for version_id in versions:
                print(f"\n{version_id}:")
                version_file = Path(f"user_data/jobs/{job_id}/versions/{version_id}.json")
                if version_file.exists():
                    import json
                    with open(version_file, 'r') as f:
                        vdata = json.load(f)
                        metrics = vdata.get("data", {}).get("metrics", {})
                        print(f"  Quality: {metrics.get('overall_quality', 0):.2f}")
                        print(f"  Precision: {metrics.get('precision_score', 0):.2f}")

        self.pause()

    def performance_dashboard(self):
        """Display performance dashboard with metrics"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "Job Processing", "Performance Dashboard"]
        self.display_breadcrumbs()

        # Get all jobs
        jobs = self.job_manager.list_jobs()

        # Calculate statistics
        total_jobs = len(jobs)
        raw_jobs = len([j for j in jobs if j.get("status") == "raw"])
        processed_jobs = len([j for j in jobs if j.get("status") == "processed"])

        # Get processing metrics
        quality_scores = []
        for job in jobs:
            if job.get("status") == "processed":
                job_data = self.job_manager.get_job_data(job["job_id"])
                if job_data["success"] and job_data.get("latest_version"):
                    metrics = job_data["latest_version"]["data"].get("metrics", {})
                    quality_scores.append(metrics.get("overall_quality", 0))

        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

        # Session statistics
        import datetime
        if self.session_stats["start_time"]:
            session_duration = datetime.datetime.now() - self.session_stats["start_time"]
            session_minutes = int(session_duration.total_seconds() / 60)
        else:
            session_minutes = 0

        if RICH_AVAILABLE:
            from rich.panel import Panel
            from rich.table import Table

            # Metrics table
            table = Table(title="Performance Metrics", box=box.ROUNDED)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="white", justify="right")

            table.add_row("Total Jobs", str(total_jobs))
            table.add_row("Raw Jobs", str(raw_jobs))
            table.add_row("Processed Jobs", str(processed_jobs))
            table.add_row("Average Quality Score", f"{avg_quality:.2f}")
            table.add_row("", "")
            table.add_row("[bold]Session Statistics[/bold]", "")
            table.add_row("Jobs Created", str(self.session_stats["jobs_created"]))
            table.add_row("Jobs Processed", str(self.session_stats["jobs_processed"]))
            table.add_row("Jobs Exported", str(self.session_stats["jobs_exported"]))
            table.add_row("Jobs Imported", str(self.session_stats["jobs_imported"]))
            table.add_row("Session Duration", f"{session_minutes} min")

            self.console.print(table)
        else:
            print("\n=== Performance Dashboard ===")
            print(f"\nTotal Jobs: {total_jobs}")
            print(f"Raw Jobs: {raw_jobs}")
            print(f"Processed Jobs: {processed_jobs}")
            print(f"Average Quality Score: {avg_quality:.2f}")
            print(f"\nSession Statistics:")
            print(f"  Jobs Created: {self.session_stats['jobs_created']}")
            print(f"  Jobs Processed: {self.session_stats['jobs_processed']}")
            print(f"  Jobs Exported: {self.session_stats['jobs_exported']}")
            print(f"  Session Duration: {session_minutes} minutes")

        self.pause()

    def view_processing_results(self):
        """View processing results for a job"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "Job Processing", "View Results"]
        self.display_breadcrumbs()

        job_id = self.get_input("\nEnter Job ID")

        job_data = self.job_manager.get_job_data(job_id)

        if not job_data["success"]:
            self.show_message(f"Error: {job_data['error']}", "error")
            self.pause()
            return

        if not job_data.get("latest_version"):
            self.show_message("No processing results found for this job", "warning")
            self.pause()
            return

        # Display results
        version_data = job_data["latest_version"]["data"]

        self.show_message("\n=== Processing Results ===\n", "info")

        if "metrics" in version_data:
            metrics = version_data["metrics"]
            print(f"Overall Quality: {metrics.get('overall_quality', 0):.2f}")
            print(f"Precision Score: {metrics.get('precision_score', 0):.2f}")
            print(f"Adversarial Score: {metrics.get('adversarial_score', 0):.2f}")
            print(f"Verification Score: {metrics.get('verification_score', 0):.2f}")

        self.pause()

    def export_job(self):
        """Export job in various formats"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "Job Processing", "Export Job"]
        self.display_breadcrumbs()

        job_id = self.get_input("\nEnter Job ID to export")

        if not job_id:
            self.show_message("Job ID is required", "error")
            self.pause()
            return

        # Get format
        format_choice = self.get_input("Export format (json/txt/html/md)", "json").lower()

        if format_choice not in ["json", "txt", "html", "md"]:
            self.show_message("Invalid format", "error")
            self.pause()
            return

        # Export
        result = self.job_manager.export_job(job_id, format=format_choice)

        if result["success"]:
            self.session_stats["jobs_exported"] += 1
            self.show_message(f"\n✅ Job exported successfully!", "success")
            self.show_message(f"File: {result['path']}", "info")
        else:
            self.show_message(f"\n❌ Error: {result['error']}", "error")

        self.pause()

    # ==================== TeamTailor Integration ====================

    def teamtailor_menu(self):
        """TeamTailor integration submenu"""
        while True:
            self.clear_screen()
            self.display_header()
            self.breadcrumbs = ["Main Menu", "TeamTailor Integration"]
            self.display_breadcrumbs()

            # Show status
            status = self.teamtailor_client.get_status()
            status_text = "✅ Connected" if status["available"] else "⚠️  Not Configured"
            self.show_message(f"Status: {status_text}\n", "info" if status["available"] else "warning")

            options = [
                ("1", "Import Job from TeamTailor"),
                ("2", "Sync Metrics from TeamTailor"),
                ("3", "View TeamTailor Status"),
                ("4", "Create Sample Configuration"),
                ("b", "Back to Main Menu")
            ]

            self.display_menu("TeamTailor Integration", options)

            choice = self.get_input("\nSelect option").lower()

            if choice == "1":
                self.import_from_teamtailor()
            elif choice == "2":
                self.sync_metrics()
            elif choice == "3":
                self.view_teamtailor_status()
            elif choice == "4":
                self.create_teamtailor_config()
            elif choice == "b":
                break
            else:
                self.show_message("Invalid option. Please try again.", "error")
                self.pause()

    def import_from_teamtailor(self):
        """Import a job from TeamTailor"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "TeamTailor", "Import Job"]
        self.display_breadcrumbs()

        status = self.teamtailor_client.get_status()
        if not status["available"]:
            self.show_message("TeamTailor API is not available", "error")
            self.show_message(f"Reason: {status['degradation_reason']}", "warning")
            self.pause()
            return

        job_id = self.get_input("\nEnter TeamTailor Job ID")

        result = self.teamtailor_client.import_to_job_manager(job_id, self.job_manager)

        if result["success"]:
            self.session_stats["jobs_imported"] += 1
            self.show_message(f"\n✅ Job imported successfully!", "success")
            self.show_message(f"Local Job ID: {result['local_job_id']}", "info")
        else:
            self.show_message(f"\n❌ Error: {result['error']}", "error")

        self.pause()

    def sync_metrics(self):
        """Sync performance metrics from TeamTailor"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "TeamTailor", "Sync Metrics"]
        self.display_breadcrumbs()

        status = self.teamtailor_client.get_status()
        if not status["available"]:
            self.show_message("TeamTailor API is not available", "error")
            self.show_message(f"Reason: {status['degradation_reason']}", "warning")
            self.pause()
            return

        # Find jobs imported from TeamTailor
        jobs = self.job_manager.list_jobs()
        tt_jobs = [j for j in jobs if j.get("job_id", "").startswith("tt_")]

        if not tt_jobs:
            self.show_message("No TeamTailor jobs found to sync", "warning")
            self.pause()
            return

        self.show_message(f"\nFound {len(tt_jobs)} TeamTailor job(s) to sync", "info")

        if not self.get_confirmation("Sync metrics for all jobs?"):
            self.show_message("Sync cancelled", "info")
            self.pause()
            return

        self.show_message("\n🔄 Syncing metrics...\n", "info")

        synced = 0
        failed = 0

        for job in tt_jobs:
            job_id = job["job_id"]
            # Extract original TeamTailor ID (remove 'tt_' prefix)
            tt_id = job_id[3:]

            self.show_message(f"Syncing {job_id}...", "info")

            try:
                # Fetch metrics from TeamTailor
                metrics_result = self.teamtailor_client.fetch_metrics(tt_id)

                if metrics_result["success"]:
                    # Update job metadata with metrics
                    updates = {
                        "notes": f"Metrics synced: Views={metrics_result.get('views', 0)}, Applications={metrics_result.get('applications', 0)}"
                    }
                    self.job_manager.update_metadata(job_id, updates)
                    self.show_message(f"  ✅ Synced (Views: {metrics_result.get('views', 0)})", "success")
                    synced += 1
                else:
                    self.show_message(f"  ⚠️  Metrics unavailable", "warning")
                    failed += 1

            except Exception as e:
                self.show_message(f"  ❌ Error: {str(e)}", "error")
                failed += 1

        # Summary
        self.show_message(f"\n=== Sync Complete ===", "info")
        self.show_message(f"Synced: {synced}", "success")
        self.show_message(f"Failed: {failed}", "error" if failed > 0 else "info")

        self.pause()

    def view_teamtailor_status(self):
        """View TeamTailor integration status"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "TeamTailor", "Status"]
        self.display_breadcrumbs()

        status = self.teamtailor_client.get_status()

        self.show_message("\n=== TeamTailor Status ===\n", "info")
        print(f"Available: {'Yes' if status['available'] else 'No'}")
        print(f"Degraded Mode: {'Yes' if status['degraded_mode'] else 'No'}")
        print(f"Config Loaded: {'Yes' if status['config_loaded'] else 'No'}")
        print(f"API Key Configured: {'Yes' if status['api_key_configured'] else 'No'}")
        print(f"Company ID Configured: {'Yes' if status['company_id_configured'] else 'No'}")
        print(f"Requests Library: {'Available' if status['requests_library'] else 'Not Available'}")

        if status['degradation_reason']:
            self.show_message(f"\nDegradation Reason: {status['degradation_reason']}", "warning")

        self.pause()

    def create_teamtailor_config(self):
        """Create sample TeamTailor configuration"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "TeamTailor", "Create Config"]
        self.display_breadcrumbs()

        result = self.teamtailor_client.create_sample_config()

        if result["success"]:
            self.show_message(f"\n✅ Sample configuration created!", "success")
            self.show_message(f"File: {result['path']}", "info")
            self.show_message(f"\n{result['message']}", "warning")
        else:
            self.show_message(f"\n❌ Error: {result['error']}", "error")

        self.pause()

    # ==================== System Status ====================

    def system_status(self):
        """Display system status"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "System Status"]
        self.display_breadcrumbs()

        # Get component status
        jobs = self.job_manager.list_jobs()
        tt_status = self.teamtailor_client.get_status()
        engine_info = self.pd_smis_engine.get_engine_info()

        if RICH_AVAILABLE:
            # Create status panel
            status_text = f"""[bold cyan]Component Status[/bold cyan]

[bold]Job Manager:[/bold]
  • Total Jobs: {len(jobs)}
  • Raw: {len([j for j in jobs if j.get('status') == 'raw'])}
  • Processed: {len([j for j in jobs if j.get('status') == 'processed'])}

[bold]TeamTailor Integration:[/bold]
  • Status: {'✅ Available' if tt_status['available'] else '⚠️  Not Configured'}
  • Degraded Mode: {'Yes' if tt_status['degraded_mode'] else 'No'}

[bold]PD-SMIS Engine:[/bold]
  • Version: {engine_info['engine_version']}
  • Wrapper Version: {engine_info['wrapper_version']}
  • Phases: {engine_info['phases_count']}
  • Validation Tiers: {engine_info['validation_tiers_count']}"""

            panel = Panel(status_text, title="System Status", border_style="green")
            self.console.print(panel)
        else:
            print("\n=== System Status ===")
            print(f"\nJob Manager:")
            print(f"  Total Jobs: {len(jobs)}")
            print(f"  Raw: {len([j for j in jobs if j.get('status') == 'raw'])}")
            print(f"  Processed: {len([j for j in jobs if j.get('status') == 'processed'])}")
            print(f"\nTeamTailor: {'Available' if tt_status['available'] else 'Not Configured'}")
            print(f"\nPD-SMIS Engine: v{engine_info['engine_version']} (Wrapper v{engine_info['wrapper_version']})")

        self.pause()

    # ==================== Settings ====================

    def settings_menu(self):
        """Settings submenu"""
        while True:
            self.clear_screen()
            self.display_header()
            self.breadcrumbs = ["Main Menu", "Settings"]
            self.display_breadcrumbs()

            options = [
                ("1", "View Engine Information"),
                ("2", "Run v5.1 Preservation Check"),
                ("b", "Back to Main Menu")
            ]

            self.display_menu("Settings", options)

            choice = self.get_input("\nSelect option").lower()

            if choice == "1":
                self.view_engine_info()
            elif choice == "2":
                self.run_preservation_check()
            elif choice == "b":
                break
            else:
                self.show_message("Invalid option. Please try again.", "error")
                self.pause()

    def view_engine_info(self):
        """View PD-SMIS engine information"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "Settings", "Engine Info"]
        self.display_breadcrumbs()

        info = self.pd_smis_engine.get_engine_info()

        self.show_message("\n=== PD-SMIS Engine Information ===\n", "info")
        print(f"Engine Version: {info['engine_version']}")
        print(f"Wrapper Version: {info['wrapper_version']}")
        print(f"Engine Path: {info['engine_path']}")
        print(f"\nPhases: {info['phases_count']}")
        for phase in info['phases']:
            print(f"  • {phase}")
        print(f"\nValidation Tiers: {info['validation_tiers_count']}")
        for tier in info['validation_tiers']:
            print(f"  • {tier}")
        print(f"\nCapabilities:")
        for cap in info['capabilities']:
            print(f"  • {cap}")

        self.pause()

    def run_preservation_check(self):
        """Run v5.1 preservation check"""
        self.clear_screen()
        self.display_header()
        self.breadcrumbs = ["Main Menu", "Settings", "Preservation Check"]
        self.display_breadcrumbs()

        self.show_message("\n🔍 Running v5.1 preservation check...\n", "info")

        import subprocess
        result = subprocess.run(
            ["./scripts/check_v5_preservation.sh"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.returncode == 0:
            self.show_message("\n✅ v5.1 engine preservation verified!", "success")
        else:
            self.show_message("\n❌ Preservation check failed!", "error")

        self.pause()


def main():
    """Main entry point"""
    try:
        clui = JobRefresherCLUI()
        clui.main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting JobRefresher...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
