"""
MultisigWallet module for BarqHWMuSig.

This module provides the core functionality for creating and managing
a 2-of-3 Bitcoin multisig wallet with hardware device integration.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import bitcoin
from bitcoin.core import (
    CMutableTransaction,
    CMutableTxIn,
    CMutableTxOut,
    COutPoint,
    CTransaction,
    Hash160,
    b2x,
    lx,
    x,
)
from bitcoin.core.script import (
    CScript,
    OP_2,
    OP_3,
    OP_CHECKMULTISIG,
    SignatureHash,
)
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2SHBitcoinAddress

from src.common.config_loader import ConfigLoader
from src.common.logger import Logger


class MultisigWallet:
    """
    A 2-of-3 Bitcoin multisig wallet implementation.
    
    This class provides functionality to create and manage a 2-of-3 multisig wallet,
    including address generation, transaction creation, and signing.
    """
    
    def __init__(self, config_loader: ConfigLoader, logger: Logger) -> None:
        """
        Initialize the MultisigWallet.
        
        Args:
            config_loader: The configuration loader instance.
            logger: The logger instance.
        """
        self.config = config_loader
        self.logger = logger
        
        # Set the Bitcoin network based on configuration
        network = self.config.get_value("BITCOIN_NETWORK", "testnet")
        if network == "mainnet":
            bitcoin.SelectParams("mainnet")
        else:
            bitcoin.SelectParams("testnet")
        
        self.wallet_dir = Path(self.config.get_value("WALLET_DIR", "wallets"))
        self.wallet_dir.mkdir(exist_ok=True)
        
        # Initialize wallet data
        self.wallet_name: Optional[str] = None
        self.public_keys: List[str] = []
        self.redeem_script: Optional[CScript] = None
        self.p2sh_address: Optional[str] = None
        self.utxos: List[Dict] = []
        
        self.logger.info("MultisigWallet initialized")
    
    def create_wallet(self, wallet_name: str, public_keys: List[str]) -> str:
        """
        Create a new 2-of-3 multisig wallet.
        
        Args:
            wallet_name: The name of the wallet.
            public_keys: List of 3 public keys in hex format.
            
        Returns:
            The P2SH address of the multisig wallet.
            
        Raises:
            ValueError: If the number of public keys is not 3.
        """
        if len(public_keys) != 3:
            raise ValueError("Exactly 3 public keys are required for a 2-of-3 multisig wallet")
        
        self.wallet_name = wallet_name
        self.public_keys = public_keys
        
        # Create redeem script: 2 <pubkey1> <pubkey2> <pubkey3> 3 CHECKMULTISIG
        self.redeem_script = CScript([OP_2] + [x(pk) for pk in public_keys] + [OP_3, OP_CHECKMULTISIG])
        
        # Create P2SH address from redeem script
        self.p2sh_address = str(P2SHBitcoinAddress.from_redeemScript(self.redeem_script))
        
        # Save wallet data
        self._save_wallet()
        
        self.logger.info(f"Created 2-of-3 multisig wallet '{wallet_name}' with address: {self.p2sh_address}")
        return self.p2sh_address
    
    def load_wallet(self, wallet_name: str) -> str:
        """
        Load an existing multisig wallet.
        
        Args:
            wallet_name: The name of the wallet to load.
            
        Returns:
            The P2SH address of the loaded wallet.
            
        Raises:
            FileNotFoundError: If the wallet file does not exist.
        """
        wallet_path = self.wallet_dir / f"{wallet_name}.json"
        if not wallet_path.exists():
            raise FileNotFoundError(f"Wallet file not found: {wallet_path}")
        
        with open(wallet_path, "r") as f:
            wallet_data = json.load(f)
        
        self.wallet_name = wallet_data["wallet_name"]
        self.public_keys = wallet_data["public_keys"]
        self.redeem_script = CScript([OP_2] + [x(pk) for pk in self.public_keys] + [OP_3, OP_CHECKMULTISIG])
        self.p2sh_address = wallet_data["p2sh_address"]
        self.utxos = wallet_data.get("utxos", [])
        
        self.logger.info(f"Loaded multisig wallet '{wallet_name}' with address: {self.p2sh_address}")
        return self.p2sh_address
    
    def update_utxos(self, utxos: List[Dict]) -> None:
        """
        Update the list of UTXOs for the wallet.
        
        Args:
            utxos: List of UTXOs, each containing txid, vout, amount, and confirmations.
        """
        self.utxos = utxos
        self._save_wallet()
        self.logger.info(f"Updated UTXOs for wallet '{self.wallet_name}': {len(utxos)} UTXOs available")
    
    def create_transaction(
        self, 
        outputs: Dict[str, float], 
        fee_rate: Optional[float] = None,
        change_address: Optional[str] = None
    ) -> Tuple[str, CMutableTransaction]:
        """
        Create an unsigned transaction.
        
        Args:
            outputs: Dictionary mapping addresses to amounts in BTC.
            fee_rate: Fee rate in satoshis per byte. If None, use the default from config.
            change_address: Address to send change to. If None, use the wallet's address.
            
        Returns:
            A tuple containing the transaction hex and the transaction object.
            
        Raises:
            ValueError: If there are insufficient funds or no UTXOs available.
        """
        if not self.wallet_name or not self.p2sh_address:
            raise ValueError("No wallet loaded")
        
        if not self.utxos:
            raise ValueError("No UTXOs available")
        
        # Use default fee rate from config if not specified
        if fee_rate is None:
            fee_rate = float(self.config.get_value("DEFAULT_FEE_RATE", "10"))
        
        # Use wallet address as change address if not specified
        if change_address is None:
            change_address = self.p2sh_address
        
        # Calculate total output amount
        total_output = sum(outputs.values())
        
        # Create transaction inputs from UTXOs
        tx_inputs = []
        total_input = 0
        
        for utxo in self.utxos:
            txid = utxo["txid"]
            vout = utxo["vout"]
            amount = utxo["amount"]
            
            # Create transaction input
            tx_in = CMutableTxIn(COutPoint(lx(txid), vout))
            tx_inputs.append(tx_in)
            
            # Add to total input amount
            total_input += amount
            
            # Break if we have enough inputs
            if total_input > total_output:
                break
        
        if total_input < total_output:
            raise ValueError(f"Insufficient funds: {total_input} BTC available, {total_output} BTC required")
        
        # Create transaction outputs
        tx_outputs = []
        
        for address, amount in outputs.items():
            # Convert amount to satoshis
            amount_satoshis = int(amount * 100000000)
            
            # Create transaction output
            tx_out = CMutableTxOut(amount_satoshis, CBitcoinAddress(address).to_scriptPubKey())
            tx_outputs.append(tx_out)
        
        # Calculate change amount (accounting for fee)
        # For simplicity, we're using a fixed fee calculation here
        # In a real implementation, we would calculate the fee based on the transaction size
        estimated_size = 200 + (len(tx_inputs) * 150) + (len(tx_outputs) * 34)
        estimated_fee = int((estimated_size * fee_rate) / 1000)
        
        change_amount = int((total_input * 100000000) - (total_output * 100000000) - estimated_fee)
        
        # Add change output if change amount is significant
        if change_amount > 1000:  # Only add change if it's more than 1000 satoshis
            change_output = CMutableTxOut(change_amount, CBitcoinAddress(change_address).to_scriptPubKey())
            tx_outputs.append(change_output)
        
        # Create the transaction
        tx = CMutableTransaction(tx_inputs, tx_outputs)
        
        # Convert to hex
        tx_hex = b2x(tx.serialize())
        
        self.logger.info(f"Created unsigned transaction for wallet '{self.wallet_name}': {tx_hex}")
        return tx_hex, tx
    
    def _save_wallet(self) -> None:
        """Save the wallet data to a file."""
        if not self.wallet_name:
            return
        
        wallet_path = self.wallet_dir / f"{self.wallet_name}.json"
        
        wallet_data = {
            "wallet_name": self.wallet_name,
            "public_keys": self.public_keys,
            "p2sh_address": self.p2sh_address,
            "utxos": self.utxos
        }
        
        with open(wallet_path, "w") as f:
            json.dump(wallet_data, f, indent=4)
        
        self.logger.debug(f"Saved wallet data to {wallet_path}") 