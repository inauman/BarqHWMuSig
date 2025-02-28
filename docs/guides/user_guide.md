# User Guide: Bitcoin Multisig Wallet

This guide explains how to use the BarqHWMuSig Bitcoin multisig wallet application. The application allows you to create and manage a 2-of-3 multisig wallet using a combination of hardware devices and a software key.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Creating a Multisig Wallet](#creating-a-multisig-wallet)
- [Building and Signing Transactions](#building-and-signing-transactions)
- [Monitoring Transactions](#monitoring-transactions)
- [Security Best Practices](#security-best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

BarqHWMuSig is a proof-of-concept Bitcoin multisig wallet that supports:

- **2-of-3 Multisignature**: Requires any 2 of 3 keys to authorize a transaction
- **Hardware Device Integration**: 
  - YubiKey (via USB or NFC)
  - Ledger Nano (via USB)
- **Software Key**: For testing or as a backup option
- **Transaction Monitoring**: Track the status of your transactions

The application provides a command-line interface (CLI) for all operations.

## Prerequisites

Before using BarqHWMuSig, you need:

1. **Hardware Devices**:
   - YubiKey with FIDO2 support
   - Ledger Nano with Bitcoin app installed

2. **System Requirements**:
   - Python 3.14.0a5 or compatible version
   - macOS, Linux, or Windows operating system
   - Internet connection for transaction broadcasting and monitoring

## Installation

The application is distributed as a Python package. To install:

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

## Getting Started

After installation, you can run the application using the CLI:

```bash
# Show help
python -m src.cli.cli_commands --help

# Show version
python -m src.cli.cli_commands --version
```

## Creating a Multisig Wallet

### Step 1: Connect Your Hardware Devices

1. Connect your YubiKey to a USB port or place it near an NFC reader
2. Connect your Ledger Nano to a USB port and open the Bitcoin app

### Step 2: Create the Wallet

```bash
python -m src.cli.cli_commands create-wallet
```

The application will:
1. Detect your connected devices
2. Retrieve public keys from each device
3. Create a 2-of-3 multisig wallet
4. Display the wallet address

### Step 3: Backup Your Wallet Information

The application will generate a backup file containing:
- Multisig wallet address
- Public keys (no private keys are stored)
- Redeem script

Save this information securely. You will need it to recover your wallet.

## Building and Signing Transactions

### Step 1: Build a Transaction

```bash
python -m src.cli.cli_commands build-transaction \
  --recipient <bitcoin-address> \
  --amount <amount-in-btc> \
  --fee-rate <fee-rate-in-sat/vbyte>
```

The application will:
1. Check your wallet balance
2. Create a transaction with the specified outputs
3. Calculate the appropriate fee
4. Display the transaction details for review

### Step 2: Sign the Transaction

```bash
python -m src.cli.cli_commands sign-transaction \
  --transaction-id <transaction-id>
```

The application will:
1. Prompt you to connect your hardware devices
2. Display transaction details on the hardware devices
3. Request signatures from the devices
4. Combine the signatures into a complete transaction

### Step 3: Broadcast the Transaction

```bash
python -m src.cli.cli_commands broadcast-transaction \
  --transaction-id <transaction-id>
```

The application will:
1. Verify that the transaction is properly signed
2. Broadcast the transaction to the Bitcoin network
3. Display the transaction ID for tracking

## Monitoring Transactions

### Track Transaction Status

```bash
python -m src.cli.cli_commands monitor-transaction \
  --transaction-id <transaction-id>
```

The application will:
1. Check if the transaction is in the mempool
2. Monitor for confirmations
3. Display real-time updates on the transaction status

### View Transaction History

```bash
python -m src.cli.cli_commands list-transactions
```

The application will display a list of all transactions associated with your wallet, including:
- Transaction ID
- Amount
- Recipients
- Status (pending, confirmed, failed)
- Confirmation count
- Timestamp

## Security Best Practices

### Hardware Device Security

1. **YubiKey**:
   - Set a PIN for your YubiKey
   - Keep your YubiKey in a secure location
   - Consider having a backup YubiKey

2. **Ledger Nano**:
   - Set a PIN for your Ledger Nano
   - Securely store your recovery phrase
   - Keep your Ledger firmware updated

### Wallet Security

1. **Backup Your Wallet Information**:
   - Store your wallet backup in a secure location
   - Consider using multiple secure storage locations

2. **Transaction Verification**:
   - Always verify transaction details on your hardware devices
   - Check recipient addresses carefully
   - Verify transaction amounts and fees

3. **Recovery Planning**:
   - Test your recovery process regularly
   - Ensure you can recover your wallet with any 2 of your 3 keys

## Troubleshooting

### Hardware Device Issues

#### YubiKey Not Detected

1. Ensure the YubiKey is properly connected
2. Try a different USB port
3. Check if the YubiKey is recognized by your operating system
4. Verify that the YubiKey has FIDO2 capability enabled

#### Ledger Nano Issues

1. Ensure the Ledger is connected and unlocked
2. Verify that the Bitcoin app is open on the Ledger
3. Check if the Ledger is in the correct mode
4. Try reconnecting the device

### Transaction Issues

#### Transaction Stuck in Mempool

1. The fee might be too low. Consider using RBF (Replace-By-Fee) to increase the fee
2. Wait for the mempool to clear
3. Check the transaction status on a block explorer

#### Transaction Rejected

1. Verify that the inputs are valid and unspent
2. Check if the transaction size is within limits
3. Ensure the fee is sufficient
4. Verify that the transaction is properly signed

### Application Issues

#### Application Crashes

1. Check the logs in the `logs/` directory
2. Verify that all dependencies are installed
3. Ensure your Python version is compatible
4. Try reinstalling the application

#### Configuration Issues

1. Check your configuration files
2. Verify that environment variables are set correctly
3. Ensure that the application has the necessary permissions

## Getting Help

If you encounter issues not covered in this guide:

1. Check the logs in the `logs/` directory
2. Consult the [Developer Guide](./developer_guide.md) for technical details
3. Contact the project maintainers for support 