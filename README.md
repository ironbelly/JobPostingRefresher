# JobRefresher v6.0

AI-Powered Job Posting Optimization System with Interactive CLI Interface

## Overview

JobRefresher v6.0 combines the proven PD-SMIS v5.1 optimization engine with a modern interactive command-line interface (CLUI), multi-job management, and TeamTailor API integration.

### Key Features

- **Interactive CLUI**: Menu-driven interface for easy navigation
- **Multi-Job Management**: Handle multiple job postings with version control
- **TeamTailor Integration**: Automatic job import and metrics synchronization
- **PD-SMIS v5.1 Engine**: Preserved optimization engine with 14-layer validation
- **Batch Processing**: Optimize multiple jobs simultaneously
- **Performance Dashboard**: Track metrics and improvements
- **Version Comparison**: Compare different job versions
- **Export Options**: Multiple export formats (Markdown, JSON, HTML, Text)

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for version control)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourorg/JobPostingRefresher.git
cd JobPostingRefresher
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install rich prompt-toolkit requests  # Optional: pip install -r requirements.txt if available
```

4. **Configure TeamTailor (optional):**
```bash
cp config/teamtailor_config.json.example user_data/config/teamtailor_config.json
# Edit user_data/config/teamtailor_config.json with your API credentials
```

5. **Launch the application:**
```bash
python3 -m clui
# Or directly: python3 clui/jbr.py
```

## Usage Guide

### Main Menu Navigation

When you launch JobRefresher, you'll see the main menu:

- **[1] Job Management** - Create, view, import, and search jobs
- **[2] Job Processing** - Optimize single or multiple jobs
- **[3] TeamTailor Integration** - Sync jobs and metrics
- **[Q] Quit** - Exit the application

### Creating a Job

1. Select `[1] Job Management` from main menu
2. Choose `Create New Job`
3. Enter job title, company name, and raw job posting content
4. Job is saved with unique ID

### Optimizing a Job

1. From Job Management, select a job
2. Choose optimization option
3. Watch the optimization phases progress
4. Review validation report
5. New optimized version is created automatically

### Importing from TeamTailor

1. Configure TeamTailor API credentials first (optional)
2. From TeamTailor Integration menu
3. Choose import option:
   - Import specific job by ID
   - Batch import jobs

### Batch Processing

1. Select `[2] Job Processing` from main menu
2. Choose `Batch Process Jobs`
3. Select filter criteria or process all
4. Monitor progress
5. Review results

## Architecture

### Directory Structure

```
JobPostingRefresher/
├── IBJobRefresher/        # v5.1 PD-SMIS engine (preserved, DO NOT MODIFY)
├── clui/                  # Command-line UI components
│   ├── __init__.py
│   ├── __main__.py       # Module entry point
│   ├── jbr.py            # Main CLUI application
│   ├── job_manager.py    # Job data management
│   ├── teamtailor_client.py  # TeamTailor API integration
│   └── pd_smis_engine.py # v5.1 engine wrapper
├── user_data/            # User data (git-ignored)
│   ├── config/          # Configuration files
│   └── jobs/            # Job storage
├── tests/               # Test suite
│   ├── unit/           # Unit tests
│   ├── test_integration_complete.py
│   ├── test_performance.py
│   ├── test_regression.py
│   ├── test_v5_preservation_final.py
│   ├── run_ci_tests.sh
│   └── check_coverage.sh
├── scripts/             # Utility scripts
│   └── check_v5_preservation.sh
├── exports/            # Export output
└── dev/v6/            # Development documentation
```

### Data Storage

Jobs are stored in `user_data/jobs/` with this structure:

```
user_data/jobs/
└── job_id/
    ├── metadata.json        # Job metadata
    ├── raw_posting.txt      # Original content
    ├── versions/            # Version history
    │   ├── v1.json
    │   └── v2.json
    └── exports/            # Exported files
```

## Configuration

### TeamTailor API (Optional)

Edit `user_data/config/teamtailor_config.json`:

```json
{
  "api_key": "your-api-key-here",
  "company_id": "your-company-id",
  "api_version": "20210218"
}
```

Get your API key from TeamTailor Settings > API & Webhooks.

## Testing

Run the test suite:

```bash
# Run all tests
python3 -m unittest discover tests/ -v

# Run specific test categories
python3 -m unittest tests.unit.test_job_manager -v        # Data layer tests
python3 -m unittest tests.test_integration_complete -v    # Integration tests
python3 -m unittest tests.test_performance -v             # Performance tests
python3 -m unittest tests.test_v5_preservation_final -v   # Preservation tests

# Run CI/CD test suite
bash tests/run_ci_tests.sh

# Check test coverage
bash tests/check_coverage.sh
```

## Development

### Adding New Features

1. Create feature branch: `git checkout -b feature/your-feature`
2. Implement in appropriate module (clui/*.py)
3. Add tests in tests/
4. Run full test suite
5. Create pull request

### Important Notes

- **NEVER modify files in IBJobRefresher/** - This preserves the v5.1 engine
- All new code goes in `clui/` directory
- User data in `user_data/` is git-ignored
- Run `bash scripts/check_v5_preservation.sh` regularly to verify v5.1 integrity

## Troubleshooting

### Common Issues

**TeamTailor connection fails:**
- Check API key in user_data/config/teamtailor_config.json
- Verify internet connection
- System works without TeamTailor (graceful degradation)

**Optimization not available:**
- Ensure PD-SMIS engine files exist in IBJobRefresher/
- Check for error messages in console
- Run preservation check: `bash scripts/check_v5_preservation.sh`

**Jobs not persisting:**
- Verify user_data/jobs/ directory exists
- Check file permissions
- Ensure adequate disk space

**Tests failing:**
- Ensure working directory is project root
- Check Python version (3.8+ required)
- Verify all dependencies installed

## Support

For issues, questions, or contributions:
- GitHub Issues: [Report issues]
- Documentation: See docs/ for detailed guides
- Tests: See tests/ for test examples

## License

[Your License Here]

## Credits

Built on the PD-SMIS v5.1 optimization engine.
v6.0 enhancements: Interactive CLUI, multi-job management, TeamTailor integration.

## Version History

- **v6.0.0** - Interactive CLUI, multi-job management, TeamTailor integration
- **v5.1.0** - PD-SMIS optimization engine baseline

---

For detailed documentation about the v5.1 engine and its optimization methodology, see `IBJobRefresher/` directory.
