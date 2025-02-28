"""
Configuration loader for the BarqHWMuSig application.

This module provides functionality to load and access configuration
from environment variables using python-dotenv.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

from dotenv import load_dotenv


class ConfigLoader:
    """
    Loads and provides access to application configuration from environment variables.
    
    This class is responsible for loading configuration from .env files and
    providing a consistent interface to access configuration values.
    """

    def __init__(self, env_file: Optional[str] = None) -> None:
        """
        Initialize the ConfigLoader.
        
        Args:
            env_file: Path to the .env file. If None, it will try to load from
                     .env.dev, .env.local, or .env in the config directory.
        """
        self.config_dir = Path("config")
        self.env_file = env_file
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """
        Load configuration from the environment file.
        
        Tries to load from the specified env_file, or falls back to
        .env.dev, .env.local, or .env in the config directory.
        
        Raises:
            FileNotFoundError: If no environment file could be found.
        """
        if self.env_file:
            env_path = self.config_dir / self.env_file
            if not env_path.exists():
                raise FileNotFoundError(f"Environment file not found: {env_path}")
            load_dotenv(env_path)
        else:
            # Try to load from .env.dev, .env.local, or .env
            for env_name in [".env.dev", ".env.local", ".env"]:
                env_path = self.config_dir / env_name
                if env_path.exists():
                    load_dotenv(env_path)
                    self.env_file = env_name
                    break
            else:
                raise FileNotFoundError(
                    "No environment file found. Please create .env.dev, .env.local, or .env in the config directory."
                )
        
        # Load all environment variables into the config dictionary
        self._load_from_env()

    def _load_from_env(self) -> None:
        """Load all environment variables into the config dictionary."""
        # Convert environment variables to appropriate types
        for key, value in os.environ.items():
            # Skip environment variables that are not related to our application
            if not key.startswith(("BITCOIN_", "LOG_", "HARDCODED_KEY_", "YUBIKEY_", "LEDGER_", "DEFAULT_", "MAX_", "MIN_")):
                continue
                
            # Convert boolean values
            if value.lower() in ("true", "yes", "1"):
                self.config[key] = True
            elif value.lower() in ("false", "no", "0"):
                self.config[key] = False
            # Convert integer values
            elif value.isdigit():
                self.config[key] = int(value)
            # Keep string values as is
            else:
                self.config[key] = value

    def get_value(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: The configuration key to retrieve.
            default: The default value to return if the key is not found.
            
        Returns:
            The configuration value, or the default if the key is not found.
        """
        return self.config.get(key, default)

    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values.
        
        Returns:
            A dictionary containing all configuration values.
        """
        return self.config.copy()

    def validate_config(self) -> bool:
        """
        Validate that all required configuration values are present.
        
        Returns:
            True if all required configuration values are present, False otherwise.
        """
        required_keys = [
            "BITCOIN_NETWORK",
            "BITCOIN_API_URL",
            "LOG_LEVEL",
            "LOG_FILE",
        ]
        
        for key in required_keys:
            if key not in self.config:
                return False
        
        return True 