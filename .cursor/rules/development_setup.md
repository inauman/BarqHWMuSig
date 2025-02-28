# Development Setup Guide

## Current Environment Status

### Project Setup
- Root folder `BarqHWMuSig` already created
- Python 3.14.0a5 already installed and pinned for the project
- Virtual environment already created
- UV package manager already installed via Homebrew

## Environment Setup for New Developers

### Python Installation
- Install Python 3.14.0a5 (for consistency with current development)
  - On macOS: `brew install python@3.14` or download from python.org
  - On Linux: Use pyenv or compile from source
  - On Windows: Download from python.org
- Ensure pip is updated to the latest version: `python -m pip install --upgrade pip`

### Package Management with UV
- Install UV: 
  - On macOS: `brew install uv` 
  - Other platforms: `pip install uv`
- Use UV for virtual environment creation: `uv venv`
- Use UV for package installation: `uv pip install <package>`
- Use UV for dependency resolution: `uv pip compile pyproject.toml -o requirements.txt`

### Project Configuration
- Use `pyproject.toml` for project configuration (PEP 621)
- Define project metadata, dependencies, and development tools in `pyproject.toml`
- Example `pyproject.toml` structure:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "barqhwmusig"
version = "0.1.0"
description = "Bitcoin Multisig POC with Hardware Wallet Integration"
readme = "README.md"
requires-python = ">=3.14"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
dependencies = [
    "python-bitcoinlib>=0.11.0",
    "yubikey-manager>=4.0.0",
    "fido2>=1.0.0",
    "pyusb>=1.2.1",
    "btchip-python>=0.1.32",
    "cryptography>=39.0.0",
    "click>=8.1.3",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.3.1",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.10.0",
    "black>=23.3.0",
    "isort>=5.12.0",
    "mypy>=1.3.0",
    "ruff>=0.0.262",
    "bandit>=1.7.5",
    "pre-commit>=3.3.1",
    "pip-audit>=2.5.5",
]

[tool.black]
line-length = 88
target-version = ["py314"]

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.14"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true

[tool.ruff]
line-length = 88
target-version = "py314"
select = ["E", "F", "B", "I", "N", "UP", "ANN", "S", "A"]
ignore = ["ANN101"]  # Missing type annotation for `self`

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "--cov=src --cov-report=term-missing"
```

## Development Tools Setup

### Code Quality Tools
- Install development dependencies: `uv pip install -e ".[dev]"`
- Set up pre-commit hooks:
  1. Create `.pre-commit-config.yaml`:
  ```yaml
  repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    - id: trailing-whitespace
    - id: end-of-file-fixer
    - id: check-yaml
    - id: check-toml
    - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    - id: black

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.262
    hooks:
    - id: ruff
      args: [--fix]

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    - id: isort

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
    - id: mypy
      additional_dependencies: [types-requests]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
    - id: bandit
      args: ["-c", "pyproject.toml"]
      additional_dependencies: ["bandit[toml]"]
  ```
  2. Install pre-commit hooks: `pre-commit install`

### Security Tools
- Run security checks regularly:
  - Dependency vulnerability scanning: `pip-audit`
  - Static security analysis: `bandit -r src/`
  - Secret scanning: `detect-secrets scan`

### Testing Setup
- Run tests with pytest: `pytest`
- Generate coverage reports: `pytest --cov=src --cov-report=html`
- Run specific test categories:
  - Unit tests: `pytest tests/unit/`
  - Integration tests: `pytest tests/integration/`
  - Security tests: `pytest tests/security/`

## Project Structure Setup

```
BarqHWMuSig/  # Root folder (already created)
├── .cursor/                  # Cursor IDE configuration
│   └── rules/                # Development rules and guidelines
├── .github/                  # GitHub workflows and templates
│   └── workflows/            # CI/CD workflows
├── config/                   # Configuration files
│   ├── .env.example          # Example environment variables
│   └── config.json           # Application configuration
├── docs/                     # Documentation
│   ├── api/                  # API documentation
│   ├── guides/               # User and developer guides
│   └── spec.md               # Project specification
├── src/                      # Source code
│   ├── bitcoin_transaction/  # Bitcoin transaction management
│   ├── device_integration/   # Device integration
│   ├── cli/                  # CLI interface
│   └── common/               # Shared utilities
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── security/             # Security tests
├── demo/                     # Demo scripts
├── .gitignore                # Git ignore file
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── pyproject.toml            # Project configuration
└── README.md                 # Project overview
```

## Development Workflow

### Initial Setup for New Developers
1. Clone the repository
2. Activate the existing virtual environment:
   - Unix/MacOS: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
3. Install dependencies: `uv pip install -e ".[dev]"`
4. Install pre-commit hooks: `pre-commit install`

### Development Cycle
1. Create a feature branch: `git checkout -b feature/feature-name`
2. Make changes
3. Run tests: `pytest`
4. Run linters and formatters: `pre-commit run --all-files`
5. Commit changes: `git commit -m "feat: add feature"`
6. Push changes: `git push origin feature/feature-name`
7. Create a pull request

### Code Review Process
1. Automated checks must pass
2. At least one reviewer must approve
3. All comments must be addressed
4. Changes must be squashed before merging

## Updates
This document should be reviewed and updated when new tools or practices are adopted. 