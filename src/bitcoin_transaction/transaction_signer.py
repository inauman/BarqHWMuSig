"""
Transaction signer module for BarqHWMuSig.

This module provides functionality for signing Bitcoin transactions
using multiple hardware devices in a 2-of-3 multisig setup.
"""

from typing import Dict, List, Optional, Tuple, Union

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
    OP_0,
    OP_CHECKMULTISIG,
    SignatureHash,
)

from src.common.logger import Logger
from src.device_integration.device_factory import DeviceFactory
from src.device_integration.hardware_device import HardwareDevice


class TransactionSigner:
    """
    Handles the signing of Bitcoin transactions using multiple hardware devices.
    
    This class provides methods for signing transactions with multiple hardware
    devices in a 2-of-3 multisig setup.
    """
    
    def __init__(self, device_factory: DeviceFactory, logger: Logger) -> None:
        """
        Initialize the TransactionSigner.
        
        Args:
            device_factory: The device factory instance.
            logger: The logger instance.
        """
        self.device_factory = device_factory
        self.logger = logger
        
        self.logger.info("TransactionSigner initialized")
    
    def sign_transaction(
        self,
        transaction: Union[CTransaction, CMutableTransaction],
        redeem_script: bytes,
        device_types: List[str],
        input_index: int = 0
    ) -> Tuple[str, CMutableTransaction]:
        """
        Sign a transaction using multiple hardware devices.
        
        Args:
            transaction: The transaction to sign.
            redeem_script: The redeem script for the multisig address.
            device_types: List of device types to use for signing.
            input_index: The index of the input to sign.
            
        Returns:
            A tuple containing the signed transaction hex and the signed transaction object.
            
        Raises:
            ValueError: If fewer than 2 device types are provided.
            ConnectionError: If a device is not connected.
        """
        if len(device_types) < 2:
            raise ValueError("At least 2 device types are required for 2-of-3 multisig")
        
        self.logger.info(f"Signing transaction with devices: {', '.join(device_types)}")
        
        # Create a mutable copy of the transaction
        mutable_tx = CMutableTransaction.from_tx(transaction)
        
        # Get signatures from each device
        signatures = []
        for device_type in device_types:
            device = self.device_factory.get_device(device_type)
            
            if not device.is_connected():
                raise ConnectionError(f"{device_type} device is not connected")
            
            signature = device.sign_transaction(mutable_tx, redeem_script, input_index)
            signatures.append(signature)
            
            self.logger.info(f"Got signature from {device_type} device")
        
        # Create the scriptSig for the multisig input
        # Format: OP_0 <sig1> <sig2> <redeem_script>
        script_sig = CScript([OP_0] + [x(sig) for sig in signatures] + [redeem_script])
        
        # Set the scriptSig for the input
        mutable_tx.vin[input_index].scriptSig = script_sig
        
        # Convert to hex
        tx_hex = b2x(mutable_tx.serialize())
        
        self.logger.info(f"Transaction signed with {len(signatures)} signatures")
        return tx_hex, mutable_tx
    
    def verify_transaction(
        self,
        transaction: Union[CTransaction, CMutableTransaction],
        redeem_script: bytes,
        input_index: int = 0
    ) -> bool:
        """
        Verify that a transaction is properly signed.
        
        Args:
            transaction: The transaction to verify.
            redeem_script: The redeem script for the multisig address.
            input_index: The index of the input to verify.
            
        Returns:
            True if the transaction is properly signed, False otherwise.
        """
        self.logger.info("Verifying transaction signatures")
        
        # TODO: Implement transaction verification
        # This would involve checking that the scriptSig is valid for the given redeem script
        # and that the signatures are valid for the transaction
        
        # For now, we'll just return True
        self.logger.info("Transaction verification not implemented yet")
        return True 