# Bitcoin Multisig POC Specification

## 1. Overview

This proof-of-concept (POC) implements a **2-of-3 Bitcoin multisig wallet** using a combination of hardware devices and an application-managed key:
- **Devices:**
  - **YubiKey** (via USB or NFC)
  - **Ledger Nano** (via USB)
  - **Hardcoded Key** (for testing within the Python app)
- **Bitcoin Integration:**  
  Leverages **python-bitcoinlib** for Bitcoin transaction management using ECDSA. (Advanced taproot/schnorr features are not prioritized in this demo.)
- **CLI:**  
  Uses **Click** to build a structured, interactive command-line interface that runs within a terminal emulator such as iTerm2.
- **Testing:**  
  Comprehensive unit and integration tests will be developed using **pytest**, **pytest-mock**, and **coverage**.
- **Environment & Configuration:**  
  Environment variables and secure configurations are managed with **python-dotenv** and built-in logging.

---

## 2. Tech Stack & Environment

- **Programming Language:** Python 3.14 (this version is already available and installed)
- **Package Manager:** uv with a `pyproject.toml` file for dependency management
- **Bitcoin Integration:**  
  - **python-bitcoinlib**
- **Device Integrations:**  
  - **YubiKey:** yubikey-manager, fido2, pyusb  
  - **Ledger Nano:** btchip-python  
  - **Hardcoded Key:** cryptography
- **CLI Interface:** Click
- **Testing Framework:** pytest, pytest-mock, coverage
- **Utilities:**  
  - **Environment:** python-dotenv  
  - **Logging:** Built-in logging module

---

## 3. Architecture & Module Breakdown

### A. Configuration & Environment Module
- **Purpose:**  
  Load environment variables, manage configuration, and initialize structured logging.
- **Key Components (located in `src/common`):**
  - **ConfigLoader:** Reads configuration from the `.env` file.
  - **Logger:** Sets up logging (levels: DEBUG, INFO, WARNING, ERROR).
- **Data Handling:**  
  Environment values, sensitive keys, and logging streams.
- **Error Handling:**  
  Invalid/missing configurations are logged and raised with descriptive error messages.

### B. Bitcoin Transaction Management Module
- **Purpose:**  
  Handle multisig wallet creation, transaction building, signing, fee estimation, broadcasting, and comprehensive transaction monitoring.
- **Key Components:**
  - **MultisigWallet:**  
    - *Methods:* `create_wallet()`, `generate_address()`, `list_keys()`
  - **TransactionBuilder:**  
    - *Methods:* `create_transaction()`, `estimate_fees()`, `build()`, `sign()`, `broadcast()`
  - **TransactionMonitor:**  
    - *Methods:* `monitor_transaction()`, `log_event()`
- **Data Handling:**  
  Raw transaction data, fee parameters, blockchain responses.
- **Error Handling:**  
  Graceful capture and logging of errors such as insufficient fees, network issues, or signing failures.

### C. Device Integration Module
- **Purpose:**  
  Provide device-specific signing using a unified interface for YubiKey, Ledger Nano, and a hardcoded key.
- **Submodules:**
  - **YubiKey Integration:**  
    Uses `yubikey-manager`, `fido2`, and `pyusb` for device detection, key retrieval, and signing.
  - **Ledger Nano Integration:**  
    Uses `btchip-python` for secure signing.
  - **Hardcoded Key Module:**  
    Uses `cryptography` for testing.
- **Unified Interface Module:**
  - **DeviceInterface (abstract interface):**  
    - *Methods:*  
      - `get_public_key()`
      - `sign_transaction(transaction_data)`
      - `verify_signature(transaction_data, signature)`
  - Each device-specific submodule implements this interface, ensuring upstream modules interact with a consistent API.
- **Error Handling:**  
  Device-specific errors are managed via the common error handling system described in Section 7.

### D. CLI/Interface Module
- **Purpose:**  
  Provide an interactive command-line interface for all wallet and transaction operations.
- **Key Components:**
  - **CLICommands:**  
    - *Commands:*  
      - `create_wallet`
      - `build_transaction`
      - `sign_transaction`
      - `broadcast_transaction`
      - `monitor_transaction`
  - **Help & Usage:**  
    Built-in help messages via Click, ensuring clear usage instructions.
- **Data Handling:**  
  Parsing command-line inputs and displaying outputs.
- **Error Handling:**  
  User-friendly error messages and structured terminal alerts.

### E. Testing Module
- **Purpose:**  
  Ensure the functionality of every component through unit and integration tests.
- **Testing Strategy:**
  - **Unit Tests:** For individual classes and functions.
  - **Integration Tests:** For end-to-end flows (wallet creation, transaction signing, broadcast, and monitoring).
  - **Mocking:** Use pytest-mock to simulate hardware interactions.
  - **Coverage:** Automated test coverage reporting.
- **Key Test Areas:**  
  Validate correct execution, error handling, and boundary conditions.

### F. Demo Module
- **Purpose:**  
  Provide a complete demonstration script that guides through:
  - Wallet creation.
  - Multisig transaction building.
  - Signing operations from each device (YubiKey, Ledger, hardcoded key).
  - Comprehensive transaction monitoring with real-time terminal alerts/logging.
- **Output:**  
  Terminal logs that reflect lifecycle events from transaction creation to confirmation milestones.

---

## 4. Detailed Project Plan

### Task Breakdown

1. **Environment Setup:**
   - [x] Root folder `BarqHWMuSig` already created.
   - [ ] Set up a Python 3.14 environment using uv.
   - [ ] Install all required packages via the `pyproject.toml` file:
     - `python-bitcoinlib`, `yubikey-manager`, `fido2`, `pyusb`, `btchip-python`, `cryptography`, `Click`, `pytest`, `pytest-mock`, `coverage`, `python-dotenv`.
   - [x] Git already initialized.

2. **Configuration & Environment Module:**
   - [ ] Create configuration files in the `config/` folder using a standard `.env` file.
   - [ ] Implement `ConfigLoader` and configure the logging system in `src/common`.

3. **Bitcoin Transaction Management Module:**
   - [ ] Implement `MultisigWallet` using python-bitcoinlib.
   - [ ] Develop `TransactionBuilder` to handle creation, fee estimation, signing, and broadcasting.
   - [ ] Build `TransactionMonitor` to track and log lifecycle events (creation, mempool, confirmations, errors).

4. **Device Integration Module:**
   - [ ] Develop the YubiKey submodule:
     - Device detection, public key retrieval, signing.
   - [ ] Develop the Ledger Nano submodule:
     - Device detection, public key retrieval, signing.
   - [ ] Develop the Hardcoded Key module:
     - Implement secure key handling and signing.
   - [ ] Create the Unified Interface (`DeviceInterface`) that standardizes the methods (`get_public_key()`, `sign_transaction()`, etc.).
   - [ ] Ensure each submodule implements the unified interface with robust error handling.

5. **CLI/Interface Module:**
   - [ ] Build CLI commands using Click under the `cli/` folder.
   - [ ] Implement commands for wallet creation, transaction operations, and monitoring.
   - [ ] Integrate clear terminal alerts and help messages.

6. **Testing Module:**
   - [ ] Write unit tests for each module and interface.
   - [ ] Develop integration tests to simulate complete multisig flows.
   - [ ] Use pytest-mock to simulate hardware responses.
   - [ ] Set up automated coverage reporting to ensure robust test coverage.

7. **Demo Module:**
   - [ ] Create a demo script (e.g., `demo/demo.py`) that demonstrates:
     - Creating a multisig wallet.
     - Building and signing a transaction with all three keys.
     - Broadcasting the transaction and monitoring its lifecycle.
   - [ ] Document demo instructions and expected outputs in `docs/`.

---

## 5. Scaffolding Guidelines & Folder Structure

**Root Folder:** `BarqHWMuSig`

```
BarqHWMuSig/
├── config/                   # Environment files and configuration (.env file)
├── docs/                     # Documentation and developer guides
│   └── spec.md               # This spec file
├── src/                      # Source code
│   ├── bitcoin_transaction/  # Bitcoin transaction management module
│   │   ├── multisig_wallet.py
│   │   ├── transaction_builder.py
│   │   └── transaction_monitor.py
│   ├── device_integration/   # Device integration module
│   │   ├── yubikey_integration.py
│   │   ├── ledger_integration.py
│   │   ├── hardcoded_key.py
│   │   └── unified_interface.py
│   ├── cli/                  # CLI commands using Click
│   │   └── cli_commands.py
│   └── common/               # Shared utilities (logging, error handling)
│       ├── logger.py
│       └── exceptions.py
├── tests/                    # Unit and integration tests
│   ├── test_bitcoin_transaction.py
│   ├── test_device_integration.py
│   └── test_cli.py
├── demo/                     # Demo scripts and instructions
│   └── demo.py
├── pyproject.toml            # Dependency and package management configuration
└── README.md                 # Project overview and setup instructions
```

**Environment Packages to Install (via pyproject.toml):**
- `python-bitcoinlib`
- `yubikey-manager`
- `fido2`
- `pyusb`
- `btchip-python`
- `cryptography`
- `Click`
- `pytest`, `pytest-mock`, `coverage`
- `python-dotenv`
- Built-in `logging` module (no installation required)

---

## 6. Module Interface Details

### A. Configuration & Environment Module
- **Classes/Interfaces (in `src/common`):**
  - **ConfigLoader**
    - *Inputs:* `.env` file.
    - *Outputs:* Config object with key-value pairs.
  - **Logger**
    - *Methods:* `setup_logger()`, with configuration for levels and output streams.

### B. Bitcoin Transaction Management Module
- **Classes/Interfaces:**
  - **MultisigWallet**
    - *Methods:*  
      - `create_wallet()`: Initializes a multisig wallet.
      - `generate_address()`: Generates a 2-of-3 multisig address.
      - `list_keys()`: Retrieves the involved public keys.
  - **TransactionBuilder**
    - *Methods:*  
      - `create_transaction()`: Build the raw transaction.
      - `estimate_fees()`: Estimate transaction fees.
      - `build()`: Assemble transaction details.
      - `sign()`: Aggregate signatures from devices.
      - `broadcast()`: Send transaction to the network.
  - **TransactionMonitor**
    - *Methods:*  
      - `monitor_transaction()`: Poll blockchain for updates.
      - `log_event()`: Log significant events (creation, mempool, confirmations, errors).

### C. Device Integration Module
- **Classes/Interfaces:**
  - **DeviceInterface (abstract)**
    - *Methods:*  
      - `get_public_key()`
      - `sign_transaction(transaction_data)`
      - `verify_signature(transaction_data, signature)`
  - **YubiKeyDevice** (implements DeviceInterface)
  - **LedgerDevice** (implements DeviceInterface)
  - **HardcodedKeyDevice** (implements DeviceInterface)

### D. CLI/Interface Module
- **Classes/Interfaces:**
  - **CLICommands**
    - *Commands:*  
      - `create_wallet()`
      - `build_transaction()`
      - `sign_transaction()`
      - `broadcast_transaction()`
      - `monitor_transaction()`
    - *Inputs:* Command-line parameters via Click.
    - *Outputs:* Terminal outputs with alerts and logging details.

### E. Testing Module
- **Components:**
  - **TestConfig:** Validates configuration loading and logging.
  - **TestBitcoinTransaction:** Tests multisig wallet creation, transaction building, signing, and broadcasting.
  - **TestDeviceIntegration:** Uses mocks to simulate YubiKey, Ledger, and hardcoded key responses.
  - **TestCLI:** Verifies that CLI commands execute and display expected outputs.

### F. Demo Module
- **Components:**
  - **DemoRunner (or demo.py script)**
    - *Flow:*  
      1. Create multisig wallet.
      2. Build a multisig transaction.
      3. Invoke signing via unified device interface.
      4. Broadcast and monitor transaction.
    - *Outputs:* Terminal logs reflecting the complete lifecycle of the transaction.

---

## 7. Error Handling Strategies

- **General:**
  - Use structured logging to capture all errors with context.
  - Categorize logs with appropriate levels (DEBUG, INFO, WARNING, ERROR).
- **Module-Specific:**
  - **Configuration Module:**  
    Invalid/missing configuration results in immediate error logging and aborting the process.
  - **Transaction Management:**  
    Validate all transaction data; retry or log network errors gracefully.
  - **Device Integration:**  
    Handle device non-detection, communication failures, or signing errors with clear error messages using the common error handling system.
  - **CLI:**  
    Display user-friendly error messages and instructions for recovery.

---

## 8. Testing Plan

- **Unit Testing:**
  - Write tests for each class and method.
  - Use pytest to cover both typical and edge-case scenarios.
- **Integration Testing:**
  - Simulate end-to-end flows from wallet creation to transaction broadcasting.
  - Use pytest-mock to simulate hardware interactions.
- **Coverage:**
  - Ensure test coverage of at least 80% across modules.
- **Error Scenarios:**
  - Test error handling for missing configurations, device failures, and network issues.
- **Continuous Integration:**
  - Automate tests to run on code commits and pull requests.

---

## 9. Demo Execution

- **Objective:**  
  Showcase the complete multisig workflow including wallet creation, multisig transaction generation, signing from three sources, and real-time monitoring.
- **Steps:**
  1. Execute the demo script (`demo/demo.py`).
  2. The script will:
     - Create and display a 2-of-3 multisig wallet.
     - Build a multisig transaction and display the raw data.
     - Invoke the unified signing interface to collect signatures from YubiKey, Ledger Nano, and the hardcoded key.
     - Broadcast the transaction to the Bitcoin network.
     - Monitor the transaction lifecycle and output terminal alerts at each stage (creation, mempool entry, confirmations, errors).
- **Outcome:**  
  Terminal output logs clearly showing every phase of the transaction lifecycle, demonstrating comprehensive functionality and error handling.

---

## 10. Summary

This specification outlines a modular and maintainable architecture for a Bitcoin multisig POC. By using a unified interface for device integration, a robust transaction management module, and a user-friendly CLI built with Click, the solution is designed for clarity, ease of testing, and comprehensive demonstration. The detailed project plan and folder structure ensure that a junior developer can implement the solution step-by-step using CursorAI IDE with minimal ambiguity.