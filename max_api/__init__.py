"""
MAX API Library
Python библиотека для работы с MAX Messenger API
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "MIT"

from .client import MAXClient
from .exceptions import (
    MAXAPIException,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
    ServiceUnavailableError,
)
from .update_manager import UpdateManager, UpdateMode

__all__ = [
    "MAXClient",
    "MAXAPIException",
    "AuthenticationError",
    "BadRequestError",
    "NotFoundError",
    "RateLimitError",
    "ServiceUnavailableError",
    "UpdateManager",
    "UpdateMode",
]
