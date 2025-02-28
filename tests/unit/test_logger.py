"""
Unit tests for the Logger class and setup_logger function.
"""

import logging
import os
import tempfile
from unittest import mock

import pytest

from src.common.logger import Logger, setup_logger


def test_setup_logger_default():
    """Test setup_logger with default parameters."""
    logger = setup_logger("test_logger")
    
    # Check logger name and level
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO
    
    # Check that there is one handler (console)
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)


def test_setup_logger_with_file():
    """Test setup_logger with a file handler."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_file = os.path.join(temp_dir, "test.log")
        logger = setup_logger("test_logger", log_file=log_file)
        
        # Check that there are two handlers (console and file)
        assert len(logger.handlers) == 2
        assert isinstance(logger.handlers[0], logging.StreamHandler)
        assert isinstance(logger.handlers[1], logging.FileHandler)
        assert logger.handlers[1].baseFilename == log_file


def test_setup_logger_level():
    """Test setup_logger with different levels."""
    # Test with string level
    logger = setup_logger("test_logger", level="DEBUG")
    assert logger.level == logging.DEBUG
    
    # Test with integer level
    logger = setup_logger("test_logger", level=logging.ERROR)
    assert logger.level == logging.ERROR


def test_setup_logger_no_console():
    """Test setup_logger without console output."""
    logger = setup_logger("test_logger", console=False)
    
    # Check that there are no handlers
    assert len(logger.handlers) == 0


def test_setup_logger_creates_log_directory():
    """Test that setup_logger creates the log directory if it doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = os.path.join(temp_dir, "logs")
        log_file = os.path.join(log_dir, "test.log")
        
        # Verify the directory doesn't exist yet
        assert not os.path.exists(log_dir)
        
        # Create logger with log file in non-existent directory
        logger = setup_logger("test_logger", log_file=log_file)
        
        # Verify the directory was created
        assert os.path.exists(log_dir)


def test_logger_class_init():
    """Test initializing the Logger class."""
    with mock.patch("src.common.logger.setup_logger") as mock_setup_logger:
        mock_setup_logger.return_value = mock.MagicMock()
        
        logger = Logger("test_logger", "DEBUG", "logs/test.log", True)
        
        # Check that setup_logger was called with the correct parameters
        mock_setup_logger.assert_called_once_with(
            "test_logger", "DEBUG", "logs/test.log", True
        )


def test_logger_class_methods():
    """Test the Logger class methods."""
    # Create a mock logger
    mock_logger = mock.MagicMock()
    
    # Patch setup_logger to return our mock logger
    with mock.patch("src.common.logger.setup_logger", return_value=mock_logger):
        logger = Logger("test_logger")
        
        # Test each method
        logger.debug("debug message")
        mock_logger.debug.assert_called_once_with("debug message")
        
        logger.info("info message")
        mock_logger.info.assert_called_once_with("info message")
        
        logger.warning("warning message")
        mock_logger.warning.assert_called_once_with("warning message")
        
        logger.error("error message")
        mock_logger.error.assert_called_once_with("error message")
        
        logger.critical("critical message")
        mock_logger.critical.assert_called_once_with("critical message")
        
        logger.exception("exception message")
        mock_logger.exception.assert_called_once_with("exception message") 