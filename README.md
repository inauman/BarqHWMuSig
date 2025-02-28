# BarqHWMuSig: Bitcoin Multisig Hardware Wallet POC

A proof-of-concept implementation of a **2-of-3 Bitcoin multisig wallet** that integrates with hardware devices.

## Overview

BarqHWMuSig demonstrates secure multisig wallet creation, transaction building, signing, and monitoring using a combination of hardware and software keys:

- **YubiKey** (via USB or NFC)
- **Ledger Nano** (via USB)
- **Hardcoded Key** (for testing within the Python app)

## Features

- **2-of-3 Multisignature Wallet**: Requires any 2 of 3 keys to authorize a transaction
- **Hardware Device Integration**: Secure key management using YubiKey and Ledger Nano
- **Transaction Management**: Build, sign, broadcast, and monitor Bitcoin transactions
- **CLI Interface**: User-friendly command-line interface for all operations
- **Comprehensive Logging**: Detailed logging of all operations and events
- **Robust Error Handling**: Graceful handling of errors and edge cases
- **Extensive Testing**: Comprehensive test suite for all components

## Requirements

- Python 3.14.0a5
- YubiKey with FIDO2 support (for hardware key integration)
- Ledger Nano with Bitcoin app (for hardware key integration)
- Internet connection (for transaction broadcasting and monitoring)

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd BarqHWMuSig

# Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

# Install dependencies
uv pip install -e .
```

### One-Click Setup for New Developers

For Unix/Linux/macOS:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

For Windows (PowerShell):
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

### Basic Usage

```bash
# Create a multisig wallet
python -m src.cli.cli_commands create-wallet

# Build a transaction
python -m src.cli.cli_commands build-transaction --recipient <address> --amount <btc-amount>

# Sign a transaction
python -m src.cli.cli_commands sign-transaction --transaction-id <txid>

# Broadcast a transaction
python -m src.cli.cli_commands broadcast-transaction --transaction-id <txid>

# Monitor a transaction
python -m src.cli.cli_commands monitor-transaction --transaction-id <txid>
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Welcome Guide](docs/welcome.md) - Start here for an overview of the project
- [User Guide](docs/guides/user_guide.md) - Guide for end users
- [Developer Guide](docs/guides/developer_guide.md) - Guide for developers
- [Contributing Guide](docs/guides/contributing.md) - How to contribute to the project
- [Project Specification](docs/spec.md) - Detailed project requirements and architecture

## Project Structure

```
BarqHWMuSig/
├── .cursor/                  # Cursor IDE configuration
│   └── rules/                # Development rules and guidelines
├── config/                   # Configuration files
│   ├── .env.example          # Example environment variables
│   └── config.json           # Application configuration
├── docs/                     # Documentation
│   ├── api/                  # API documentation
│   ├── guides/               # User and developer guides
│   └── spec.md               # Project specification
├── scripts/                  # Setup and utility scripts
│   ├── setup.sh              # Unix/Linux/macOS setup script
│   └── setup.ps1             # Windows PowerShell setup script
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
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Development

### Setting Up Development Environment

1. Follow the installation instructions above
2. Install development dependencies: `uv pip install -e ".[dev]"`
3. Install pre-commit hooks: `pre-commit install`

### Running Tests

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/unit/

# Run tests with coverage
pytest --cov=src --cov-report=html
```

### Code Quality

We use several tools to ensure code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Linting
- **mypy**: Type checking
- **bandit**: Security linting

Run all checks with:

```bash
pre-commit run --all-files
```

## Security Considerations

This project implements several security best practices:

- Hardware-based key management
- Multisignature wallet for distributed security
- Input validation at all levels
- Secure transaction signing
- Comprehensive error handling

However, as this is a proof-of-concept, it should not be used for managing significant amounts of Bitcoin without thorough security review.

## License

[MIT License](LICENSE)

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/guides/contributing.md) for details on how to contribute to the project.

## Acknowledgements

- [python-bitcoinlib](https://github.com/petertodd/python-bitcoinlib) for Bitcoin transaction management
- [YubiKey](https://www.yubico.com/) for secure hardware key management
- [Ledger](https://www.ledger.com/) for secure hardware wallet integration 