"""
Device factory module for BarqHWMuSig.

This module provides a factory for creating and managing hardware device instances.
"""

from typing import Dict, Optional, Type

from src.common.logger import Logger
from src.device_integration.hardware_device import HardwareDevice
from src.device_integration.ledger_device import LedgerDevice
from src.device_integration.yubikey_device import YubiKeyDevice


class DeviceFactory:
    """
    Factory for creating and managing hardware device instances.
    
    This class provides methods for creating and retrieving hardware device
    instances based on device type.
    """
    
    # Device type constants
    YUBIKEY = "yubikey"
    LEDGER = "ledger"
    
    def __init__(self, logger: Logger) -> None:
        """
        Initialize the DeviceFactory.
        
        Args:
            logger: The logger instance.
        """
        self.logger = logger
        self._devices: Dict[str, HardwareDevice] = {}
        
        # Register device types
        self._device_types: Dict[str, Type[HardwareDevice]] = {
            self.YUBIKEY: YubiKeyDevice,
            self.LEDGER: LedgerDevice,
        }
        
        self.logger.info("DeviceFactory initialized")
    
    def get_device(self, device_type: str) -> HardwareDevice:
        """
        Get a hardware device instance.
        
        If a device of the specified type already exists, it will be returned.
        Otherwise, a new device instance will be created.
        
        Args:
            device_type: The type of device to get.
            
        Returns:
            The hardware device instance.
            
        Raises:
            ValueError: If the device type is not supported.
        """
        device_type = device_type.lower()
        
        if device_type not in self._device_types:
            raise ValueError(f"Unsupported device type: {device_type}")
        
        if device_type not in self._devices:
            # Create a new device instance
            device_class = self._device_types[device_type]
            self._devices[device_type] = device_class(self.logger)
            self.logger.info(f"Created new {device_type} device instance")
        
        return self._devices[device_type]
    
    def connect_device(self, device_type: str) -> bool:
        """
        Connect to a hardware device.
        
        Args:
            device_type: The type of device to connect to.
            
        Returns:
            True if connection is successful, False otherwise.
            
        Raises:
            ValueError: If the device type is not supported.
        """
        device = self.get_device(device_type)
        return device.connect()
    
    def disconnect_device(self, device_type: str) -> None:
        """
        Disconnect from a hardware device.
        
        Args:
            device_type: The type of device to disconnect from.
            
        Raises:
            ValueError: If the device type is not supported.
        """
        if device_type.lower() not in self._devices:
            return
        
        device = self._devices[device_type.lower()]
        device.disconnect()
    
    def disconnect_all_devices(self) -> None:
        """Disconnect from all connected hardware devices."""
        for device_type, device in self._devices.items():
            if device.is_connected():
                device.disconnect()
                self.logger.info(f"Disconnected from {device_type} device")
    
    def is_device_connected(self, device_type: str) -> bool:
        """
        Check if a hardware device is connected.
        
        Args:
            device_type: The type of device to check.
            
        Returns:
            True if the device is connected, False otherwise.
            
        Raises:
            ValueError: If the device type is not supported.
        """
        device_type = device_type.lower()
        
        if device_type not in self._device_types:
            raise ValueError(f"Unsupported device type: {device_type}")
        
        if device_type not in self._devices:
            return False
        
        return self._devices[device_type].is_connected() 