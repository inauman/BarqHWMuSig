#!/usr/bin/env python3
"""
BarqHWMuSig Demo Script

This script demonstrates the full functionality of the BarqHWMuSig application,
including wallet creation, transaction building, signing with multiple hardware devices,
and transaction broadcasting.
"""

import os
import sys
import time
from pathlib import Path

# Add the parent directory to the path so we can import the src package
sys.path.append(str(Path(__file__).parent.parent))

from src.common.config_loader import ConfigLoader
from src.common.logger import Logger, setup_logger
from src.bitcoin_transaction.multisig_wallet import MultisigWallet
from src.bitcoin_transaction.transaction_signer import TransactionSigner
from src.device_integration.device_factory import DeviceFactory


def setup_environment():
    """Set up the environment for the demo."""
    # Set up logger
    logger = Logger("BarqHWMuSig Demo", level="INFO")
    logger.info("Setting up environment for BarqHWMuSig demo")

    # Load configuration
    config = ConfigLoader()
    
    # Create device factory
    device_factory = DeviceFactory(logger)
    
    return logger, config, device_factory


def create_wallet(logger, config):
    """Create a multisig wallet."""
    logger.info("Creating a 2-of-3 multisig wallet")
    
    # Create a MultisigWallet instance
    wallet = MultisigWallet(config, logger)
    
    # Define the public keys for the multisig wallet
    # In a real scenario, these would be obtained from hardware devices
    public_keys = [
        "02a1633cafcc01ebfb6d78e39f687a1f0995c62fc95f51ead10a02ee0be551b5dc",
        "03433f246a12e6486a51ff08802228c61cf895175a9b49ed4766ea9a9294a3c7fe",
        "02c25e2c5bac7a32d7be381a6b0e7e423c8d5f9b00ce99a7a0c868cf4955641d3c"
    ]
    
    # Create the wallet
    wallet_name = "demo_wallet"
    address = wallet.create_wallet(wallet_name, public_keys)
    
    logger.info(f"Created wallet '{wallet_name}' with address: {address}")
    
    # For demo purposes, add some mock UTXOs
    utxos = [
        {
            "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "vout": 0,
            "amount": 1.0,
            "confirmations": 6
        }
    ]
    
    wallet.update_utxos(utxos)
    logger.info(f"Added mock UTXOs to wallet: {utxos}")
    
    return wallet


def create_transaction(wallet, logger):
    """Create a transaction using the wallet."""
    logger.info("Creating a transaction")
    
    # Define the outputs for the transaction
    # In a real scenario, this would be a real Bitcoin address
    outputs = {"2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX": 0.5}
    
    # Create the transaction
    tx_hex, tx = wallet.create_transaction(outputs)
    
    logger.info(f"Created transaction: {tx_hex[:64]}...")
    logger.info(f"Transaction has {len(tx.vin)} inputs and {len(tx.vout)} outputs")
    
    return tx_hex, tx


def sign_transaction(tx, wallet, device_factory, logger):
    """Sign the transaction using hardware devices."""
    logger.info("Signing the transaction with hardware devices")
    
    # Create a TransactionSigner instance
    transaction_signer = TransactionSigner(device_factory, logger)
    
    # Define the device types to use for signing
    device_types = ["yubikey", "ledger"]
    
    # Connect to the devices
    for device_type in device_types:
        device = device_factory.get_device(device_type)
        if not device.is_connected():
            logger.info(f"Connecting to {device_type} device")
            device.connect()
    
    # Sign the transaction
    try:
        signed_tx_hex, signed_tx = transaction_signer.sign_transaction(
            tx, wallet.redeem_script, device_types
        )
        
        logger.info(f"Transaction signed successfully: {signed_tx_hex[:64]}...")
        logger.info(f"Transaction has {len(signed_tx.vin)} inputs with signatures")
        
        return signed_tx_hex, signed_tx
    except Exception as e:
        logger.error(f"Failed to sign transaction: {str(e)}")
        return None, None
    finally:
        # Disconnect from the devices
        for device_type in device_types:
            device = device_factory.get_device(device_type)
            if device.is_connected():
                logger.info(f"Disconnecting from {device_type} device")
                device.disconnect()


def broadcast_transaction(signed_tx_hex, logger):
    """Broadcast the transaction to the Bitcoin network."""
    logger.info("Broadcasting the transaction to the Bitcoin network")
    
    # In a real scenario, this would use a Bitcoin RPC client or a third-party API
    # For demo purposes, we'll just simulate the broadcast
    
    logger.info("Transaction broadcast simulation started")
    time.sleep(1)  # Simulate network delay
    
    # Simulate a transaction ID
    txid = "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
    
    logger.info(f"Transaction broadcast successful with txid: {txid}")
    
    return txid


def monitor_transaction(txid, logger):
    """Monitor the transaction for confirmations."""
    logger.info(f"Monitoring transaction {txid} for confirmations")
    
    # In a real scenario, this would use a Bitcoin RPC client or a third-party API
    # For demo purposes, we'll just simulate the monitoring
    
    for i in range(1, 4):
        logger.info(f"Checking transaction status... (attempt {i})")
        time.sleep(1)  # Simulate network delay
        
        # Simulate confirmations
        confirmations = i
        logger.info(f"Transaction has {confirmations} confirmation(s)")
    
    logger.info("Transaction monitoring complete")


def run_demo():
    """Run the full demo."""
    logger, config, device_factory = setup_environment()
    
    logger.info("Starting BarqHWMuSig demo")
    logger.info("=" * 80)
    
    # Step 1: Create a wallet
    wallet = create_wallet(logger, config)
    logger.info("=" * 80)
    
    # Step 2: Create a transaction
    tx_hex, tx = create_transaction(wallet, logger)
    logger.info("=" * 80)
    
    # Step 3: Sign the transaction
    signed_tx_hex, signed_tx = sign_transaction(tx, wallet, device_factory, logger)
    if signed_tx_hex is None:
        logger.error("Demo failed at the signing step")
        return
    logger.info("=" * 80)
    
    # Step 4: Broadcast the transaction
    txid = broadcast_transaction(signed_tx_hex, logger)
    logger.info("=" * 80)
    
    # Step 5: Monitor the transaction
    monitor_transaction(txid, logger)
    logger.info("=" * 80)
    
    logger.info("BarqHWMuSig demo completed successfully")


if __name__ == "__main__":
    run_demo() 