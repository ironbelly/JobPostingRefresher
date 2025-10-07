# JobRefresher v6.0 - Quick Reference Card

## 🚨 CRITICAL RULES - NEVER VIOLATE
1. **NEVER modify any file in /IBJobRefresher/** - These are the v5.1 engine files
2. **ALWAYS check v5.1 checksums** before and after major operations
3. **ALL new code goes in /clui/** directory
4. **User data goes in /user_data/** (git-ignored)

## 📁 Directory Structure
```
JobPostingRefresher/
├── IBJobRefresher/        # ⚠️ DO NOT MODIFY - v5.1 engine
│   ├── main.py           # Core v5.1 entry point
│   ├── job_optimizer.py  # 14-layer validation system
│   └── prompts/          # Prompt templates with markers
├── clui/                 # ✅ ALL NEW v6.0 CODE HERE
│   ├── jbr.py           # Main CLUI entry point
│   ├── job_manager.py   # Job CRUD operations
│   ├── teamtailor_client.py  # API integration
│   └── engine_wrapper.py     # Safe v5.1 wrapper
├── user_data/           # User-specific data (git-ignored)
│   ├── jobs/           # Job storage
│   ├── config/         # Configuration
│   └── logs/           # Application logs
├── tests/              # Test suite
└── dev/v6/            # Development documentation
```

## 🎯 Milestone Execution Order
1. **M1**: Project Foundation → Directory setup, git, Python environment
2. **M2**: Data Layer → JobManager with CRUD operations
3. **M3**: API Integration → TeamTailor client with graceful degradation
4. **M4**: Engine Wrapper → Safe isolation of v5.1 engine
5. **M5**: CLUI Core → Interactive menu system with Rich
6. **M6**: CLUI Features → Enhanced UX features
7. **M7**: Testing Framework → Comprehensive test suite
8. **M8**: Final Integration → Documentation and release

## 🔧 Key Components

### JobManager (clui/job_manager.py)
```python
# Core operations
manager = JobManager()
job_id = manager.create_job(title, company, description, url)
job = manager.get_job(job_id)
manager.update_job(job_id, updates)
jobs = manager.list_jobs(status="active")
```

### TeamTailorClient (clui/teamtailor_client.py)
```python
# API operations with graceful degradation
client = TeamTailorClient(api_token)
job_data = client.fetch_job(job_id)  # Returns None if offline
metrics = client.fetch_metrics(job_id)  # Returns {} if offline
```

### EngineWrapper (clui/engine_wrapper.py)
```python
# Safe v5.1 engine interaction
wrapper = EngineWrapper()
result = wrapper.optimize_job(job_dict)  # Handles all format conversion
# Never directly import from IBJobRefresher!
```

### JobRefresherCLUI (clui/jbr.py)
```python
# Main application
app = JobRefresherCLUI()
app.run()  # Starts interactive menu
```

## 📝 File Storage Format

### Job Directory Structure
```
user_data/jobs/{job_id}/
├── metadata.json       # Job metadata
├── original.md        # Original job posting
├── current.md         # Latest optimized version
└── versions/          # Version history
    ├── v1/
    │   ├── content.md
    │   └── metadata.json
    └── v2/...
```

### Metadata Structure
```json
{
    "id": "uuid-string",
    "title": "Job Title",
    "company": "Company Name",
    "status": "active|archived|draft",
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z",
    "source": "manual|teamtailor|import",
    "url": "https://...",
    "versions": ["v1", "v2"],
    "current_version": "v2",
    "metrics": {}
}
```

## 🔐 v5.1 Preservation Checks

### Quick Verification
```bash
# Check if v5.1 files are intact
python3 -c "
import json, hashlib
from pathlib import Path

with open('dev/v6/v51_baseline.json') as f:
    baseline = json.load(f)

for filepath, expected in baseline.items():
    with open(filepath, 'rb') as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    if actual != expected:
        print(f'❌ MODIFIED: {filepath}')
        exit(1)
print('✅ v5.1 files intact')
"
```

### Create Baseline (M1 Task)
```python
import json, hashlib
from pathlib import Path

v51_files = list(Path("IBJobRefresher").rglob("*.py"))
baseline = {}

for file in v51_files:
    with open(file, 'rb') as f:
        baseline[str(file)] = hashlib.sha256(f.read()).hexdigest()

with open("dev/v6/v51_baseline.json", 'w') as f:
    json.dump(baseline, f, indent=2)
```

## ⚠️ Common Pitfalls to Avoid

1. **Importing from IBJobRefresher**
   ```python
   # ❌ WRONG - Direct import
   from IBJobRefresher.main import optimize_job

   # ✅ CORRECT - Use wrapper
   from clui.engine_wrapper import EngineWrapper
   wrapper = EngineWrapper()
   ```

2. **Modifying prompt markers**
   ```python
   # ❌ WRONG - Changing markers
   content = content.replace("[PROJECT DESCRIPTION]", description)

   # ✅ CORRECT - Preserve exact format
   # Markers must remain exactly: [PROJECT DESCRIPTION]
   ```

3. **Hardcoding paths**
   ```python
   # ❌ WRONG
   with open("/home/user/jobs/job.json") as f:

   # ✅ CORRECT
   job_path = Path("user_data/jobs") / job_id / "metadata.json"
   ```

4. **Not handling offline mode**
   ```python
   # ❌ WRONG
   data = client.fetch_job(job_id)
   process(data)  # Crashes if None

   # ✅ CORRECT
   data = client.fetch_job(job_id)
   if data:
       process(data)
   else:
       self.console.print("[yellow]Offline mode - using cached data[/yellow]")
   ```

## 🧪 Testing Commands

### Run specific milestone tests
```bash
# Test v5.1 preservation
pytest tests/test_v5_preservation.py -v

# Test data layer
pytest tests/test_job_manager.py -v

# Test API integration (with mocking)
pytest tests/test_teamtailor_client.py -v

# Full test suite
pytest tests/ --cov=clui --cov-report=term-missing
```

### Manual testing
```bash
# Test CLUI launch
python3 clui/jbr.py

# Test job creation via CLI
python3 -c "from clui.job_manager import JobManager; m = JobManager(); print(m.create_job('Test', 'Company', 'Description', 'http://example.com'))"
```

## 🚀 Quick Start for Each Milestone

### Starting a milestone
```bash
# 1. Check dependencies
python dev/v6/dependency_checker.py <milestone_number>

# 2. Read milestone file
cat dev/v6/M<number>_*.md

# 3. Create a git branch
git checkout -b milestone-<number>

# 4. Start implementation following the tasks
```

### Completing a milestone
```bash
# 1. Run validation tests
python dev/v6/validate_milestone.py <number>

# 2. Verify v5.1 preservation
python3 scripts/verify_checksums.py

# 3. Update execution tracker
# Mark all tasks as ✅ in EXECUTION_TRACKER.md

# 4. Create completion marker
touch dev/v6/.milestone_<number>_complete

# 5. Commit and merge
git add -A
git commit -m "Complete Milestone <number>: <description>"
git checkout main
git merge milestone-<number>
```

## 💡 Key Implementation Patterns

### Error Handling Pattern
```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    self.console.print(f"[red]Error: {e}[/red]")
    return self.graceful_fallback()
```

### Graceful Degradation Pattern
```python
# API calls
data = client.fetch_data()
if data is None:
    # Offline mode - use cache or defaults
    data = self.load_cached_data()
    self.console.print("[yellow]Using cached data (offline)[/yellow]")
```

### File Operation Pattern
```python
from pathlib import Path

# Always use Path for file operations
base_path = Path("user_data/jobs")
job_path = base_path / job_id
job_path.mkdir(parents=True, exist_ok=True)

# Always check existence
if not job_path.exists():
    raise FileNotFoundError(f"Job {job_id} not found")
```

### Version Management Pattern
```python
# Creating new version
version_num = len(job['versions']) + 1
version_id = f"v{version_num}"
version_path = job_path / "versions" / version_id
version_path.mkdir(parents=True, exist_ok=True)

# Save version files
(version_path / "content.md").write_text(content)
(version_path / "metadata.json").write_text(json.dumps(metadata, indent=2))
```

## 🎨 Rich Console Patterns

### Menu Display
```python
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt

console = Console()

# Display menu
table = Table(title="Main Menu")
table.add_column("Option", style="cyan")
table.add_column("Description")
table.add_row("1", "Job Management")
table.add_row("2", "Import from TeamTailor")
console.print(table)

# Get choice
choice = IntPrompt.ask("Select option", choices=["1", "2"])
```

### Status Messages
```python
# Success
console.print("[green]✓[/green] Job created successfully")

# Warning
console.print("[yellow]⚠[/yellow] API unavailable, using offline mode")

# Error
console.print("[red]✗[/red] Failed to save job")

# Info
console.print("[blue]ℹ[/blue] Loading job data...")
```

## 📊 Performance Considerations

- **File I/O**: Cache frequently accessed data in memory
- **API Calls**: Implement rate limiting and caching
- **v5.1 Engine**: Single-threaded, expect 10-30s per optimization
- **Search**: Index job titles and companies for fast lookup
- **Startup**: Lazy-load components to improve launch time

## 🔗 External Dependencies

```python
# requirements.txt
pydantic>=2.0.0      # Data validation
rich>=13.0.0         # Terminal UI
requests>=2.28.0     # API calls
python-dateutil>=2.8.0  # Date handling
pytest>=7.0.0        # Testing
pytest-cov>=4.0.0    # Coverage
python-dotenv>=1.0.0 # Environment variables
```

## 📚 Additional Resources

- Design v5.1 Analysis: `IBJobRefresher/design_v5.1_analysis.md`
- Design v6.0 Simplified: `IBJobRefresher/design_v6.0_simplified.md`
- Milestone Details: `dev/v6/M*.md`
- Execution Tracker: `dev/v6/EXECUTION_TRACKER.md`
- Dependency Checker: `dev/v6/DEPENDENCY_CHECKER.md`

---

*Quick Reference v1.0 - Keep this file open while implementing*