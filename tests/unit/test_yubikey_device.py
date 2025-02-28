"""
Unit tests for the YubiKeyDevice class.
"""

from unittest import mock

import pytest
import bitcoin
from bitcoin.core import CMutableTransaction
from bitcoin.core.script import CScript, SignatureHash

# Set Bitcoin network to testnet for testing
bitcoin.SelectParams("testnet")

from src.common.logger import Logger
from src.device_integration.yubikey_device import YubiKeyDevice


@pytest.fixture
def mock_logger():
    """Create a mock logger."""
    return mock.MagicMock(spec=Logger)


@pytest.fixture
def yubikey_device(mock_logger):
    """Create a YubiKeyDevice instance."""
    return YubiKeyDevice(mock_logger)


def test_init(yubikey_device):
    """Test initialization of the YubiKeyDevice."""
    assert yubikey_device.logger is not None
    assert not yubikey_device.is_connected()


def test_connect(yubikey_device):
    """Test connecting to the YubiKey device."""
    result = yubikey_device.connect()
    assert result is True
    assert yubikey_device.is_connected()


def test_disconnect(yubikey_device):
    """Test disconnecting from the YubiKey device."""
    # Connect first
    yubikey_device.connect()
    assert yubikey_device.is_connected()

    # Then disconnect
    result = yubikey_device.disconnect()
    assert result is True
    assert not yubikey_device.is_connected()


def test_is_connected(yubikey_device):
    """Test checking if the YubiKey device is connected."""
    assert not yubikey_device.is_connected()
    yubikey_device.connect()
    assert yubikey_device.is_connected()
    yubikey_device.disconnect()
    assert not yubikey_device.is_connected()


def test_get_public_key_not_connected(yubikey_device):
    """Test getting the public key when the device is not connected."""
    with pytest.raises(ConnectionError):
        yubikey_device.get_public_key()


def test_get_public_key(yubikey_device):
    """Test getting the public key."""
    # Connect to the device
    yubikey_device.connect()

    # Get the public key
    public_key = yubikey_device.get_public_key()

    # Check that the public key is a string and has the correct format
    assert isinstance(public_key, str)
    assert len(public_key) == 66  # 33 bytes in hex = 66 characters
    assert public_key.startswith("02") or public_key.startswith("03")


def test_sign_transaction_not_connected(yubikey_device):
    """Test signing a transaction when the device is not connected."""
    mock_transaction = mock.MagicMock(spec=CMutableTransaction)
    mock_redeem_script = b"mock_redeem_script"

    with pytest.raises(ConnectionError):
        yubikey_device.sign_transaction(mock_transaction, mock_redeem_script)


def test_sign_transaction(yubikey_device):
    """Test signing a transaction."""
    # Connect to the device
    yubikey_device.connect()

    # Create a mock transaction and redeem script
    mock_transaction = mock.MagicMock(spec=CMutableTransaction)
    mock_redeem_script = b"mock_redeem_script"

    # Mock the SignatureHash function
    with mock.patch("src.device_integration.yubikey_device.SignatureHash", return_value=b"mock_sighash"):
        # Sign the transaction
        signature = yubikey_device.sign_transaction(mock_transaction, mock_redeem_script)

        # Check that the signature is a string and ends with "01" (SIGHASH_ALL)
        assert isinstance(signature, str)
        assert signature.endswith("01")


def test_sign_transaction_exception(yubikey_device):
    """Test signing a transaction with an exception."""
    # Connect to the device
    yubikey_device.connect()

    # Create a mock transaction and redeem script
    mock_transaction = mock.MagicMock(spec=CMutableTransaction)
    mock_redeem_script = b"mock_redeem_script"

    # Mock the SignatureHash function to raise an exception
    with mock.patch("src.device_integration.yubikey_device.SignatureHash", side_effect=Exception("Test exception")):
        # Sign the transaction
        with pytest.raises(ValueError) as excinfo:
            yubikey_device.sign_transaction(mock_transaction, mock_redeem_script)

        # Check that the exception message contains the original exception message
        assert "Test exception" in str(excinfo.value)


def test_mock_sign(yubikey_device):
    """Test the mock signing function."""
    # Connect to the device
    yubikey_device.connect()

    # Sign some data
    signature = yubikey_device._mock_sign(b"test data")

    # Check that the signature is bytes
    assert isinstance(signature, bytes)
    # Check that the signature has the correct length for a DER-encoded ECDSA signature
    assert len(signature) >= 69 