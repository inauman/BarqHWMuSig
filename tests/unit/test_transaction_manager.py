"""
Unit tests for the TransactionManager class.
"""

import json
from unittest import mock

import pytest
import requests

from src.bitcoin_transaction.transaction_manager import TransactionManager
from src.common.config_loader import ConfigLoader
from src.common.logger import Logger


@pytest.fixture
def mock_config():
    """Create a mock ConfigLoader."""
    with mock.patch.object(ConfigLoader, "_load_config"):
        config = ConfigLoader()
        config.config = {
            "BITCOIN_API_URL": "https://blockstream.info/testnet/api",
            "BITCOIN_API_KEY": "test_api_key"
        }
        return config


@pytest.fixture
def mock_logger():
    """Create a mock Logger."""
    return mock.MagicMock(spec=Logger)


@pytest.fixture
def tx_manager(mock_config, mock_logger):
    """Create a TransactionManager instance."""
    return TransactionManager(mock_config, mock_logger)


def test_init(tx_manager):
    """Test initializing the TransactionManager."""
    assert tx_manager.api_url == "https://blockstream.info/testnet/api"
    assert tx_manager.api_key == "test_api_key"


def test_init_no_api_url():
    """Test initializing the TransactionManager with no API URL."""
    config = mock.MagicMock(spec=ConfigLoader)
    config.get_value.return_value = None
    logger = mock.MagicMock(spec=Logger)
    
    with pytest.raises(ValueError, match="BITCOIN_API_URL not set in configuration"):
        TransactionManager(config, logger)


def test_get_utxos(tx_manager):
    """Test getting UTXOs."""
    # Mock the requests.get method
    with mock.patch("requests.get") as mock_get:
        # Mock the response for the UTXOs
        mock_utxo_response = mock.MagicMock()
        mock_utxo_response.json.return_value = [
            {
                "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                "vout": 0,
                "status": {"block_height": 6}
            }
        ]
        
        # Mock the response for the transaction details
        mock_tx_response = mock.MagicMock()
        mock_tx_response.json.return_value = {
            "vout": [
                {
                    "value": 100000000  # 1 BTC in satoshis
                }
            ]
        }
        
        # Set up the mock to return the appropriate response for each call
        mock_get.side_effect = [mock_utxo_response, mock_tx_response]
        
        # Call the method
        utxos = tx_manager.get_utxos("2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX")
        
        # Check that the requests were made correctly
        mock_get.assert_any_call(
            "https://blockstream.info/testnet/api/address/2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX/utxo",
            headers={"Authorization": "Bearer test_api_key"}
        )
        
        mock_get.assert_any_call(
            "https://blockstream.info/testnet/api/tx/1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            headers={"Authorization": "Bearer test_api_key"}
        )
        
        # Check that the UTXOs were processed correctly
        assert len(utxos) == 1
        assert utxos[0]["txid"] == "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        assert utxos[0]["vout"] == 0
        assert utxos[0]["amount"] == 1.0
        assert utxos[0]["confirmations"] == 6


def test_get_utxos_request_exception(tx_manager):
    """Test getting UTXOs with a request exception."""
    # Mock the requests.get method to raise an exception
    with mock.patch("requests.get", side_effect=requests.RequestException("Test error")):
        # Call the method and check that it raises the exception
        with pytest.raises(requests.RequestException, match="Test error"):
            tx_manager.get_utxos("2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX")


def test_broadcast_transaction(tx_manager):
    """Test broadcasting a transaction."""
    # Mock the requests.post method
    with mock.patch("requests.post") as mock_post:
        # Mock the response
        mock_response = mock.MagicMock()
        mock_response.json.return_value = {
            "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        }
        mock_post.return_value = mock_response
        
        # Call the method
        txid = tx_manager.broadcast_transaction("test_tx_hex")
        
        # Check that the request was made correctly
        mock_post.assert_called_once_with(
            "https://blockstream.info/testnet/api/tx",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer test_api_key"
            },
            json={"tx": "test_tx_hex"}
        )
        
        # Check that the txid was returned correctly
        assert txid == "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"


def test_broadcast_transaction_request_exception(tx_manager):
    """Test broadcasting a transaction with a request exception."""
    # Mock the requests.post method to raise an exception
    with mock.patch("requests.post", side_effect=requests.RequestException("Test error")):
        # Call the method and check that it raises the exception
        with pytest.raises(requests.RequestException, match="Test error"):
            tx_manager.broadcast_transaction("test_tx_hex")


def test_broadcast_transaction_no_txid(tx_manager):
    """Test broadcasting a transaction with no txid in the response."""
    # Mock the requests.post method
    with mock.patch("requests.post") as mock_post:
        # Mock the response
        mock_response = mock.MagicMock()
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response
        
        # Call the method and check that it raises an exception
        with pytest.raises(ValueError, match="Transaction broadcast successful but no txid returned"):
            tx_manager.broadcast_transaction("test_tx_hex")


def test_get_transaction_status(tx_manager):
    """Test getting transaction status."""
    # Mock the requests.get method
    with mock.patch("requests.get") as mock_get:
        # Mock the response
        mock_response = mock.MagicMock()
        mock_response.json.return_value = {
            "status": {
                "confirmed": True,
                "block_height": 100,
                "block_hash": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                "block_time": 1600000000
            },
            "fee": 1000  # 1000 satoshis
        }
        mock_get.return_value = mock_response
        
        # Call the method
        status = tx_manager.get_transaction_status("test_txid")
        
        # Check that the request was made correctly
        mock_get.assert_called_once_with(
            "https://blockstream.info/testnet/api/tx/test_txid",
            headers={"Authorization": "Bearer test_api_key"}
        )
        
        # Check that the status was processed correctly
        assert status["txid"] == "test_txid"
        assert status["confirmed"] is True
        assert status["block_height"] == 100
        assert status["block_hash"] == "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        assert status["block_time"] == 1600000000
        assert status["fee"] == 0.00001  # 1000 satoshis = 0.00001 BTC


def test_get_transaction_status_request_exception(tx_manager):
    """Test getting transaction status with a request exception."""
    # Mock the requests.get method to raise an exception
    with mock.patch("requests.get", side_effect=requests.RequestException("Test error")):
        # Call the method and check that it raises the exception
        with pytest.raises(requests.RequestException, match="Test error"):
            tx_manager.get_transaction_status("test_txid")


def test_get_current_block_height(tx_manager):
    """Test getting the current block height."""
    # Mock the requests.get method
    with mock.patch("requests.get") as mock_get:
        # Mock the response
        mock_response = mock.MagicMock()
        mock_response.text = "100"
        mock_get.return_value = mock_response
        
        # Call the method
        height = tx_manager._get_current_block_height()
        
        # Check that the request was made correctly
        mock_get.assert_called_once_with(
            "https://blockstream.info/testnet/api/blocks/tip/height",
            headers={"Authorization": "Bearer test_api_key"}
        )
        
        # Check that the height was returned correctly
        assert height == 100


def test_get_current_block_height_request_exception(tx_manager):
    """Test getting the current block height with a request exception."""
    # Mock the requests.get method to raise an exception
    with mock.patch("requests.get", side_effect=requests.RequestException("Test error")):
        # Call the method and check that it raises the exception
        with pytest.raises(requests.RequestException, match="Test error"):
            tx_manager._get_current_block_height()


def test_wait_for_confirmation(tx_manager):
    """Test waiting for confirmation."""
    # Mock the get_transaction_status and _get_current_block_height methods
    with mock.patch.object(tx_manager, "get_transaction_status") as mock_get_status, \
         mock.patch.object(tx_manager, "_get_current_block_height") as mock_get_height, \
         mock.patch("time.sleep") as mock_sleep:
        
        # Mock the responses
        mock_get_status.return_value = {
            "txid": "test_txid",
            "confirmed": True,
            "block_height": 100
        }
        mock_get_height.return_value = 101  # 1 confirmation
        
        # Call the method
        status = tx_manager.wait_for_confirmation("test_txid")
        
        # Check that the methods were called correctly
        mock_get_status.assert_called_once_with("test_txid")
        mock_get_height.assert_called_once()
        
        # Check that the status was returned correctly
        assert status["txid"] == "test_txid"
        assert status["confirmed"] is True
        assert status["block_height"] == 100


def test_wait_for_confirmation_timeout(tx_manager):
    """Test waiting for confirmation with a timeout."""
    # Mock the get_transaction_status and _get_current_block_height methods
    with mock.patch.object(tx_manager, "get_transaction_status") as mock_get_status, \
         mock.patch.object(tx_manager, "_get_current_block_height") as mock_get_height, \
         mock.patch("time.sleep") as mock_sleep, \
         mock.patch("time.time") as mock_time:
        
        # Mock the responses
        mock_get_status.return_value = {
            "txid": "test_txid",
            "confirmed": False
        }
        
        # Mock time.time to simulate timeout
        mock_time.side_effect = [0, 3601]  # Start time, end time (1 hour + 1 second)
        
        # Call the method and check that it raises a timeout
        with pytest.raises(TimeoutError, match="Timeout waiting for confirmation of transaction test_txid"):
            tx_manager.wait_for_confirmation("test_txid", timeout=3600)
        
        # Check that the methods were called correctly
        mock_get_status.assert_called_once_with("test_txid")
        mock_time.assert_called()
        mock_sleep.assert_not_called()  # Should not sleep if timeout is exceeded 