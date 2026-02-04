"""
Logging configuration for FloatChat Ultra
Uses loguru for beautiful, structured logging
"""

import sys
from pathlib import Path
from loguru import logger
from .config import settings


def setup_logger():
    """
    Configure loguru logger with file and console output
    """
    # Remove default handler
    logger.remove()
    
    # Add console handler with color
    logger.add(
        sys.stderr,
        format=settings.log_format,
        level=settings.log_level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # Add file handler for all logs
    log_file = Path(settings.data_logs_dir) / "floatchat.log"
    logger.add(
        log_file,
        format=settings.log_format,
        level="DEBUG",
        rotation="100 MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    # Add separate file for errors only
    error_log_file = Path(settings.data_logs_dir) / "errors.log"
    logger.add(
        error_log_file,
        format=settings.log_format,
        level="ERROR",
        rotation="50 MB",
        retention="90 days",
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    logger.info(f"Logger initialized - Level: {settings.log_level}")
    logger.info(f"Log files: {log_file}, {error_log_file}")
    
    return logger


# Initialize logger on import
setup_logger()


def get_logger(name: str = None):
    """
    Get a logger instance
    
    Args:
        name: Optional name for the logger (e.g., module name)
    
    Returns:
        Logger instance
    """
    if name:
        return logger.bind(name=name)
    return logger
