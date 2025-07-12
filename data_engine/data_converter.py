import requests
import hashlib
import time
import json
import threading
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Tuple
import sqlite3
import os
from datetime import datetime, timedelta
import schedule
import numpy as np

from blockchain.core import Blockchain, Transaction

class DataSource:
    """Represents a source of internet data"""
    
    def __init__(self, source_id: str, source_type: str, url: str, weight: float = 1.0):
        self.source_id = source_id
        self.source_type = source_type  # 'web', 'api', 'rss', 'social'
        self.url = url
        self.weight = weight  # Importance multiplier for currency conversion
        self.last_accessed = None
        self.data_collected = 0.0  # MB of data collected
        self.currency_generated = 0.0
    
    def to_dict(self) -> Dict:
        return {
            'source_id': self.source_id,
            'source_type': self.source_type,
            'url': self.url,
            'weight': self.weight,
            'last_accessed': self.last_accessed,
            'data_collected': self.data_collected,
            'currency_generated': self.currency_generated
        }

class DataCollector:
    """Collects data from various internet sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DataCoin-Collector/1.0'
        })
    
    def collect_web_data(self, url: str) -> Tuple[float, Dict]:
        """Collect data from a web page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Calculate data size in MB
            content_size = len(response.content) / (1024 * 1024)
            
            # Parse content for additional metrics
            soup = BeautifulSoup(response.content, 'html.parser')
            
            metrics = {
                'content_size_mb': content_size,
                'text_length': len(soup.get_text()),
                'links_count': len(soup.find_all('a')),
                'images_count': len(soup.find_all('img')),
                'scripts_count': len(soup.find_all('script')),
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
            
            return content_size, metrics
            
        except Exception as e:
            print(f"Error collecting data from {url}: {e}")
            return 0.0, {}
    
    def collect_api_data(self, url: str, params: Dict = None) -> Tuple[float, Dict]:
        """Collect data from an API endpoint"""
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            content_size = len(response.content) / (1024 * 1024)
            
            try:
                json_data = response.json()
                data_points = len(json_data) if isinstance(json_data, list) else 1
            except:
                data_points = 0
            
            metrics = {
                'content_size_mb': content_size,
                'data_points': data_points,
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
            
            return content_size, metrics
            
        except Exception as e:
            print(f"Error collecting API data from {url}: {e}")
            return 0.0, {}

class DataValueCalculator:
    """Calculates the currency value of collected data"""
    
    def __init__(self):
        self.base_rate = 0.001  # Base: 1 MB = 0.001 coins
        self.quality_multipliers = {
            'high': 2.0,
            'medium': 1.0,
            'low': 0.5
        }
        self.source_type_multipliers = {
            'api': 1.5,
            'web': 1.0,
            'rss': 0.8,
            'social': 1.2
        }
    
    def calculate_data_quality(self, metrics: Dict) -> str:
        """Determine data quality based on metrics"""
        score = 0
        
        # Size-based scoring
        if metrics.get('content_size_mb', 0) > 1.0:
            score += 2
        elif metrics.get('content_size_mb', 0) > 0.1:
            score += 1
        
        # Response time scoring (faster = better)
        response_time = metrics.get('response_time', 10)
        if response_time < 1.0:
            score += 2
        elif response_time < 5.0:
            score += 1
        
        # Content richness (for web data)
        if metrics.get('links_count', 0) > 10:
            score += 1
        if metrics.get('images_count', 0) > 5:
            score += 1
        
        # API data points
        if metrics.get('data_points', 0) > 100:
            score += 2
        elif metrics.get('data_points', 0) > 10:
            score += 1
        
        if score >= 6:
            return 'high'
        elif score >= 3:
            return 'medium'
        else:
            return 'low'
    
    def calculate_currency_value(self, data_size_mb: float, source: DataSource, metrics: Dict) -> float:
        """Calculate currency value for collected data"""
        base_value = data_size_mb * self.base_rate
        
        # Apply quality multiplier
        quality = self.calculate_data_quality(metrics)
        quality_multiplier = self.quality_multipliers[quality]
        
        # Apply source type multiplier
        source_multiplier = self.source_type_multipliers.get(source.source_type, 1.0)
        
        # Apply source weight
        weight_multiplier = source.weight
        
        # Time-based bonus (recent data is more valuable)
        time_bonus = 1.0
        if source.last_accessed:
            hours_since_last = (time.time() - source.last_accessed) / 3600
            if hours_since_last < 1:
                time_bonus = 1.5
            elif hours_since_last < 24:
                time_bonus = 1.2
        
        final_value = base_value * quality_multiplier * source_multiplier * weight_multiplier * time_bonus
        
        return round(final_value, 6)

class DataConverter:
    """Main data conversion engine"""
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.collector = DataCollector()
        self.calculator = DataValueCalculator()
        self.sources: Dict[str, DataSource] = {}
        self.is_running = False
        self.conversion_thread = None
        
        # Initialize database
        self.db_path = "data_engine/data_converter.db"
        self._ensure_directory()
        self._init_database()
        self._load_sources()
    
    def _ensure_directory(self):
        """Ensure data engine directory exists"""
        os.makedirs("data_engine", exist_ok=True)
    
    def _init_database(self):
        """Initialize data converter database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_sources (
                source_id TEXT PRIMARY KEY,
                source_type TEXT,
                url TEXT,
                weight REAL,
                last_accessed REAL,
                data_collected REAL,
                currency_generated REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversion_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT,
                timestamp REAL,
                data_size_mb REAL,
                currency_value REAL,
                quality TEXT,
                metrics TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_sources(self):
        """Load data sources from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM data_sources')
        for row in cursor.fetchall():
            source = DataSource(row[0], row[1], row[2], row[3])
            source.last_accessed = row[4]
            source.data_collected = row[5]
            source.currency_generated = row[6]
            self.sources[source.source_id] = source
        
        conn.close()
    
    def add_data_source(self, source_id: str, source_type: str, url: str, weight: float = 1.0) -> bool:
        """Add a new data source"""
        if source_id in self.sources:
            print(f"Source {source_id} already exists")
            return False
        
        source = DataSource(source_id, source_type, url, weight)
        self.sources[source_id] = source
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO data_sources 
            (source_id, source_type, url, weight, last_accessed, data_collected, currency_generated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (source.source_id, source.source_type, source.url, source.weight, 
              source.last_accessed, source.data_collected, source.currency_generated))
        
        conn.commit()
        conn.close()
        
        print(f"Added data source: {source_id}")
        return True
    
    def collect_and_convert(self, source_id: str, recipient_address: str) -> Optional[Transaction]:
        """Collect data from a source and convert to currency"""
        if source_id not in self.sources:
            print(f"Source {source_id} not found")
            return None
        
        source = self.sources[source_id]
        
        # Collect data
        if source.source_type == 'api':
            data_size, metrics = self.collector.collect_api_data(source.url)
        else:
            data_size, metrics = self.collector.collect_web_data(source.url)
        
        if data_size == 0:
            return None
        
        # Calculate currency value
        currency_value = self.calculator.calculate_currency_value(data_size, source, metrics)
        
        # Update source stats
        source.last_accessed = time.time()
        source.data_collected += data_size
        source.currency_generated += currency_value
        
        # Save conversion history
        quality = self.calculator.calculate_data_quality(metrics)
        self._save_conversion_history(source_id, data_size, currency_value, quality, metrics)
        
        # Update database
        self._update_source_in_db(source)
        
        # Create blockchain transaction
        transaction = self.blockchain.convert_data_to_currency(data_size, recipient_address)
        
        print(f"Converted {data_size:.6f} MB from {source_id} to {currency_value:.6f} DataCoins")
        return transaction
    
    def _save_conversion_history(self, source_id: str, data_size: float, currency_value: float, quality: str, metrics: Dict):
        """Save conversion to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversion_history 
            (source_id, timestamp, data_size_mb, currency_value, quality, metrics)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (source_id, time.time(), data_size, currency_value, quality, json.dumps(metrics)))
        
        conn.commit()
        conn.close()
    
    def _update_source_in_db(self, source: DataSource):
        """Update source in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE data_sources 
            SET last_accessed = ?, data_collected = ?, currency_generated = ?
            WHERE source_id = ?
        ''', (source.last_accessed, source.data_collected, source.currency_generated, source.source_id))
        
        conn.commit()
        conn.close()
    
    def start_auto_conversion(self, recipient_address: str, interval_minutes: int = 60):
        """Start automatic data conversion"""
        if self.is_running:
            print("Auto conversion already running")
            return
        
        self.is_running = True
        
        def conversion_worker():
            while self.is_running:
                for source_id in self.sources:
                    if self.is_running:
                        try:
                            self.collect_and_convert(source_id, recipient_address)
                            time.sleep(10)  # Brief pause between sources
                        except Exception as e:
                            print(f"Error in auto conversion for {source_id}: {e}")
                
                # Wait for next cycle
                for _ in range(interval_minutes * 60):
                    if not self.is_running:
                        break
                    time.sleep(1)
        
        self.conversion_thread = threading.Thread(target=conversion_worker, daemon=True)
        self.conversion_thread.start()
        print(f"Started auto conversion every {interval_minutes} minutes")
    
    def stop_auto_conversion(self):
        """Stop automatic data conversion"""
        self.is_running = False
        if self.conversion_thread:
            self.conversion_thread.join(timeout=5)
        print("Stopped auto conversion")
    
    def get_conversion_stats(self) -> Dict:
        """Get conversion statistics"""
        total_data = sum(source.data_collected for source in self.sources.values())
        total_currency = sum(source.currency_generated for source in self.sources.values())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM conversion_history')
        total_conversions = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT quality, COUNT(*) FROM conversion_history 
            GROUP BY quality
        ''')
        quality_stats = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_sources': len(self.sources),
            'total_data_collected_mb': round(total_data, 6),
            'total_currency_generated': round(total_currency, 6),
            'total_conversions': total_conversions,
            'quality_distribution': quality_stats,
            'conversion_rate': round(total_currency / total_data if total_data > 0 else 0, 6),
            'is_auto_running': self.is_running
        }
    
    def get_source_list(self) -> List[Dict]:
        """Get list of all data sources"""
        return [source.to_dict() for source in self.sources.values()]

# Default data sources for demonstration
DEFAULT_DATA_SOURCES = [
    {
        'source_id': 'news_api',
        'source_type': 'api',
        'url': 'https://jsonplaceholder.typicode.com/posts',
        'weight': 1.5
    },
    {
        'source_id': 'wikipedia_random',
        'source_type': 'web',
        'url': 'https://en.wikipedia.org/wiki/Special:Random',
        'weight': 1.2
    },
    {
        'source_id': 'github_api',
        'source_type': 'api',
        'url': 'https://api.github.com/repositories',
        'weight': 1.8
    },
    {
        'source_id': 'hackernews',
        'source_type': 'web',
        'url': 'https://news.ycombinator.com/',
        'weight': 1.3
    }
]