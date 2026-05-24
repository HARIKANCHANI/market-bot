"""
Centralized Logging Configuration for All Bots
Controls file logging, console logging, and log levels per bot
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# =============================================================================
# LOGGING CONFIGURATION - Control All Bots From Here
# =============================================================================

LOGGING_CONFIG = {
    "bots": {
        "market_bot_lite": {
            "file_logging": False,      # Enable/disable file logging
            "console_logging": True,    # Enable/disable console output
            "log_level": "INFO"         # DEBUG, INFO, WARNING, ERROR, CRITICAL
        },
        "market_bot_lite_incremental": {
            "file_logging": False,
            "console_logging": True,
            "log_level": "INFO"
        },
        "market_bot_pro": {
            "file_logging": False,
            "console_logging": True,
            "log_level": "INFO"
        },
        "market_bot_pro_incremental": {
            "file_logging": False,
            "console_logging": True,
            "log_level": "INFO"
        },
        "market_bot_ai": {
            "file_logging": True,       # ✅ ENABLED for full bot run
            "console_logging": True,
            "log_level": "INFO"
        },
        "market_bot_ai_incremental": {
            "file_logging": False,
            "console_logging": True,
            "log_level": "INFO"
        },
        "market_bot_excel": {
            "file_logging": False,
            "console_logging": True,
            "log_level": "INFO"
        },
    }
}

# =============================================================================
# LOGGING SETUP FUNCTION
# =============================================================================

def setup_bot_logging(bot_name):
    """
    Setup centralized logging for a specific bot
    
    Args:
        bot_name (str): Name of the bot (must match key in LOGGING_CONFIG)
    
    Returns:
        logging.Logger: Configured logger instance
    
    Features:
        - File logging: Configurable per bot (default: OFF)
        - Console logging: Configurable per bot (default: ON)
        - Log level: Configurable per bot (default: INFO)
        - Log rotation: Automatic for DEBUG level (10MB limit)
        - Format: Detailed with line numbers
    
    Example:
        >>> logger = setup_bot_logging("market_bot_lite")
        >>> logger.info("Processing stocks...")
    """
    # Get bot configuration
    if bot_name not in LOGGING_CONFIG["bots"]:
        raise ValueError(
            f"Bot '{bot_name}' not found in LOGGING_CONFIG. "
            f"Available bots: {list(LOGGING_CONFIG['bots'].keys())}"
        )
    
    config = LOGGING_CONFIG["bots"][bot_name]
    
    # Extract settings
    file_logging_enabled = config.get("file_logging", False)
    console_logging_enabled = config.get("console_logging", True)
    log_level_str = config.get("log_level", "INFO")
    
    # Convert log level string to logging constant
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    
    # Create logger
    logger = logging.getLogger(bot_name)
    logger.setLevel(log_level)
    
    # Remove any existing handlers (avoid duplicates on re-runs)
    logger.handlers.clear()
    
    # Log message format (detailed with line numbers)
    log_format = "%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
    
    # CONSOLE HANDLER (if enabled)
    if console_logging_enabled:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # FILE HANDLER (if enabled)
    if file_logging_enabled:
        # Create logs directory if it doesn't exist
        logs_dir = "logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        # Generate log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{bot_name}_{timestamp}.log"
        log_filepath = os.path.join(logs_dir, log_filename)
        
        # Rotation based on log level
        if log_level_str.upper() == "DEBUG":
            # DEBUG mode: Rotate after 10MB
            file_handler = RotatingFileHandler(
                log_filepath,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
        else:
            # Non-DEBUG mode: Single file, no rotation
            file_handler = logging.FileHandler(
                log_filepath,
                encoding='utf-8'
            )
        
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Log initialization message
        logger.info(f"File logging initialized: {log_filepath}")
    
    # Prevent propagation to root logger (avoid duplicate messages)
    logger.propagate = False
    
    return logger
