"""
Test script for Bitcoin Core regtest integration.
"""

import logging
import sys
from pathlib import Path

from src.common.config_loader import ConfigLoader
from src.common.logger import Logger
from src.bitcoin_transaction.transaction_manager import TransactionManager


def main():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )
    logger = Logger("RegTest")
    
    # Load configuration
    config = ConfigLoader()
    
    # Create transaction manager
    tx_manager = TransactionManager(config, logger)
    
    # Create a new address
    address = str(tx_manager.rpc.call("getnewaddress"))
    logger.info(f"Created new address: {address}")
    
    # Generate 101 blocks (to make coins spendable)
    block_hashes = tx_manager.generate_blocks(101)
    logger.info(f"Generated {len(block_hashes)} blocks")
    
    # Get blockchain info
    info = tx_manager.rpc.call("getblockchaininfo")
    logger.info(f"Current block height: {info['blocks']}")
    
    # Send some coins to the address
    amount = 10.0  # 10 BTC
    txid = tx_manager.fund_address(address, amount)
    logger.info(f"Sent {amount} BTC to {address}. TXID: {txid}")
    
    # Wait for confirmation
    status = tx_manager.wait_for_confirmation(txid)
    logger.info(f"Transaction confirmed with {status['confirmations']} confirmations")
    
    # Get UTXOs for the address
    utxos = tx_manager.get_utxos(address)
    logger.info(f"Found {len(utxos)} UTXOs for address {address}:")
    for utxo in utxos:
        logger.info(f"  - {utxo['amount']} BTC ({utxo['confirmations']} confirmations)")


if __name__ == "__main__":
    main() 