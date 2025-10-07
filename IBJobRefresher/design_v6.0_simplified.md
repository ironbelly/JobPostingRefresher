# JobRefresher v6.0 Simplified Design Document

## Overview

JobRefresher v6.0 adds two key capabilities to the existing v5.1 framework:
1. **Multi-job management** using a simple folder-based structure with markdown files
2. **TeamTailor API integration** to automatically fetch job data and KPIs

This design maintains the simplicity of the current system while adding these conveniences.

## 1. Folder Structure for Multi-Job Management

### 1.1 Directory Organization

```
JobPostingRefresher/
├── config/
│   └── teamtailor_config.json    # API credentials
├── jobs/                          # All job data stored here
│   ├── job_001_senior_dev/       # Folder per job (ID + title slug)
│   │   ├── metadata.json         # Job metadata and TeamTailor ID
│   │   ├── v1/                   # Version 1
│   │   │   ├── title.md
│   │   │   ├── posting.md
│   │   │   ├── project.md
│   │   │   └── metrics.json
│   │   ├── v2/                   # Version 2
│   │   │   ├── title.md
│   │   │   ├── posting.md
│   │   │   ├── project.md
│   │   │   └── metrics.json
│   │   └── current_version.txt   # Points to current version (e.g., "v2")
│   └── job_002_backend_eng/
│       └── ...
└── IBJobRefresher/                # Existing PD-SMIS engine
    └── ...
```

### 1.2 File Formats

#### metadata.json
```json
{
  "job_id": "job_001",
  "teamtailor_id": "12345",
  "created_date": "2024-01-15",
  "last_synced": "2024-01-20T10:30:00Z",
  "status": "active",
  "tags": ["engineering", "senior", "remote"]
}
```

#### title.md
```markdown
Senior Frontend Developer - E-Commerce Platform
```

#### posting.md
```markdown
We're looking for a Senior Frontend Developer to join our team...
[Full job posting content]
```

#### project.md
```markdown
We're building a next-generation e-commerce platform using React and Node.js...
[Project description]
```

#### metrics.json
```json
{
  "date_measured": "2024-01-20",
  "source": "teamtailor",
  "kpis": {
    "visit_application_rate": 2.1,
    "application_screening_rate": 45.0,
    "application_interview_rate": 15.0,
    "interview_offer_rate": 25.0,
    "offer_hire_rate": 60.0
  },
  "ad_metrics": {
    "spend": 5000,
    "impressions": 50000,
    "clicks": 500,
    "ctr": 1.0,
    "cpc": 10.0,
    "conversion_rate": 2.0
  }
}
```

## 2. Interactive CLUI Interface

### 2.1 Interface Overview

Instead of command-line arguments, the system provides an interactive menu-driven interface with navigation, making it more accessible for non-technical users.

```
╔════════════════════════════════════════════════════════════╗
║            JobRefresher v6.0 - Interactive Mode           ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  [1] Job Management                                       ║
║      • View all jobs                                      ║
║      • Create new job                                     ║
║      • Import from TeamTailor                             ║
║      • Search jobs                                        ║
║                                                            ║
║  [2] Job Processing                                       ║
║      • Select & optimize job                              ║
║      • Batch process jobs                                 ║
║      • View processing history                            ║
║                                                            ║
║  [3] Metrics & Analytics                                  ║
║      • Sync metrics from TeamTailor                       ║
║      • Compare job versions                               ║
║      • View performance dashboard                         ║
║                                                            ║
║  [4] Configuration                                        ║
║      • TeamTailor settings                                ║
║      • Processing preferences                             ║
║      • Export settings                                    ║
║                                                            ║
║  [Q] Quit                                                  ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
Enter choice:
```

### 2.2 Navigation System

The CLUI uses a hierarchical navigation system with breadcrumbs:

```
Home > Job Management > View Jobs

╔════════════════════════════════════════════════════════════╗
║                        Job List                           ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  ID    Title                    Status    Version  Metrics ║
║  ────  ─────────────────────   ────────  ────────  ────── ║
║  [1]   Senior Frontend Dev      Active    v3       ✓       ║
║  [2]   Backend Engineer         Active    v2       ✓       ║
║  [3]   Product Manager          Draft     v1       ✗       ║
║  [4]   DevOps Engineer          Active    v4       ✓       ║
║  [5]   Data Scientist           Archived  v2       ✓       ║
║                                                            ║
║  Page 1 of 3  [N]ext  [P]rev  [S]earch  [F]ilter          ║
║                                                            ║
║  Actions:                                                  ║
║  [V] View Details  [E] Edit  [O] Optimize  [D] Delete     ║
║  [C] Compare Versions  [X] Export  [B] Back to Menu       ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
Select job number or action:
```

### 2.3 Interactive Forms

For data input, the system uses interactive forms with validation:

```
Home > Job Management > Create New Job

╔════════════════════════════════════════════════════════════╗
║                    Create New Job                         ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Job Title:                                               ║
║  > Senior Frontend Developer_                             ║
║                                                            ║
║  Company/Department:                                      ║
║  > Engineering Team_                                      ║
║                                                            ║
║  Import from TeamTailor? [Y/N]: N                         ║
║                                                            ║
║  Job Description (press Ctrl+D when done):                ║
║  > We are looking for an experienced frontend developer   ║
║  > to join our engineering team. You will be responsible  ║
║  > for building user interfaces..._                       ║
║                                                            ║
║  Project Description (optional, press Ctrl+D when done):  ║
║  > _                                                       ║
║                                                            ║
║  Initial KPIs (optional):                                 ║
║    Visit/Application Rate (%): 2.1_                       ║
║    Application/Interview Rate (%): 15_                    ║
║                                                            ║
║  [S] Save  [C] Cancel  [I] Import from TeamTailor Instead ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

### 2.4 Job Detail View

Interactive job detail view with actions:

```
Home > Job Management > job_001_senior_dev

╔════════════════════════════════════════════════════════════╗
║              Job Details - Senior Frontend Dev            ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Status: Active          Version: v3      ID: job_001     ║
║  Created: 2024-01-15     Modified: 2024-01-20             ║
║  TeamTailor ID: 12345    Last Sync: 2024-01-20 10:30      ║
║                                                            ║
║  ┌─ Current Metrics ─────────────────────────────────┐    ║
║  │ Visit → Application:        2.1% (↓ from 2.5%)    │    ║
║  │ Application → Interview:    15%  (↑ from 12%)     │    ║
║  │ Interview → Offer:          25%  (stable)         │    ║
║  │ Offer → Hire:               60%  (↑ from 50%)     │    ║
║  └───────────────────────────────────────────────────┘    ║
║                                                            ║
║  Version History:                                         ║
║  • v3 (current) - 2024-01-20 - Optimized for clarity      ║
║  • v2          - 2024-01-18 - Added remote benefits       ║
║  • v1          - 2024-01-15 - Initial version             ║
║                                                            ║
║  Actions:                                                  ║
║  [O] Optimize  [E] Edit  [V] View Full Text  [C] Compare  ║
║  [S] Sync Metrics  [N] New Version  [X] Export  [B] Back  ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
Select action:
```

### 2.5 Processing Workflow

Interactive optimization process with progress display:

```
Home > Job Processing > Optimize

╔════════════════════════════════════════════════════════════╗
║                  Job Optimization Process                 ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Selected: job_001_senior_dev (v3)                        ║
║                                                            ║
║  ┌─ Processing Pipeline ─────────────────────────────┐    ║
║  │                                                    │    ║
║  │  Phase 0: Collection        [████████████] 100%   │    ║
║  │  Phase 1: Extraction        [████████████] 100%   │    ║
║  │  Phase 2: Hypothesis        [████████░░░░]  75%   │    ║
║  │  Phase 3: Optimization      [░░░░░░░░░░░░]   0%   │    ║
║  │  Phase 4: Generation        [░░░░░░░░░░░░]   0%   │    ║
║  │  Phase 5: Validation        [░░░░░░░░░░░░]   0%   │    ║
║  │  Phase 6: Learning          [░░░░░░░░░░░░]   0%   │    ║
║  │                                                    │    ║
║  └───────────────────────────────────────────────────┘    ║
║                                                            ║
║  Current: Analyzing KPI bottlenecks...                    ║
║  • Identified low visit/application rate                  ║
║  • Title lacks clarity on seniority benefits              ║
║  • Missing remote work emphasis                           ║
║                                                            ║
║  [P] Pause  [C] Cancel  [V] Verbose Mode                  ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

### 2.6 Core Python Structure

```python
# jbr.py - Main CLUI entry point
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import curses
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, TextColumn
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from teamtailor_client import TeamTailorClient
from job_manager import JobManager
from pd_smis_engine import PDSMISEngine

class JobRefresherCLUI:
    def __init__(self):
        self.console = Console()
        self.job_manager = JobManager()
        self.teamtailor = TeamTailorClient()
        self.engine = PDSMISEngine()
        self.current_path = ["Home"]
        self.running = True

    def run(self):
        """Main CLUI loop"""
        self.console.clear()

        while self.running:
            try:
                if len(self.current_path) == 1:
                    self.show_main_menu()
                else:
                    self.route_to_section()
            except KeyboardInterrupt:
                if self.confirm_exit():
                    self.running = False
                    self.console.print("\n[bold green]Thank you for using JobRefresher![/bold green]")
            except Exception as e:
                self.console.print(f"[bold red]Error: {e}[/bold red]")
                input("Press Enter to continue...")

    def show_main_menu(self):
        """Display main menu"""
        self.console.clear()
        self.display_header()

        menu = Panel(
            """[bold cyan]Main Menu[/bold cyan]

[1] Job Management
    • View all jobs
    • Create new job
    • Import from TeamTailor
    • Search jobs

[2] Job Processing
    • Select & optimize job
    • Batch process jobs
    • View processing history

[3] Metrics & Analytics
    • Sync metrics from TeamTailor
    • Compare job versions
    • View performance dashboard

[4] Configuration
    • TeamTailor settings
    • Processing preferences
    • Export settings

[Q] Quit""",
            title="JobRefresher v6.0 - Interactive Mode",
            border_style="bright_blue"
        )

        self.console.print(menu)
        choice = prompt("\nEnter choice: ").strip().upper()

        if choice == '1':
            self.current_path.append("Job Management")
            self.job_management_menu()
        elif choice == '2':
            self.current_path.append("Job Processing")
            self.job_processing_menu()
        elif choice == '3':
            self.current_path.append("Metrics & Analytics")
            self.metrics_menu()
        elif choice == '4':
            self.current_path.append("Configuration")
            self.configuration_menu()
        elif choice == 'Q':
            self.running = False

    def job_management_menu(self):
        """Job management submenu"""
        self.console.clear()
        self.display_breadcrumbs()

        while True:
            jobs = self.job_manager.list_jobs()

            # Create table
            table = Table(title="Job List", show_header=True, header_style="bold magenta")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Title", style="green")
            table.add_column("Status", justify="center")
            table.add_column("Version", justify="center")
            table.add_column("Metrics", justify="center")

            for idx, job in enumerate(jobs, 1):
                metrics_symbol = "✓" if job.get('has_metrics') else "✗"
                table.add_row(
                    f"[{idx}]",
                    job.get('title', 'Untitled'),
                    job.get('status', 'Unknown'),
                    job.get('current_version', 'v1'),
                    metrics_symbol
                )

            self.console.print(table)

            # Show actions
            self.console.print("\n[bold]Actions:[/bold]")
            self.console.print("[V] View Details  [N] New Job  [I] Import from TeamTailor")
            self.console.print("[E] Edit  [O] Optimize  [D] Delete  [S] Search")
            self.console.print("[B] Back to Main Menu")

            action = prompt("\nSelect job number or action: ").strip().upper()

            if action == 'B':
                self.current_path.pop()
                break
            elif action == 'N':
                self.create_new_job()
            elif action == 'I':
                self.import_from_teamtailor()
            elif action.isdigit():
                job_idx = int(action) - 1
                if 0 <= job_idx < len(jobs):
                    self.view_job_details(jobs[job_idx])
            # Handle other actions...

    def create_new_job(self):
        """Interactive job creation form"""
        self.console.clear()
        self.display_breadcrumbs()

        self.console.print(Panel("[bold cyan]Create New Job[/bold cyan]", expand=False))

        # Collect job information
        job_title = prompt("Job Title: ")
        company = prompt("Company/Department (optional): ")

        import_choice = prompt("Import from TeamTailor? [Y/N]: ").strip().upper()

        if import_choice == 'Y':
            teamtailor_id = prompt("TeamTailor Job ID: ")
            self.import_specific_job(teamtailor_id)
            return

        # Multi-line input for job description
        self.console.print("\n[dim]Job Description (press Ctrl+D or type 'END' on a new line when done):[/dim]")
        job_description = self.get_multiline_input()

        self.console.print("\n[dim]Project Description (optional, press Ctrl+D or type 'END' when done):[/dim]")
        project_description = self.get_multiline_input()

        # KPIs
        self.console.print("\n[bold]Initial KPIs (optional, press Enter to skip):[/bold]")
        visit_rate = prompt("Visit/Application Rate (%): ") or "0"
        interview_rate = prompt("Application/Interview Rate (%): ") or "0"

        # Confirm and save
        self.console.print("\n[bold]Review:[/bold]")
        self.console.print(f"Title: {job_title}")
        self.console.print(f"Company: {company or 'Not specified'}")
        self.console.print(f"Description: {len(job_description)} characters")
        self.console.print(f"Project: {len(project_description)} characters")

        if prompt("\nSave job? [Y/N]: ").strip().upper() == 'Y':
            job_id = self.job_manager.create_job(
                title=job_title,
                company=company,
                description=job_description,
                project=project_description,
                kpis={
                    'visit_application_rate': float(visit_rate),
                    'application_interview_rate': float(interview_rate)
                }
            )
            self.console.print(f"[bold green]Job created successfully! ID: {job_id}[/bold green]")
            input("\nPress Enter to continue...")

    def get_multiline_input(self):
        """Get multi-line input from user"""
        lines = []
        while True:
            try:
                line = input()
                if line.upper() == 'END':
                    break
                lines.append(line)
            except EOFError:
                break
        return '\n'.join(lines)

    def view_job_details(self, job):
        """Display detailed job view with actions"""
        self.console.clear()
        job_path = job['path']
        job_data = self.job_manager.get_job_data(job_path)

        # Display job details
        panel = Panel(
            f"""[bold cyan]Job Details[/bold cyan]

[bold]Title:[/bold] {job_data.get('title', 'Untitled')}
[bold]Status:[/bold] {job.get('status', 'Unknown')}
[bold]Version:[/bold] {job.get('current_version', 'v1')}
[bold]ID:[/bold] {job.get('job_id')}
[bold]Created:[/bold] {job.get('created_date', 'Unknown')}
[bold]TeamTailor ID:[/bold] {job.get('teamtailor_id', 'Not linked')}

[bold]Current Metrics:[/bold]
  Visit → Application:     {job_data.get('metrics', {}).get('kpis', {}).get('visit_application_rate', 0)}%
  Application → Interview: {job_data.get('metrics', {}).get('kpis', {}).get('application_interview_rate', 0)}%
  Interview → Offer:       {job_data.get('metrics', {}).get('kpis', {}).get('interview_offer_rate', 0)}%
  Offer → Hire:           {job_data.get('metrics', {}).get('kpis', {}).get('offer_hire_rate', 0)}%

[bold]Actions:[/bold]
[O] Optimize  [E] Edit  [V] View Full Text  [C] Compare Versions
[S] Sync Metrics  [N] New Version  [X] Export  [B] Back""",
            title=f"Job: {job.get('name')}",
            border_style="bright_blue"
        )

        self.console.print(panel)
        action = prompt("\nSelect action: ").strip().upper()

        if action == 'O':
            self.optimize_job(job_path)
        elif action == 'V':
            self.view_full_text(job_data)
        elif action == 'S':
            self.sync_metrics(job)
        elif action == 'B':
            return
        # Handle other actions...

    def optimize_job(self, job_path):
        """Run optimization process with progress display"""
        self.console.clear()
        self.console.print(Panel("[bold cyan]Job Optimization Process[/bold cyan]", expand=False))

        # Get job data
        job_data = self.job_manager.get_job_data(job_path)

        phases = [
            ("Phase 0: Collection", "Collecting source materials..."),
            ("Phase 1: Extraction", "Extracting semantic fingerprints..."),
            ("Phase 2: Hypothesis", "Analyzing KPI bottlenecks..."),
            ("Phase 3: Optimization", "Designing interventions..."),
            ("Phase 4: Generation", "Generating optimized content..."),
            ("Phase 5: Validation", "Running validation suite..."),
            ("Phase 6: Learning", "Extracting insights...")
        ]

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:

            for phase_name, phase_desc in phases:
                task = progress.add_task(f"[cyan]{phase_name}[/cyan]: {phase_desc}", total=100)

                # Simulate processing (would be replaced with actual PD-SMIS calls)
                for i in range(100):
                    progress.update(task, advance=1)
                    time.sleep(0.01)  # Simulate work

                # Show phase results
                if "Hypothesis" in phase_name:
                    self.console.print("  • Identified low visit/application rate")
                    self.console.print("  • Title lacks clarity on seniority benefits")
                    self.console.print("  • Missing remote work emphasis")

        # Process through PD-SMIS engine
        optimized_result = self.engine.process_job(job_data)

        # Save results
        new_version_path = self.job_manager.create_version(job_path)
        self.job_manager.save_processed_job(job_path, new_version_path.name, optimized_result)

        self.console.print("\n[bold green]Optimization complete![/bold green]")
        self.console.print(f"Results saved to: {new_version_path}")
        input("\nPress Enter to continue...")

    def display_breadcrumbs(self):
        """Display navigation breadcrumbs"""
        breadcrumb = " > ".join(self.current_path)
        self.console.print(f"[dim]{breadcrumb}[/dim]\n")

    def display_header(self):
        """Display application header"""
        header = Panel(
            "[bold cyan]JobRefresher v6.0[/bold cyan]\n"
            "[dim]AI-Powered Job Posting Optimization System[/dim]",
            style="bright_blue",
            expand=False
        )
        self.console.print(header)
        self.console.print()

    def confirm_exit(self):
        """Confirm before exiting"""
        return prompt("\nAre you sure you want to exit? [Y/N]: ").strip().upper() == 'Y'


# Entry point for running the CLUI
if __name__ == "__main__":
    app = JobRefresherCLUI()
    app.run()
```

## 3. TeamTailor API Integration

### 3.1 Simple API Client

```python
# teamtailor_client.py
import requests
import json
from pathlib import Path

class TeamTailorClient:
    def __init__(self):
        self.config = self._load_config()
        self.base_url = "https://api.teamtailor.com/v1"
        self.headers = {
            "Authorization": f"Token token={self.config['api_key']}",
            "X-Api-Version": "20210218",
            "Content-Type": "application/json"
        }

    def _load_config(self):
        """Load TeamTailor configuration"""
        config_path = Path("config/teamtailor_config.json")
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
        return {}

    def fetch_job(self, job_id):
        """Fetch job details from TeamTailor"""
        response = requests.get(
            f"{self.base_url}/jobs/{job_id}",
            headers=self.headers
        )

        if response.status_code == 200:
            data = response.json()
            job = data['data']

            return {
                'title': job['attributes']['title'],
                'description': job['attributes']['body'],
                'project_description': job['attributes'].get('pitch', ''),
                'status': job['attributes']['status']
            }
        else:
            raise Exception(f"Failed to fetch job: {response.status_code}")

    def fetch_metrics(self, job_id):
        """Fetch job application metrics"""
        # Fetch candidates for this job
        response = requests.get(
            f"{self.base_url}/candidates",
            params={"filter[job_id]": job_id},
            headers=self.headers
        )

        if response.status_code == 200:
            data = response.json()
            candidates = data['data']

            # Calculate funnel metrics
            total = len(candidates)
            screened = sum(1 for c in candidates if c['attributes']['stage'] != 'archive')
            interviewed = sum(1 for c in candidates if 'interview' in c['attributes']['stage'])
            offered = sum(1 for c in candidates if c['attributes']['stage'] == 'offer')
            hired = sum(1 for c in candidates if c['attributes']['stage'] == 'hired')

            # Note: Visit data might need to come from a different endpoint
            # This is a simplified calculation
            metrics = {
                "date_measured": datetime.now().isoformat(),
                "source": "teamtailor",
                "kpis": {
                    "visit_application_rate": 2.1,  # Would need actual visit data
                    "application_screening_rate": (screened / total * 100) if total > 0 else 0,
                    "application_interview_rate": (interviewed / total * 100) if total > 0 else 0,
                    "interview_offer_rate": (offered / interviewed * 100) if interviewed > 0 else 0,
                    "offer_hire_rate": (hired / offered * 100) if offered > 0 else 0
                }
            }

            return metrics
        else:
            raise Exception(f"Failed to fetch metrics: {response.status_code}")
```

## 4. Job Manager

### 4.1 Simple Job Management

```python
# job_manager.py
import json
import shutil
from pathlib import Path
from datetime import datetime

class JobManager:
    def __init__(self):
        self.jobs_dir = Path("jobs")
        self.jobs_dir.mkdir(exist_ok=True)

    def list_jobs(self):
        """List all jobs"""
        jobs = []

        for job_dir in self.jobs_dir.iterdir():
            if job_dir.is_dir():
                jobs.append(self._read_job_info(job_dir))

        return jobs

    def _read_job_info(self, job_path):
        """Read job information from folder"""
        metadata_path = job_path / "metadata.json"
        current_version_path = job_path / "current_version.txt"

        info = {
            "path": str(job_path),
            "name": job_path.name
        }

        if metadata_path.exists():
            with open(metadata_path) as f:
                info.update(json.load(f))

        if current_version_path.exists():
            with open(current_version_path) as f:
                info['current_version'] = f.read().strip()

        return info

    def create_version(self, job_path):
        """Create a new version of a job"""
        job_path = Path(job_path)

        # Get current version
        current_version_file = job_path / "current_version.txt"
        with open(current_version_file) as f:
            current = f.read().strip()

        # Determine new version number
        current_num = int(current.replace('v', ''))
        new_version = f"v{current_num + 1}"

        # Copy current version to new version
        current_path = job_path / current
        new_path = job_path / new_version
        shutil.copytree(current_path, new_path)

        # Update current version pointer
        with open(current_version_file, 'w') as f:
            f.write(new_version)

        print(f"Created new version: {new_version}")
        return new_path

    def get_job_data(self, job_path, version=None):
        """Read job data for processing"""
        job_path = Path(job_path)

        if version is None:
            # Get current version
            with open(job_path / "current_version.txt") as f:
                version = f.read().strip()

        version_path = job_path / version

        # Read all components
        data = {}

        # Read title
        title_path = version_path / "title.md"
        if title_path.exists():
            with open(title_path) as f:
                data['title'] = f.read().strip()

        # Read posting
        posting_path = version_path / "posting.md"
        if posting_path.exists():
            with open(posting_path) as f:
                data['posting'] = f.read()

        # Read project description
        project_path = version_path / "project.md"
        if project_path.exists():
            with open(project_path) as f:
                data['project_description'] = f.read()

        # Read metrics
        metrics_path = version_path / "metrics.json"
        if metrics_path.exists():
            with open(metrics_path) as f:
                data['metrics'] = json.load(f)

        return data

    def save_processed_job(self, job_path, version, optimized_data):
        """Save processed job data to version folder"""
        version_path = Path(job_path) / version

        # Save optimized title
        if 'title' in optimized_data:
            with open(version_path / "title.md", 'w') as f:
                f.write(optimized_data['title'])

        # Save optimized posting
        if 'posting' in optimized_data:
            with open(version_path / "posting.md", 'w') as f:
                f.write(optimized_data['posting'])

        # Update metrics with projections
        if 'projected_metrics' in optimized_data:
            metrics_path = version_path / "metrics.json"
            if metrics_path.exists():
                with open(metrics_path) as f:
                    metrics = json.load(f)
            else:
                metrics = {}

            metrics['projections'] = optimized_data['projected_metrics']

            with open(metrics_path, 'w') as f:
                json.dump(metrics, f, indent=2)

        print(f"Saved optimized job data to {version_path}")
```

## 5. Integration with PD-SMIS Engine

### 5.1 Engine Wrapper

```python
# pd_smis_engine.py
from pathlib import Path
import subprocess
import json

class PDSMISEngine:
    def __init__(self):
        self.engine_path = Path("IBJobRefresher")

    def process_job(self, job_data):
        """Process job through PD-SMIS engine"""

        # Format data for PD-SMIS input
        formatted_input = self._format_for_pdsmis(job_data)

        # Run through existing PD-SMIS modules
        # This would integrate with the existing markdown-based system
        # For now, this is a placeholder for the integration

        # The actual implementation would:
        # 1. Format the job_data into the expected PD-SMIS input format
        # 2. Run through all the phases
        # 3. Return the optimized result

        optimized_result = {
            'title': job_data.get('title', '') + ' [Optimized]',
            'posting': job_data.get('posting', '') + '\n\n[Optimizations applied]',
            'projected_metrics': {
                'visit_application_rate': 3.5,
                'application_screening_rate': 55.0,
                # ... etc
            },
            'validation_report': {
                'passed': True,
                'checks': ['tier_enforcement', 'adversarial_validation', 'semantic_diff']
            }
        }

        return optimized_result

    def _format_for_pdsmis(self, job_data):
        """Format job data for PD-SMIS input"""
        formatted = f"""[PROJECT DESCRIPTION]
{job_data.get('project_description', '')}
[/PROJECT DESCRIPTION]

[ORIGINAL JOB TITLE]
{job_data.get('title', '')}
[/ORIGINAL JOB TITLE]

[ORIGINAL JOB POSTING]
{job_data.get('posting', '')}
[/ORIGINAL JOB POSTING]

[ORIGINAL JOB KPIs]
"""

        if 'metrics' in job_data and 'kpis' in job_data['metrics']:
            kpis = job_data['metrics']['kpis']
            formatted += f"""- Visit/Application Conversion: {kpis.get('visit_application_rate', 0)}%
- Application/Initial Screening: {kpis.get('application_screening_rate', 0)}%
- Application/Interview: {kpis.get('application_interview_rate', 0)}%
- Interview/Offer: {kpis.get('interview_offer_rate', 0)}%
- Offer/Hire: {kpis.get('offer_hire_rate', 0)}%"""

        formatted += "\n[/ORIGINAL JOB KPIs]"

        return formatted
```

## 6. Configuration

### 6.1 TeamTailor Configuration

```json
// config/teamtailor_config.json
{
  "api_key": "YOUR_API_KEY_HERE",
  "company_id": "YOUR_COMPANY_ID",
  "api_version": "20210218"
}
```

## 7. Usage Workflow

### 7.1 Typical User Flow with CLUI

1. **Launch the Interactive Interface**:
   ```bash
   python jbr.py
   ```
   This opens the interactive CLUI with a main menu.

2. **First-Time Setup**:
   - Select `[4] Configuration` from main menu
   - Choose `TeamTailor settings`
   - Enter your API credentials when prompted
   - The system saves them to `user_data/config/teamtailor_config.json`

3. **Import Jobs from TeamTailor**:
   - From main menu, select `[1] Job Management`
   - Press `[I]` for Import from TeamTailor
   - Enter the TeamTailor job ID when prompted
   - System fetches job data and creates folder structure automatically

4. **View and Manage Jobs**:
   - In Job Management menu, see all jobs in a table format
   - Select a job number to view details
   - Use navigation keys to browse through job lists
   - Filter and search capabilities available

5. **Optimize a Job**:
   - Select a job from the list
   - Press `[O]` to optimize
   - Watch real-time progress through all PD-SMIS phases
   - Review optimization results
   - System automatically creates a new version

6. **Compare Versions**:
   - From job details, press `[C]` for Compare Versions
   - Select two versions to compare side-by-side
   - See highlighted differences and improvements

7. **Sync Latest Metrics**:
   - From job details, press `[S]` to sync
   - System fetches latest KPIs from TeamTailor
   - Updates are reflected immediately in the interface

### 7.2 Keyboard Navigation

- **Number keys [1-9]**: Select menu items or jobs
- **[N]ext / [P]rev**: Navigate through paginated lists
- **[B]ack**: Return to previous menu
- **[Q]uit**: Exit the application (with confirmation)
- **[Ctrl+C]**: Emergency exit (with confirmation)
- **[Enter]**: Confirm selections
- **[Tab]**: Auto-complete in search fields

## 8. CLUI Features & Benefits

### 8.1 Interactive Features

1. **Context-Aware Navigation**: Breadcrumbs show current location in the interface
2. **Real-Time Progress**: Visual progress bars for optimization phases
3. **Smart Forms**: Input validation and helpful prompts for data entry
4. **Table Views**: Organized display of jobs with sorting and filtering
5. **Color Coding**: Status indicators using colors (green for success, red for errors)
6. **Pagination**: Handle large job lists with easy navigation
7. **Search & Filter**: Quick job discovery with search capabilities

### 8.2 User Experience Benefits

- **No Command Memorization**: Menu-driven interface guides users
- **Visual Feedback**: Clear indication of what's happening at each step
- **Error Prevention**: Input validation prevents common mistakes
- **Undo Support**: Can revert to previous versions easily
- **Batch Operations**: Select multiple jobs for bulk processing
- **Help System**: Context-sensitive help available at any screen
- **Accessibility**: Keyboard-only navigation, screen reader compatible

### 8.3 Advanced CLUI Features

```python
# Additional CLUI features implementation

class AdvancedCLUIFeatures:
    def search_jobs(self):
        """Interactive job search with filters"""
        self.console.clear()
        self.display_breadcrumbs()

        search_term = prompt("Search jobs (title/description): ")
        status_filter = prompt("Filter by status (active/draft/archived/all): ") or "all"

        results = self.job_manager.search_jobs(
            query=search_term,
            status=status_filter
        )

        # Display results in table format
        self.display_job_table(results)

    def batch_process(self):
        """Process multiple jobs at once"""
        self.console.clear()
        self.display_breadcrumbs()

        jobs = self.job_manager.list_jobs()
        self.console.print("[bold]Select jobs to process (comma-separated numbers):[/bold]")

        # Display numbered job list
        for idx, job in enumerate(jobs, 1):
            self.console.print(f"[{idx}] {job['title']} ({job['status']})")

        selection = prompt("\nEnter job numbers (e.g., 1,3,5): ")
        selected_indices = [int(x.strip())-1 for x in selection.split(',')]

        # Process selected jobs with progress bar
        with Progress(console=self.console) as progress:
            task = progress.add_task("[cyan]Processing jobs...", total=len(selected_indices))

            for idx in selected_indices:
                job = jobs[idx]
                self.engine.process_job(self.job_manager.get_job_data(job['path']))
                progress.update(task, advance=1)

    def performance_dashboard(self):
        """Display metrics dashboard"""
        self.console.clear()
        self.display_breadcrumbs()

        # Create metrics visualization
        table = Table(title="Performance Dashboard", show_header=True)
        table.add_column("Job", style="cyan")
        table.add_column("Version", justify="center")
        table.add_column("Visit→App", justify="center")
        table.add_column("App→Interview", justify="center")
        table.add_column("Trend", justify="center")

        jobs = self.job_manager.list_jobs()
        for job in jobs:
            if job.get('has_metrics'):
                data = self.job_manager.get_job_data(job['path'])
                metrics = data.get('metrics', {}).get('kpis', {})

                trend = "📈" if metrics.get('visit_application_rate', 0) > 2.0 else "📉"

                table.add_row(
                    job['title'][:30],
                    job['current_version'],
                    f"{metrics.get('visit_application_rate', 0):.1f}%",
                    f"{metrics.get('application_interview_rate', 0):.1f}%",
                    trend
                )

        self.console.print(table)
        input("\nPress Enter to continue...")

    def export_job(self, job_path, format="markdown"):
        """Export job in various formats"""
        self.console.clear()
        self.display_breadcrumbs()

        export_formats = {
            "1": ("Markdown", "markdown"),
            "2": ("JSON", "json"),
            "3": ("HTML", "html"),
            "4": ("PDF", "pdf")
        }

        self.console.print("[bold]Select export format:[/bold]")
        for key, (name, _) in export_formats.items():
            self.console.print(f"[{key}] {name}")

        choice = prompt("\nSelect format: ")
        if choice in export_formats:
            _, format_type = export_formats[choice]
            output_path = self.job_manager.export_job(job_path, format_type)
            self.console.print(f"[bold green]Exported to: {output_path}[/bold green]")
            input("\nPress Enter to continue...")
```

## 9. Key Design Decisions

1. **Interactive CLUI**: Menu-driven interface instead of command-line arguments
2. **Visual Feedback**: Progress bars, tables, and color-coded status
3. **Markdown Storage**: All content stored as markdown files for easy reading/editing
4. **Version Folders**: Simple v1, v2, v3 folder structure for iterations
5. **JSON for Structured Data**: Metrics and metadata in JSON for easy parsing
6. **Minimal Dependencies**: Rich for terminal UI, requests for API calls
7. **Existing Engine Integration**: Wrapper around existing PD-SMIS modules
8. **No Database**: Everything is file-based as requested

## 9. Benefits of This Approach

- **Simple and Incremental**: Builds on existing v5.1 without major changes
- **Human-Readable**: All data in markdown/JSON files
- **Version Control Friendly**: Works well with git
- **Easy Backup**: Just copy the jobs folder
- **No Complex Dependencies**: Minimal Python requirements
- **Flexible**: Easy to extend without architectural changes

## 10. Data Separation and Version Control

### 10.1 Directory Structure with Data Separation

```
JobPostingRefresher/
├── .gitignore                    # Excludes sensitive data
├── README.md                     # Documentation
├── jbr.py                        # Main CLI script
├── teamtailor_client.py          # TeamTailor integration
├── job_manager.py                # Job management
├── pd_smis_engine.py             # Engine wrapper
├── config/
│   └── teamtailor_config.json.example  # Example config (tracked)
├── user_data/                    # All user data (NOT tracked)
│   ├── config/
│   │   └── teamtailor_config.json      # Actual credentials (ignored)
│   └── jobs/                     # All job data (ignored)
│       ├── job_001_senior_dev/
│       └── job_002_backend_eng/
└── IBJobRefresher/               # Core engine (tracked)
    └── ...
```

### 10.2 .gitignore File

```gitignore
# User data - never commit these
/user_data/
user_data/**

# Config files with sensitive data
config/teamtailor_config.json
*.secret
*.key
*_credentials.json

# Environment files
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

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp
*.bak
```

### 10.3 Setup Instructions for Users

```markdown
## First Time Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourorg/JobPostingRefresher.git
   cd JobPostingRefresher
   ```

2. **Create user data directory:**
   ```bash
   mkdir -p user_data/config
   mkdir -p user_data/jobs
   ```

3. **Copy and configure TeamTailor settings:**
   ```bash
   cp config/teamtailor_config.json.example user_data/config/teamtailor_config.json
   # Edit user_data/config/teamtailor_config.json with your API credentials
   ```

4. **Start using:**
   ```bash
   python jbr.py import --teamtailor-id 12345
   ```

## Updating the Application

1. **Pull latest changes (your data is safe):**
   ```bash
   git pull origin main
   ```

2. **Your data remains untouched in user_data/**

## Backup Your Data

To backup your jobs and config:
```bash
tar -czf jobrefresher_backup_$(date +%Y%m%d).tar.gz user_data/
```

To restore:
```bash
tar -xzf jobrefresher_backup_20240120.tar.gz
```
```

### 10.4 Updated Python Code to Use user_data Path

```python
# Updated paths in jbr.py
class JobRefresherCLI:
    def __init__(self):
        self.user_data_dir = Path("user_data")
        self.user_data_dir.mkdir(exist_ok=True)

        self.jobs_dir = self.user_data_dir / "jobs"
        self.jobs_dir.mkdir(exist_ok=True)

        self.config_dir = self.user_data_dir / "config"
        self.config_dir.mkdir(exist_ok=True)

        self.job_manager = JobManager(self.jobs_dir)
        self.teamtailor = TeamTailorClient(self.config_dir)
        self.engine = PDSMISEngine()

# Updated TeamTailorClient
class TeamTailorClient:
    def __init__(self, config_dir):
        self.config_dir = Path(config_dir)
        self.config = self._load_config()

    def _load_config(self):
        """Load TeamTailor configuration from user_data"""
        config_path = self.config_dir / "teamtailor_config.json"

        # Check if config exists, if not create from example
        if not config_path.exists():
            example_path = Path("config/teamtailor_config.json.example")
            if example_path.exists():
                print(f"Please configure TeamTailor API in: {config_path}")
                shutil.copy(example_path, config_path)
                return {}

        with open(config_path) as f:
            return json.load(f)

# Updated JobManager
class JobManager:
    def __init__(self, jobs_dir):
        self.jobs_dir = Path(jobs_dir)
        self.jobs_dir.mkdir(parents=True, exist_ok=True)
```

### 10.5 Example Configuration File (tracked in git)

```json
// config/teamtailor_config.json.example
{
  "api_key": "YOUR_API_KEY_HERE",
  "company_id": "YOUR_COMPANY_ID_HERE",
  "api_version": "20210218",
  "_comment": "Copy this file to user_data/config/teamtailor_config.json and add your credentials"
}
```

## 11. Benefits of This Approach

1. **Clean Separation**: Application code vs user data
2. **Safe Updates**: `git pull` never overwrites user data
3. **No Accidental Commits**: Sensitive data in ignored directories
4. **Easy Backup**: All user data in one directory
5. **Multiple Environments**: Can have different user_data folders
6. **Simple Migration**: Just copy user_data folder to new machine

## 12. Python Requirements

### 12.1 Dependencies

```txt
# requirements.txt
rich>=13.0.0           # Terminal UI components
prompt-toolkit>=3.0.0  # Interactive prompts
requests>=2.28.0       # API calls
python-dateutil>=2.8.0 # Date handling
colorama>=0.4.0        # Windows terminal colors (optional)
```

### 12.2 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the CLUI
python jbr.py
```

## 13. CLUI vs Traditional CLI Comparison

| Feature | Traditional CLI | Interactive CLUI |
|---------|----------------|------------------|
| Learning Curve | Steep - must memorize commands | Gentle - menu-driven |
| Error Prevention | Limited - wrong syntax fails | High - validation at each step |
| User Guidance | Man pages/help text | Interactive prompts |
| Visual Feedback | Text output only | Progress bars, tables, colors |
| Navigation | Command history | Hierarchical menus |
| Batch Operations | Complex scripts | Built-in multi-select |
| Data Entry | Single-line arguments | Multi-line forms |
| Accessibility | Basic | Screen reader optimized |

## 14. Future Extensibility

While keeping it simple now, this structure allows for future additions:

### 14.1 Potential Enhancements
- **Web Interface**: Could provide same functionality via web browser
- **API Server**: RESTful API for programmatic access
- **Database Cache**: Optional SQLite for performance with large datasets
- **More ATS Integrations**: Greenhouse, Lever, Workday following same pattern
- **AI Model Selection**: Support for different LLMs (GPT-4, Claude, etc.)
- **Collaborative Features**: Multi-user support with role-based access
- **Automated Workflows**: Schedule regular optimization runs

### 14.2 Plugin Architecture
```python
# Future plugin system
class CLUIPlugin:
    def register_menu_items(self):
        """Add new menu items to main interface"""
        pass

    def register_job_actions(self):
        """Add new actions for job management"""
        pass

    def register_export_formats(self):
        """Add new export format handlers"""
        pass
```

## 15. Core Functionality Preservation & Verification

### 15.1 Critical Preservation Requirements

**MANDATORY**: The following components from v5.1 MUST remain completely unchanged:

```yaml
preserved_components:
  phase_modules:
    - phases/phase_0_collection.md         # DO NOT MODIFY
    - phases/phase_0_5_iteration.md        # DO NOT MODIFY
    - phases/phase_0_6_error_handling.md   # DO NOT MODIFY
    - phases/phase_1_extraction.md         # DO NOT MODIFY
    - phases/phase_2_hypothesis.md         # DO NOT MODIFY
    - phases/phase_3_optimization.md       # DO NOT MODIFY
    - phases/phase_4_generation.md         # DO NOT MODIFY
    - phases/phase_6_learning.md           # DO NOT MODIFY
    - phases/phase_7_iteration.md          # DO NOT MODIFY

  validation_modules:
    - validation/adversarial_validation.md  # DO NOT MODIFY
    - validation/precision_tiers.md        # DO NOT MODIFY
    - validation/validation_orchestrator.md # DO NOT MODIFY
    - validation/verification_suite.md     # DO NOT MODIFY

  safeguards:
    - safeguards/critical_safeguards.md    # DO NOT MODIFY

  core_components:
    - components/output_format.md          # DO NOT MODIFY
    - orchestrator.md                      # DO NOT MODIFY
```

### 15.2 Prompt Integrity Verification

**Critical Prompt Preservation Checklist**:

```markdown
## Phase 0 - Collection Prompts
☐ Verify PROJECT DESCRIPTION markers remain: [PROJECT DESCRIPTION] ... [/PROJECT DESCRIPTION]
☐ Verify JOB TITLE markers remain: [ORIGINAL JOB TITLE] ... [/ORIGINAL JOB TITLE]
☐ Verify JOB POSTING markers remain: [ORIGINAL JOB POSTING] ... [/ORIGINAL JOB POSTING]
☐ Verify KPI markers remain: [ORIGINAL JOB KPIs] ... [/ORIGINAL JOB KPIs]
☐ Verify AD DATA markers remain: [ORIGINAL AD DATA] ... [/ORIGINAL AD DATA]

## Phase 1 - Extraction Prompts
☐ Semantic fingerprinting instructions unchanged
☐ Role/Project/Company segregation logic intact
☐ Fact extraction methodology preserved
☐ Immutability constraints maintained

## Phase 2 - Hypothesis Prompts
☐ KPI bottleneck analysis prompts unchanged
☐ Statistical analysis requirements intact
☐ Hypothesis generation framework preserved
☐ Evidence chain requirements maintained

## Phase 3 - Optimization Prompts
☐ Intervention design methodology unchanged
☐ Evidence-based optimization rules intact
☐ Constraint satisfaction requirements preserved
☐ A/B testing framework maintained

## Phase 4 - Generation Prompts
☐ Precision tier enforcement unchanged
☐ Semantic diff requirements intact
☐ Creative constraint boundaries preserved
☐ Fact preservation rules maintained

## Validation Suite Prompts
☐ All 14 validation layers intact
☐ Adversarial validation prompts unchanged
☐ Precision tier definitions preserved
☐ Verification thresholds maintained
```

### 15.3 Integration Testing Requirements

```python
# test_core_preservation.py
import hashlib
import json
from pathlib import Path

class CorePreservationTests:
    """Verify core PD-SMIS modules remain unchanged"""

    # MD5 checksums of critical files (v5.1 baseline)
    EXPECTED_CHECKSUMS = {
        "phases/phase_0_collection.md": "COMPUTE_ACTUAL_MD5_HERE",
        "phases/phase_1_extraction.md": "COMPUTE_ACTUAL_MD5_HERE",
        "phases/phase_2_hypothesis.md": "COMPUTE_ACTUAL_MD5_HERE",
        "phases/phase_3_optimization.md": "COMPUTE_ACTUAL_MD5_HERE",
        "phases/phase_4_generation.md": "COMPUTE_ACTUAL_MD5_HERE",
        "validation/adversarial_validation.md": "COMPUTE_ACTUAL_MD5_HERE",
        "validation/precision_tiers.md": "COMPUTE_ACTUAL_MD5_HERE",
        "orchestrator.md": "COMPUTE_ACTUAL_MD5_HERE"
    }

    def verify_file_integrity(self):
        """Ensure critical files haven't been modified"""
        for file_path, expected_checksum in self.EXPECTED_CHECKSUMS.items():
            actual_checksum = self.compute_checksum(file_path)
            assert actual_checksum == expected_checksum, \
                f"CRITICAL: {file_path} has been modified!"

    def verify_prompt_markers(self):
        """Ensure all prompt markers are intact"""
        required_markers = [
            "[PROJECT DESCRIPTION]", "[/PROJECT DESCRIPTION]",
            "[ORIGINAL JOB TITLE]", "[/ORIGINAL JOB TITLE]",
            "[ORIGINAL JOB POSTING]", "[/ORIGINAL JOB POSTING]",
            "[ORIGINAL JOB KPIs]", "[/ORIGINAL JOB KPIs]"
        ]

        # Check that pd_smis_engine.py formats data correctly
        formatted_input = self.engine._format_for_pdsmis(test_data)
        for marker in required_markers:
            assert marker in formatted_input, f"Missing marker: {marker}"

    def verify_phase_sequence(self):
        """Ensure phase execution order unchanged"""
        expected_sequence = [
            "phase_0_collection",
            "phase_0_5_iteration",
            "phase_1_extraction",
            "phase_2_hypothesis",
            "phase_3_optimization",
            "phase_4_generation",
            "phase_4_5_adversarial",
            "phase_5_verification",
            "phase_6_learning",
            "phase_7_iteration"
        ]

        actual_sequence = self.engine.get_phase_sequence()
        assert actual_sequence == expected_sequence, \
            "Phase sequence has been altered!"

    def verify_validation_layers(self):
        """Ensure all 14 validation layers present"""
        expected_layers = [
            "semantic_diff_check",
            "hallucination_detection",
            "fact_preservation",
            "kpi_impact_validation",
            "tier_enforcement",
            "adversarial_validation",
            "role_boundary_check",
            "project_boundary_check",
            "company_boundary_check",
            "statistical_validation",
            "constraint_satisfaction",
            "evidence_chain_validation",
            "iteration_consistency",
            "final_safety_check"
        ]

        for layer in expected_layers:
            assert self.validator.has_layer(layer), \
                f"Missing validation layer: {layer}"
```

### 15.4 Wrapper Isolation Pattern

**CRITICAL**: The CLUI must only wrap, never modify core functionality:

```python
# pd_smis_wrapper.py - SAFE wrapper pattern
class PDSMISWrapper:
    """
    Wrapper that ONLY formats I/O, never modifies core logic
    """

    def __init__(self):
        self.core_engine = PDSMISEngine()  # Unmodified v5.1 engine

    def process_job(self, job_data):
        """
        Wrapper method that ONLY handles data transformation
        """
        # Step 1: Transform CLUI data to v5.1 format
        v5_formatted = self._transform_to_v5_format(job_data)

        # Step 2: Pass to UNMODIFIED v5.1 engine
        result = self.core_engine.process(v5_formatted)

        # Step 3: Transform v5.1 output for CLUI display
        clui_formatted = self._transform_to_clui_format(result)

        return clui_formatted

    def _transform_to_v5_format(self, job_data):
        """Convert CLUI data structure to v5.1 expected format"""
        # ONLY data transformation, no logic changes
        return f"""[PROJECT DESCRIPTION]
{job_data.get('project_description', '')}
[/PROJECT DESCRIPTION]

[ORIGINAL JOB TITLE]
{job_data.get('title', '')}
[/ORIGINAL JOB TITLE]

[ORIGINAL JOB POSTING]
{job_data.get('posting', '')}
[/ORIGINAL JOB POSTING]

[ORIGINAL JOB KPIs]
{self._format_kpis(job_data.get('metrics', {}))}
[/ORIGINAL JOB KPIs]"""
```

### 15.5 Development Verification Checklist

**Before Each Commit - Mandatory Checks**:

```markdown
## Pre-Commit Verification Checklist

### File Integrity
☐ Run `test_core_preservation.py` - MUST PASS
☐ Verify no changes to files in `preserved_components` list
☐ Confirm all .md phase files unchanged (use git diff)

### Prompt Integrity
☐ Search for all [MARKER] tags - verify none modified
☐ Verify prompt text in phases/* unchanged
☐ Confirm validation rules text unchanged

### Functional Integrity
☐ Run existing v5.1 integration tests - MUST PASS
☐ Process test job through v5.1 directly - baseline output
☐ Process same job through CLUI - output MUST match
☐ Verify all 14 validation layers execute

### Architecture Integrity
☐ Verify wrapper pattern maintained (no core modifications)
☐ Check phase sequence unchanged
☐ Confirm orchestrator.md unmodified
☐ Validate output_format.md structure preserved

### Regression Tests
☐ Test single job processing (v5.1 mode)
☐ Test iteration handling
☐ Test error scenarios
☐ Test validation failures
☐ Test adversarial validation triggers
```

### 15.6 Continuous Verification Script

```bash
#!/bin/bash
# verify_integrity.sh - Run before every commit

echo "=== PD-SMIS Core Integrity Verification ==="

# 1. Check for modifications to protected files
echo "Checking protected files..."
PROTECTED_FILES=(
    "IBJobRefresher/orchestrator.md"
    "IBJobRefresher/phases/*.md"
    "IBJobRefresher/validation/*.md"
    "IBJobRefresher/safeguards/*.md"
    "IBJobRefresher/components/output_format.md"
)

for file in "${PROTECTED_FILES[@]}"; do
    if git diff --name-only | grep -q "$file"; then
        echo "ERROR: Protected file modified: $file"
        exit 1
    fi
done

# 2. Run checksum verification
echo "Verifying file checksums..."
python test_core_preservation.py

# 3. Run prompt marker verification
echo "Checking prompt markers..."
grep -r "\[PROJECT DESCRIPTION\]" IBJobRefresher/phases/ || exit 1
grep -r "\[ORIGINAL JOB TITLE\]" IBJobRefresher/phases/ || exit 1
grep -r "\[ORIGINAL JOB POSTING\]" IBJobRefresher/phases/ || exit 1
grep -r "\[ORIGINAL JOB KPIs\]" IBJobRefresher/phases/ || exit 1

# 4. Run integration tests
echo "Running v5.1 integration tests..."
python IBJobRefresher/tests/integration_tests.py || exit 1

# 5. Compare outputs
echo "Comparing v5.1 vs CLUI outputs..."
python compare_outputs.py test_job.json || exit 1

echo "=== All Integrity Checks Passed ==="
```

### 15.7 Critical Implementation Rules

**ABSOLUTE RULES - NO EXCEPTIONS**:

1. **NEVER edit files in the `preserved_components` list**
2. **NEVER modify prompt text within phase modules**
3. **NEVER change the phase execution sequence**
4. **NEVER alter validation thresholds or rules**
5. **NEVER modify the orchestrator.md logic**
6. **ONLY add new files, never modify existing v5.1 files**
7. **ONLY use wrapper pattern for integration**
8. **ALWAYS verify outputs match between v5.1 and CLUI**

### 15.8 Prompt Wording Preservation Tests

```python
# test_prompt_preservation.py
import re
from pathlib import Path

class PromptPreservationTests:
    """Verify exact prompt wording remains unchanged"""

    # Critical prompt phrases that MUST remain exactly as-is
    CRITICAL_PHRASES = {
        "phase_1_extraction.md": [
            "Extract semantic fingerprints",
            "Segregate facts into Role/Project/Company categories",
            "Maintain immutability of core facts",
            "Preserve exact numerical values",
            "No interpretation or modification"
        ],
        "phase_2_hypothesis.md": [
            "Identify KPI bottlenecks using statistical analysis",
            "Generate evidence-based hypotheses",
            "Map each hypothesis to measurable outcomes",
            "Prioritize by potential impact"
        ],
        "phase_3_optimization.md": [
            "Design interventions based on evidence",
            "Maintain semantic equivalence",
            "Apply precision tier constraints",
            "Generate A/B testable variations"
        ],
        "adversarial_validation.md": [
            "Act as hostile validator",
            "Challenge every claim aggressively",
            "Detect any hallucination or fabrication",
            "Verify factual accuracy with extreme prejudice"
        ],
        "precision_tiers.md": [
            "Tier 1: Exact reproduction only",
            "Tier 2: Minor grammatical improvements allowed",
            "Tier 3: Moderate rephrasing permitted",
            "Tier 4: Significant restructuring allowed",
            "Tier 5: Complete creative freedom"
        ]
    }

    def verify_exact_phrases(self):
        """Ensure critical phrases remain word-for-word identical"""
        for file_name, phrases in self.CRITICAL_PHRASES.items():
            file_path = Path(f"IBJobRefresher/{file_name}")

            if file_path.exists():
                content = file_path.read_text()

                for phrase in phrases:
                    if phrase not in content:
                        raise AssertionError(
                            f"CRITICAL: Phrase '{phrase}' missing or modified in {file_name}!"
                        )

    def verify_prompt_structure(self):
        """Ensure prompt structure patterns remain intact"""
        structure_patterns = {
            "INPUT_MARKERS": r'\[.*?\].*?\[/.*?\]',
            "INSTRUCTION_FORMAT": r'^##\s+.*?:$',
            "CONSTRAINT_FORMAT": r'^-\s+MUST.*?$',
            "VALIDATION_FORMAT": r'^VALIDATE:.*?$'
        }

        for pattern_name, regex in structure_patterns.items():
            for phase_file in Path("IBJobRefresher/phases").glob("*.md"):
                content = phase_file.read_text()
                if not re.search(regex, content, re.MULTILINE):
                    print(f"Warning: Pattern {pattern_name} not found in {phase_file.name}")

    def generate_prompt_snapshot(self):
        """Create baseline snapshot of all prompts for comparison"""
        snapshot = {}

        for phase_file in Path("IBJobRefresher").rglob("*.md"):
            if any(protected in str(phase_file) for protected in
                   ["phases/", "validation/", "safeguards/"]):

                # Extract all instruction lines (lines starting with -, *, or numbers)
                content = phase_file.read_text()
                instructions = re.findall(
                    r'^[\-\*\d]+\.?\s+(.+)$',
                    content,
                    re.MULTILINE
                )

                snapshot[str(phase_file)] = {
                    "checksum": hashlib.md5(content.encode()).hexdigest(),
                    "instruction_count": len(instructions),
                    "instructions": instructions[:10]  # First 10 as sample
                }

        return snapshot

    def compare_snapshots(self, baseline, current):
        """Compare current prompts against baseline"""
        differences = []

        for file_path, baseline_data in baseline.items():
            if file_path in current:
                current_data = current[file_path]

                if baseline_data["checksum"] != current_data["checksum"]:
                    differences.append({
                        "file": file_path,
                        "type": "MODIFIED",
                        "baseline_checksum": baseline_data["checksum"],
                        "current_checksum": current_data["checksum"]
                    })
            else:
                differences.append({
                    "file": file_path,
                    "type": "DELETED"
                })

        return differences
```

### 15.9 Output Comparison Framework

```python
# compare_outputs.py
import json
import difflib
from typing import Dict, Any

class OutputComparator:
    """Ensure v5.1 and CLUI produce identical optimization results"""

    def compare_job_outputs(self, v5_output: str, clui_output: str) -> Dict[str, Any]:
        """Compare outputs from v5.1 and CLUI processing"""

        comparison = {
            "identical": False,
            "differences": [],
            "similarity_score": 0.0
        }

        # Normalize outputs (remove timestamps, formatting differences)
        v5_normalized = self._normalize_output(v5_output)
        clui_normalized = self._normalize_output(clui_output)

        # Exact match check
        if v5_normalized == clui_normalized:
            comparison["identical"] = True
            comparison["similarity_score"] = 1.0
            return comparison

        # Detailed diff analysis
        diff = difflib.unified_diff(
            v5_normalized.splitlines(),
            clui_normalized.splitlines(),
            lineterm=''
        )

        for line in diff:
            if line.startswith('+') or line.startswith('-'):
                comparison["differences"].append(line)

        # Calculate similarity score
        matcher = difflib.SequenceMatcher(None, v5_normalized, clui_normalized)
        comparison["similarity_score"] = matcher.ratio()

        # Flag critical differences
        if comparison["similarity_score"] < 0.99:
            comparison["critical_error"] = "Output divergence detected!"

        return comparison

    def _normalize_output(self, output: str) -> str:
        """Remove timestamps and formatting differences"""
        # Remove timestamps
        output = re.sub(r'\d{4}-\d{2}-\d{2}T?\d{2}:\d{2}:\d{2}', '', output)

        # Remove version-specific formatting
        output = re.sub(r'v5\.1|v6\.0', 'vX', output)

        # Normalize whitespace
        output = ' '.join(output.split())

        return output

    def verify_validation_results(self, v5_validation: Dict, clui_validation: Dict):
        """Ensure all 14 validation layers produce same results"""

        required_validations = [
            "semantic_diff_check",
            "hallucination_detection",
            "fact_preservation",
            "kpi_impact_validation",
            "tier_enforcement",
            "adversarial_validation",
            "role_boundary_check",
            "project_boundary_check",
            "company_boundary_check",
            "statistical_validation",
            "constraint_satisfaction",
            "evidence_chain_validation",
            "iteration_consistency",
            "final_safety_check"
        ]

        for validation in required_validations:
            assert validation in v5_validation, f"v5.1 missing {validation}"
            assert validation in clui_validation, f"CLUI missing {validation}"
            assert v5_validation[validation] == clui_validation[validation], \
                f"Validation {validation} results differ!"
```

### 15.10 Comprehensive Test Suite

```python
# test_suite.py - Complete verification test suite
import unittest
import json
from pathlib import Path
from typing import Dict, List

class PD_SMIS_IntegrityTestSuite(unittest.TestCase):
    """Complete test suite to ensure v5.1 integrity"""

    @classmethod
    def setUpClass(cls):
        """Create baseline snapshots before any tests"""
        cls.baseline_snapshot = cls.create_baseline_snapshot()
        cls.test_job_data = cls.load_test_job()

    @staticmethod
    def create_baseline_snapshot() -> Dict:
        """Create complete snapshot of v5.1 state"""
        snapshot = {
            "files": {},
            "prompts": {},
            "markers": [],
            "validation_layers": [],
            "phase_sequence": []
        }

        # Capture all protected files
        for protected_file in Path("IBJobRefresher").rglob("*.md"):
            with open(protected_file, 'r') as f:
                content = f.read()
                snapshot["files"][str(protected_file)] = {
                    "checksum": hashlib.md5(content.encode()).hexdigest(),
                    "size": len(content),
                    "lines": content.count('\n')
                }

        # Capture all prompt markers
        snapshot["markers"] = [
            "[PROJECT DESCRIPTION]", "[/PROJECT DESCRIPTION]",
            "[ORIGINAL JOB TITLE]", "[/ORIGINAL JOB TITLE]",
            "[ORIGINAL JOB POSTING]", "[/ORIGINAL JOB POSTING]",
            "[ORIGINAL JOB KPIs]", "[/ORIGINAL JOB KPIs]",
            "[ORIGINAL AD DATA]", "[/ORIGINAL AD DATA]",
            "[USER FEEDBACK]", "[/USER FEEDBACK]"
        ]

        # Capture validation layers
        snapshot["validation_layers"] = [
            "semantic_diff_check", "hallucination_detection",
            "fact_preservation", "kpi_impact_validation",
            "tier_enforcement", "adversarial_validation",
            "role_boundary_check", "project_boundary_check",
            "company_boundary_check", "statistical_validation",
            "constraint_satisfaction", "evidence_chain_validation",
            "iteration_consistency", "final_safety_check"
        ]

        # Capture phase sequence
        snapshot["phase_sequence"] = [
            "phase_0_collection", "phase_0_5_iteration",
            "phase_1_extraction", "phase_2_hypothesis",
            "phase_3_optimization", "phase_4_generation",
            "phase_4_5_adversarial", "phase_5_verification",
            "phase_6_learning", "phase_7_iteration"
        ]

        return snapshot

    def test_01_file_integrity(self):
        """Test that no protected files have been modified"""
        current_snapshot = self.create_baseline_snapshot()

        for file_path, baseline_data in self.baseline_snapshot["files"].items():
            self.assertIn(file_path, current_snapshot["files"],
                         f"Protected file missing: {file_path}")

            current_data = current_snapshot["files"][file_path]
            self.assertEqual(baseline_data["checksum"], current_data["checksum"],
                           f"File modified: {file_path}")

    def test_02_prompt_markers_intact(self):
        """Test that all prompt markers remain unchanged"""
        for marker in self.baseline_snapshot["markers"]:
            found = False
            for phase_file in Path("IBJobRefresher/phases").glob("*.md"):
                if marker in phase_file.read_text():
                    found = True
                    break

            self.assertTrue(found, f"Marker missing: {marker}")

    def test_03_validation_layers_complete(self):
        """Test that all 14 validation layers are present"""
        # This would check the actual validation module
        for layer in self.baseline_snapshot["validation_layers"]:
            # Verify layer exists in validation system
            self.assertTrue(
                self._check_validation_layer_exists(layer),
                f"Validation layer missing: {layer}"
            )

    def test_04_phase_sequence_unchanged(self):
        """Test that phase execution order is unchanged"""
        # This would check the orchestrator
        current_sequence = self._get_current_phase_sequence()
        self.assertEqual(
            self.baseline_snapshot["phase_sequence"],
            current_sequence,
            "Phase sequence has been modified"
        )

    def test_05_wrapper_isolation(self):
        """Test that wrapper doesn't modify core logic"""
        from clui.pd_smis_wrapper import PDSMISWrapper

        wrapper = PDSMISWrapper()

        # Test that wrapper only transforms data
        test_input = {"title": "Test", "posting": "Test posting"}
        formatted = wrapper._transform_to_v5_format(test_input)

        # Check format matches v5.1 expectations
        self.assertIn("[PROJECT DESCRIPTION]", formatted)
        self.assertIn("[ORIGINAL JOB TITLE]", formatted)
        self.assertIn("[ORIGINAL JOB POSTING]", formatted)

    def test_06_output_equivalence(self):
        """Test that v5.1 and CLUI produce identical outputs"""
        # Process through v5.1 directly
        v5_output = self._process_through_v5(self.test_job_data)

        # Process through CLUI wrapper
        clui_output = self._process_through_clui(self.test_job_data)

        # Normalize and compare
        comparator = OutputComparator()
        result = comparator.compare_job_outputs(v5_output, clui_output)

        self.assertGreaterEqual(
            result["similarity_score"], 0.99,
            f"Output divergence: {result['differences']}"
        )

    def test_07_critical_phrases_preserved(self):
        """Test that critical prompt phrases remain exact"""
        tester = PromptPreservationTests()
        tester.verify_exact_phrases()  # Should not raise

    def test_08_no_core_modifications(self):
        """Test that no core v5.1 files have been edited"""
        # Check git status for protected files
        import subprocess

        result = subprocess.run(
            ["git", "diff", "--name-only", "IBJobRefresher/"],
            capture_output=True,
            text=True
        )

        modified_files = result.stdout.strip().split('\n') if result.stdout else []

        protected_patterns = [
            "orchestrator.md",
            "phases/",
            "validation/",
            "safeguards/",
            "components/output_format.md"
        ]

        for modified_file in modified_files:
            for pattern in protected_patterns:
                self.assertNotIn(pattern, modified_file,
                               f"Protected file modified: {modified_file}")


if __name__ == "__main__":
    # Run complete test suite
    unittest.main(verbosity=2)
```

### 15.11 Safe Development Pattern

```
JobPostingRefresher/
├── IBJobRefresher/          # DO NOT MODIFY ANYTHING HERE
│   ├── orchestrator.md      # PROTECTED - Core orchestration logic
│   ├── phases/              # PROTECTED - All phase modules
│   │   ├── phase_0_collection.md
│   │   ├── phase_1_extraction.md
│   │   ├── phase_2_hypothesis.md
│   │   ├── phase_3_optimization.md
│   │   ├── phase_4_generation.md
│   │   ├── phase_6_learning.md
│   │   └── phase_7_iteration.md
│   ├── validation/          # PROTECTED - Validation suite
│   │   ├── adversarial_validation.md
│   │   ├── precision_tiers.md
│   │   ├── validation_orchestrator.md
│   │   └── verification_suite.md
│   ├── safeguards/          # PROTECTED - Critical safeguards
│   │   └── critical_safeguards.md
│   └── components/          # PROTECTED - Core components
│       └── output_format.md
│
├── clui/                    # NEW - All CLUI code goes here
│   ├── jbr.py              # CLUI entry point
│   ├── job_manager.py      # Job management (NEW)
│   ├── teamtailor_client.py # API integration (NEW)
│   └── pd_smis_wrapper.py  # SAFE wrapper only - NO LOGIC CHANGES
│
├── user_data/               # User data directory
│   ├── config/             # User configuration
│   └── jobs/               # Job storage
│
├── tests/                   # Verification test suite
│   ├── test_core_preservation.py  # File integrity tests
│   ├── test_prompt_preservation.py # Prompt wording tests
│   ├── test_suite.py              # Complete test suite
│   ├── compare_outputs.py        # Output comparison
│   ├── verify_integrity.sh       # Pre-commit script
│   └── baseline_snapshot.json    # v5.1 baseline for comparison
│
├── .gitignore              # Excludes user_data/
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

### 15.12 Implementation Safeguards Summary

**The Three-Layer Protection Strategy**:

1. **Layer 1 - File Protection**:
   - Git hooks prevent modifications to protected files
   - Checksums verify file integrity
   - Directory structure enforces separation

2. **Layer 2 - Prompt Protection**:
   - Exact phrase matching ensures wording unchanged
   - Marker verification confirms structure intact
   - Pattern matching validates prompt format

3. **Layer 3 - Output Protection**:
   - Output comparison ensures identical results
   - Validation layer verification confirms all checks run
   - Phase sequence validation ensures correct execution

**Development Workflow**:
```bash
# 1. Before starting work
./tests/verify_integrity.sh baseline

# 2. During development - work ONLY in clui/ directory
cd clui/
# Make changes only here

# 3. Before committing
./tests/verify_integrity.sh
python tests/test_suite.py

# 4. Commit only if all tests pass
git add clui/
git commit -m "Add CLUI feature - core v5.1 unchanged"
```

## 16. Conclusion

JobRefresher v6.0 with its interactive CLUI represents a significant usability improvement over traditional command-line interfaces while maintaining the simplicity and file-based architecture of v5.1. The menu-driven navigation, visual feedback, and interactive forms make the system accessible to non-technical users while preserving all the power of the PD-SMIS optimization engine.

Key advantages of the CLUI approach:
- **User-Friendly**: No need to memorize commands or syntax
- **Error-Resistant**: Input validation and guided workflows prevent mistakes
- **Visual Clarity**: Tables, progress bars, and color coding provide clear feedback
- **Efficient Navigation**: Hierarchical menus with breadcrumbs for easy orientation
- **Flexible Data Entry**: Support for multi-line input and complex forms
- **Batch Capabilities**: Built-in support for processing multiple jobs
- **Extensible Design**: Easy to add new features without breaking existing functionality

The system successfully bridges the gap between powerful AI-driven optimization and practical daily use, making advanced job posting optimization accessible to HR professionals and recruiters without requiring technical expertise.

---

*Document Version: 2.0 - CLUI Enhanced*
*Design Date: 2024*
*Framework: PD-SMIS v5.1 with Interactive CLUI Layer*