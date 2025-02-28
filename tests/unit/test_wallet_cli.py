"""
Unit tests for the wallet CLI commands.
"""

import json
import os
from unittest import mock

import click
import pytest
from click.testing import CliRunner

from src.cli.wallet_cli import cli


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


@pytest.fixture
def mock_wallet():
    """Create a mock MultisigWallet."""
    wallet = mock.MagicMock()
    wallet.create_wallet.return_value = "2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX"
    wallet.load_wallet.return_value = "2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX"
    return wallet


@pytest.fixture
def mock_device_factory():
    """Create a mock DeviceFactory."""
    factory = mock.MagicMock()
    factory.connect_device.return_value = True
    factory.is_device_connected.return_value = True
    return factory


@pytest.fixture
def mock_tx_manager():
    """Create a mock TransactionManager."""
    manager = mock.MagicMock()
    manager.get_utxos.return_value = [
        {
            "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "vout": 0,
            "amount": 1.0,
            "confirmations": 6
        }
    ]
    manager.broadcast_transaction.return_value = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    manager.wait_for_confirmation.return_value = {
        "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "confirmed": True,
        "block_height": 100,
        "block_hash": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "block_time": 1600000000,
        "fee": 0.00001
    }
    return manager


@pytest.fixture
def mock_tx_signer():
    """Create a mock TransactionSigner."""
    signer = mock.MagicMock()
    signer.sign_transaction.return_value = (
        "signed_tx_hex",
        mock.MagicMock()
    )
    return signer


@pytest.fixture
def mock_context(mock_wallet, mock_device_factory, mock_tx_manager, mock_tx_signer):
    """Create a mock context for the CLI."""
    return {
        "wallet": mock_wallet,
        "device_factory": mock_device_factory,
        "tx_manager": mock_tx_manager,
        "tx_signer": mock_tx_signer,
        "logger": mock.MagicMock()
    }


def test_create_wallet(runner, mock_context):
    """Test the create-wallet command."""
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            ["create-wallet", "test_wallet", "pubkey1", "pubkey2", "pubkey3"],
            obj=mock_context
        )
        
        assert result.exit_code == 0
        assert "Created wallet 'test_wallet' with address: 2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX" in result.output
        
        mock_context["wallet"].create_wallet.assert_called_once_with(
            "test_wallet", ["pubkey1", "pubkey2", "pubkey3"]
        )


def test_create_wallet_error(runner, mock_context):
    """Test the create-wallet command with an error."""
    mock_context["wallet"].create_wallet.side_effect = ValueError("Test error")
    
    result = runner.invoke(
        cli,
        ["create-wallet", "test_wallet", "pubkey1", "pubkey2", "pubkey3"],
        obj=mock_context
    )
    
    assert result.exit_code == 1
    assert "Error: Test error" in result.output


def test_load_wallet(runner, mock_context):
    """Test the load-wallet command."""
    result = runner.invoke(
        cli,
        ["load-wallet", "test_wallet"],
        obj=mock_context
    )
    
    assert result.exit_code == 0
    assert "Loaded wallet 'test_wallet' with address: 2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX" in result.output
    
    mock_context["wallet"].load_wallet.assert_called_once_with("test_wallet")


def test_load_wallet_error(runner, mock_context):
    """Test the load-wallet command with an error."""
    mock_context["wallet"].load_wallet.side_effect = FileNotFoundError("Wallet file not found")
    
    result = runner.invoke(
        cli,
        ["load-wallet", "test_wallet"],
        obj=mock_context
    )
    
    assert result.exit_code == 1
    assert "Error: Wallet file not found" in result.output


def test_connect_device(runner, mock_context):
    """Test the connect-device command."""
    result = runner.invoke(
        cli,
        ["connect-device", "yubikey"],
        obj=mock_context
    )
    
    assert result.exit_code == 0
    assert "Connected to yubikey device" in result.output
    
    mock_context["device_factory"].connect_device.assert_called_once_with("yubikey")


def test_connect_device_error(runner, mock_context):
    """Test the connect-device command with an error."""
    mock_context["device_factory"].connect_device.return_value = False
    
    result = runner.invoke(
        cli,
        ["connect-device", "yubikey"],
        obj=mock_context
    )
    
    assert result.exit_code == 1
    assert "Failed to connect to yubikey device" in result.output


def test_get_public_key(runner, mock_context):
    """Test the get-public-key command."""
    # Create a mock device
    mock_device = mock.MagicMock()
    mock_device.is_connected.return_value = True
    mock_device.get_public_key.return_value = "02a1633cafcc01ebfb6d78e39f687a1f0995c62fc95f51ead10a02ee0be551b5dc"
    
    # Set up the device factory to return the mock device
    mock_context["device_factory"].get_device.return_value = mock_device
    
    result = runner.invoke(
        cli,
        ["get-public-key", "yubikey"],
        obj=mock_context
    )
    
    assert result.exit_code == 0
    assert "Public key from yubikey device: 02a1633cafcc01ebfb6d78e39f687a1f0995c62fc95f51ead10a02ee0be551b5dc" in result.output
    
    mock_context["device_factory"].get_device.assert_called_once_with("yubikey")
    mock_device.get_public_key.assert_called_once()


def test_get_public_key_not_connected(runner, mock_context):
    """Test the get-public-key command when the device is not connected."""
    # Create a mock device
    mock_device = mock.MagicMock()
    mock_device.is_connected.return_value = False
    
    # Set up the device factory to return the mock device
    mock_context["device_factory"].get_device.return_value = mock_device
    
    result = runner.invoke(
        cli,
        ["get-public-key", "yubikey"],
        obj=mock_context
    )
    
    assert result.exit_code == 1
    assert "Device yubikey is not connected" in result.output


def test_update_utxos(runner, mock_context):
    """Test the update-utxos command."""
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            ["update-utxos", "test_wallet"],
            obj=mock_context
        )
        
        assert result.exit_code == 0
        assert "Updated UTXOs for wallet 'test_wallet': 1 UTXOs available" in result.output
        
        mock_context["wallet"].load_wallet.assert_called_once_with("test_wallet")
        mock_context["tx_manager"].get_utxos.assert_called_once()
        mock_context["wallet"].update_utxos.assert_called_once()


def test_update_utxos_error(runner, mock_context):
    """Test the update-utxos command with an error."""
    mock_context["wallet"].load_wallet.side_effect = FileNotFoundError("Wallet file not found")
    
    result = runner.invoke(
        cli,
        ["update-utxos", "test_wallet"],
        obj=mock_context
    )
    
    assert result.exit_code == 1
    assert "Error: Wallet file not found" in result.output


def test_create_transaction(runner, mock_context):
    """Test the create-transaction command."""
    # Set up the mock wallet to return a transaction
    mock_context["wallet"].create_transaction.return_value = ("tx_hex", mock.MagicMock())
    
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            ["create-transaction", "test_wallet", "2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX", "0.5"],
            obj=mock_context
        )
        
        assert result.exit_code == 0
        assert "Created unsigned transaction: tx_hex" in result.output
        assert "Transaction saved to test_wallet_unsigned_tx.json" in result.output
        
        mock_context["wallet"].load_wallet.assert_called_once_with("test_wallet")
        mock_context["wallet"].create_transaction.assert_called_once_with(
            {"2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX": 0.5},
            None,
            None
        )
        
        # Check that the transaction file was created
        assert os.path.exists("test_wallet_unsigned_tx.json")
        with open("test_wallet_unsigned_tx.json", "r") as f:
            tx_data = json.load(f)
            assert tx_data["tx_hex"] == "tx_hex"
            assert tx_data["outputs"] == {"2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX": 0.5}


def test_create_transaction_with_options(runner, mock_context):
    """Test the create-transaction command with fee rate and change address options."""
    # Set up the mock wallet to return a transaction
    mock_context["wallet"].create_transaction.return_value = ("tx_hex", mock.MagicMock())
    
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "create-transaction",
                "test_wallet",
                "2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX",
                "0.5",
                "--fee-rate", "20",
                "--change-address", "2MzQwSSnBHWHqSAqtTVQ6v47XtaisrJa1Vc"
            ],
            obj=mock_context
        )
        
        assert result.exit_code == 0
        
        mock_context["wallet"].create_transaction.assert_called_once_with(
            {"2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX": 0.5},
            20.0,
            "2MzQwSSnBHWHqSAqtTVQ6v47XtaisrJa1Vc"
        )


def test_create_transaction_error(runner, mock_context):
    """Test the create-transaction command with an error."""
    mock_context["wallet"].create_transaction.side_effect = ValueError("Insufficient funds")
    
    result = runner.invoke(
        cli,
        ["create-transaction", "test_wallet", "2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX", "0.5"],
        obj=mock_context
    )
    
    assert result.exit_code == 1
    assert "Error: Insufficient funds" in result.output


def test_sign_transaction(runner, mock_context):
    """Test the sign-transaction command."""
    # Create a mock transaction file
    tx_data = {
        "tx_hex": "unsigned_tx_hex",
        "outputs": {"2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX": 0.5}
    }
    
    with runner.isolated_filesystem():
        # Create the transaction file
        with open("test_wallet_unsigned_tx.json", "w") as f:
            json.dump(tx_data, f)
        
        # Set up the mock wallet
        mock_context["wallet"].redeem_script = b"mock_redeem_script"
        
        result = runner.invoke(
            cli,
            ["sign-transaction", "test_wallet", "test_wallet_unsigned_tx.json", "yubikey", "ledger"],
            obj=mock_context
        )
        
        assert result.exit_code == 0
        assert "Signed transaction: signed_tx_hex" in result.output
        assert "Transaction saved to test_wallet_signed_tx.json" in result.output
        
        mock_context["wallet"].load_wallet.assert_called_once_with("test_wallet")
        mock_context["device_factory"].is_device_connected.assert_any_call("yubikey")
        mock_context["device_factory"].is_device_connected.assert_any_call("ledger")
        mock_context["tx_signer"].sign_transaction.assert_called_once()
        
        # Check that the signed transaction file was created
        assert os.path.exists("test_wallet_signed_tx.json")
        with open("test_wallet_signed_tx.json", "r") as f:
            signed_tx_data = json.load(f)
            assert signed_tx_data["tx_hex"] == "signed_tx_hex"
            assert signed_tx_data["outputs"] == {"2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX": 0.5}


def test_sign_transaction_error(runner, mock_context):
    """Test the sign-transaction command with an error."""
    # Create a mock transaction file
    tx_data = {
        "tx_hex": "unsigned_tx_hex",
        "outputs": {"2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX": 0.5}
    }
    
    with runner.isolated_filesystem():
        # Create the transaction file
        with open("test_wallet_unsigned_tx.json", "w") as f:
            json.dump(tx_data, f)
        
        # Set up the mock wallet
        mock_context["wallet"].redeem_script = b"mock_redeem_script"
        
        # Set up the mock signer to raise an error
        mock_context["tx_signer"].sign_transaction.side_effect = ValueError("Signing error")
        
        result = runner.invoke(
            cli,
            ["sign-transaction", "test_wallet", "test_wallet_unsigned_tx.json", "yubikey", "ledger"],
            obj=mock_context
        )
        
        assert result.exit_code == 1
        assert "Error: Signing error" in result.output


def test_broadcast_transaction(runner, mock_context):
    """Test the broadcast-transaction command."""
    # Create a mock transaction file
    tx_data = {
        "tx_hex": "signed_tx_hex",
        "outputs": {"2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX": 0.5}
    }
    
    with runner.isolated_filesystem():
        # Create the transaction file
        with open("test_wallet_signed_tx.json", "w") as f:
            json.dump(tx_data, f)
        
        result = runner.invoke(
            cli,
            ["broadcast-transaction", "test_wallet_signed_tx.json"],
            obj=mock_context
        )
        
        assert result.exit_code == 0
        assert "Transaction broadcast successful. TXID: 1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef" in result.output
        
        mock_context["tx_manager"].broadcast_transaction.assert_called_once_with("signed_tx_hex")


def test_broadcast_transaction_error(runner, mock_context):
    """Test the broadcast-transaction command with an error."""
    # Create a mock transaction file
    tx_data = {
        "tx_hex": "signed_tx_hex",
        "outputs": {"2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX": 0.5}
    }
    
    with runner.isolated_filesystem():
        # Create the transaction file
        with open("test_wallet_signed_tx.json", "w") as f:
            json.dump(tx_data, f)
        
        # Set up the mock transaction manager to raise an error
        mock_context["tx_manager"].broadcast_transaction.side_effect = ValueError("Broadcast error")
        
        result = runner.invoke(
            cli,
            ["broadcast-transaction", "test_wallet_signed_tx.json"],
            obj=mock_context
        )
        
        assert result.exit_code == 1
        assert "Error: Broadcast error" in result.output


def test_wait_for_confirmation(runner, mock_context):
    """Test the wait-for-confirmation command."""
    result = runner.invoke(
        cli,
        ["wait-for-confirmation", "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"],
        obj=mock_context
    )
    
    assert result.exit_code == 0
    assert "Transaction 1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef confirmed with 1 confirmation(s)" in result.output
    assert "Block height: 100" in result.output
    
    mock_context["tx_manager"].wait_for_confirmation.assert_called_once_with(
        "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        1,
        3600
    )


def test_wait_for_confirmation_with_options(runner, mock_context):
    """Test the wait-for-confirmation command with options."""
    result = runner.invoke(
        cli,
        [
            "wait-for-confirmation",
            "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "--confirmations", "6",
            "--timeout", "7200"
        ],
        obj=mock_context
    )
    
    assert result.exit_code == 0
    
    mock_context["tx_manager"].wait_for_confirmation.assert_called_once_with(
        "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        6,
        7200
    )


def test_wait_for_confirmation_error(runner, mock_context):
    """Test the wait-for-confirmation command with an error."""
    # Set up the mock transaction manager to raise an error
    mock_context["tx_manager"].wait_for_confirmation.side_effect = TimeoutError("Timeout waiting for confirmation")
    
    result = runner.invoke(
        cli,
        ["wait-for-confirmation", "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"],
        obj=mock_context
    )
    
    assert result.exit_code == 1
    assert "Error: Timeout waiting for confirmation" in result.output 