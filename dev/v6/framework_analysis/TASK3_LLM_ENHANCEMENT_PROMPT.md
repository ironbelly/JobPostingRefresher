# Task 3: LLM Prompt for .gfdocs Framework Enhancement

## System Instructions for Enhancement Agent

You are an expert framework architect tasked with enhancing the .gfdocs task generation system to produce output quality matching or exceeding SuperClaude's effectiveness. You have been provided with comprehensive analysis documents and must now implement specific enhancements to achieve this goal.

---

## YOUR MISSION

Transform the .gfdocs framework from its current checklist-based approach to a sophisticated task generation system that produces clear, granular, executable instructions requiring zero ambiguity or guesswork from executing agents.

## CONTEXT DOCUMENTS

You have access to:
1. **TASK1_ANALYSIS_ROADMAP.md** - Detailed analysis of both frameworks with identified differentiators
2. **TASK2_CONTEXT_REFERENCE.md** - Comprehensive reference guide with patterns and examples
3. **Existing .gfdocs structure** at `/config/workspace/JobPostingRefresher/.gfdoc/`
4. **SuperClaude examples** at `/config/workspace/JobPostingRefresher/dev/v6/M*.md`

## ENHANCEMENT OBJECTIVES

### Primary Goal
Enhance .gfdocs to generate task lists with:
- **100% Execution Clarity**: Every task executable without interpretation
- **Complete Context**: All necessary information embedded inline
- **Progressive Validation**: Multi-layer verification at each stage
- **Zero Ambiguity**: No room for agent confusion or questions
- **Scalable Hierarchy**: Support for complex, multi-phase projects

### Success Criteria
The enhanced framework must:
1. Generate tasks with executable commands, not descriptions
2. Embed all necessary context within each task
3. Include validation steps at multiple points
4. Support parallel execution where applicable
5. Maintain backward compatibility with existing .gfdocs workflows

---

## IMPLEMENTATION TASKS

### Phase 1: Core Enhancement Implementation

#### Task 1.1: Create Milestone Structure System
**Location**: `/config/workspace/JobPostingRefresher/.gfdoc/rules/prompts/milestone_structure.md`

Create a new prompt component that adds milestone organization to task generation:

```markdown
# Milestone Structure Template

## Milestone Format
Each major phase becomes a milestone with:
- Clear objective and purpose
- Explicit success criteria
- Dependency declarations
- Grouped related tasks
- Validation suite

## Template Structure
```yaml
milestone:
  id: "M{number}"
  title: "{clear_objective}"
  purpose: "{specific_goal}"
  success_criteria:
    - "{measurable_outcome_1}"
    - "{measurable_outcome_2}"
  dependencies:
    - required: ["{milestone_id}"]
    - optional: ["{milestone_id}"]
  tasks:
    - id: "{milestone}.{task_number}"
      title: "{specific_action}"
      type: "executable|validation|checkpoint"
```

## Integration Instructions
1. Identify major phases in the task
2. Group related checklist items into milestones
3. Add dependency relationships
4. Include validation criteria
```

#### Task 1.2: Implement Command Template System
**Location**: `/config/workspace/JobPostingRefresher/.gfdoc/rules/prompts/command_templates.md`

Add executable command generation to replace descriptive tasks:

```python
# Command Template Generator

def enhance_task_with_commands(task_description, context):
    """
    Transform descriptive task into executable commands
    """
    template = f"""
### Original Task
{task_description}

### Executable Implementation
```bash
# Pre-execution verification
{generate_prerequisites(task_description)}

# Main execution commands
{extract_commands(task_description, context)}

# Post-execution validation
{generate_validation(task_description)}
```

### Verification
- [ ] Prerequisites met: {list_prerequisites()}
- [ ] Commands executed successfully
- [ ] Validation passed: {validation_criteria()}
"""
    return template

def generate_prerequisites(task):
    """Generate pre-flight checks"""
    checks = []
    if "file" in task:
        checks.append("[ -f {file} ] && echo '✅ File exists' || echo '❌ File missing'")
    if "directory" in task:
        checks.append("[ -d {dir} ] && echo '✅ Directory exists' || echo '❌ Directory missing'")
    return "\n".join(checks)

def extract_commands(task, context):
    """Extract or generate executable commands"""
    # Analyze task description
    # Reference context for specifics
    # Generate appropriate commands
    pass

def generate_validation(task):
    """Create validation commands"""
    # Based on task outcome
    # Generate verification steps
    pass
```

#### Task 1.3: Enhance Interview Process
**Location**: `/config/workspace/JobPostingRefresher/.gfdoc/templates/enhanced_interview_template.md`

Upgrade the ibtaskbuilder interview to capture more granular information:

```markdown
# Enhanced IB Task Builder Interview

## Stage 1: Core Intent (Existing)
[Keep existing questions]

## Stage 2: Technical Specification (NEW)
### Commands and Tools
- What specific commands/tools will be used?
- What are the exact file paths involved?
- What validation commands confirm success?

### Dependencies and Prerequisites
- What must exist before this task?
- What other tasks can run in parallel?
- What are the rollback procedures?

### Context Requirements
- What documentation is needed inline?
- What examples should be provided?
- What error cases should be handled?

## Stage 3: Validation Criteria (ENHANCED)
### Success Metrics
- How do we verify each step succeeded?
- What are the expected outputs?
- What tests confirm correctness?

### Error Handling
- What errors are anticipated?
- What are the recovery procedures?
- When should the task abort vs retry?
```

#### Task 1.4: Create Validation Framework
**Location**: `/config/workspace/JobPostingRefresher/.gfdoc/rules/validation_framework.md`

Implement multi-layer validation system:

```markdown
# Validation Framework

## Validation Layers

### Layer 1: Pre-Execution Validation
Before any task execution:
```bash
# Check prerequisites
validate_prerequisites() {
    echo "Checking prerequisites..."
    # File existence
    # Permission verification
    # Dependency completion
    # Resource availability
}
```

### Layer 2: Inline Validation
During task execution:
```bash
# Validate each step
execute_with_validation() {
    command || { echo "Failed: $command"; exit 1; }
    validate_output
}
```

### Layer 3: Post-Execution Testing
After task completion:
```bash
# Comprehensive verification
run_validation_suite() {
    test_file_creation
    test_content_validity
    test_integration_points
    test_performance_metrics
}
```

### Layer 4: Integration Validation
System-wide coherence:
```bash
# Integration tests
validate_system_integration() {
    check_cross_component_compatibility
    verify_data_flow
    test_end_to_end_scenarios
}
```
```

### Phase 2: Prompt System Enhancement

#### Task 2.1: Upgrade Worker Prompts
**Location**: `/config/workspace/JobPostingRefresher/.gfdoc/rules/prompts/enhanced_worker_prompt.md`

Transform the worker prompt to handle enhanced task structure:

```markdown
# Enhanced Worker Prompt

## Role Evolution
You are a precision task executor working with enhanced, milestone-based task structures containing executable commands and inline validation.

## New Capabilities
1. **Command Execution**: Run provided bash/code blocks exactly as specified
2. **Inline Validation**: Execute verification commands after each step
3. **Milestone Awareness**: Understand task relationships and dependencies
4. **Parallel Processing**: Identify and execute concurrent tasks
5. **Checkpoint Management**: Create rollback points before critical operations

## Execution Protocol

### For Each Milestone
1. Verify all dependencies are met
2. Review success criteria
3. Execute tasks in dependency order
4. Run validation suite
5. Create milestone completion marker

### For Each Task
1. **Read Executable Block**
   - Identify command blocks marked with ```bash```
   - Note validation commands
   - Understand expected outputs

2. **Execute Precisely**
   ```bash
   # Run exactly as provided
   {command_from_task}

   # Capture output
   OUTPUT=$(command_from_task)

   # Validate immediately
   {validation_command}
   ```

3. **Verify Success**
   - Check exit codes
   - Validate output format
   - Confirm file creation/modification
   - Run provided tests

4. **Document Evidence**
   - Capture command outputs
   - Screenshot results if applicable
   - Note any deviations
   - Record validation results

## Enhanced Handoff Format
```yaml
milestone: M{number}
milestone_status: complete|partial|blocked
tasks_completed:
  - task_id: {milestone.task}
    commands_executed: [list]
    validation_results: [pass|fail]
    evidence: {output_capture}
dependencies_verified: [list]
next_milestone_ready: boolean
rollback_points_created: [list]
```
```

#### Task 2.2: Enhance QA Prompts
**Location**: `/config/workspace/JobPostingRefresher/.gfdoc/rules/prompts/enhanced_qa_prompt.md`

Upgrade QA to validate enhanced task execution:

```markdown
# Enhanced QA Validation Prompt

## Expanded Validation Scope

### Command Verification
- Were exact commands executed as specified?
- Do outputs match expected results?
- Are all validation commands passing?

### Milestone Validation
- Are all milestone dependencies satisfied?
- Do outcomes meet success criteria?
- Is system state consistent with expectations?

### Evidence Assessment
- Is execution evidence complete?
- Are validation results documented?
- Can execution be reproduced?

## Multi-Layer QA Protocol

### Layer 1: Execution Accuracy
```python
def validate_execution_accuracy(handoff):
    """Verify commands were executed exactly as specified"""
    for task in handoff.tasks_completed:
        assert task.commands_executed == task.specified_commands
        assert task.exit_codes == 0
        assert task.validation_results == "pass"
```

### Layer 2: Output Validation
```python
def validate_outputs(handoff):
    """Verify outputs match expectations"""
    for task in handoff.tasks_completed:
        assert file_exists(task.expected_files)
        assert content_matches(task.expected_content)
        assert metrics_within_bounds(task.performance_metrics)
```

### Layer 3: Integration Testing
```python
def validate_integration(milestone):
    """Verify milestone integration"""
    assert dependencies_resolved(milestone)
    assert system_coherent(milestone)
    assert can_proceed_to_next(milestone)
```
```

### Phase 3: Output Generation Enhancement

#### Task 3.1: Create Enhanced Task Generator
**Location**: `/config/workspace/JobPostingRefresher/.gfdoc/scripts/enhanced_task_generator.py`

Build the enhanced task generation system:

```python
#!/usr/bin/env python3
"""
Enhanced Task Generator for .gfdocs Framework
Produces SuperClaude-quality task lists with executable precision
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Milestone:
    id: str
    title: str
    purpose: str
    success_criteria: List[str]
    dependencies: Dict[str, List[str]]
    tasks: List['Task']
    validation_tests: List['ValidationTest']

@dataclass
class Task:
    id: str
    title: str
    description: str
    commands: List[str]
    validation: List[str]
    context: Dict[str, str]
    prerequisites: List[str]
    outputs: List[str]
    can_parallel: bool = False

@dataclass
class ValidationTest:
    id: str
    description: str
    commands: List[str]
    expected_result: str

class EnhancedTaskGenerator:
    def __init__(self, interview_data: Dict):
        self.interview_data = interview_data
        self.milestones = []

    def generate(self) -> str:
        """Generate enhanced task list from interview data"""
        self._extract_milestones()
        self._enhance_tasks()
        self._add_validation()
        self._identify_parallelization()
        return self._format_output()

    def _extract_milestones(self):
        """Convert phases to milestone structure"""
        for phase in self.interview_data.get('phases', []):
            milestone = Milestone(
                id=f"M{phase['number']}",
                title=phase['title'],
                purpose=phase['description'],
                success_criteria=self._generate_success_criteria(phase),
                dependencies=self._extract_dependencies(phase),
                tasks=[],
                validation_tests=[]
            )
            self.milestones.append(milestone)

    def _enhance_tasks(self):
        """Transform checklist items into executable tasks"""
        for milestone in self.milestones:
            for item in self._get_milestone_items(milestone):
                task = self._create_enhanced_task(item)
                milestone.tasks.append(task)

    def _create_enhanced_task(self, item: Dict) -> Task:
        """Convert checklist item to enhanced task"""
        return Task(
            id=self._generate_task_id(item),
            title=item['description'],
            description=self._enhance_description(item),
            commands=self._generate_commands(item),
            validation=self._generate_validation_commands(item),
            context=self._embed_context(item),
            prerequisites=self._identify_prerequisites(item),
            outputs=self._identify_outputs(item),
            can_parallel=self._check_parallelizable(item)
        )

    def _generate_commands(self, item: Dict) -> List[str]:
        """Generate executable commands for task"""
        commands = []

        # Analyze task description
        if 'create' in item['description'].lower():
            commands.extend(self._generate_creation_commands(item))
        elif 'modify' in item['description'].lower():
            commands.extend(self._generate_modification_commands(item))
        elif 'test' in item['description'].lower():
            commands.extend(self._generate_test_commands(item))

        return commands

    def _generate_validation_commands(self, item: Dict) -> List[str]:
        """Generate validation commands for task"""
        validations = []

        # Add file existence checks
        for output in self._identify_outputs(item):
            validations.append(f"[ -f {output} ] && echo '✅ {output} created' || echo '❌ {output} missing'")

        # Add content validation
        if 'json' in str(item.get('outputs', [])):
            validations.append("python -m json.tool {file} > /dev/null && echo '✅ Valid JSON' || echo '❌ Invalid JSON'")

        return validations

    def _format_output(self) -> str:
        """Format enhanced task list as markdown"""
        output = ["# Enhanced Task List - Generated by .gfdocs\n"]
        output.append("## Overview\n")
        output.append(f"Total Milestones: {len(self.milestones)}\n")
        output.append(f"Total Tasks: {sum(len(m.tasks) for m in self.milestones)}\n\n")

        for milestone in self.milestones:
            output.append(self._format_milestone(milestone))

        return "\n".join(output)

    def _format_milestone(self, milestone: Milestone) -> str:
        """Format individual milestone"""
        return f"""
## {milestone.id}: {milestone.title}

### Purpose
{milestone.purpose}

### Success Criteria
{chr(10).join(f"- {criterion}" for criterion in milestone.success_criteria)}

### Dependencies
- Required: {', '.join(milestone.dependencies.get('required', ['None']))}
- Optional: {', '.join(milestone.dependencies.get('optional', ['None']))}

### Tasks
{self._format_tasks(milestone.tasks)}

### Validation Tests
{self._format_validation_tests(milestone.validation_tests)}
"""

    def _format_tasks(self, tasks: List[Task]) -> str:
        """Format task list with executable commands"""
        formatted = []
        for task in tasks:
            formatted.append(f"""
#### {task.id}: {task.title}

**Prerequisites:**
{chr(10).join(f"- {prereq}" for prereq in task.prerequisites)}

**Execution Commands:**
```bash
{chr(10).join(task.commands)}
```

**Validation:**
```bash
{chr(10).join(task.validation)}
```

**Expected Outputs:**
{chr(10).join(f"- {output}" for output in task.outputs)}
""")
        return "\n".join(formatted)

# Integration with existing .gfdocs
def enhance_ibtask_output(task_file_path: str) -> str:
    """Enhance existing .gfdocs task file"""
    task_data = parse_existing_task(task_file_path)
    generator = EnhancedTaskGenerator(task_data)
    enhanced_output = generator.generate()
    return enhanced_output
```

### Phase 4: Integration and Testing

#### Task 4.1: Create Integration Tests
**Location**: `/config/workspace/JobPostingRefresher/.gfdoc/tests/enhancement_tests.py`

```python
#!/usr/bin/env python3
"""
Test suite for .gfdocs enhancement validation
"""

import pytest
from pathlib import Path

class TestEnhancementQuality:
    def test_command_generation(self):
        """Verify commands are executable not descriptive"""
        enhanced_task = generate_enhanced_task("Create configuration file")
        assert "touch" in enhanced_task.commands or "cat >" in enhanced_task.commands
        assert "Create" not in enhanced_task.commands  # Should not be descriptive

    def test_validation_inclusion(self):
        """Verify validation steps are included"""
        enhanced_task = generate_enhanced_task("Create test.json")
        assert any("[ -f test.json ]" in cmd for cmd in enhanced_task.validation)

    def test_context_embedding(self):
        """Verify context is embedded inline"""
        enhanced_task = generate_enhanced_task("Implement API endpoint")
        assert enhanced_task.context  # Should have context
        assert "reference" not in enhanced_task.context  # Should not reference external

    def test_milestone_structure(self):
        """Verify milestone hierarchy is created"""
        milestones = generate_milestones(sample_interview_data)
        assert all(m.dependencies is not None for m in milestones)
        assert all(m.success_criteria for m in milestones)

    def test_parallel_identification(self):
        """Verify parallel tasks are identified"""
        tasks = generate_tasks_from_checklist(sample_checklist)
        parallel_tasks = [t for t in tasks if t.can_parallel]
        assert len(parallel_tasks) > 0  # Should identify some parallel tasks

    def test_output_quality_metrics(self):
        """Verify output meets quality targets"""
        enhanced_output = enhance_task_list(original_task_list)

        # Clarity score: % of tasks with executable commands
        clarity_score = calculate_clarity_score(enhanced_output)
        assert clarity_score >= 0.9  # 90% clarity target

        # Context score: % of tasks with inline context
        context_score = calculate_context_score(enhanced_output)
        assert context_score >= 0.85  # 85% context target

        # Validation score: % of tasks with verification
        validation_score = calculate_validation_score(enhanced_output)
        assert validation_score >= 0.8  # 80% validation target
```

#### Task 4.2: Create Migration Script
**Location**: `/config/workspace/JobPostingRefresher/.gfdoc/scripts/migrate_to_enhanced.sh`

```bash
#!/bin/bash
# Migration script for .gfdocs enhancement

echo "Starting .gfdocs Enhancement Migration"
echo "======================================="

# Backup existing system
backup_dir=".gfdoc_backup_$(date +%Y%m%d_%H%M%S)"
echo "Creating backup at $backup_dir..."
cp -r .gfdoc "$backup_dir"

# Install enhanced components
echo "Installing enhanced components..."
cp framework_analysis/enhanced_*.md .gfdoc/rules/prompts/
cp framework_analysis/enhanced_task_generator.py .gfdoc/scripts/
chmod +x .gfdoc/scripts/enhanced_task_generator.py

# Update configuration
echo "Updating configuration..."
cat >> .gfdoc/config.yaml << EOF
# Enhancement Configuration
enhancement:
  enabled: true
  command_templates: true
  milestone_structure: true
  inline_validation: true
  parallel_marking: true
  context_embedding: true
EOF

# Run tests
echo "Running enhancement tests..."
python -m pytest .gfdoc/tests/enhancement_tests.py

if [ $? -eq 0 ]; then
    echo "✅ Enhancement migration successful!"
else
    echo "❌ Tests failed. Rolling back..."
    rm -rf .gfdoc
    mv "$backup_dir" .gfdoc
    exit 1
fi

echo "Migration complete. Enhanced .gfdocs ready for use."
```

### Phase 5: Documentation and Training

#### Task 5.1: Create Enhancement Documentation
**Location**: `/config/workspace/JobPostingRefresher/.gfdoc/docs/ENHANCEMENT_GUIDE.md`

```markdown
# .gfdocs Enhancement Guide

## Overview
This guide documents the enhancements made to achieve SuperClaude-level task generation quality.

## New Features

### 1. Milestone Structure
Tasks are now organized into hierarchical milestones with:
- Clear objectives
- Explicit dependencies
- Success criteria
- Validation suites

### 2. Command Templates
All tasks include:
- Executable bash/code commands
- No interpretation required
- Direct copy-paste execution

### 3. Inline Validation
Multi-layer verification:
- Pre-execution checks
- Inline validation
- Post-execution tests
- Integration verification

### 4. Context Embedding
All necessary context included:
- No external references needed
- Examples provided inline
- Complete information for execution

### 5. Parallel Execution Support
Tasks marked for concurrent execution:
- Dependency analysis
- Parallel markers
- Synchronization points

## Usage Examples

### Enhanced Task Example
```markdown
#### Task 2.3: Create API Client
**Prerequisites:**
- Python environment activated
- requests library installed

**Execution Commands:**
```bash
# Create client file
cat > api_client.py << 'EOF'
import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        return requests.get(f"{self.base_url}/{endpoint}")
EOF

# Validate syntax
python -m py_compile api_client.py
```

**Validation:**
```bash
# File exists
[ -f api_client.py ] && echo "✅ File created" || echo "❌ File missing"

# Valid Python
python -c "import api_client" && echo "✅ Valid Python" || echo "❌ Syntax error"
```
```

## Migration Path
1. Run migration script
2. Test with sample task
3. Compare output quality
4. Deploy incrementally
5. Monitor metrics
```

---

## EXECUTION INSTRUCTIONS

### Step 1: Analyze Current State
1. Review the existing .gfdocs framework at `/config/workspace/JobPostingRefresher/.gfdoc/`
2. Examine the SuperClaude examples at `/config/workspace/JobPostingRefresher/dev/v6/M*.md`
3. Read the analysis documents in `framework_analysis/`

### Step 2: Implement Core Enhancements
1. Create the new prompt components as specified
2. Implement the command template system
3. Enhance the interview process
4. Build the validation framework

### Step 3: Upgrade Prompt System
1. Enhance worker prompts with new capabilities
2. Upgrade QA prompts for enhanced validation
3. Test with sample tasks

### Step 4: Build Generation System
1. Implement the enhanced task generator
2. Create integration tests
3. Build migration script

### Step 5: Validate and Deploy
1. Run comprehensive tests
2. Measure quality metrics
3. Deploy with migration script
4. Document and train

## SUCCESS METRICS

Your enhancement is successful when:
1. **Clarity Score** ≥ 90% - Tasks executable without interpretation
2. **Context Score** ≥ 85% - Tasks contain all necessary information
3. **Validation Score** ≥ 80% - Tasks include verification steps
4. **Success Rate** ≥ 95% - First-attempt task completion
5. **Efficiency Gain** ≥ 30% - Reduction in execution time

## VALIDATION CHECKLIST

Before declaring success, verify:
- [ ] All tasks contain executable commands, not descriptions
- [ ] Context is embedded inline, not referenced externally
- [ ] Validation steps are included at multiple layers
- [ ] Dependencies and prerequisites are explicit
- [ ] Parallel execution opportunities are marked
- [ ] Error handling and recovery procedures are included
- [ ] The framework maintains backward compatibility
- [ ] Quality metrics meet or exceed targets
- [ ] Documentation is complete and clear
- [ ] Tests pass comprehensively

---

## REMEMBER

The goal is not just to match SuperClaude's quality, but to create a framework that:
- Eliminates ALL ambiguity in task execution
- Provides COMPLETE context for every operation
- Enables PERFECT execution on first attempt
- Scales ELEGANTLY with project complexity
- Maintains SIMPLICITY in its interface

Your enhanced .gfdocs framework should enable any LLM to execute complex projects with the same precision and clarity as a human expert following detailed instructions.