"""
DataCoin Blockchain Package

This package contains the core blockchain implementation including:
- Block and Transaction classes
- Proof-of-work mining
- Blockchain validation
- Corporate governance mechanisms
"""

from .core import Blockchain, Block, Transaction

__all__ = ['Blockchain', 'Block', 'Transaction']
__version__ = '1.0.0'