"""
Unit tests for the MultisigWallet class.
"""

import json
import os
import tempfile
from pathlib import Path
from unittest import mock

import pytest
import bitcoin
from bitcoin.core import CMutableTransaction, b2x, x
from bitcoin.core.script import CScript, OP_2, OP_3, OP_CHECKMULTISIG

# Set Bitcoin network to testnet for testing
bitcoin.SelectParams("testnet")

from src.bitcoin_transaction.multisig_wallet import MultisigWallet
from src.common.config_loader import ConfigLoader
from src.common.logger import Logger


@pytest.fixture
def mock_config():
    """Create a mock ConfigLoader."""
    with mock.patch.object(ConfigLoader, "_load_config"):
        config = ConfigLoader()
        config.config = {
            "BITCOIN_NETWORK": "testnet",
            "WALLET_DIR": "test_wallets"
        }
        return config


@pytest.fixture
def mock_logger():
    """Create a mock Logger."""
    return mock.MagicMock(spec=Logger)


@pytest.fixture
def wallet(mock_config, mock_logger):
    """Create a MultisigWallet instance."""
    with mock.patch("bitcoin.SelectParams"):
        wallet = MultisigWallet(mock_config, mock_logger)
        # Mock the wallet_dir to use a temporary directory
        wallet.wallet_dir = Path(tempfile.mkdtemp())
        return wallet


@pytest.fixture
def public_keys():
    """Create test public keys."""
    return [
        "02a1633cafcc01ebfb6d78e39f687a1f0995c62fc95f51ead10a02ee0be551b5dc",
        "03433f246a12e6486a51ff08802228c61cf895175a9b49ed4766ea9a9294a3c7fe",
        "02c25e2c5bac7a32d7be381a6b0e7e423c8d5f9b00ce99a7a0c868cf4955641d3c"
    ]


def test_create_wallet(wallet, public_keys):
    """Test creating a wallet."""
    wallet_name = "test_wallet"
    
    # Create the wallet
    address = wallet.create_wallet(wallet_name, public_keys)
    
    # Check that the wallet was created correctly
    assert wallet.wallet_name == wallet_name
    assert wallet.public_keys == public_keys
    assert wallet.p2sh_address == address
    
    # Check that the redeem script was created correctly
    expected_redeem_script = CScript([OP_2] + [x(pk) for pk in public_keys] + [OP_3, OP_CHECKMULTISIG])
    assert wallet.redeem_script == expected_redeem_script
    
    # Check that the wallet file was created
    wallet_path = wallet.wallet_dir / f"{wallet_name}.json"
    assert wallet_path.exists()
    
    # Check the contents of the wallet file
    with open(wallet_path, "r") as f:
        wallet_data = json.load(f)
    
    assert wallet_data["wallet_name"] == wallet_name
    assert wallet_data["public_keys"] == public_keys
    assert wallet_data["p2sh_address"] == address
    assert "utxos" in wallet_data


def test_load_wallet(wallet, public_keys):
    """Test loading a wallet."""
    wallet_name = "test_wallet"
    
    # Create a wallet file
    wallet_path = wallet.wallet_dir / f"{wallet_name}.json"
    wallet_data = {
        "wallet_name": wallet_name,
        "public_keys": public_keys,
        "p2sh_address": "2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX",
        "utxos": []
    }
    
    with open(wallet_path, "w") as f:
        json.dump(wallet_data, f)
    
    # Load the wallet
    address = wallet.load_wallet(wallet_name)
    
    # Check that the wallet was loaded correctly
    assert wallet.wallet_name == wallet_name
    assert wallet.public_keys == public_keys
    assert wallet.p2sh_address == "2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX"
    assert address == "2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX"
    
    # Check that the redeem script was created correctly
    expected_redeem_script = CScript([OP_2] + [x(pk) for pk in public_keys] + [OP_3, OP_CHECKMULTISIG])
    assert wallet.redeem_script == expected_redeem_script


def test_update_utxos(wallet, public_keys):
    """Test updating UTXOs."""
    wallet_name = "test_wallet"
    
    # Create the wallet
    wallet.create_wallet(wallet_name, public_keys)
    
    # Update UTXOs
    utxos = [
        {
            "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "vout": 0,
            "amount": 1.0,
            "confirmations": 6
        }
    ]
    
    wallet.update_utxos(utxos)
    
    # Check that the UTXOs were updated
    assert wallet.utxos == utxos
    
    # Check that the wallet file was updated
    wallet_path = wallet.wallet_dir / f"{wallet_name}.json"
    with open(wallet_path, "r") as f:
        wallet_data = json.load(f)
    
    assert wallet_data["utxos"] == utxos


def test_create_transaction(wallet, public_keys):
    """Test creating a transaction."""
    wallet_name = "test_wallet"
    
    # Create the wallet
    wallet.create_wallet(wallet_name, public_keys)
    
    # Add UTXOs
    utxos = [
        {
            "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "vout": 0,
            "amount": 1.0,
            "confirmations": 6
        }
    ]
    
    wallet.update_utxos(utxos)
    
    # Create a transaction
    outputs = {"2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX": 0.5}
    tx_hex, tx = wallet.create_transaction(outputs)
    
    # Check that the transaction was created
    assert isinstance(tx_hex, str)
    assert isinstance(tx, CMutableTransaction)
    assert len(tx.vin) == 1
    assert len(tx.vout) == 2  # Output + change
    
    # Check that the transaction hex is valid
    assert tx_hex == b2x(tx.serialize())


def test_create_transaction_insufficient_funds(wallet, public_keys):
    """Test creating a transaction with insufficient funds."""
    wallet_name = "test_wallet"
    
    # Create the wallet
    wallet.create_wallet(wallet_name, public_keys)
    
    # Add UTXOs
    utxos = [
        {
            "txid": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "vout": 0,
            "amount": 0.1,
            "confirmations": 6
        }
    ]
    
    wallet.update_utxos(utxos)
    
    # Create a transaction with insufficient funds
    outputs = {"2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX": 0.5}
    
    with pytest.raises(ValueError, match="Insufficient funds"):
        wallet.create_transaction(outputs)


def test_create_transaction_no_utxos(wallet, public_keys):
    """Test creating a transaction with no UTXOs."""
    wallet_name = "test_wallet"
    
    # Create the wallet
    wallet.create_wallet(wallet_name, public_keys)
    
    # Create a transaction with no UTXOs
    outputs = {"2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX": 0.5}
    
    with pytest.raises(ValueError, match="No UTXOs available"):
        wallet.create_transaction(outputs)


def test_create_transaction_no_wallet(wallet):
    """Test creating a transaction with no wallet loaded."""
    # Create a transaction with no wallet loaded
    outputs = {"2N1Ffz3WaNzbeLFBb51xyFMHYSEUXcbiSoX": 0.5}
    
    with pytest.raises(ValueError, match="No wallet loaded"):
        wallet.create_transaction(outputs) 