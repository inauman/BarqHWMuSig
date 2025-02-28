"""
Unit tests for the TransactionSigner class.
"""

import json
from unittest import mock

import pytest
import bitcoin
from bitcoin.core import CMutableTransaction, b2x, x
from bitcoin.core.script import CScript, OP_2, OP_3, OP_CHECKMULTISIG

# Set Bitcoin network to testnet for testing
bitcoin.SelectParams("testnet")

from src.bitcoin_transaction.transaction_signer import TransactionSigner
from src.common.logger import Logger
from src.device_integration.device_factory import DeviceFactory
from src.device_integration.hardware_device import HardwareDevice


@pytest.fixture
def mock_logger():
    """Create a mock Logger."""
    return mock.MagicMock(spec=Logger)


@pytest.fixture
def mock_device():
    """Create a mock HardwareDevice."""
    device = mock.MagicMock(spec=HardwareDevice)
    device.is_connected.return_value = True
    device.sign_transaction.return_value = "01020304"  # Mock signature
    return device


@pytest.fixture
def mock_device_factory(mock_device, mock_logger):
    """Create a mock DeviceFactory."""
    factory = mock.MagicMock(spec=DeviceFactory)
    factory.get_device.return_value = mock_device
    factory.is_device_connected.return_value = True
    return factory


@pytest.fixture
def transaction_signer(mock_device_factory, mock_logger):
    """Create a TransactionSigner instance."""
    return TransactionSigner(mock_device_factory, mock_logger)


@pytest.fixture
def mock_transaction():
    """Create a mock transaction."""
    return mock.MagicMock(spec=CMutableTransaction)


@pytest.fixture
def redeem_script():
    """Create a test redeem script."""
    public_keys = [
        "02a1633cafcc01ebfb6d78e39f687a1f0995c62fc95f51ead10a02ee0be551b5dc",
        "03433f246a12e6486a51ff08802228c61cf895175a9b49ed4766ea9a9294a3c7fe",
        "02c25e2c5bac7a32d7be381a6b0e7e423c8d5f9b00ce99a7a0c868cf4955641d3c"
    ]
    return CScript([OP_2] + [x(pk) for pk in public_keys] + [OP_3, OP_CHECKMULTISIG])


def test_init(transaction_signer, mock_device_factory, mock_logger):
    """Test initializing the TransactionSigner."""
    assert transaction_signer.device_factory == mock_device_factory
    assert transaction_signer.logger == mock_logger


def test_sign_transaction(transaction_signer, mock_transaction, redeem_script, mock_device_factory, mock_device):
    """Test signing a transaction."""
    # Set up the mock transaction
    mock_transaction.serialize.return_value = b"mock_tx_bytes"
    
    # Set up the mock device
    mock_device.sign_transaction.return_value = "01020304"
    
    # Call the method
    device_types = ["yubikey", "ledger"]
    tx_hex, signed_tx = transaction_signer.sign_transaction(
        mock_transaction, redeem_script, device_types
    )
    
    # Check that the device factory was called correctly
    mock_device_factory.get_device.assert_any_call("yubikey")
    mock_device_factory.get_device.assert_any_call("ledger")
    
    # Check that the device was called correctly
    mock_device.is_connected.assert_called()
    mock_device.sign_transaction.assert_called_with(mock_transaction, redeem_script, 0)
    
    # Check that the transaction was modified correctly
    assert signed_tx == mock_transaction
    assert mock_transaction.vin[0].scriptSig is not None


def test_sign_transaction_not_enough_devices(transaction_signer, mock_transaction, redeem_script):
    """Test signing a transaction with not enough devices."""
    # Call the method with only one device
    device_types = ["yubikey"]
    
    # Check that it raises an error
    with pytest.raises(ValueError, match="At least 2 device types are required for 2-of-3 multisig"):
        transaction_signer.sign_transaction(mock_transaction, redeem_script, device_types)


def test_sign_transaction_device_not_connected(transaction_signer, mock_transaction, redeem_script, mock_device_factory, mock_device):
    """Test signing a transaction with a device that is not connected."""
    # Set up the mock device to report as not connected
    mock_device.is_connected.return_value = False
    
    # Call the method
    device_types = ["yubikey", "ledger"]
    
    # Check that it raises an error
    with pytest.raises(ConnectionError):
        transaction_signer.sign_transaction(mock_transaction, redeem_script, device_types)


def test_sign_transaction_with_different_devices(transaction_signer, mock_transaction, redeem_script, mock_device_factory):
    """Test signing a transaction with different devices."""
    # Create different mock devices
    yubikey_device = mock.MagicMock(spec=HardwareDevice)
    yubikey_device.is_connected.return_value = True
    yubikey_device.sign_transaction.return_value = "yubikey_signature"
    
    ledger_device = mock.MagicMock(spec=HardwareDevice)
    ledger_device.is_connected.return_value = True
    ledger_device.sign_transaction.return_value = "ledger_signature"
    
    # Set up the device factory to return different devices
    mock_device_factory.get_device.side_effect = lambda device_type: {
        "yubikey": yubikey_device,
        "ledger": ledger_device
    }[device_type]
    
    # Call the method
    device_types = ["yubikey", "ledger"]
    tx_hex, signed_tx = transaction_signer.sign_transaction(
        mock_transaction, redeem_script, device_types
    )
    
    # Check that both devices were called
    yubikey_device.sign_transaction.assert_called_once()
    ledger_device.sign_transaction.assert_called_once()


def test_verify_transaction(transaction_signer, mock_transaction, redeem_script):
    """Test verifying a transaction."""
    # Call the method
    result = transaction_signer.verify_transaction(mock_transaction, redeem_script)
    
    # Check that it returns True (since the implementation is a placeholder)
    assert result is True 