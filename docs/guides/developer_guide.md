# Developer Guide

This guide provides detailed information for developers working on the BarqHWMuSig project. It covers the project architecture, development workflow, and best practices.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Module Breakdown](#module-breakdown)
- [Development Environment](#development-environment)
- [Development Workflow](#development-workflow)
- [Testing Strategy](#testing-strategy)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

BarqHWMuSig follows a modular architecture with clear separation of concerns. The application is divided into several key modules:

1. **Configuration & Environment Module**
   - Manages configuration loading and logging setup
   - Handles environment variables and secure configuration

2. **Bitcoin Transaction Management Module**
   - Handles multisig wallet creation
   - Manages transaction building, signing, and broadcasting
   - Monitors transaction status

3. **Device Integration Module**
   - Provides a unified interface for different signing devices
   - Implements device-specific integrations (YubiKey, Ledger, Hardcoded Key)

4. **CLI Interface Module**
   - Provides a command-line interface for all operations
   - Handles user input and output formatting

Each module is designed to be independent with well-defined interfaces, allowing for easy testing and maintenance.

## Module Breakdown

### Configuration & Environment Module

**Key Components:**
- `ConfigLoader`: Loads configuration from environment variables and config files
- `Logger`: Sets up structured logging with appropriate levels

**Interfaces:**
```python
class ConfigLoader:
    def load_config(self) -> Dict[str, Any]: ...
    def get_value(self, key: str, default: Optional[Any] = None) -> Any: ...
    def validate_config(self) -> bool: ...

def setup_logger(name: str, level: str = "INFO") -> logging.Logger: ...
```

### Bitcoin Transaction Management Module

**Key Components:**
- `MultisigWallet`: Manages multisig wallet creation and address generation
- `TransactionBuilder`: Handles transaction creation, fee estimation, and building
- `TransactionMonitor`: Monitors transaction status and lifecycle events

**Interfaces:**
```python
class MultisigWallet:
    def create_wallet(self, public_keys: List[str], m: int = 2) -> None: ...
    def generate_address(self) -> str: ...
    def list_keys(self) -> List[str]: ...

class TransactionBuilder:
    def create_transaction(self, outputs: List[Dict[str, Any]], fee_rate: int) -> None: ...
    def estimate_fees(self, tx_size: int, fee_rate: int) -> int: ...
    def build(self) -> Dict[str, Any]: ...
    def sign(self, signatures: List[str]) -> None: ...
    def broadcast(self) -> str: ...

class TransactionMonitor:
    def monitor_transaction(self, txid: str) -> None: ...
    def log_event(self, event_type: str, details: Dict[str, Any]) -> None: ...
```

### Device Integration Module

**Key Components:**
- `DeviceInterface`: Abstract interface for all signing devices
- `YubiKeyDevice`: YubiKey-specific implementation
- `LedgerDevice`: Ledger-specific implementation
- `HardcodedKeyDevice`: Testing implementation

**Interfaces:**
```python
class DeviceInterface(Protocol):
    def get_public_key(self) -> str: ...
    def sign_transaction(self, transaction_data: Dict[str, Any]) -> str: ...
    def verify_signature(self, transaction_data: Dict[str, Any], signature: str) -> bool: ...
    def report_error(self) -> None: ...

class YubiKeyDevice(DeviceInterface):
    # Implementation of DeviceInterface for YubiKey
    ...

class LedgerDevice(DeviceInterface):
    # Implementation of DeviceInterface for Ledger
    ...

class HardcodedKeyDevice(DeviceInterface):
    # Implementation of DeviceInterface for testing
    ...
```

### CLI Interface Module

**Key Components:**
- `CLICommands`: Implements Click commands for all operations

**Interfaces:**
```python
@click.group()
def cli(): ...

@cli.command()
def create_wallet(): ...

@cli.command()
def build_transaction(): ...

@cli.command()
def sign_transaction(): ...

@cli.command()
def broadcast_transaction(): ...

@cli.command()
def monitor_transaction(): ...
```

## Development Environment

### Python Version

This project uses Python 3.14.0a5 (alpha version). Be aware of potential compatibility issues with this alpha release.

### Virtual Environment

A virtual environment is already set up in the project root. Activate it with:

```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### Package Management

We use `uv` for package management:

```bash
# Install dependencies
uv pip install -e ".[dev]"

# Add a new dependency
uv pip install new-package
uv pip freeze > requirements.txt
```

### Code Quality Tools

We use several tools to ensure code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Linting
- **mypy**: Type checking
- **bandit**: Security linting

These tools are configured in `pyproject.toml` and can be run via pre-commit hooks:

```bash
pre-commit run --all-files
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Implement Your Changes

Follow these guidelines:
- Keep classes under 300 lines
- Keep functions under 50 lines
- Use type hints for all function parameters and return values
- Write tests for your code
- Document your code with Google-style docstrings

### 3. Run Tests

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/unit/test_specific_module.py

# Run tests with coverage
pytest --cov=src --cov-report=html
```

### 4. Run Linters and Formatters

```bash
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

### 6. Create a Pull Request

- Ensure all tests pass
- Ensure all linters pass
- Request a code review
- Address any feedback

## Testing Strategy

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

### Test Coverage

- Aim for at least 80% test coverage across all modules
- Aim for 100% test coverage for critical paths (crypto operations)

### Mocking

Use `pytest-mock` for mocking:

```python
def test_with_mock(mocker):
    mock_device = mocker.Mock(spec=DeviceInterface)
    mock_device.get_public_key.return_value = "mock_public_key"
    # Test with mock_device
```

## Security Considerations

### Key Management

- Never store private keys in code or logs
- Use hardware security modules when possible
- Implement proper key derivation paths
- Validate all public keys before use

### Transaction Security

- Validate all transaction inputs and outputs
- Implement proper fee estimation with bounds checking
- Verify signatures before broadcasting
- Implement transaction monitoring

### Error Handling

- Never expose sensitive information in error messages
- Log detailed errors internally
- Implement appropriate error recovery
- Validate system state after errors

## Troubleshooting

### Common Issues

#### Python 3.14.0a5 Compatibility Issues

Python 3.14.0a5 is an alpha release and may have compatibility issues with some packages. If you encounter issues:

1. Check if the package has a version compatible with Python 3.14
2. Consider using a compatibility layer or wrapper
3. Document any workarounds in the code

#### Hardware Device Connection Issues

If you have trouble connecting to hardware devices:

1. Ensure the device is properly connected
2. Check if the required drivers are installed
3. Verify that the device is in the correct mode
4. Check the logs for detailed error messages

#### Transaction Broadcasting Issues

If transactions fail to broadcast:

1. Verify that the transaction is properly signed
2. Check the fee rate (too low may cause rejection)
3. Verify that the inputs are valid and unspent
4. Check network connectivity

### Debugging Tips

1. Use logging with appropriate levels:
   ```python
   logger.debug("Detailed debug information")
   logger.info("General information")
   logger.warning("Warning message")
   logger.error("Error message")
   ```

2. Use the Python debugger:
   ```python
   import pdb; pdb.set_trace()
   ```

3. Check the logs in `logs/` directory

## Additional Resources

- [Python 3.14 Documentation](https://docs.python.org/3.14/)
- [Bitcoin Developer Documentation](https://developer.bitcoin.org/)
- [YubiKey Developer Documentation](https://developers.yubico.com/)
- [Ledger Developer Documentation](https://developers.ledger.com/) 