"""
Logging configuration for the BarqHWMuSig application.

This module provides a function to set up logging with appropriate levels
and handlers for both console and file output.
"""

import logging
import os
from pathlib import Path
from typing import Optional, Union


def setup_logger(
    name: str,
    level: Union[str, int] = "INFO",
    log_file: Optional[str] = None,
    console: bool = True,
) -> logging.Logger:
    """
    Set up a logger with the specified name and level.
    
    Args:
        name: The name of the logger.
        level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: The path to the log file. If None, no file handler will be added.
        console: Whether to add a console handler.
        
    Returns:
        A configured logger instance.
    """
    # Convert string level to logging level
    if isinstance(level, str):
        level = getattr(logging, level.upper())
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    
    # Clear existing handlers
    logger.handlers = []
    
    # Add console handler if requested
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # Add file handler if log_file is provided
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir:
            Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    
    return logger


class Logger:
    """
    A wrapper class for the logging module.
    
    This class provides a simple interface to the logging module,
    with methods for each logging level.
    """
    
    def __init__(
        self,
        name: str,
        level: Union[str, int] = "INFO",
        log_file: Optional[str] = None,
        console: bool = True,
    ) -> None:
        """
        Initialize the Logger.
        
        Args:
            name: The name of the logger.
            level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            log_file: The path to the log file. If None, no file handler will be added.
            console: Whether to add a console handler.
        """
        self.logger = setup_logger(name, level, log_file, console)
    
    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log a critical message."""
        self.logger.critical(message)
    
    def exception(self, message: str) -> None:
        """Log an exception message with traceback."""
        self.logger.exception(message) 