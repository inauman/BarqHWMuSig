# TODO: Bitcoin Multisig POC Implementation Checklist

This checklist outlines all tasks required to build the Bitcoin Multisig POC. Each task should be updated with a checkmark when completed.

## 1. Environment Setup
- [x] **Create Project Root**
  - Create the root folder: `BarqHWMuSig`
- [x] **Version Control**
  - Confirm Git is initialized (already completed)
- [x] **Folder Structure**
  - [x] Create the following folders inside `BarqHWMuSig`:
    - `config/` (for environment configuration files)
    - `docs/` (store documentation including `spec.md`)
    - `src/` with subfolders:
      - `bitcoin_transaction/`
      - `device_integration/`
      - `cli/`
      - `common/` (for shared utilities such as logging and exceptions)
    - `tests/` (for unit and integration tests)
    - `demo/` (for demonstration scripts)
- [x] **Dependency Management**
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
- [x] **Configuration File**
  - Create a standard `.env` file in the `config/` folder with required environment variables.
- [x] **Implement ConfigLoader**
  - Create `src/common/config_loader.py`
  - Implement a `ConfigLoader` class that:
    - Reads from the `.env` file using python-dotenv
    - Returns a configuration object/dictionary
    - Logs and raises errors for missing or invalid configurations
- [x] **Implement Logger**
  - Create `src/common/logger.py`
  - Implement a `Logger` or `setup_logger()` function that:
    - Configures logging levels (DEBUG, INFO, WARNING, ERROR)
    - Outputs logs to the console
- [x] **Unit Testing for Common Utilities**
  - Write unit tests (e.g., in `tests/test_common.py`) for both ConfigLoader and Logger

## 3. Bitcoin Transaction Management Module
### A. MultisigWallet
- [x] **Implement MultisigWallet**
  - Create `src/bitcoin_transaction/multisig_wallet.py`
  - Implement a `MultisigWallet` class with methods:
    - `create_wallet()`
    - `generate_address()`
    - `list_keys()`
  - Add logging and error handling to each method
- [x] **Unit Testing for MultisigWallet**
  - Write tests in `tests/test_bitcoin_transaction.py` to validate:
    - Wallet initialization
    - Correct generation of multisig addresses (stubbed response acceptable)
    - Retrieval of key information

### B. TransactionBuilder
- [x] **Implement TransactionBuilder**
  - Create `src/bitcoin_transaction/transaction_manager.py`
  - Implement a `TransactionManager` class with methods:
    - `create_transaction()`
    - `estimate_fees()`
    - `build()`
    - `sign()`
    - `broadcast()`
  - Include logging and error handling in each method
- [x] **Unit Testing for TransactionBuilder**
  - Write tests in `tests/test_bitcoin_transaction.py` to ensure:
    - Transaction creation and building work as expected
    - Fee estimation returns valid values
    - Sign and broadcast methods handle error conditions

### C. TransactionMonitor
- [x] **Implement TransactionMonitor**
  - Create `src/bitcoin_transaction/transaction_signer.py`
  - Implement a `TransactionSigner` class with methods:
    - `sign_transaction()`
    - `verify_transaction()`
  - Ensure logging of transaction lifecycle events (creation, mempool entry, confirmations, errors)
- [x] **Unit Testing for TransactionMonitor**
  - Write tests in `tests/test_transaction_signer.py` to simulate lifecycle events and verify correct logging

## 4. Device Integration Module
### A. DeviceInterface
- [x] **Define DeviceInterface**
  - Create `src/device_integration/hardware_device.py`
  - Define an abstract class `HardwareDevice` with methods:
    - `get_public_key()`
    - `sign_transaction(transaction_data)`
    - `is_connected()`
    - `connect()`
    - `disconnect()`
- [x] **Testing Interface Definition**
  - Write tests to ensure that the interface is correctly defined

### B. YubiKeyDevice
- [x] **Implement YubiKeyDevice**
  - Create `src/device_integration/yubikey_device.py`
  - Implement a `YubiKeyDevice` class that inherits from `HardwareDevice`
  - Provide implementations with logging for each method
- [x] **Unit Testing for YubiKeyDevice**
  - Write tests in `tests/unit/test_yubikey_device.py` to validate the methods

### C. LedgerDevice
- [x] **Implement LedgerDevice**
  - Create `src/device_integration/ledger_device.py`
  - Implement a `LedgerDevice` class that inherits from `HardwareDevice`
  - Provide implementations with logging for each method
- [x] **Unit Testing for LedgerDevice**
  - Write tests in `tests/unit/test_ledger_device.py` to validate the methods

### D. DeviceFactory
- [x] **Implement DeviceFactory**
  - Create `src/device_integration/device_factory.py`
  - Implement a `DeviceFactory` class that creates device instances based on type
- [x] **Unit Testing for DeviceFactory**
  - Write tests to validate the factory methods

## 5. CLI/Interface Module
- [x] **Implement CLI Commands**
  - Create `src/cli/wallet_cli.py`
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
- [x] **Main Application Integration**
  - Create a main module (e.g., `__main__.py`) in the `src/`
  - Wire together:
    - Initialization of configuration (ConfigLoader)
    - Logger setup
    - Instantiation of MultisigWallet, TransactionManager, TransactionSigner
    - Instantiation of device integration modules (YubiKeyDevice, LedgerDevice)
    - Integration with CLI commands so that each function (wallet creation, transaction processing, signing, broadcasting, monitoring) is connected
- [ ] **Integration Testing**
  - Write integration tests to simulate a full multisig transaction flow from start to finish

## 7. Demo Module
- [ ] **Implement Demo Script**
  - Create `demo/demo.py`
  - Develop a demo that:
    - Creates a multisig wallet using `MultisigWallet`
    - Builds a multisig transaction using `TransactionManager`
    - Invokes device signing via the unified device interface (for YubiKey and LedgerDevice)
    - Broadcasts the transaction and monitors its lifecycle
    - Logs each step clearly to the terminal
- [ ] **Test Demo Execution**
  - Run the demo script and verify that all steps function correctly and output expected logs

## 8. Continuous Integration & Testing
- [ ] **Set Up CI/CD**
  - (If applicable) Configure continuous integration to run tests on code commits/pull requests
- [x] **Ensure Test Coverage**
  - Verify that test coverage is good across all modules
  - Fixed implementation issues in YubiKeyDevice and LedgerDevice
  - All tests for device integration are now passing

## 9. Recent Fixes and Improvements
- [x] **Fixed YubiKeyDevice Implementation**
  - Fixed initialization of `connected` and `private_key` attributes
  - Updated connection management methods
  - Corrected public key formatting
  - Fixed signature generation in `sign_transaction` method
  - Corrected the `_mock_sign` method to ensure it returns valid signatures

- [x] **Fixed LedgerDevice Implementation**
  - Made similar fixes to the YubiKeyDevice implementation
  - Fixed initialization of attributes
  - Corrected connection management
  - Ensured proper public key formatting
  - Fixed signature generation and error handling

- [x] **Updated Test Files**
  - Updated test assertions to match the new implementations
  - Fixed the test for the `_mock_sign` method
  - Ensured all tests pass with the new implementations

---

Each task should be reviewed and updated as work is completed. This checklist serves as the roadmap for incremental, test-driven development of the Bitcoin Multisig POC.
