"""
DataCoin Data Engine Package

This package handles internet data collection and conversion including:
- Web scraping and API data collection
- Data quality assessment and valuation
- Automated data harvesting
- Currency conversion mechanisms
"""

from .data_converter import DataConverter, DataSource, DataCollector, DataValueCalculator, DEFAULT_DATA_SOURCES

__all__ = ['DataConverter', 'DataSource', 'DataCollector', 'DataValueCalculator', 'DEFAULT_DATA_SOURCES']
__version__ = '1.0.0'