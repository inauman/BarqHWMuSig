"""
Hardware device integration base module for BarqHWMuSig.

This module provides the base class for hardware device integration,
defining the interface that all hardware device implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union

from bitcoin.core import CMutableTransaction, CTransaction

from src.common.logger import Logger


class HardwareDevice(ABC):
    """
    Abstract base class for hardware device integration.
    
    This class defines the interface that all hardware device implementations
    must follow to integrate with the BarqHWMuSig application.
    """
    
    def __init__(self, logger: Logger) -> None:
        """
        Initialize the hardware device.
        
        Args:
            logger: The logger instance.
        """
        self.logger = logger
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Connect to the hardware device.
        
        Returns:
            True if connection is successful, False otherwise.
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the hardware device."""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Check if the device is connected.
        
        Returns:
            True if the device is connected, False otherwise.
        """
        pass
    
    @abstractmethod
    def get_public_key(self) -> str:
        """
        Get the public key from the hardware device.
        
        Returns:
            The public key in hexadecimal format.
            
        Raises:
            ConnectionError: If the device is not connected.
        """
        pass
    
    @abstractmethod
    def sign_transaction(
        self, 
        transaction: Union[CTransaction, CMutableTransaction], 
        redeem_script: bytes,
        input_index: int = 0
    ) -> str:
        """
        Sign a transaction using the hardware device.
        
        Args:
            transaction: The transaction to sign.
            redeem_script: The redeem script for the multisig address.
            input_index: The index of the input to sign.
            
        Returns:
            The signature in hexadecimal format.
            
        Raises:
            ConnectionError: If the device is not connected.
            ValueError: If the transaction cannot be signed.
        """
        pass 