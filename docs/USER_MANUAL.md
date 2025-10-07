# JobRefresher v6.0 User Manual

## Table of Contents

1. [Getting Started](#getting-started)
2. [Job Management](#job-management)
3. [Optimization Process](#optimization-process)
4. [TeamTailor Integration](#teamtailor-integration)
5. [Analytics & Reporting](#analytics--reporting)
6. [Tips & Best Practices](#tips--best-practices)
7. [Keyboard Shortcuts](#keyboard-shortcuts)

---

## Getting Started

### First Launch

1. **Start the application:**
   ```bash
   python3 -m clui
   # Or directly:
   python3 clui/jbr.py
   ```

2. **Main Menu Overview:**
   ```
   ╔════════════════════════════════════════╗
   ║     JobRefresher v6.0 Main Menu       ║
   ╠════════════════════════════════════════╣
   ║  [1] Job Management                   ║
   ║  [2] Job Processing                   ║
   ║  [3] TeamTailor Integration           ║
   ║  [Q] Quit                             ║
   ╚════════════════════════════════════════╝
   ```

3. **Navigation:**
   - Enter the number of your choice (e.g., `1` for Job Management)
   - Press `Q` to quit at any menu
   - Press `B` to go back to the previous menu

### Understanding Job Storage

Jobs are stored in `user_data/jobs/` with this structure:

```
user_data/jobs/
└── job_12345/
    ├── metadata.json        # Job information (title, company, dates)
    ├── raw_posting.txt      # Original job posting content
    ├── versions/            # Optimization history
    │   ├── v1.json         # First optimization
    │   ├── v2.json         # Second optimization
    │   └── v3.json         # Third optimization
    └── exports/            # Exported files
        ├── job_12345.json
        ├── job_12345.md
        └── job_12345.html
```

---

## Job Management

### Creating a New Job

1. From Main Menu, select `[1] Job Management`
2. Select `[1] Create New Job`
3. Enter the following information:
   - **Job Title**: The position name (e.g., "Senior Software Engineer")
   - **Company Name**: The hiring company (e.g., "Acme Corp")
   - **Raw Job Posting**: Paste the complete job posting text

**Example:**
```
Job Title: Senior Software Engineer
Company Name: Acme Corp
Raw Job Posting:
We are seeking a talented Senior Software Engineer to join our growing team.
The ideal candidate will have 5+ years of experience with Python and AWS...
```

4. System generates a unique Job ID (e.g., `job_12345`)
5. Job is saved and ready for optimization

### Viewing Job Details

1. From Job Management menu, select `[2] View Job Details`
2. Enter the Job ID or select from list
3. View comprehensive job information:
   - Basic metadata (title, company, created date)
   - Current status and version
   - Raw posting content
   - Optimization history (if any)

### Searching for Jobs

1. Select `[3] Search Jobs`
2. Choose search criteria:
   - **By Title**: Search job titles (case-insensitive)
   - **By Company**: Find all jobs for a company
   - **By Date Range**: Jobs created within specific timeframe
   - **By Status**: Filter by processing status

**Example Searches:**
```
Search by title: "engineer" → Finds all engineering positions
Search by company: "acme" → All Acme Corp jobs
Search by date: "2024-01-01 to 2024-12-31" → Year 2024 jobs
```

### Importing Jobs

**From File:**
1. Select `[4] Import Job`
2. Choose `[1] Import from File`
3. Provide file path (supports .txt, .md, .json)
4. System extracts job information and creates new job entry

**From TeamTailor:**
1. Select `[4] Import Job`
2. Choose `[2] Import from TeamTailor`
3. Enter TeamTailor Job ID
4. System fetches job details and metrics automatically

### Deleting Jobs

1. Select `[5] Delete Job`
2. Enter Job ID to delete
3. **Confirm deletion** (this is permanent!)
4. System removes job and all associated data

⚠️ **Warning**: Deletion is irreversible. All versions and exports will be lost.

---

## Optimization Process

### Single Job Optimization

1. From Main Menu, select `[2] Job Processing`
2. Choose `[1] Optimize Single Job`
3. Enter Job ID
4. Watch the optimization phases progress:

**Phase Sequence:**
```
[Phase 0] Collection & Analysis     ━━━━━━━━ 100%
[Phase 1] Information Extraction    ━━━━━━━━ 100%
[Phase 2] Hypothesis Generation     ━━━━━━━━ 100%
[Phase 3] Optimization Strategy     ━━━━━━━━ 100%
[Phase 4] Content Generation        ━━━━━━━━ 100%
[Phase 6] Learning Integration      ━━━━━━━━ 100%
[Phase 7] Iterative Refinement      ━━━━━━━━ 100%
```

5. Review validation report:

**Validation Results:**
```
╔═══════════════════════════════════════╗
║     Validation Report                ║
╠═══════════════════════════════════════╣
║  Precision Score:      87.5%  ✓      ║
║  Adversarial Score:    92.0%  ✓      ║
║  Verification Score:   89.3%  ✓      ║
║  Overall Quality:      89.6%  ✓      ║
╚═══════════════════════════════════════╝
```

6. New version automatically created (e.g., v2.json)

### Batch Processing

Process multiple jobs simultaneously:

1. Select `[2] Batch Process Jobs`
2. Choose filter criteria:
   - **All jobs**: Process entire job database
   - **By company**: All jobs for specific company
   - **By date range**: Jobs created within timeframe
   - **From list**: Manually select specific jobs

3. Monitor progress:
```
Batch Processing Progress:
━━━━━━━━━━━━━━━━ 45% (9/20 jobs)

Current: job_12350 - "Marketing Manager"
Status: Phase 3 - Optimization Strategy
```

4. Review batch results summary:
```
Batch Processing Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Jobs:       20
Successful:       18  (90%)
Failed:           2   (10%)
Avg Quality:      88.7%
Total Time:       12m 34s
```

### Version Comparison

Compare different versions of a job:

1. From Job Management, select `[6] Compare Versions`
2. Enter Job ID
3. Select two versions to compare (e.g., v1 vs v3)
4. View side-by-side comparison:

```
╔════════════════════════════════════════╗
║       Version Comparison              ║
╠════════════════════════════════════════╣
║  Version 1          Version 3          ║
║  Quality: 78.5%     Quality: 89.6%     ║
║  Length: 450 words  Length: 420 words  ║
║                                        ║
║  [Content differences highlighted]     ║
╚════════════════════════════════════════╝
```

---

## TeamTailor Integration

### Initial Setup

1. Obtain API credentials from TeamTailor:
   - Log into TeamTailor account
   - Go to Settings → API & Webhooks
   - Generate new API key

2. Configure JobRefresher:
   ```bash
   cp config/teamtailor_config.json.example user_data/config/teamtailor_config.json
   ```

3. Edit `user_data/config/teamtailor_config.json`:
   ```json
   {
     "api_key": "your-api-key-here",
     "company_id": "your-company-id",
     "api_version": "20210218"
   }
   ```

### Importing Jobs from TeamTailor

1. From Main Menu, select `[3] TeamTailor Integration`
2. Choose `[1] Import Jobs`
3. Options:
   - **Single job**: Enter TeamTailor Job ID
   - **Batch import**: Import multiple jobs by criteria
   - **All active jobs**: Import all currently active postings

4. System fetches:
   - Job posting content
   - Application metrics (views, applications, conversion rates)
   - Job metadata (status, categories, locations)

### Syncing Metrics

Keep job metrics up-to-date:

1. Select `[2] Sync Metrics`
2. Choose sync scope:
   - **Single job**: Update metrics for one job
   - **All imported jobs**: Refresh all TeamTailor-sourced jobs
   - **By date range**: Jobs imported within timeframe

3. System updates:
   - View counts
   - Application counts
   - Conversion rates
   - Last modified timestamps

### Pushing Optimized Content

After optimization, push improved content back:

1. Optimize job in JobRefresher
2. Select `[3] Push Optimized Job`
3. Enter Job ID
4. Select version to push (e.g., v3)
5. Confirm push to TeamTailor
6. System updates TeamTailor posting with optimized content

⚠️ **Important**: Review optimized content before pushing to live job posting.

---

## Analytics & Reporting

### Performance Dashboard

View system-wide analytics:

1. From Main Menu, select `[2] Job Processing`
2. Choose `[3] Performance Dashboard`

**Dashboard Sections:**

**Overall Statistics:**
```
╔═══════════════════════════════════════╗
║     Performance Dashboard            ║
╠═══════════════════════════════════════╣
║  Total Jobs:              156         ║
║  Jobs Processed:          142         ║
║  Processing Rate:         91.0%       ║
║  Avg Quality Score:       88.3%       ║
║  Total Processing Time:   8h 23m      ║
╚═══════════════════════════════════════╝
```

**Quality Metrics:**
- Average precision scores
- Average adversarial scores
- Average verification scores
- Quality trends over time

**Processing Efficiency:**
- Average time per job
- Phase-by-phase timing breakdown
- Batch processing statistics

**Top Performing Jobs:**
- Highest quality scores
- Most improved jobs (v1 vs latest)
- Best conversion rates (if TeamTailor data available)

### Exporting Reports

Generate reports for analysis:

1. From Job Management, select `[7] Export Job`
2. Enter Job ID
3. Choose export format:
   - **JSON**: Machine-readable, full data structure
   - **Markdown**: Human-readable, formatted text
   - **HTML**: Web-ready, styled presentation
   - **Text**: Plain text, simple format

4. Files saved to `user_data/jobs/{job_id}/exports/`

**Export Uses:**
- Share optimized postings with team
- Archive job versions
- Import into other systems
- Review optimization improvements

---

## Tips & Best Practices

### Optimization Tips

**1. Start with Good Content**
- Provide complete, detailed original job postings
- Include all requirements, responsibilities, and benefits
- Better input = better optimization results

**2. Iterative Improvement**
- Run optimization multiple times to refine results
- Compare versions to see improvements
- Each iteration builds on previous learnings

**3. Quality Review**
- Always review optimized content before publishing
- Check for accuracy and company voice alignment
- Validate that key requirements are preserved

**4. Batch Processing Strategy**
- Group similar jobs for batch processing
- Process during off-peak hours for better performance
- Review batch results for quality consistency

### System Performance

**1. Regular Maintenance**
- Clean up old job versions periodically
- Archive completed jobs
- Keep exports organized

**2. Backup Strategy**
- `user_data/jobs/` contains all job data
- Regular backups of this directory preserve all work
- Export important jobs in multiple formats

**3. Resource Management**
- Processing time varies by job complexity
- Longer jobs take more time to optimize
- Batch processing uses more system resources

### TeamTailor Integration

**1. API Rate Limits**
- TeamTailor has API rate limits
- System automatically handles rate limiting
- Large batch imports may take longer

**2. Metric Sync Frequency**
- Sync metrics weekly for active jobs
- More frequent syncing for high-traffic postings
- Historical metrics preserved in job versions

**3. Content Pushing**
- Test with non-critical jobs first
- Review optimized content thoroughly
- Keep original versions as backup

---

## Keyboard Shortcuts

### Navigation

| Key | Action |
|-----|--------|
| `1-9` | Select menu option |
| `Q` | Quit current menu |
| `B` | Go back to previous menu |
| `H` | Show help |

### During Processing

| Key | Action |
|-----|--------|
| `Ctrl+C` | Cancel current operation |
| `P` | Pause processing |
| `R` | Resume processing |
| `S` | Show current status |

### Job Management

| Key | Action |
|-----|--------|
| `N` | Create new job |
| `V` | View job details |
| `E` | Export current job |
| `D` | Delete current job |

### Quick Actions

| Key | Action |
|-----|--------|
| `F` | Find/Search jobs |
| `L` | List all jobs |
| `I` | Import job |
| `O` | Optimize current job |

---

## Troubleshooting

### Common Issues

**"Job not found" Error**
- Verify Job ID is correct
- Use search function to find job
- Check that job wasn't deleted

**Optimization Fails**
- Ensure PD-SMIS engine files exist in `IBJobRefresher/`
- Check console for error messages
- Run preservation check: `bash scripts/check_v5_preservation.sh`

**TeamTailor Connection Error**
- Verify API key in `user_data/config/teamtailor_config.json`
- Check internet connection
- Confirm API key is still valid in TeamTailor settings

**Slow Performance**
- Close other applications to free resources
- Process jobs individually instead of batch
- Check available disk space

### Getting Help

**In-Application Help**
- Press `H` at any menu for context-specific help
- View tooltips and descriptions on each screen

**Documentation**
- `README.md` - Installation and overview
- `docs/MIGRATION_GUIDE.md` - Upgrading from v5.1
- `docs/QUICK_REFERENCE.md` - Command reference

**Support Resources**
- GitHub Issues: Report bugs and request features
- Test Suite: Run tests to verify system health

---

## Appendix

### File Locations

| Type | Location |
|------|----------|
| Job Data | `user_data/jobs/` |
| Configuration | `user_data/config/` |
| Exports | `user_data/jobs/{job_id}/exports/` |
| Logs | `user_data/logs/` |

### Version Information

**Current Version**: v6.0.0

**Major Features**:
- Interactive CLUI interface
- Multi-job management with version control
- TeamTailor API integration
- Batch processing capabilities
- Performance analytics dashboard

**Engine Version**: PD-SMIS v5.1 (preserved)

---

**Last Updated**: 2024
**Document Version**: 1.0
