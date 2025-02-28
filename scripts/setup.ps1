# PowerShell setup script for BarqHWMuSig development environment

# Function to print colored messages
function Write-ColorOutput {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [Parameter(Mandatory=$true)]
        [string]$Color
    )
    
    $originalColor = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $Color
    Write-Output $Message
    $host.UI.RawUI.ForegroundColor = $originalColor
}

# Check if Python 3.14 is installed
function Check-Python {
    Write-ColorOutput "Checking Python version..." "Yellow"
    
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3.14") {
            Write-ColorOutput "Python 3.14 is installed." "Green"
            $script:pythonCmd = "python"
            return $true
        }
        
        $pythonVersion = python3 --version 2>&1
        if ($pythonVersion -match "Python 3.14") {
            Write-ColorOutput "Python 3.14 is installed." "Green"
            $script:pythonCmd = "python3"
            return $true
        }
        
        $pythonVersion = py -3.14 --version 2>&1
        if ($pythonVersion -match "Python 3.14") {
            Write-ColorOutput "Python 3.14 is installed." "Green"
            $script:pythonCmd = "py -3.14"
            return $true
        }
        
        Write-ColorOutput "Python 3.14 is not installed. Please install Python 3.14.0a5 or later." "Red"
        Write-ColorOutput "Visit https://www.python.org/downloads/ to download Python 3.14." "Yellow"
        return $false
    }
    catch {
        Write-ColorOutput "Error checking Python version: $_" "Red"
        Write-ColorOutput "Please install Python 3.14.0a5 or later." "Yellow"
        return $false
    }
}

# Check if uv is installed
function Check-UV {
    Write-ColorOutput "Checking if uv is installed..." "Yellow"
    
    try {
        $null = Get-Command uv -ErrorAction Stop
        Write-ColorOutput "uv is installed." "Green"
        return $true
    }
    catch {
        Write-ColorOutput "uv is not installed. Attempting to install..." "Yellow"
        
        try {
            & $script:pythonCmd -m pip install uv
            Write-ColorOutput "uv installed successfully." "Green"
            return $true
        }
        catch {
            Write-ColorOutput "Could not install uv. Please install it manually:" "Red"
            Write-ColorOutput "pip install uv" "Yellow"
            return $false
        }
    }
}

# Activate or create virtual environment
function Setup-Venv {
    Write-ColorOutput "Setting up virtual environment..." "Yellow"
    
    # Check if venv directory exists
    if (Test-Path -Path "venv") {
        Write-ColorOutput "Virtual environment already exists. Activating..." "Green"
        
        # Activate the virtual environment
        try {
            & .\venv\Scripts\Activate.ps1
            Write-ColorOutput "Virtual environment activated." "Green"
            return $true
        }
        catch {
            Write-ColorOutput "Error activating virtual environment: $_" "Red"
            Write-ColorOutput "Please activate the virtual environment manually: .\venv\Scripts\Activate.ps1" "Yellow"
            return $false
        }
    }
    else {
        Write-ColorOutput "Creating new virtual environment..." "Yellow"
        
        try {
            & $script:pythonCmd -m venv venv
            
            # Activate the virtual environment
            & .\venv\Scripts\Activate.ps1
            
            Write-ColorOutput "Virtual environment created and activated." "Green"
            return $true
        }
        catch {
            Write-ColorOutput "Error creating virtual environment: $_" "Red"
            Write-ColorOutput "Please create and activate the virtual environment manually." "Yellow"
            return $false
        }
    }
}

# Install dependencies
function Install-Dependencies {
    Write-ColorOutput "Installing dependencies..." "Yellow"
    
    # Check if pyproject.toml exists
    if (Test-Path -Path "pyproject.toml") {
        try {
            & uv pip install -e ".[dev]"
            Write-ColorOutput "Dependencies installed successfully." "Green"
            return $true
        }
        catch {
            Write-ColorOutput "Error installing dependencies: $_" "Red"
            return $false
        }
    }
    else {
        Write-ColorOutput "pyproject.toml not found. Cannot install dependencies." "Red"
        return $false
    }
}

# Set up pre-commit hooks
function Setup-Precommit {
    Write-ColorOutput "Setting up pre-commit hooks..." "Yellow"
    
    try {
        $null = Get-Command pre-commit -ErrorAction Stop
    }
    catch {
        Write-ColorOutput "Installing pre-commit..." "Yellow"
        & uv pip install pre-commit
    }
    
    try {
        & pre-commit install
        Write-ColorOutput "Pre-commit hooks installed successfully." "Green"
        return $true
    }
    catch {
        Write-ColorOutput "Error installing pre-commit hooks: $_" "Red"
        return $false
    }
}

# Create necessary directories if they don't exist
function Create-Directories {
    Write-ColorOutput "Creating necessary directories..." "Yellow"
    
    $directories = @(
        "config",
        "docs\api",
        "docs\guides",
        "src\bitcoin_transaction",
        "src\device_integration",
        "src\cli",
        "src\common",
        "tests\unit",
        "tests\integration",
        "tests\security",
        "demo"
    )
    
    foreach ($dir in $directories) {
        if (-not (Test-Path -Path $dir)) {
            New-Item -Path $dir -ItemType Directory -Force | Out-Null
        }
    }
    
    Write-ColorOutput "Directories created successfully." "Green"
    return $true
}

# Create example .env file if it doesn't exist
function Create-EnvExample {
    Write-ColorOutput "Creating example .env file..." "Yellow"
    
    $envPath = "config\.env.example"
    
    if (-not (Test-Path -Path $envPath)) {
        $envContent = @"
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
"@
        
        Set-Content -Path $envPath -Value $envContent
        Write-ColorOutput "Example .env file created at $envPath" "Green"
    }
    else {
        Write-ColorOutput "Example .env file already exists." "Green"
    }
    
    return $true
}

# Create example config.json if it doesn't exist
function Create-ConfigJson {
    Write-ColorOutput "Creating example config.json file..." "Yellow"
    
    $configPath = "config\config.json"
    
    if (-not (Test-Path -Path $configPath)) {
        $configContent = @"
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
"@
        
        Set-Content -Path $configPath -Value $configContent
        Write-ColorOutput "Example config.json file created at $configPath" "Green"
    }
    else {
        Write-ColorOutput "Config.json file already exists." "Green"
    }
    
    return $true
}

# Create __init__.py files in all source directories
function Create-InitFiles {
    Write-ColorOutput "Creating __init__.py files in source directories..." "Yellow"
    
    $initFiles = @(
        "src\__init__.py",
        "src\bitcoin_transaction\__init__.py",
        "src\device_integration\__init__.py",
        "src\cli\__init__.py",
        "src\common\__init__.py",
        "tests\__init__.py",
        "tests\unit\__init__.py",
        "tests\integration\__init__.py",
        "tests\security\__init__.py"
    )
    
    foreach ($file in $initFiles) {
        if (-not (Test-Path -Path $file)) {
            New-Item -Path $file -ItemType File -Force | Out-Null
        }
    }
    
    Write-ColorOutput "__init__.py files created successfully." "Green"
    return $true
}

# Run tests to verify setup
function Run-Tests {
    Write-ColorOutput "Running tests to verify setup..." "Yellow"
    
    try {
        $null = Get-Command pytest -ErrorAction Stop
        
        # Check if there are any tests to run
        if (Test-Path -Path "tests") {
            $testFiles = Get-ChildItem -Path "tests" -Recurse -Filter "test_*.py"
            if ($testFiles.Count -gt 0) {
                & pytest
                Write-ColorOutput "Tests completed successfully." "Green"
            }
            else {
                Write-ColorOutput "No tests found. Skipping test execution." "Yellow"
            }
        }
        else {
            Write-ColorOutput "Tests directory not found. Skipping test execution." "Yellow"
        }
    }
    catch {
        Write-ColorOutput "pytest not found. Skipping test execution." "Red"
    }
    
    return $true
}

# Main function
function Main {
    Write-ColorOutput "==========================================" "Green"
    Write-ColorOutput "  BarqHWMuSig Development Setup Script" "Green"
    Write-ColorOutput "==========================================" "Green"
    
    $success = $true
    
    if (-not (Check-Python)) { $success = $false }
    if (-not (Check-UV)) { $success = $false }
    if (-not (Setup-Venv)) { $success = $false }
    if (-not (Install-Dependencies)) { $success = $false }
    if (-not (Setup-Precommit)) { $success = $false }
    if (-not (Create-Directories)) { $success = $false }
    if (-not (Create-EnvExample)) { $success = $false }
    if (-not (Create-ConfigJson)) { $success = $false }
    if (-not (Create-InitFiles)) { $success = $false }
    if (-not (Run-Tests)) { $success = $false }
    
    if ($success) {
        Write-ColorOutput "==========================================" "Green"
        Write-ColorOutput "  Setup completed successfully!" "Green"
        Write-ColorOutput "==========================================" "Green"
        Write-ColorOutput "Next steps:" "Green"
        Write-ColorOutput "1. Review the documentation in docs\" "Yellow"
        Write-ColorOutput "2. Copy config\.env.example to config\.env and update values" "Yellow"
        Write-ColorOutput "3. Start developing!" "Yellow"
        Write-ColorOutput "==========================================" "Green"
    }
    else {
        Write-ColorOutput "==========================================" "Red"
        Write-ColorOutput "  Setup completed with errors." "Red"
        Write-ColorOutput "  Please review the output above and fix any issues." "Red"
        Write-ColorOutput "==========================================" "Red"
    }
}

# Run the main function
Main 