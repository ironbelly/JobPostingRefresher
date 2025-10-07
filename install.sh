#!/bin/bash
# JobRefresher v6.0 Installation Script
# Automates setup process with error handling and validation

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
PYTHON_MIN_VERSION="3.8"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   JobRefresher v6.0 Installation     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Function: Print status message
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

# Function: Print success message
print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

# Function: Print error message
print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Function: Print warning message
print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Function: Check Python version
check_python_version() {
    print_status "Checking Python version..."

    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        echo "Please install Python 3.8 or higher from https://python.org"
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]; }; then
        print_error "Python version $PYTHON_VERSION is too old"
        echo "Python $PYTHON_MIN_VERSION or higher is required"
        exit 1
    fi

    print_success "Python $PYTHON_VERSION detected"
}

# Function: Check Git installation
check_git() {
    print_status "Checking Git installation..."

    if ! command -v git &> /dev/null; then
        print_warning "Git is not installed (optional but recommended)"
        echo "Install Git from https://git-scm.com for version control features"
    else
        GIT_VERSION=$(git --version | cut -d' ' -f3)
        print_success "Git $GIT_VERSION detected"
    fi
}

# Function: Create virtual environment
create_virtualenv() {
    print_status "Creating virtual environment..."

    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists"
        read -p "Remove and recreate? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf venv
            print_status "Removed existing virtual environment"
        else
            print_status "Using existing virtual environment"
            return 0
        fi
    fi

    python3 -m venv venv

    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment"
        echo "Try: sudo apt-get install python3-venv (Debian/Ubuntu)"
        exit 1
    fi

    print_success "Virtual environment created"
}

# Function: Activate virtual environment
activate_virtualenv() {
    print_status "Activating virtual environment..."

    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        print_success "Virtual environment activated"
    else
        print_error "Virtual environment activation script not found"
        exit 1
    fi
}

# Function: Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."

    # Upgrade pip first
    python3 -m pip install --upgrade pip > /dev/null 2>&1

    # Install core dependencies
    print_status "Installing core dependencies (rich, prompt-toolkit, requests)..."
    pip install rich prompt-toolkit requests

    if [ $? -ne 0 ]; then
        print_error "Failed to install dependencies"
        exit 1
    fi

    print_success "Core dependencies installed"

    # Install optional dependencies
    print_status "Installing optional dependencies..."
    pip install coverage > /dev/null 2>&1 || print_warning "Coverage not installed (optional)"

    print_success "Dependencies installation complete"
}

# Function: Create directory structure
create_directories() {
    print_status "Creating directory structure..."

    mkdir -p user_data/jobs
    mkdir -p user_data/config
    mkdir -p user_data/logs
    mkdir -p exports
    mkdir -p docs

    print_success "Directory structure created"
}

# Function: Copy configuration templates
setup_config() {
    print_status "Setting up configuration files..."

    # Create TeamTailor config template if it doesn't exist
    TEAMTAILOR_CONFIG="user_data/config/teamtailor_config.json"

    if [ ! -f "$TEAMTAILOR_CONFIG" ]; then
        cat > "$TEAMTAILOR_CONFIG" << 'EOF'
{
  "api_key": "your-api-key-here",
  "company_id": "your-company-id",
  "api_version": "20210218"
}
EOF
        print_success "TeamTailor config template created"
        print_warning "Edit $TEAMTAILOR_CONFIG with your API credentials"
    else
        print_status "TeamTailor config already exists"
    fi
}

# Function: Verify v5.1 preservation
verify_v51_preservation() {
    print_status "Verifying v5.1 PD-SMIS engine preservation..."

    if [ ! -f "scripts/check_v5_preservation.sh" ]; then
        print_warning "Preservation check script not found (optional)"
        return 0
    fi

    bash scripts/check_v5_preservation.sh > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        print_success "v5.1 engine preservation verified"
    else
        print_error "v5.1 engine preservation check failed"
        echo "Run: bash scripts/check_v5_preservation.sh for details"
        exit 1
    fi
}

# Function: Run tests
run_tests() {
    print_status "Running test suite..."

    read -p "Run tests to verify installation? (Y/n): " -n 1 -r
    echo

    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        python3 -m unittest discover tests/ -v

        if [ $? -eq 0 ]; then
            print_success "All tests passed"
        else
            print_error "Some tests failed"
            echo "Review test output above for details"
            read -p "Continue anyway? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
    else
        print_status "Skipping tests"
    fi
}

# Function: Create launcher script
create_launcher() {
    print_status "Creating launcher script..."

    LAUNCHER="jobrefresher"

    cat > "$LAUNCHER" << 'EOF'
#!/bin/bash
# JobRefresher v6.0 Launcher

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Launch application
python3 -m clui "$@"
EOF

    chmod +x "$LAUNCHER"
    print_success "Launcher script created: ./$LAUNCHER"
}

# Function: Display completion message
display_completion() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   Installation Complete! 🎉           ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo ""
    echo -e "  1. ${GREEN}Activate virtual environment:${NC}"
    echo -e "     ${YELLOW}source venv/bin/activate${NC}"
    echo ""
    echo -e "  2. ${GREEN}Configure TeamTailor (optional):${NC}"
    echo -e "     ${YELLOW}nano user_data/config/teamtailor_config.json${NC}"
    echo ""
    echo -e "  3. ${GREEN}Launch JobRefresher:${NC}"
    echo -e "     ${YELLOW}./jobrefresher${NC}"
    echo -e "     or"
    echo -e "     ${YELLOW}python3 -m clui${NC}"
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo -e "  - User Manual:     ${YELLOW}docs/USER_MANUAL.md${NC}"
    echo -e "  - Quick Reference: ${YELLOW}docs/QUICK_REFERENCE.md${NC}"
    echo -e "  - README:          ${YELLOW}README.md${NC}"
    echo ""
    echo -e "${BLUE}Support:${NC}"
    echo -e "  - Run tests:       ${YELLOW}python3 -m unittest discover tests/ -v${NC}"
    echo -e "  - Check coverage:  ${YELLOW}bash tests/check_coverage.sh${NC}"
    echo ""
}

# Main installation flow
main() {
    echo "Starting installation process..."
    echo ""

    # Change to project directory
    cd "$PROJECT_DIR"

    # Run installation steps
    check_python_version
    check_git
    create_virtualenv
    activate_virtualenv
    install_dependencies
    create_directories
    setup_config
    verify_v51_preservation
    run_tests
    create_launcher

    # Display completion message
    display_completion
}

# Run main installation
main

exit 0
