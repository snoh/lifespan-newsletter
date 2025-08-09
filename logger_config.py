"""
Structured logging configuration using structlog
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict

import structlog
from structlog.stdlib import LoggerFactory


def configure_logging(
    log_file: Path = Path("summary.log"),
    log_level: str = "INFO",
    enable_json: bool = True
) -> None:
    """
    Configure structured logging with both console and file output
    
    Args:
        log_file: Path to log file
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        enable_json: Whether to use JSON format for file logging
    """
    # Shared processors for all loggers
    shared_processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    
    # Configure structlog
    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Console handler with colored output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=structlog.dev.ConsoleRenderer(colors=True)
        )
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    if enable_json:
        file_handler.setFormatter(
            structlog.stdlib.ProcessorFormatter(
                processor=structlog.processors.JSONRenderer()
            )
        )
    else:
        file_handler.setFormatter(
            structlog.stdlib.ProcessorFormatter(
                processor=structlog.dev.ConsoleRenderer(colors=False)
            )
        )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Suppress noisy third-party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)


def get_logger(name: str, **context: Any) -> structlog.BoundLogger:
    """
    Get a structured logger with optional context
    
    Args:
        name: Logger name (usually __name__)
        **context: Additional context to bind to logger
    
    Returns:
        Configured structlog BoundLogger
    """
    logger = structlog.get_logger(name)
    if context:
        logger = logger.bind(**context)
    return logger


def log_function_call(func_name: str, **kwargs: Any) -> Dict[str, Any]:
    """
    Create a log context for function calls
    
    Args:
        func_name: Function name
        **kwargs: Function arguments to log
    
    Returns:
        Log context dictionary
    """
    return {
        "function": func_name,
        "args": {k: v for k, v in kwargs.items() if not k.startswith('_')}
    }


def log_article_context(article_id: str, title: str = "", source: str = "") -> Dict[str, Any]:
    """
    Create a log context for article processing
    
    Args:
        article_id: Unique article identifier
        title: Article title (truncated for logging)
        source: Article source
    
    Returns:
        Log context dictionary
    """
    return {
        "article_id": article_id,
        "title": title[:50] + "..." if len(title) > 50 else title,
        "source": source,
    }


def log_processing_step(step: str, **context: Any) -> Dict[str, Any]:
    """
    Create a log context for processing steps
    
    Args:
        step: Processing step name (e.g., 'rss_fetch', 'summarize', 'export')
        **context: Additional step-specific context
    
    Returns:
        Log context dictionary
    """
    return {
        "processing_step": step,
        **context
    }
