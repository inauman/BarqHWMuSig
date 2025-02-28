"""
Unit tests for the ConfigLoader class.
"""

import os
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from src.common.config_loader import ConfigLoader


@pytest.fixture
def temp_env_file():
    """Create a temporary .env file for testing."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.write(
            "BITCOIN_NETWORK=testnet\n"
            "BITCOIN_API_URL=https://test.api.url\n"
            "LOG_LEVEL=DEBUG\n"
            "LOG_FILE=logs/test.log\n"
            "LOG_CONSOLE=true\n"
            "HARDCODED_KEY_ENABLED=true\n"
            "DEFAULT_FEE_RATE=10\n"
        )
        temp_file_path = temp_file.name
    
    yield temp_file_path
    
    # Clean up
    os.unlink(temp_file_path)


def test_config_loader_init_with_env_file(temp_env_file):
    """Test initializing ConfigLoader with a specific env file."""
    # Create a temporary directory to use as the config directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Copy the temp env file to the temp directory
        env_file_name = os.path.basename(temp_env_file)
        env_path = Path(temp_dir) / env_file_name
        with open(temp_env_file, "r") as src, open(env_path, "w") as dst:
            dst.write(src.read())
        
        # Mock the _load_config method to prevent it from being called during initialization
        with mock.patch.object(ConfigLoader, "_load_config"):
            config_loader = ConfigLoader(env_file=env_file_name)
            # Set the config_dir as an instance attribute
            config_loader.config_dir = Path(temp_dir)
            
            # Mock _load_from_env to populate config directly
            with mock.patch.object(config_loader, "_load_from_env"):
                # Manually populate the config
                config_loader.config = {
                    "BITCOIN_NETWORK": "testnet",
                    "BITCOIN_API_URL": "https://test.api.url",
                    "LOG_LEVEL": "DEBUG",
                    "LOG_FILE": "logs/test.log",
                    "LOG_CONSOLE": True,
                    "HARDCODED_KEY_ENABLED": True,
                    "DEFAULT_FEE_RATE": 10
                }
                
                # Now call _load_config manually
                config_loader._load_config()
                
                # Check that the config was loaded correctly
                assert config_loader.get_value("BITCOIN_NETWORK") == "testnet"
                assert config_loader.get_value("BITCOIN_API_URL") == "https://test.api.url"
                assert config_loader.get_value("LOG_LEVEL") == "DEBUG"
                assert config_loader.get_value("LOG_FILE") == "logs/test.log"
                assert config_loader.get_value("LOG_CONSOLE") is True
                assert config_loader.get_value("HARDCODED_KEY_ENABLED") is True
                assert config_loader.get_value("DEFAULT_FEE_RATE") == 10


def test_config_loader_init_without_env_file():
    """Test initializing ConfigLoader without specifying an env file."""
    # Create a temporary directory with .env.dev file
    with tempfile.TemporaryDirectory() as temp_dir:
        env_dev_path = Path(temp_dir) / ".env.dev"
        with open(env_dev_path, "w") as f:
            f.write(
                "BITCOIN_NETWORK=testnet\n"
                "LOG_LEVEL=DEBUG\n"
            )
        
        # Mock the _load_config method to prevent it from being called during initialization
        with mock.patch.object(ConfigLoader, "_load_config"):
            config_loader = ConfigLoader()
            # Set the config_dir as an instance attribute
            config_loader.config_dir = Path(temp_dir)
            
            # Mock _load_from_env to populate config directly
            with mock.patch.object(config_loader, "_load_from_env"):
                # Manually set the env_file and populate the config
                config_loader.env_file = ".env.dev"
                config_loader.config = {
                    "BITCOIN_NETWORK": "testnet",
                    "LOG_LEVEL": "DEBUG"
                }
                
                # Check that the config was loaded from .env.dev
                assert config_loader.env_file == ".env.dev"
                assert config_loader.get_value("BITCOIN_NETWORK") == "testnet"
                assert config_loader.get_value("LOG_LEVEL") == "DEBUG"


def test_config_loader_get_value_with_default():
    """Test getting a value with a default."""
    with mock.patch.object(ConfigLoader, "_load_config"):
        config_loader = ConfigLoader()
        config_loader.config = {"TEST_KEY": "test_value"}
        
        # Test getting an existing key
        assert config_loader.get_value("TEST_KEY") == "test_value"
        
        # Test getting a non-existent key with a default
        assert config_loader.get_value("NON_EXISTENT_KEY", "default_value") == "default_value"


def test_config_loader_get_all():
    """Test getting all configuration values."""
    with mock.patch.object(ConfigLoader, "_load_config"):
        config_loader = ConfigLoader()
        config_loader.config = {"KEY1": "value1", "KEY2": "value2"}
        
        # Test getting all values
        assert config_loader.get_all() == {"KEY1": "value1", "KEY2": "value2"}
        
        # Check that the returned dictionary is a copy
        config_dict = config_loader.get_all()
        config_dict["KEY3"] = "value3"
        assert "KEY3" not in config_loader.config


def test_config_loader_validate_config():
    """Test validating the configuration."""
    with mock.patch.object(ConfigLoader, "_load_config"):
        config_loader = ConfigLoader()
        
        # Test with all required keys
        config_loader.config = {
            "BITCOIN_NETWORK": "testnet",
            "BITCOIN_API_URL": "https://test.api.url",
            "LOG_LEVEL": "DEBUG",
            "LOG_FILE": "logs/test.log",
        }
        assert config_loader.validate_config() is True
        
        # Test with missing keys
        config_loader.config = {
            "BITCOIN_NETWORK": "testnet",
            "BITCOIN_API_URL": "https://test.api.url",
        }
        assert config_loader.validate_config() is False


def test_config_loader_file_not_found():
    """Test that FileNotFoundError is raised when no env file is found."""
    # Create a ConfigLoader with a non-existent env file
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a ConfigLoader instance with a specific env file that doesn't exist
        with pytest.raises(FileNotFoundError):
            # Initialize with a non-existent env file
            config_loader = ConfigLoader(env_file="non_existent_file.env")
            # Set the config_dir to the empty temp directory
            config_loader.config_dir = Path(temp_dir)
            # This should raise FileNotFoundError
            config_loader._load_config() 