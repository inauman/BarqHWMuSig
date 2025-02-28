# Welcome to BarqHWMuSig

Welcome to the Bitcoin Multisig Proof of Concept (POC) project! This document serves as your starting point for understanding the project, setting up your development environment, and contributing to the codebase.

## Project Overview

BarqHWMuSig is a proof-of-concept implementation of a **2-of-3 Bitcoin multisig wallet** that integrates with hardware devices:
- **YubiKey** (via USB or NFC)
- **Ledger Nano** (via USB)
- **Hardcoded Key** (for testing within the Python app)

The project demonstrates secure multisig wallet creation, transaction building, signing, and monitoring using a combination of hardware and software keys.

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd BarqHWMuSig
   ```

2. **Activate the virtual environment**
   ```bash
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   uv pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Run the demo**
   ```bash
   python -m demo.demo
   ```

## Documentation Index

### Project Documentation

- [Project Specification](./spec.md) - Detailed project requirements and architecture
- [API Documentation](./api/README.md) - Documentation for the project's APIs
- [User Guide](./guides/user_guide.md) - Guide for end users
- [Developer Guide](./guides/developer_guide.md) - Guide for developers

### Development Guidelines

- [Python Best Practices](../.cursor/rules/python_best_practices.md) - Python coding standards and best practices
- [Development Setup](../.cursor/rules/development_setup.md) - Environment setup and workflow
- [Bitcoin Security Guidelines](../.cursor/rules/bitcoin_security.md) - Security considerations for Bitcoin applications
- [Code Review Checklist](../.cursor/rules/code_review_checklist.md) - Checklist for code reviews

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
└── README.md                 # Project overview
```

## Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the [Python Best Practices](../.cursor/rules/python_best_practices.md)
   - Ensure proper test coverage
   - Document your code

3. **Run tests and linters**
   ```bash
   # Run tests
   pytest
   
   # Run linters and formatters
   pre-commit run --all-files
   ```

4. **Commit your changes**
   ```bash
   git commit -m "feat: add your feature"
   ```

5. **Create a pull request**
   - Ensure all checks pass
   - Request a code review
   - Address any feedback

## Environment Notes

- **Python Version**: This project uses Python 3.14.0a5 (alpha version)
- **Package Management**: We use `uv` instead of pip for faster, more secure package management
- **Configuration**: Project configuration is managed through `pyproject.toml` and environment variables

## Getting Help

If you have any questions or run into issues:
1. Check the existing documentation
2. Review the code and comments
3. Reach out to the project maintainers

## Contributing

We welcome contributions! Please see our [Contributing Guide](./guides/contributing.md) for details on how to contribute to the project.

---

Happy coding! 🚀 