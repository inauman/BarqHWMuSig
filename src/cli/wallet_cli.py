"""
Command-line interface for the BarqHWMuSig wallet.

This module provides a command-line interface for interacting with the
BarqHWMuSig wallet, including creating wallets, managing devices,
and creating and signing transactions.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import click

from src.bitcoin_transaction.multisig_wallet import MultisigWallet
from src.bitcoin_transaction.transaction_manager import TransactionManager
from src.bitcoin_transaction.transaction_signer import TransactionSigner
from src.common.config_loader import ConfigLoader
from src.common.logger import Logger
from src.device_integration.device_factory import DeviceFactory


@click.group()
@click.option(
    "--config-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Path to the configuration directory",
)
@click.option(
    "--env-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Path to the environment file",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    help="Log level",
)
@click.pass_context
def cli(ctx, config_dir, env_file, log_level):
    """BarqHWMuSig - Bitcoin Multisig Wallet with Hardware Device Integration."""
    # Initialize configuration
    config_loader = ConfigLoader(env_file)
    
    # Override config directory if provided
    if config_dir:
        config_loader.config_dir = Path(config_dir)
    
    # Initialize logger
    log_file = config_loader.get_value("LOG_FILE", "logs/barqhwmusig.log")
    log_level = log_level or config_loader.get_value("LOG_LEVEL", "INFO")
    logger = Logger.setup_logger("barqhwmusig", log_file, log_level)
    
    # Initialize device factory
    device_factory = DeviceFactory(logger)
    
    # Initialize wallet
    wallet = MultisigWallet(config_loader, logger)
    
    # Initialize transaction manager
    tx_manager = TransactionManager(config_loader, logger)
    
    # Initialize transaction signer
    tx_signer = TransactionSigner(device_factory, logger)
    
    # Store objects in context
    ctx.obj = {
        "config": config_loader,
        "logger": logger,
        "device_factory": device_factory,
        "wallet": wallet,
        "tx_manager": tx_manager,
        "tx_signer": tx_signer,
    }
    
    logger.info("CLI initialized")


@cli.command()
@click.argument("wallet_name", type=str)
@click.argument("public_keys", type=str, nargs=3)
@click.pass_context
def create_wallet(ctx, wallet_name, public_keys):
    """
    Create a new 2-of-3 multisig wallet.
    
    WALLET_NAME is the name of the wallet to create.
    PUBLIC_KEYS are the 3 public keys to use for the multisig wallet.
    """
    wallet = ctx.obj["wallet"]
    logger = ctx.obj["logger"]
    
    try:
        address = wallet.create_wallet(wallet_name, public_keys)
        click.echo(f"Created wallet '{wallet_name}' with address: {address}")
    except Exception as e:
        logger.error(f"Failed to create wallet: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("wallet_name", type=str)
@click.pass_context
def load_wallet(ctx, wallet_name):
    """
    Load an existing wallet.
    
    WALLET_NAME is the name of the wallet to load.
    """
    wallet = ctx.obj["wallet"]
    logger = ctx.obj["logger"]
    
    try:
        address = wallet.load_wallet(wallet_name)
        click.echo(f"Loaded wallet '{wallet_name}' with address: {address}")
    except Exception as e:
        logger.error(f"Failed to load wallet: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("device_type", type=click.Choice(["yubikey", "ledger"], case_sensitive=False))
@click.pass_context
def connect_device(ctx, device_type):
    """
    Connect to a hardware device.
    
    DEVICE_TYPE is the type of device to connect to (yubikey or ledger).
    """
    device_factory = ctx.obj["device_factory"]
    logger = ctx.obj["logger"]
    
    try:
        success = device_factory.connect_device(device_type)
        if success:
            click.echo(f"Connected to {device_type} device")
        else:
            click.echo(f"Failed to connect to {device_type} device", err=True)
            sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to connect to device: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("device_type", type=click.Choice(["yubikey", "ledger"], case_sensitive=False))
@click.pass_context
def get_public_key(ctx, device_type):
    """
    Get the public key from a hardware device.
    
    DEVICE_TYPE is the type of device to get the public key from (yubikey or ledger).
    """
    device_factory = ctx.obj["device_factory"]
    logger = ctx.obj["logger"]
    
    try:
        device = device_factory.get_device(device_type)
        if not device.is_connected():
            click.echo(f"Device {device_type} is not connected", err=True)
            sys.exit(1)
        
        public_key = device.get_public_key()
        click.echo(f"Public key from {device_type} device: {public_key}")
    except Exception as e:
        logger.error(f"Failed to get public key: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("wallet_name", type=str)
@click.pass_context
def update_utxos(ctx, wallet_name):
    """
    Update the UTXOs for a wallet.
    
    WALLET_NAME is the name of the wallet to update.
    """
    wallet = ctx.obj["wallet"]
    tx_manager = ctx.obj["tx_manager"]
    logger = ctx.obj["logger"]
    
    try:
        # Load the wallet
        wallet.load_wallet(wallet_name)
        
        # Get UTXOs from the blockchain
        utxos = tx_manager.get_utxos(wallet.p2sh_address)
        
        # Update the wallet
        wallet.update_utxos(utxos)
        
        click.echo(f"Updated UTXOs for wallet '{wallet_name}': {len(utxos)} UTXOs available")
    except Exception as e:
        logger.error(f"Failed to update UTXOs: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("wallet_name", type=str)
@click.argument("output_address", type=str)
@click.argument("amount", type=float)
@click.option("--fee-rate", type=float, help="Fee rate in satoshis per byte")
@click.option("--change-address", type=str, help="Address to send change to")
@click.pass_context
def create_transaction(ctx, wallet_name, output_address, amount, fee_rate, change_address):
    """
    Create an unsigned transaction.
    
    WALLET_NAME is the name of the wallet to use.
    OUTPUT_ADDRESS is the address to send to.
    AMOUNT is the amount to send in BTC.
    """
    wallet = ctx.obj["wallet"]
    logger = ctx.obj["logger"]
    
    try:
        # Load the wallet
        wallet.load_wallet(wallet_name)
        
        # Create the transaction
        outputs = {output_address: amount}
        tx_hex, tx = wallet.create_transaction(outputs, fee_rate, change_address)
        
        # Save the transaction to a file
        tx_file = f"{wallet_name}_unsigned_tx.json"
        with open(tx_file, "w") as f:
            json.dump({
                "tx_hex": tx_hex,
                "outputs": outputs,
                "fee_rate": fee_rate,
                "change_address": change_address
            }, f, indent=4)
        
        click.echo(f"Created unsigned transaction: {tx_hex}")
        click.echo(f"Transaction saved to {tx_file}")
    except Exception as e:
        logger.error(f"Failed to create transaction: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("wallet_name", type=str)
@click.argument("tx_file", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument("device_types", type=str, nargs=2)
@click.pass_context
def sign_transaction(ctx, wallet_name, tx_file, device_types):
    """
    Sign a transaction with hardware devices.
    
    WALLET_NAME is the name of the wallet to use.
    TX_FILE is the path to the transaction file.
    DEVICE_TYPES are the types of devices to use for signing (yubikey and/or ledger).
    """
    wallet = ctx.obj["wallet"]
    tx_signer = ctx.obj["tx_signer"]
    logger = ctx.obj["logger"]
    
    try:
        # Load the wallet
        wallet.load_wallet(wallet_name)
        
        # Load the transaction
        with open(tx_file, "r") as f:
            tx_data = json.load(f)
        
        tx_hex = tx_data["tx_hex"]
        
        # Connect to devices
        device_factory = ctx.obj["device_factory"]
        for device_type in device_types:
            if not device_factory.is_device_connected(device_type):
                device_factory.connect_device(device_type)
        
        # Sign the transaction
        from bitcoin.core import CMutableTransaction, x
        tx = CMutableTransaction.deserialize(x(tx_hex))
        redeem_script = wallet.redeem_script
        
        signed_tx_hex, signed_tx = tx_signer.sign_transaction(tx, redeem_script, device_types)
        
        # Save the signed transaction to a file
        signed_tx_file = f"{wallet_name}_signed_tx.json"
        with open(signed_tx_file, "w") as f:
            json.dump({
                "tx_hex": signed_tx_hex,
                "outputs": tx_data["outputs"],
                "fee_rate": tx_data.get("fee_rate"),
                "change_address": tx_data.get("change_address")
            }, f, indent=4)
        
        click.echo(f"Signed transaction: {signed_tx_hex}")
        click.echo(f"Transaction saved to {signed_tx_file}")
    except Exception as e:
        logger.error(f"Failed to sign transaction: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("tx_file", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.pass_context
def broadcast_transaction(ctx, tx_file):
    """
    Broadcast a transaction to the Bitcoin network.
    
    TX_FILE is the path to the transaction file.
    """
    tx_manager = ctx.obj["tx_manager"]
    logger = ctx.obj["logger"]
    
    try:
        # Load the transaction
        with open(tx_file, "r") as f:
            tx_data = json.load(f)
        
        tx_hex = tx_data["tx_hex"]
        
        # Broadcast the transaction
        txid = tx_manager.broadcast_transaction(tx_hex)
        
        click.echo(f"Transaction broadcast successful. TXID: {txid}")
    except Exception as e:
        logger.error(f"Failed to broadcast transaction: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("txid", type=str)
@click.option("--confirmations", type=int, default=1, help="Number of confirmations to wait for")
@click.option("--timeout", type=int, default=3600, help="Timeout in seconds")
@click.pass_context
def wait_for_confirmation(ctx, txid, confirmations, timeout):
    """
    Wait for a transaction to be confirmed.
    
    TXID is the transaction ID to monitor.
    """
    tx_manager = ctx.obj["tx_manager"]
    logger = ctx.obj["logger"]
    
    try:
        click.echo(f"Waiting for {confirmations} confirmation(s) for transaction {txid}...")
        status = tx_manager.wait_for_confirmation(txid, confirmations, timeout)
        
        click.echo(f"Transaction {txid} confirmed with {confirmations} confirmation(s)")
        click.echo(f"Block height: {status.get('block_height')}")
        click.echo(f"Block hash: {status.get('block_hash')}")
        click.echo(f"Block time: {status.get('block_time')}")
        click.echo(f"Fee: {status.get('fee')} BTC")
    except Exception as e:
        logger.error(f"Failed to wait for confirmation: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli(obj={}) 