"""
TransactionManager module for BarqHWMuSig.

This module provides functionality for interacting with the Bitcoin blockchain,
including fetching UTXOs, broadcasting transactions, and monitoring transaction status.
"""

import json
import time
from typing import Dict, List, Optional, Union

import requests
from bitcoin.core import CMutableTransaction, b2x, lx, x

from src.common.config_loader import ConfigLoader
from src.common.logger import Logger


class TransactionManager:
    """
    Manages Bitcoin transactions and blockchain interactions.
    
    This class provides methods for fetching UTXOs, broadcasting transactions,
    and monitoring transaction status using a Bitcoin API.
    """
    
    def __init__(self, config_loader: ConfigLoader, logger: Logger) -> None:
        """
        Initialize the TransactionManager.
        
        Args:
            config_loader: The configuration loader instance.
            logger: The logger instance.
        """
        self.config = config_loader
        self.logger = logger
        
        # Get API URL from config
        self.api_url = self.config.get_value("BITCOIN_API_URL")
        if not self.api_url:
            raise ValueError("BITCOIN_API_URL not set in configuration")
        
        # Set API key if available
        self.api_key = self.config.get_value("BITCOIN_API_KEY")
        
        self.logger.info("TransactionManager initialized")
    
    def get_utxos(self, address: str) -> List[Dict]:
        """
        Get unspent transaction outputs (UTXOs) for an address.
        
        Args:
            address: The Bitcoin address to query.
            
        Returns:
            A list of UTXOs, each containing txid, vout, amount, and confirmations.
            
        Raises:
            requests.RequestException: If the API request fails.
        """
        self.logger.debug(f"Fetching UTXOs for address: {address}")
        
        # For testing/mocking purposes, we'll implement a simple API call
        # In a real implementation, this would use a specific blockchain API
        try:
            # Example API endpoint for Blockstream's API
            url = f"{self.api_url}/address/{address}/utxo"
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Parse response
            utxos_raw = response.json()
            
            # Convert to our format
            utxos = []
            for utxo in utxos_raw:
                # Get transaction details to get the amount
                tx_url = f"{self.api_url}/tx/{utxo['txid']}"
                tx_response = requests.get(tx_url, headers=headers)
                tx_response.raise_for_status()
                tx_data = tx_response.json()
                
                # Extract amount from the transaction output
                amount = tx_data["vout"][utxo["vout"]]["value"] / 100000000  # Convert satoshis to BTC
                
                utxos.append({
                    "txid": utxo["txid"],
                    "vout": utxo["vout"],
                    "amount": amount,
                    "confirmations": utxo.get("status", {}).get("block_height", 0)
                })
            
            self.logger.info(f"Found {len(utxos)} UTXOs for address {address}")
            return utxos
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch UTXOs: {str(e)}")
            raise
    
    def broadcast_transaction(self, tx_hex: str) -> str:
        """
        Broadcast a transaction to the Bitcoin network.
        
        Args:
            tx_hex: The transaction in hexadecimal format.
            
        Returns:
            The transaction ID (txid) if successful.
            
        Raises:
            requests.RequestException: If the API request fails.
            ValueError: If the transaction is rejected by the network.
        """
        self.logger.debug(f"Broadcasting transaction: {tx_hex}")
        
        try:
            # Example API endpoint for Blockstream's API
            url = f"{self.api_url}/tx"
            
            headers = {
                "Content-Type": "application/json"
            }
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            data = {"tx": tx_hex}
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            # Parse response to get txid
            txid = response.json().get("txid")
            if not txid:
                raise ValueError("Transaction broadcast successful but no txid returned")
            
            self.logger.info(f"Transaction broadcast successful. TXID: {txid}")
            return txid
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to broadcast transaction: {str(e)}")
            raise
    
    def get_transaction_status(self, txid: str) -> Dict:
        """
        Get the status of a transaction.
        
        Args:
            txid: The transaction ID to query.
            
        Returns:
            A dictionary containing transaction status information.
            
        Raises:
            requests.RequestException: If the API request fails.
        """
        self.logger.debug(f"Checking status of transaction: {txid}")
        
        try:
            # Example API endpoint for Blockstream's API
            url = f"{self.api_url}/tx/{txid}"
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Parse response
            tx_data = response.json()
            
            # Extract relevant information
            status = {
                "txid": txid,
                "confirmed": tx_data.get("status", {}).get("confirmed", False),
                "block_height": tx_data.get("status", {}).get("block_height"),
                "block_hash": tx_data.get("status", {}).get("block_hash"),
                "block_time": tx_data.get("status", {}).get("block_time"),
                "fee": tx_data.get("fee", 0) / 100000000,  # Convert satoshis to BTC
            }
            
            self.logger.info(f"Transaction {txid} status: {'Confirmed' if status['confirmed'] else 'Unconfirmed'}")
            return status
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to get transaction status: {str(e)}")
            raise
    
    def wait_for_confirmation(self, txid: str, confirmations: int = 1, timeout: int = 3600) -> Dict:
        """
        Wait for a transaction to receive a specified number of confirmations.
        
        Args:
            txid: The transaction ID to monitor.
            confirmations: The number of confirmations to wait for.
            timeout: Maximum time to wait in seconds.
            
        Returns:
            The final transaction status.
            
        Raises:
            TimeoutError: If the transaction does not receive the required confirmations within the timeout.
        """
        self.logger.info(f"Waiting for {confirmations} confirmation(s) for transaction {txid}")
        
        start_time = time.time()
        
        while True:
            # Check if we've exceeded the timeout
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Timeout waiting for confirmation of transaction {txid}")
            
            # Get current status
            status = self.get_transaction_status(txid)
            
            # Check if confirmed
            if status.get("confirmed", False):
                # Get current block height
                current_height = self._get_current_block_height()
                
                # Calculate number of confirmations
                tx_height = status.get("block_height", 0)
                current_confirmations = current_height - tx_height + 1 if tx_height > 0 else 0
                
                self.logger.debug(f"Transaction {txid} has {current_confirmations} confirmation(s)")
                
                if current_confirmations >= confirmations:
                    self.logger.info(f"Transaction {txid} confirmed with {current_confirmations} confirmation(s)")
                    return status
            
            # Wait before checking again
            time.sleep(60)  # Check every minute
    
    def _get_current_block_height(self) -> int:
        """
        Get the current block height of the Bitcoin blockchain.
        
        Returns:
            The current block height.
            
        Raises:
            requests.RequestException: If the API request fails.
        """
        try:
            # Example API endpoint for Blockstream's API
            url = f"{self.api_url}/blocks/tip/height"
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Parse response
            height = int(response.text)
            
            return height
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to get current block height: {str(e)}")
            raise 