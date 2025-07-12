"""
DataCoin API Package

This package provides the RESTful API interface including:
- FastAPI server implementation
- HTTP endpoints for all operations
- Request/response models
- CORS and middleware configuration
"""

from .main import app

__all__ = ['app']
__version__ = '1.0.0'