# TODO: Bitcoin Multisig POC Implementation Checklist

This checklist outlines all tasks required to build the Bitcoin Multisig POC. Each task should be updated with a checkmark when completed.

## 1. Environment Setup
- [ ] **Create Project Root**
  - Create the root folder: `BarqHWMuSig`
- [ ] **Version Control**
  - Confirm Git is initialized (already completed)
- [ ] **Folder Structure**
  - [ ] Create the following folders inside `BarqHWMuSig`:
    - `config/` (for environment configuration files)
    - `docs/` (store documentation including `spec.md`)
    - `src/` with subfolders:
      - `bitcoin_transaction/`
      - `device_integration/`
      - `cli/`
      - `common/` (for shared utilities such as logging and exceptions)
    - `tests/` (for unit and integration tests)
    - `demo/` (for demonstration scripts)
- [ ] **Dependency Management**
  - Create a `pyproject.toml` file for dependency management using uv
  - Include dependencies:
    - `python-bitcoinlib`
    - `yubikey-manager`
    - `fido2`
    - `pyusb`
    - `btchip-python`
    - `cryptography`
    - `Click`
    - `pytest`, `pytest-mock`, `coverage`
    - `python-dotenv`
  - Ensure the Python version is explicitly set to 3.14

## 2. Configuration & Environment Module
- [ ] **Configuration File**
  - Create a standard `.env` file in the `config/` folder with required environment variables.
- [ ] **Implement ConfigLoader**
  - Create `src/common/config_loader.py`
  - Implement a `ConfigLoader` class that:
    - Reads from the `.env` file using python-dotenv
    - Returns a configuration object/dictionary
    - Logs and raises errors for missing or invalid configurations
- [ ] **Implement Logger**
  - Create `src/common/logger.py`
  - Implement a `Logger` or `setup_logger()` function that:
    - Configures logging levels (DEBUG, INFO, WARNING, ERROR)
    - Outputs logs to the console
- [ ] **Unit Testing for Common Utilities**
  - Write unit tests (e.g., in `tests/test_common.py`) for both ConfigLoader and Logger

## 3. Bitcoin Transaction Management Module
### A. MultisigWallet
- [ ] **Implement MultisigWallet**
  - Create `src/bitcoin_transaction/multisig_wallet.py`
  - Implement a `MultisigWallet` class with methods:
    - `create_wallet()`
    - `generate_address()`
    - `list_keys()`
  - Add logging and error handling to each method
- [ ] **Unit Testing for MultisigWallet**
  - Write tests in `tests/test_bitcoin_transaction.py` to validate:
    - Wallet initialization
    - Correct generation of multisig addresses (stubbed response acceptable)
    - Retrieval of key information

### B. TransactionBuilder
- [ ] **Implement TransactionBuilder**
  - Create `src/bitcoin_transaction/transaction_builder.py`
  - Implement a `TransactionBuilder` class with methods:
    - `create_transaction()`
    - `estimate_fees()`
    - `build()`
    - `sign()`
    - `broadcast()`
  - Include logging and error handling in each method
- [ ] **Unit Testing for TransactionBuilder**
  - Write tests in `tests/test_bitcoin_transaction.py` to ensure:
    - Transaction creation and building work as expected
    - Fee estimation returns valid values
    - Sign and broadcast methods handle error conditions

### C. TransactionMonitor
- [ ] **Implement TransactionMonitor**
  - Create `src/bitcoin_transaction/transaction_monitor.py`
  - Implement a `TransactionMonitor` class with methods:
    - `monitor_transaction()`
    - `log_event()`
  - Ensure logging of transaction lifecycle events (creation, mempool entry, confirmations, errors)
- [ ] **Unit Testing for TransactionMonitor**
  - Write tests in `tests/test_bitcoin_transaction.py` to simulate lifecycle events and verify correct logging

## 4. Device Integration Module
### A. DeviceInterface
- [ ] **Define DeviceInterface**
  - Create `src/device_integration/unified_interface.py`
  - Define an abstract class `DeviceInterface` with methods:
    - `get_public_key()`
    - `sign_transaction(transaction_data)`
    - `verify_signature(transaction_data, signature)`
- [ ] **Testing Interface Definition**
  - Write tests to ensure that the interface is correctly defined

### B. YubiKeyDevice
- [ ] **Implement YubiKeyDevice**
  - Create `src/device_integration/yubikey_integration.py`
  - Implement a `YubiKeyDevice` class that inherits from `DeviceInterface`
  - Provide stub implementations with logging for each method
- [ ] **Unit Testing for YubiKeyDevice**
  - Write tests in `tests/test_device_integration.py` to validate the stub methods

### C. LedgerDevice
- [ ] **Implement LedgerDevice**
  - Create `src/device_integration/ledger_integration.py`
  - Implement a `LedgerDevice` class that inherits from `DeviceInterface`
  - Provide stub implementations with logging for each method
- [ ] **Unit Testing for LedgerDevice**
  - Write tests in `tests/test_device_integration.py` to validate the stub methods

### D. HardcodedKeyDevice
- [ ] **Implement HardcodedKeyDevice**
  - Create `src/device_integration/hardcoded_key.py`
  - Implement a `HardcodedKeyDevice` class that inherits from `DeviceInterface`
  - Use the cryptography package for key handling in the stub methods
- [ ] **Unit Testing for HardcodedKeyDevice**
  - Write tests in `tests/test_device_integration.py` to validate the stub methods

## 5. CLI/Interface Module
- [ ] **Implement CLI Commands**
  - Create `src/cli/cli_commands.py`
  - Implement CLI commands using Click for:
    - `create_wallet`
    - `build_transaction`
    - `sign_transaction`
    - `broadcast_transaction`
    - `monitor_transaction`
  - Ensure each command includes proper help messages and parses inputs correctly
- [ ] **Unit Testing for CLI**
  - Write tests in `tests/test_cli.py` to simulate CLI inputs and verify that the correct module methods are invoked

## 6. Integration and Wiring
- [ ] **Main Application Integration**
  - Create a main module (e.g., `main.py`) in the root or `src/`
  - Wire together:
    - Initialization of configuration (ConfigLoader)
    - Logger setup
    - Instantiation of MultisigWallet, TransactionBuilder, TransactionMonitor
    - Instantiation of device integration modules (YubiKeyDevice, LedgerDevice, HardcodedKeyDevice)
    - Integration with CLI commands so that each function (wallet creation, transaction processing, signing, broadcasting, monitoring) is connected
- [ ] **Integration Testing**
  - Write integration tests to simulate a full multisig transaction flow from start to finish

## 7. Demo Module
- [ ] **Implement Demo Script**
  - Create `demo/demo.py`
  - Develop a demo that:
    - Creates a multisig wallet using `MultisigWallet`
    - Builds a multisig transaction using `TransactionBuilder`
    - Invokes device signing via the unified device interface (for YubiKey, LedgerDevice, and HardcodedKeyDevice)
    - Broadcasts the transaction and monitors its lifecycle with `TransactionMonitor`
    - Logs each step clearly to the terminal
- [ ] **Test Demo Execution**
  - Run the demo script and verify that all steps function correctly and output expected logs

## 8. Continuous Integration & Testing
- [ ] **Set Up CI/CD**
  - (If applicable) Configure continuous integration to run tests on code commits/pull requests
- [ ] **Ensure Test Coverage**
  - Verify that overall test coverage is at least 80% across all modules

---

Each task should be reviewed and updated as work is completed. This checklist serves as the roadmap for incremental, test-driven development of the Bitcoin Multisig POC.
