"""
DataCoin Wallet Package

This package provides wallet management functionality including:
- RSA key generation and management
- Wallet creation and loading
- Transaction creation and history
- Secure storage with SQLite
"""

from .wallet import Wallet, WalletManager

__all__ = ['Wallet', 'WalletManager']
__version__ = '1.0.0'