# BarqHWMuSig

A proof-of-concept implementation of a 2-of-3 Bitcoin multisig wallet with hardware device integration.

## Features

- **Multisignature Wallet**: Create and manage 2-of-3 Bitcoin multisig wallets
- **Hardware Device Integration**: Support for YubiKey and Ledger hardware devices
- **Transaction Management**: Create, sign, and broadcast Bitcoin transactions
- **Command-Line Interface**: Easy-to-use CLI for all wallet operations
- **Comprehensive Logging**: Detailed logging for all operations
- **Robust Error Handling**: Graceful handling of errors and edge cases
- **Extensive Testing**: Comprehensive test suite for all components

## Requirements

- Python 3.14.0a5 or higher
- YubiKey with FIDO2 support (for YubiKey integration)
- Ledger Nano with Bitcoin app (for Ledger integration)
- Internet connection (for blockchain API access)

## Quick Start

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/BarqHWMuSig.git
   cd BarqHWMuSig
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the package and dependencies:
   ```
   pip install -e ".[dev]"
   ```

### One-Click Setup for New Developers

#### Unix/Linux/macOS

```bash
./scripts/setup.sh
```

#### Windows

```powershell
.\scripts\setup.ps1
```

### Basic Usage

1. Create a new wallet:
   ```
   python -m src create-wallet my_wallet <pubkey1> <pubkey2> <pubkey3>
   ```

2. Connect to a hardware device:
   ```
   python -m src connect-device yubikey
   ```

3. Get a public key from a hardware device:
   ```
   python -m src get-public-key yubikey
   ```

4. Update UTXOs for a wallet:
   ```
   python -m src update-utxos my_wallet
   ```

5. Create a transaction:
   ```
   python -m src create-transaction my_wallet <address> <amount>
   ```

6. Sign a transaction:
   ```
   python -m src sign-transaction my_wallet my_wallet_unsigned_tx.json yubikey ledger
   ```

7. Broadcast a transaction:
   ```
   python -m src broadcast-transaction my_wallet_signed_tx.json
   ```

8. Wait for transaction confirmation:
   ```
   python -m src wait-for-confirmation <txid>
   ```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- [User Guide](docs/guides/user_guide.md): Detailed instructions for using the wallet
- [Developer Guide](docs/guides/developer_guide.md): Information for developers
- [API Reference](docs/api/README.md): API documentation
- [Contributing Guide](docs/guides/contributing.md): Guidelines for contributing to the project

## Project Structure

- `src/`: Source code
  - `bitcoin_transaction/`: Bitcoin transaction handling
  - `cli/`: Command-line interface
  - `common/`: Common utilities
  - `device_integration/`: Hardware device integration
- `tests/`: Test suite
  - `unit/`: Unit tests
  - `integration/`: Integration tests
- `docs/`: Documentation
- `config/`: Configuration files
- `scripts/`: Utility scripts

## Development

### Setting Up the Development Environment

Follow the installation instructions above, then:

1. Install development dependencies:
   ```
   pip install -e ".[dev]"
   ```

2. Install pre-commit hooks:
   ```
   pre-commit install
   ```

### Running Tests

```
python -m pytest
```

### Code Quality

```
black src tests
isort src tests
mypy src
ruff src tests
```

## Security Considerations

This project is a proof-of-concept and should not be used with real Bitcoin on mainnet without thorough security review. The following security measures are implemented:

- Hardware device integration for secure key storage
- 2-of-3 multisig for enhanced security
- Comprehensive logging for audit trails
- Input validation and error handling

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see the [Contributing Guide](docs/guides/contributing.md) for details.

## Acknowledgements

- [python-bitcoinlib](https://github.com/petertodd/python-bitcoinlib) for Bitcoin functionality
- [YubiKey](https://www.yubico.com/) for FIDO2 security key functionality
- [Ledger](https://www.ledger.com/) for hardware wallet functionality 