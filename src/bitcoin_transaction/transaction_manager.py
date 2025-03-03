"""
TransactionManager module for BarqHWMuSig.

This module provides functionality for interacting with the Bitcoin blockchain,
including fetching UTXOs, broadcasting transactions, and monitoring transaction status.
"""

import json
import time
from typing import Dict, List, Optional, Union
from pathlib import Path

import requests
from bitcoin import SelectParams
from bitcoin.rpc import Proxy, JSONRPCError

from src.common.config_loader import ConfigLoader
from src.common.logger import Logger


class TransactionManager:
    """
    Manages Bitcoin transactions and blockchain interactions.
    
    This class provides methods for fetching UTXOs, broadcasting transactions,
    and monitoring transaction status using either Bitcoin Core RPC or a Bitcoin API.
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
        
        # Determine which Bitcoin interface to use based on network
        self.network = self.config.get_value("BITCOIN_NETWORK", "testnet")
        
        # Set the network parameters
        SelectParams(self.network)
        
        if self.network == "regtest":
            # Use Bitcoin Core RPC for regtest mode
            self.logger.info("Using Bitcoin Core RPC for regtest mode")
            
            # Use the specific bitcoin-regtest.conf file
            btc_conf_file = str(Path.home() / ".bitcoin/bitcoin-regtest.conf")
            self.rpc = Proxy(btc_conf_file=btc_conf_file, timeout=30)
            self.use_rpc = True
            
            # Test the connection
            try:
                info = self.rpc.call("getblockchaininfo")
                self.logger.info(f"Connected to Bitcoin Core ({info['chain']} mode)")
            except Exception as e:
                self.logger.error(f"Failed to connect to Bitcoin Core: {e}")
                raise
        else:
            # Use API for mainnet/testnet
            self.use_rpc = False
            
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
        
        if self.use_rpc:
            # Use Bitcoin Core RPC for regtest mode
            try:
                # Import the address to the wallet if it's not already there
                try:
                    self.rpc.call("importaddress", address, "", False)
                except JSONRPCError as e:
                    # If the address is already imported, this is fine
                    self.logger.debug(f"Address import note: {e}")
                
                # Get the UTXOs
                unspent = self.rpc.call("listunspent", 0, 9999999, [address])
                
                # Convert to our format
                utxos = []
                for utxo in unspent:
                    utxos.append({
                        "txid": utxo["txid"],
                        "vout": utxo["vout"],
                        "amount": utxo["amount"],
                        "confirmations": utxo["confirmations"]
                    })
                
                self.logger.info(f"Found {len(utxos)} UTXOs for address {address}")
                return utxos
            except JSONRPCError as e:
                self.logger.error(f"RPC error fetching UTXOs: {e}")
                raise
        
        # For testnet/mainnet, use the API
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
            self.logger.error(f"Error fetching UTXOs: {e}")
            raise
    
    def broadcast_transaction(self, tx_hex: str) -> str:
        """
        Broadcast a raw transaction to the network.
        
        Args:
            tx_hex: The raw transaction in hexadecimal format.
            
        Returns:
            The transaction ID.
            
        Raises:
            requests.RequestException: If the API request fails.
        """
        self.logger.debug(f"Broadcasting transaction: {tx_hex[:64]}...")
        
        if self.use_rpc:
            # Use Bitcoin Core RPC for regtest mode
            try:
                txid = self.rpc.call("sendrawtransaction", tx_hex)
                self.logger.info(f"Transaction broadcast successful. TXID: {txid}")
                return txid
            except JSONRPCError as e:
                self.logger.error(f"RPC error broadcasting transaction: {e}")
                raise
        
        # For testnet/mainnet, use the API
        try:
            # Example API endpoint for Blockstream's API
            url = f"{self.api_url}/tx"
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.post(url, data=tx_hex, headers=headers)
            response.raise_for_status()
            
            # The response should be the transaction ID
            txid = response.text.strip()
            
            self.logger.info(f"Transaction broadcast successful. TXID: {txid}")
            return txid
        except requests.RequestException as e:
            self.logger.error(f"Error broadcasting transaction: {e}")
            raise
    
    def get_transaction_status(self, txid: str) -> Dict:
        """
        Get the status of a transaction.
        
        Args:
            txid: The transaction ID.
            
        Returns:
            A dictionary containing the transaction status.
            
        Raises:
            requests.RequestException: If the API request fails.
        """
        self.logger.debug(f"Getting status for transaction: {txid}")
        
        if self.use_rpc:
            # Use Bitcoin Core RPC for regtest mode
            try:
                # First try gettransaction for wallet transactions
                try:
                    tx_info = self.rpc.call("gettransaction", txid)
                    
                    status = {
                        "txid": txid,
                        "confirmations": tx_info.get("confirmations", 0),
                        "confirmed": tx_info.get("confirmations", 0) > 0,
                        "block_hash": tx_info.get("blockhash"),
                        "block_height": None,  # Not provided by gettransaction
                        "timestamp": tx_info.get("time")
                    }
                    
                    # Get block height if confirmed
                    if status["block_hash"]:
                        block = self.rpc.call("getblock", status["block_hash"])
                        status["block_height"] = block.get("height")
                    
                    self.logger.info(f"Transaction {txid} has {status['confirmations']} confirmations")
                    return status
                    
                except JSONRPCError as e:
                    # If not a wallet transaction, try getrawtransaction
                    if e.error.get("code") == -5:  # No such wallet transaction
                        tx_info = self.rpc.call("getrawtransaction", txid, True)
                        
                        status = {
                            "txid": txid,
                            "confirmations": tx_info.get("confirmations", 0),
                            "confirmed": tx_info.get("confirmations", 0) > 0,
                            "block_hash": tx_info.get("blockhash"),
                            "block_height": None,
                            "timestamp": tx_info.get("time")
                        }
                        
                        # Get block height if confirmed
                        if status["block_hash"]:
                            block = self.rpc.call("getblock", status["block_hash"])
                            status["block_height"] = block.get("height")
                        
                        self.logger.info(f"Transaction {txid} has {status['confirmations']} confirmations")
                        return status
                    else:
                        raise
                        
            except JSONRPCError as e:
                self.logger.error(f"RPC error getting transaction status: {e}")
                return {
                    "txid": txid,
                    "confirmations": 0,
                    "confirmed": False,
                    "block_hash": None,
                    "block_height": None,
                    "timestamp": None,
                    "error": str(e)
                }
        
        # For testnet/mainnet, use the API
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
            
            # Check if the transaction is confirmed
            status = tx_data.get("status", {})
            confirmed = status.get("confirmed", False)
            block_height = status.get("block_height")
            block_hash = status.get("block_hash")
            
            # Get the number of confirmations if confirmed
            confirmations = 0
            if confirmed and block_height:
                # Get current block height
                current_height = self.get_block_height()
                confirmations = current_height - block_height + 1
            
            result = {
                "txid": txid,
                "confirmations": confirmations,
                "confirmed": confirmed,
                "block_hash": block_hash,
                "block_height": block_height,
                "timestamp": tx_data.get("timestamp")
            }
            
            self.logger.info(f"Transaction {txid} has {confirmations} confirmations")
            return result
        except requests.RequestException as e:
            self.logger.error(f"Error getting transaction status: {e}")
            return {
                "txid": txid,
                "confirmations": 0,
                "confirmed": False,
                "block_hash": None,
                "block_height": None,
                "timestamp": None,
                "error": str(e)
            }
    
    def wait_for_confirmation(self, txid: str, min_confirmations: int = 1, timeout: int = 60) -> Dict:
        """
        Wait for a transaction to be confirmed.
        
        Args:
            txid: The transaction ID to monitor.
            min_confirmations: Minimum number of confirmations required.
            timeout: Maximum time to wait in seconds.
            
        Returns:
            Transaction status dictionary.
            
        Raises:
            TimeoutError: If the transaction is not confirmed within the timeout.
        """
        start_time = time.time()
        while True:
            status = self.get_transaction_status(txid)
            if status["confirmations"] >= min_confirmations:
                return status
            
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Transaction {txid} not confirmed within {timeout} seconds")
            
            # Generate a block in regtest mode
            if self.use_rpc:
                address = str(self.rpc.call("getnewaddress"))
                self.rpc.call("generatetoaddress", 1, address)
                self.logger.debug("Generated a new block in regtest mode")
            else:
                # Wait a bit before checking again
                time.sleep(10)
    
    def get_block_height(self) -> int:
        """
        Get the current block height.
        
        Returns:
            The current block height.
            
        Raises:
            requests.RequestException: If the API request fails.
        """
        if self.use_rpc:
            # Use Bitcoin Core RPC for regtest mode
            try:
                return self.rpc.call("getblockcount")
            except JSONRPCError as e:
                self.logger.error(f"RPC error getting block height: {e}")
                raise
        
        # For testnet/mainnet, use the API
        try:
            url = f"{self.api_url}/blocks/tip/height"
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return int(response.text)
        except requests.RequestException as e:
            self.logger.error(f"Error getting block height: {e}")
            raise
    
    def generate_blocks(self, num_blocks: int) -> List[str]:
        """
        Generate new blocks in regtest mode.
        
        Args:
            num_blocks: Number of blocks to generate.
            
        Returns:
            List of block hashes.
            
        Raises:
            RuntimeError: If not in regtest mode.
        """
        if not self.use_rpc:
            raise RuntimeError("Block generation only available in regtest mode")
        
        try:
            address = str(self.rpc.call("getnewaddress"))
            block_hashes = self.rpc.call("generatetoaddress", num_blocks, address)
            return block_hashes
        except JSONRPCError as e:
            self.logger.error(f"RPC error generating blocks: {e}")
            raise
    
    def fund_address(self, address: str, amount: float) -> str:
        """
        Fund an address with the specified amount in regtest mode.
        
        Args:
            address: The address to fund.
            amount: The amount in BTC.
            
        Returns:
            The transaction ID.
            
        Raises:
            RuntimeError: If not in regtest mode.
        """
        if not self.use_rpc:
            raise RuntimeError("Address funding only available in regtest mode")
        
        try:
            txid = self.rpc.call("sendtoaddress", address, amount)
            return txid
        except JSONRPCError as e:
            self.logger.error(f"RPC error funding address: {e}")
            raise 