"""
Unit tests for the LedgerDevice class.
"""

from unittest import mock

import pytest
import bitcoin
from bitcoin.core import CMutableTransaction, CScript
from bitcoin.core.script import SignatureHash

# Set Bitcoin network to testnet for testing
bitcoin.SelectParams("testnet")

from src.common.logger import Logger
from src.device_integration.ledger_device import LedgerDevice


@pytest.fixture
def mock_logger():
    """Create a mock logger."""
    return mock.MagicMock(spec=Logger)


@pytest.fixture
def ledger_device(mock_logger):
    """Create a LedgerDevice instance."""
    return LedgerDevice(mock_logger)


def test_init(ledger_device):
    """Test initialization of the LedgerDevice."""
    assert ledger_device.logger is not None
    assert not ledger_device.is_connected()


def test_connect(ledger_device):
    """Test connecting to the Ledger device."""
    result = ledger_device.connect()
    assert result is True
    assert ledger_device.is_connected()


def test_disconnect(ledger_device):
    """Test disconnecting from the Ledger device."""
    # Connect first
    ledger_device.connect()
    assert ledger_device.is_connected()

    # Then disconnect
    result = ledger_device.disconnect()
    assert result is True
    assert not ledger_device.is_connected()


def test_is_connected(ledger_device):
    """Test checking if the Ledger device is connected."""
    assert not ledger_device.is_connected()
    ledger_device.connect()
    assert ledger_device.is_connected()
    ledger_device.disconnect()
    assert not ledger_device.is_connected()


def test_get_public_key_not_connected(ledger_device):
    """Test getting the public key when the device is not connected."""
    with pytest.raises(ConnectionError):
        ledger_device.get_public_key()


def test_get_public_key(ledger_device):
    """Test getting the public key."""
    # Connect to the device
    ledger_device.connect()

    # Get the public key
    public_key = ledger_device.get_public_key()

    # Check that the public key is a string and has the correct format
    assert isinstance(public_key, str)
    assert len(public_key) == 66  # 33 bytes in hex = 66 characters
    assert public_key.startswith("02") or public_key.startswith("03")


def test_sign_transaction_not_connected(ledger_device):
    """Test signing a transaction when the device is not connected."""
    mock_transaction = mock.MagicMock(spec=CMutableTransaction)
    mock_redeem_script = b"mock_redeem_script"

    with pytest.raises(ConnectionError):
        ledger_device.sign_transaction(mock_transaction, mock_redeem_script)


def test_sign_transaction(ledger_device):
    """Test signing a transaction."""
    # Connect to the device
    ledger_device.connect()
    
    # Create a mock transaction and redeem script
    mock_transaction = mock.MagicMock(spec=CMutableTransaction)
    mock_redeem_script = b"mock_redeem_script"
    
    # Mock the SignatureHash function and _mock_sign method
    with mock.patch("src.device_integration.ledger_device.SignatureHash", return_value=b"mock_sighash"), \
         mock.patch.object(ledger_device, "_mock_sign", return_value=b"mock_signature"):
        
        # Sign the transaction
        signature = ledger_device.sign_transaction(mock_transaction, mock_redeem_script)
        
        # Check that the signature is a string and ends with "01" (SIGHASH_ALL)
        assert isinstance(signature, str)
        assert signature.endswith("01")
        
        # Check that _mock_sign was called with the correct arguments
        ledger_device._mock_sign.assert_called_once_with(b"mock_sighash")


def test_sign_transaction_exception(ledger_device):
    """Test signing a transaction with an exception."""
    # Connect to the device
    ledger_device.connect()
    
    # Create a mock transaction and redeem script
    mock_transaction = mock.MagicMock(spec=CMutableTransaction)
    mock_redeem_script = b"mock_redeem_script"
    
    # Mock the SignatureHash function to raise an exception
    with mock.patch("src.device_integration.ledger_device.SignatureHash", side_effect=Exception("Test error")):
        # Try to sign the transaction
        with pytest.raises(ValueError, match="Failed to sign transaction: Test error"):
            ledger_device.sign_transaction(mock_transaction, mock_redeem_script)


def test_mock_sign(ledger_device):
    """Test the mock signing function."""
    # Connect to the device
    ledger_device.connect()
    
    # Sign some data
    signature = ledger_device._mock_sign(b"test data")
    
    # Check that the signature is bytes
    assert isinstance(signature, bytes)


def test_sign_transaction_with_input_index(ledger_device):
    """Test signing a transaction with a specific input index."""
    # Connect to the device
    ledger_device.connect()
    
    # Create a mock transaction and redeem script
    mock_transaction = mock.MagicMock(spec=CMutableTransaction)
    mock_redeem_script = b"mock_redeem_script"
    input_index = 2
    
    # Mock the SignatureHash function and _mock_sign method
    with mock.patch("src.device_integration.ledger_device.SignatureHash") as mock_sighash, \
         mock.patch.object(ledger_device, "_mock_sign", return_value=b"mock_signature"):
        
        # Sign the transaction
        ledger_device.sign_transaction(mock_transaction, mock_redeem_script, input_index)
        
        # Check that SignatureHash was called with the correct input index
        mock_sighash.assert_called_once_with(mock.ANY, mock_transaction, input_index, 0x01) 