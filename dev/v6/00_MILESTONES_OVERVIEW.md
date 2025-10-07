# JobRefresher v6.0 Development Milestones Overview

## Milestone Structure

Each milestone is a self-contained development unit that can be:
- Executed independently (with dependencies noted)
- Tested in isolation
- Validated before proceeding
- Rolled back if needed

## Execution Order

### Foundation Track (Required First)
1. **M1_PROJECT_FOUNDATION** - Core setup and v5.1 preservation
2. **M2_DATA_LAYER** - Job management system

### Integration Track (Parallel Possible)
3. **M3_API_INTEGRATION** - TeamTailor connectivity
4. **M4_ENGINE_WRAPPER** - PD-SMIS v5.1 integration

### Interface Track
5. **M5_CLUI_CORE** - Basic interactive interface
6. **M6_CLUI_FEATURES** - Enhanced user experience

### Quality Track
7. **M7_TESTING_FRAMEWORK** - Preservation and validation
8. **M8_FINAL_INTEGRATION** - Polish and release prep

## Milestone File Structure

Each milestone file contains:
- **Purpose**: Clear objective and success criteria
- **Dependencies**: Required prior milestones
- **Start Procedure**: Pre-flight checks and setup
- **Tasks**: Numbered, granular implementation steps
- **Validation Tests**: Specific tests to verify completion
- **Completion Procedure**: Final checks and handoff
- **Rollback Plan**: How to undo if needed

## Execution Guidelines for LLMs

1. **Always complete Start Procedure first**
2. **Execute tasks in exact numerical order**
3. **Run validation after EVERY 5 tasks**
4. **Document any deviations in `/dev/v6/execution_log.md`**
5. **Complete ALL validation tests before marking milestone done**
6. **Never skip Completion Procedure**

## Critical Rules

- **NEVER modify files in `/IBJobRefresher/`** - Core v5.1 must remain intact
- **All new code in `/clui/`** - Maintain separation
- **User data in `/user_data/`** - Never commit this directory
- **Test preservation after EACH milestone** - Ensure v5.1 integrity
- **Create checkpoints** - Git commit after each milestone completion

## Quick Status Check Commands

```bash
# Check milestone completion
ls -la /dev/v6/*.COMPLETE

# Verify v5.1 preservation
md5sum IBJobRefresher/phases/*.md > /tmp/v5_checksums.txt
diff /tmp/v5_checksums.txt dev/v6/v5_baseline_checksums.txt

# Test current functionality
python clui/jbr.py --test-mode

# Check for uncommitted changes
git status
```