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

__all__ = [
    "MAXClient",
    "MAXAPIException",
    "AuthenticationError",
    "BadRequestError",
    "NotFoundError",
    "RateLimitError",
    "ServiceUnavailableError",
]
