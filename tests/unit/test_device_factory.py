"""
Unit tests for the DeviceFactory class.
"""

from unittest import mock

import pytest

from src.common.logger import Logger
from src.device_integration.device_factory import DeviceFactory
from src.device_integration.hardware_device import HardwareDevice
from src.device_integration.ledger_device import LedgerDevice
from src.device_integration.yubikey_device import YubiKeyDevice


@pytest.fixture
def mock_logger():
    """Create a mock Logger."""
    return mock.MagicMock(spec=Logger)


@pytest.fixture
def device_factory(mock_logger):
    """Create a DeviceFactory instance."""
    return DeviceFactory(mock_logger)


def test_init(device_factory, mock_logger):
    """Test initializing the DeviceFactory."""
    assert device_factory.logger == mock_logger
    assert device_factory._devices == {}
    assert device_factory._device_types == {
        DeviceFactory.YUBIKEY: YubiKeyDevice,
        DeviceFactory.LEDGER: LedgerDevice,
    }


def test_get_device(device_factory):
    """Test getting a device."""
    # Get a YubiKey device
    device = device_factory.get_device(DeviceFactory.YUBIKEY)
    
    # Check that the device is of the correct type
    assert isinstance(device, YubiKeyDevice)
    
    # Check that the device is stored in the factory
    assert DeviceFactory.YUBIKEY in device_factory._devices
    assert device_factory._devices[DeviceFactory.YUBIKEY] == device
    
    # Get the same device again
    device2 = device_factory.get_device(DeviceFactory.YUBIKEY)
    
    # Check that it's the same instance
    assert device2 is device


def test_get_device_case_insensitive(device_factory):
    """Test getting a device with case-insensitive device type."""
    # Get a YubiKey device with uppercase
    device = device_factory.get_device(DeviceFactory.YUBIKEY.upper())
    
    # Check that the device is of the correct type
    assert isinstance(device, YubiKeyDevice)
    
    # Check that the device is stored in the factory with lowercase key
    assert DeviceFactory.YUBIKEY in device_factory._devices
    assert device_factory._devices[DeviceFactory.YUBIKEY] == device


def test_get_device_unsupported_type(device_factory):
    """Test getting a device with an unsupported type."""
    # Try to get a device with an unsupported type
    with pytest.raises(ValueError, match="Unsupported device type: unsupported"):
        device_factory.get_device("unsupported")


def test_connect_device(device_factory):
    """Test connecting to a device."""
    # Mock the device
    mock_device = mock.MagicMock(spec=HardwareDevice)
    mock_device.connect.return_value = True
    
    # Replace the get_device method to return the mock device
    device_factory.get_device = mock.MagicMock(return_value=mock_device)
    
    # Connect to the device
    result = device_factory.connect_device(DeviceFactory.YUBIKEY)
    
    # Check that the device was connected
    device_factory.get_device.assert_called_once_with(DeviceFactory.YUBIKEY)
    mock_device.connect.assert_called_once()
    assert result is True


def test_disconnect_device(device_factory):
    """Test disconnecting from a device."""
    # Create a mock device
    mock_device = mock.MagicMock(spec=HardwareDevice)
    
    # Add the device to the factory
    device_factory._devices[DeviceFactory.YUBIKEY] = mock_device
    
    # Disconnect from the device
    device_factory.disconnect_device(DeviceFactory.YUBIKEY)
    
    # Check that the device was disconnected
    mock_device.disconnect.assert_called_once()


def test_disconnect_device_not_in_factory(device_factory):
    """Test disconnecting from a device that is not in the factory."""
    # Disconnect from a device that is not in the factory
    device_factory.disconnect_device(DeviceFactory.YUBIKEY)
    
    # Check that no error was raised
    assert True


def test_disconnect_all_devices(device_factory):
    """Test disconnecting from all devices."""
    # Create mock devices
    yubikey_device = mock.MagicMock(spec=HardwareDevice)
    yubikey_device.is_connected.return_value = True
    
    ledger_device = mock.MagicMock(spec=HardwareDevice)
    ledger_device.is_connected.return_value = False
    
    # Add the devices to the factory
    device_factory._devices[DeviceFactory.YUBIKEY] = yubikey_device
    device_factory._devices[DeviceFactory.LEDGER] = ledger_device
    
    # Disconnect from all devices
    device_factory.disconnect_all_devices()
    
    # Check that only the connected device was disconnected
    yubikey_device.disconnect.assert_called_once()
    ledger_device.disconnect.assert_not_called()


def test_is_device_connected(device_factory):
    """Test checking if a device is connected."""
    # Create a mock device
    mock_device = mock.MagicMock(spec=HardwareDevice)
    mock_device.is_connected.return_value = True
    
    # Add the device to the factory
    device_factory._devices[DeviceFactory.YUBIKEY] = mock_device
    
    # Check if the device is connected
    result = device_factory.is_device_connected(DeviceFactory.YUBIKEY)
    
    # Check that the device was checked
    mock_device.is_connected.assert_called_once()
    assert result is True


def test_is_device_connected_not_in_factory(device_factory):
    """Test checking if a device is connected when it's not in the factory."""
    # Check if a device is connected when it's not in the factory
    result = device_factory.is_device_connected(DeviceFactory.YUBIKEY)
    
    # Check that the result is False
    assert result is False


def test_is_device_connected_unsupported_type(device_factory):
    """Test checking if a device is connected with an unsupported type."""
    # Try to check if a device is connected with an unsupported type
    with pytest.raises(ValueError, match="Unsupported device type: unsupported"):
        device_factory.is_device_connected("unsupported") 