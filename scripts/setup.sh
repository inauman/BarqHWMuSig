#!/bin/bash
# One-click setup script for BarqHWMuSig development environment

# Exit on error
set -e

# Print colored messages
print_green() {
    echo -e "\033[0;32m$1\033[0m"
}

print_yellow() {
    echo -e "\033[0;33m$1\033[0m"
}

print_red() {
    echo -e "\033[0;31m$1\033[0m"
}

# Check if Python 3.14 is installed
check_python() {
    print_yellow "Checking Python version..."
    if command -v python3.14 &> /dev/null; then
        print_green "Python 3.14 is installed."
        PYTHON_CMD="python3.14"
    elif command -v python3 &> /dev/null && python3 --version | grep -q "Python 3.14"; then
        print_green "Python 3.14 is installed."
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null && python --version | grep -q "Python 3.14"; then
        print_green "Python 3.14 is installed."
        PYTHON_CMD="python"
    else
        print_red "Python 3.14 is not installed. Please install Python 3.14.0a5 or later."
        print_yellow "Visit https://www.python.org/downloads/ to download Python 3.14."
        exit 1
    fi
}

# Check if uv is installed
check_uv() {
    print_yellow "Checking if uv is installed..."
    if command -v uv &> /dev/null; then
        print_green "uv is installed."
    else
        print_yellow "uv is not installed. Attempting to install..."
        if command -v pip &> /dev/null; then
            pip install uv
            print_green "uv installed successfully."
        elif command -v brew &> /dev/null; then
            brew install uv
            print_green "uv installed successfully via Homebrew."
        else
            print_red "Could not install uv. Please install it manually:"
            print_yellow "pip install uv"
            print_yellow "or"
            print_yellow "brew install uv (on macOS)"
            exit 1
        fi
    fi
}

# Activate or create virtual environment
setup_venv() {
    print_yellow "Setting up virtual environment..."
    
    # Check if venv directory exists
    if [ -d "venv" ]; then
        print_green "Virtual environment already exists. Activating..."
        
        # Determine the activation script based on OS
        if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
            source venv/bin/activate
        elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
            source venv/Scripts/activate
        else
            print_red "Unsupported OS. Please activate the virtual environment manually."
            exit 1
        fi
    else
        print_yellow "Creating new virtual environment..."
        $PYTHON_CMD -m venv venv
        
        # Activate the virtual environment
        if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
            source venv/bin/activate
        elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
            source venv/Scripts/activate
        else
            print_red "Unsupported OS. Please activate the virtual environment manually."
            exit 1
        fi
        
        print_green "Virtual environment created and activated."
    fi
}

# Install dependencies
install_dependencies() {
    print_yellow "Installing dependencies..."
    
    # Check if pyproject.toml exists
    if [ -f "pyproject.toml" ]; then
        uv pip install -e ".[dev]"
        print_green "Dependencies installed successfully."
    else
        print_red "pyproject.toml not found. Cannot install dependencies."
        exit 1
    fi
}

# Set up pre-commit hooks
setup_precommit() {
    print_yellow "Setting up pre-commit hooks..."
    
    # Check if pre-commit is installed
    if ! command -v pre-commit &> /dev/null; then
        print_yellow "Installing pre-commit..."
        uv pip install pre-commit
    fi
    
    # Install pre-commit hooks
    pre-commit install
    print_green "Pre-commit hooks installed successfully."
}

# Create necessary directories if they don't exist
create_directories() {
    print_yellow "Creating necessary directories..."
    
    # Create directories if they don't exist
    mkdir -p config
    mkdir -p docs/api
    mkdir -p docs/guides
    mkdir -p src/bitcoin_transaction
    mkdir -p src/device_integration
    mkdir -p src/cli
    mkdir -p src/common
    mkdir -p tests/unit
    mkdir -p tests/integration
    mkdir -p tests/security
    mkdir -p demo
    
    print_green "Directories created successfully."
}

# Create example .env file if it doesn't exist
create_env_example() {
    print_yellow "Creating example .env file..."
    
    if [ ! -f "config/.env.example" ]; then
        cat > config/.env.example << EOL
# BarqHWMuSig Environment Configuration

# Bitcoin Network
# Options: mainnet, testnet, regtest
BITCOIN_NETWORK=testnet

# API Endpoints
BITCOIN_API_URL=https://blockstream.info/testnet/api/
BITCOIN_API_KEY=your_api_key_here

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/barqhwmusig.log

# Security
# WARNING: Only use this for testing!
HARDCODED_KEY_ENABLED=false
HARDCODED_KEY_PATH=

# Hardware Devices
YUBIKEY_ENABLED=true
LEDGER_ENABLED=true

# Transaction Settings
DEFAULT_FEE_RATE=5
MAX_FEE_RATE=100
MIN_FEE_RATE=1
EOL
        print_green "Example .env file created at config/.env.example"
    else
        print_green "Example .env file already exists."
    fi
}

# Create example config.json if it doesn't exist
create_config_json() {
    print_yellow "Creating example config.json file..."
    
    if [ ! -f "config/config.json" ]; then
        cat > config/config.json << EOL
{
    "bitcoin": {
        "network": "testnet",
        "api_url": "https://blockstream.info/testnet/api/",
        "fee_estimation": {
            "default_fee_rate": 5,
            "max_fee_rate": 100,
            "min_fee_rate": 1
        }
    },
    "devices": {
        "yubikey": {
            "enabled": true,
            "timeout": 30
        },
        "ledger": {
            "enabled": true,
            "timeout": 30
        },
        "hardcoded_key": {
            "enabled": false,
            "warning": "Only use for testing!"
        }
    },
    "logging": {
        "level": "INFO",
        "file": "logs/barqhwmusig.log",
        "console": true
    },
    "transaction": {
        "confirmation_threshold": 6,
        "monitoring_interval": 60
    }
}
EOL
        print_green "Example config.json file created at config/config.json"
    else
        print_green "Config.json file already exists."
    fi
}

# Create __init__.py files in all source directories
create_init_files() {
    print_yellow "Creating __init__.py files in source directories..."
    
    touch src/__init__.py
    touch src/bitcoin_transaction/__init__.py
    touch src/device_integration/__init__.py
    touch src/cli/__init__.py
    touch src/common/__init__.py
    touch tests/__init__.py
    touch tests/unit/__init__.py
    touch tests/integration/__init__.py
    touch tests/security/__init__.py
    
    print_green "__init__.py files created successfully."
}

# Run tests to verify setup
run_tests() {
    print_yellow "Running tests to verify setup..."
    
    if command -v pytest &> /dev/null; then
        # Check if there are any tests to run
        if [ -d "tests" ] && [ "$(ls -A tests)" ]; then
            pytest
            print_green "Tests completed successfully."
        else
            print_yellow "No tests found. Skipping test execution."
        fi
    else
        print_red "pytest not found. Skipping test execution."
    fi
}

# Main function
main() {
    print_green "=========================================="
    print_green "  BarqHWMuSig Development Setup Script"
    print_green "=========================================="
    
    check_python
    check_uv
    setup_venv
    install_dependencies
    setup_precommit
    create_directories
    create_env_example
    create_config_json
    create_init_files
    run_tests
    
    print_green "=========================================="
    print_green "  Setup completed successfully!"
    print_green "=========================================="
    print_green "Next steps:"
    print_yellow "1. Review the documentation in docs/"
    print_yellow "2. Copy config/.env.example to config/.env and update values"
    print_yellow "3. Start developing!"
    print_green "=========================================="
}

# Run the main function
main 