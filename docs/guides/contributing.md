# Contributing Guide

Thank you for your interest in contributing to the BarqHWMuSig project! This guide will help you understand how to contribute effectively.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Security Considerations](#security-considerations)
- [Community](#community)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. We expect all contributors to:

- Be respectful and considerate of others
- Use inclusive language
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.14.0a5
- Git
- UV package manager
- Hardware devices for testing (optional)

### Setting Up Your Development Environment

1. **Fork the repository**

2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/BarqHWMuSig.git
   cd BarqHWMuSig
   ```

3. **Activate the virtual environment**
   ```bash
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   uv pip install -e ".[dev]"
   ```

5. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Development Workflow

### 1. Choose an Issue

- Look for issues labeled `good first issue` if you're new to the project
- Comment on the issue to let others know you're working on it
- Ask questions if anything is unclear

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Use a descriptive branch name that reflects the changes you're making:
- `feature/` for new features
- `bugfix/` for bug fixes
- `docs/` for documentation changes
- `test/` for test additions or changes
- `refactor/` for code refactoring

### 3. Make Your Changes

Follow these guidelines:
- Keep classes under 300 lines
- Keep functions under 50 lines
- Use type hints for all function parameters and return values
- Write tests for your code
- Document your code with Google-style docstrings
- Follow the "Don't Trust, Validate" philosophy

### 4. Run Tests and Linters

```bash
# Run tests
pytest

# Run linters and formatters
pre-commit run --all-files
```

### 5. Commit Your Changes

Follow the conventional commits format:

```bash
git commit -m "feat: add new feature"
git commit -m "fix: fix bug in transaction builder"
git commit -m "docs: update documentation"
git commit -m "test: add tests for new feature"
git commit -m "refactor: improve code structure"
```

### 6. Keep Your Branch Updated

```bash
git fetch origin
git rebase origin/main
```

## Pull Request Process

1. **Push your changes to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a pull request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the pull request template

3. **Address review feedback**
   - Make requested changes
   - Push additional commits to your branch
   - Respond to comments

4. **Update your PR if needed**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Merge**
   - Once approved, your PR will be merged
   - Delete your branch after merging

## Coding Standards

We follow strict coding standards to ensure code quality and consistency:

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with Black's modifications
- Use Black for code formatting
- Use isort for import sorting
- Use Ruff for linting

### Type Annotations

- Use type hints for all function parameters and return values
- Use mypy for static type checking
- Use Protocol for interface definitions
- Use TypeVar for generic types

### Documentation

- Use Google-style docstrings
- Document all public APIs
- Include examples in docstrings for complex functions
- Document exceptions that may be raised

### Security

- Never store private keys in code or logs
- Use environment variables for configuration
- Validate all input data
- Use secure random number generation
- Follow principle of least privilege

## Testing Guidelines

### Test Coverage

- Aim for at least 80% test coverage across all modules
- Aim for 100% test coverage for critical paths (crypto operations)
- Write tests before code (TDD approach)
- Test both positive and negative cases
- Test edge cases and boundary conditions

### Test Types

1. **Unit Tests**
   - Test individual components in isolation
   - Mock external dependencies
   - Located in `tests/unit/`

2. **Integration Tests**
   - Test interactions between components
   - May use real or mocked external services
   - Located in `tests/integration/`

3. **Security Tests**
   - Test security-specific functionality
   - Test error handling and edge cases
   - Located in `tests/security/`

### Test Naming

Use descriptive test names that indicate:
- What is being tested
- Under what conditions
- What the expected outcome is

Example: `test_transaction_builder_with_invalid_inputs_raises_validation_error`

## Documentation Guidelines

### Code Documentation

- Document all public APIs
- Use Google-style docstrings
- Include examples for complex functions
- Document exceptions that may be raised
- Keep documentation in sync with code

### Project Documentation

- Update README.md with significant changes
- Update user and developer guides as needed
- Create new documentation for new features
- Use clear, concise language
- Include examples and diagrams where helpful

## Security Considerations

Security is a top priority for this project. When contributing:

- Follow the [Bitcoin Security Guidelines](../../.cursor/rules/bitcoin_security.md)
- Never commit private keys or sensitive data
- Use secure random number generation
- Validate all inputs
- Implement proper error handling
- Consider the security implications of your changes

If you discover a security vulnerability:
1. **Do not** open a public issue
2. Email the project maintainers directly
3. Provide details of the vulnerability
4. Allow time for the issue to be addressed before disclosure

## Community

### Communication Channels

- GitHub Issues: For bug reports, feature requests, and discussions
- Pull Requests: For code contributions
- Email: For security vulnerabilities or private inquiries

### Recognition

All contributors will be recognized in the project's CONTRIBUTORS.md file. We value all contributions, whether they're code, documentation, design, or community support.

### Feedback

We welcome feedback on the contribution process. If you have suggestions for improving this guide or the contribution workflow, please open an issue or submit a pull request.

---

Thank you for contributing to BarqHWMuSig! Your efforts help make this project better for everyone. 