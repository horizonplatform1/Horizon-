"""
Advanced Analytics and Tracking Engine
Provides AI-powered insights, predictions, and comprehensive tracking
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import json
import logging
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import os
import yfinance as yf

from blockchain.core import Blockchain


class MarketAnalyzer:
    """Advanced market analysis and prediction system"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.companies = ['GOOGL', 'MSFT', 'CMCSA']
        self.analysis_cache = {}
        self.last_analysis_time = {}
        
    def collect_comprehensive_data(self, symbol: str, period: str = "2y") -> pd.DataFrame:
        """Collect comprehensive market data with technical indicators"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                return pd.DataFrame()
            
            # Basic technical indicators
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['SMA_200'] = data['Close'].rolling(window=200).mean()
            
            # Exponential moving averages
            data['EMA_12'] = data['Close'].ewm(span=12).mean()
            data['EMA_26'] = data['Close'].ewm(span=26).mean()
            
            # MACD
            data['MACD'] = data['EMA_12'] - data['EMA_26']
            data['MACD_Signal'] = data['MACD'].ewm(span=9).mean()
            data['MACD_Histogram'] = data['MACD'] - data['MACD_Signal']
            
            # RSI
            data['RSI'] = self._calculate_rsi(data['Close'])
            
            # Bollinger Bands
            data['BB_Middle'] = data['Close'].rolling(window=20).mean()
            bb_std = data['Close'].rolling(window=20).std()
            data['BB_Upper'] = data['BB_Middle'] + (bb_std * 2)
            data['BB_Lower'] = data['BB_Middle'] - (bb_std * 2)
            data['BB_Width'] = data['BB_Upper'] - data['BB_Lower']
            
            # Volatility indicators
            data['Volatility'] = data['Close'].rolling(window=20).std()
            data['ATR'] = self._calculate_atr(data)
            
            # Volume indicators
            data['Volume_SMA'] = data['Volume'].rolling(window=20).mean()
            data['Volume_Ratio'] = data['Volume'] / data['Volume_SMA']
            
            # Price momentum
            data['Price_Change'] = data['Close'].pct_change()
            data['Price_Momentum'] = data['Close'].pct_change(periods=10)
            
            # Support and resistance levels
            data['Support'] = data['Low'].rolling(window=20).min()
            data['Resistance'] = data['High'].rolling(window=20).max()
            
            return data
            
        except Exception as e:
            logging.error(f"Error collecting data for {symbol}: {e}")
            return pd.DataFrame()
    
    def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_atr(self, data: pd.DataFrame, window: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        return true_range.rolling(window).mean()
    
    def perform_comprehensive_analysis(self, symbol: str) -> Dict[str, Any]:
        """Perform comprehensive market analysis"""
        try:
            # Check cache
            if (symbol in self.analysis_cache and 
                symbol in self.last_analysis_time and
                (datetime.now() - self.last_analysis_time[symbol]).seconds < 3600):  # 1 hour cache
                return self.analysis_cache[symbol]
            
            data = self.collect_comprehensive_data(symbol)
            if data.empty:
                return {'error': 'No data available'}
            
            current_price = data['Close'].iloc[-1]
            
            # Technical analysis
            technical_analysis = self._analyze_technical_indicators(data)
            
            # Trend analysis
            trend_analysis = self._analyze_trends(data)
            
            # Volatility analysis
            volatility_analysis = self._analyze_volatility(data)
            
            # Volume analysis
            volume_analysis = self._analyze_volume(data)
            
            # Support/Resistance analysis
            support_resistance = self._analyze_support_resistance(data)
            
            # Price prediction
            price_prediction = self._predict_price_movement(data, symbol)
            
            # Risk assessment
            risk_assessment = self._assess_risk(data)
            
            # Generate trading signals
            trading_signals = self._generate_trading_signals(data)
            
            analysis = {
                'symbol': symbol,
                'current_price': current_price,
                'last_updated': datetime.now().isoformat(),
                'technical_analysis': technical_analysis,
                'trend_analysis': trend_analysis,
                'volatility_analysis': volatility_analysis,
                'volume_analysis': volume_analysis,
                'support_resistance': support_resistance,
                'price_prediction': price_prediction,
                'risk_assessment': risk_assessment,
                'trading_signals': trading_signals
            }
            
            # Cache results
            self.analysis_cache[symbol] = analysis
            self.last_analysis_time[symbol] = datetime.now()
            
            return analysis
            
        except Exception as e:
            logging.error(f"Error in comprehensive analysis for {symbol}: {e}")
            return {'error': str(e)}
    
    def _analyze_technical_indicators(self, data: pd.DataFrame) -> Dict:
        """Analyze technical indicators"""
        latest = data.iloc[-1]
        
        # RSI analysis
        rsi_signal = "neutral"
        if latest['RSI'] < 30:
            rsi_signal = "oversold"
        elif latest['RSI'] > 70:
            rsi_signal = "overbought"
        
        # MACD analysis
        macd_signal = "neutral"
        if latest['MACD'] > latest['MACD_Signal']:
            macd_signal = "bullish"
        elif latest['MACD'] < latest['MACD_Signal']:
            macd_signal = "bearish"
        
        # Bollinger Bands analysis
        bb_signal = "neutral"
        if latest['Close'] < latest['BB_Lower']:
            bb_signal = "oversold"
        elif latest['Close'] > latest['BB_Upper']:
            bb_signal = "overbought"
        
        return {
            'rsi': {
                'value': latest['RSI'],
                'signal': rsi_signal
            },
            'macd': {
                'value': latest['MACD'],
                'signal_line': latest['MACD_Signal'],
                'histogram': latest['MACD_Histogram'],
                'signal': macd_signal
            },
            'bollinger_bands': {
                'upper': latest['BB_Upper'],
                'middle': latest['BB_Middle'],
                'lower': latest['BB_Lower'],
                'width': latest['BB_Width'],
                'signal': bb_signal
            }
        }
    
    def _analyze_trends(self, data: pd.DataFrame) -> Dict:
        """Analyze price trends"""
        latest = data.iloc[-1]
        
        # Moving average trends
        sma_trend = "neutral"
        if latest['Close'] > latest['SMA_20'] > latest['SMA_50']:
            sma_trend = "bullish"
        elif latest['Close'] < latest['SMA_20'] < latest['SMA_50']:
            sma_trend = "bearish"
        
        # Price momentum
        momentum_signal = "neutral"
        if latest['Price_Momentum'] > 0.02:  # 2% positive momentum
            momentum_signal = "strong_bullish"
        elif latest['Price_Momentum'] > 0:
            momentum_signal = "bullish"
        elif latest['Price_Momentum'] < -0.02:
            momentum_signal = "strong_bearish"
        else:
            momentum_signal = "bearish"
        
        return {
            'sma_trend': sma_trend,
            'momentum': {
                'value': latest['Price_Momentum'],
                'signal': momentum_signal
            },
            'price_vs_sma20': (latest['Close'] - latest['SMA_20']) / latest['SMA_20'],
            'price_vs_sma50': (latest['Close'] - latest['SMA_50']) / latest['SMA_50']
        }
    
    def _analyze_volatility(self, data: pd.DataFrame) -> Dict:
        """Analyze volatility patterns"""
        latest = data.iloc[-1]
        
        volatility_30d = data['Close'].pct_change().rolling(30).std() * np.sqrt(252)
        current_volatility = volatility_30d.iloc[-1]
        
        volatility_signal = "normal"
        if current_volatility > 0.3:
            volatility_signal = "high"
        elif current_volatility < 0.15:
            volatility_signal = "low"
        
        return {
            'current_volatility': current_volatility,
            'volatility_signal': volatility_signal,
            'atr': latest['ATR'],
            'bb_width': latest['BB_Width']
        }
    
    def _analyze_volume(self, data: pd.DataFrame) -> Dict:
        """Analyze volume patterns"""
        latest = data.iloc[-1]
        
        volume_signal = "normal"
        if latest['Volume_Ratio'] > 2:
            volume_signal = "high"
        elif latest['Volume_Ratio'] < 0.5:
            volume_signal = "low"
        
        return {
            'current_volume': latest['Volume'],
            'volume_sma': latest['Volume_SMA'],
            'volume_ratio': latest['Volume_Ratio'],
            'volume_signal': volume_signal
        }
    
    def _analyze_support_resistance(self, data: pd.DataFrame) -> Dict:
        """Analyze support and resistance levels"""
        latest = data.iloc[-1]
        
        return {
            'support': latest['Support'],
            'resistance': latest['Resistance'],
            'distance_to_support': (latest['Close'] - latest['Support']) / latest['Close'],
            'distance_to_resistance': (latest['Resistance'] - latest['Close']) / latest['Close']
        }
    
    def _predict_price_movement(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Predict price movement using ML models"""
        try:
            # Prepare features for prediction
            features = ['RSI', 'MACD', 'BB_Width', 'Volume_Ratio', 'Price_Momentum', 'ATR']
            
            # Clean data
            ml_data = data[features + ['Close']].dropna()
            
            if len(ml_data) < 50:  # Not enough data
                return {'error': 'Insufficient data for prediction'}
            
            # Create target variable (next day's price change)
            ml_data['Target'] = ml_data['Close'].shift(-1).pct_change()
            ml_data = ml_data.dropna()
            
            X = ml_data[features]
            y = ml_data['Target']
            
            # Train model
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            if symbol not in self.scalers:
                self.scalers[symbol] = StandardScaler()
                X_train_scaled = self.scalers[symbol].fit_transform(X_train)
            else:
                X_train_scaled = self.scalers[symbol].transform(X_train)
            
            X_test_scaled = self.scalers[symbol].transform(X_test)
            
            # Train model
            model = GradientBoostingRegressor(n_estimators=100, random_state=42)
            model.fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test_scaled)
            
            # Evaluate model
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Predict next price movement
            latest_features = X.iloc[-1:].values
            latest_scaled = self.scalers[symbol].transform(latest_features)
            predicted_change = model.predict(latest_scaled)[0]
            
            current_price = data['Close'].iloc[-1]
            predicted_price = current_price * (1 + predicted_change)
            
            confidence = max(0, min(100, r2 * 100))  # Convert R² to confidence percentage
            
            return {
                'predicted_price_change': predicted_change,
                'predicted_price': predicted_price,
                'current_price': current_price,
                'confidence': confidence,
                'model_performance': {
                    'mse': mse,
                    'r2_score': r2
                }
            }
            
        except Exception as e:
            logging.error(f"Error in price prediction for {symbol}: {e}")
            return {'error': str(e)}
    
    def _assess_risk(self, data: pd.DataFrame) -> Dict:
        """Assess investment risk"""
        returns = data['Close'].pct_change().dropna()
        
        # Calculate risk metrics
        volatility = returns.std() * np.sqrt(252)  # Annualized volatility
        var_95 = returns.quantile(0.05)  # Value at Risk (95%)
        
        # Sharpe ratio (assuming risk-free rate of 2%)
        excess_returns = returns.mean() * 252 - 0.02
        sharpe_ratio = excess_returns / volatility if volatility > 0 else 0
        
        # Maximum drawdown
        cumulative_returns = (1 + returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        risk_level = "medium"
        if volatility > 0.3:
            risk_level = "high"
        elif volatility < 0.15:
            risk_level = "low"
        
        return {
            'volatility': volatility,
            'var_95': var_95,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'risk_level': risk_level
        }
    
    def _generate_trading_signals(self, data: pd.DataFrame) -> Dict:
        """Generate comprehensive trading signals"""
        latest = data.iloc[-1]
        
        signals = []
        strength = 0
        
        # RSI signals
        if latest['RSI'] < 30:
            signals.append("RSI oversold - potential buy")
            strength += 1
        elif latest['RSI'] > 70:
            signals.append("RSI overbought - potential sell")
            strength -= 1
        
        # MACD signals
        if latest['MACD'] > latest['MACD_Signal']:
            signals.append("MACD bullish crossover")
            strength += 1
        elif latest['MACD'] < latest['MACD_Signal']:
            signals.append("MACD bearish crossover")
            strength -= 1
        
        # Moving average signals
        if latest['Close'] > latest['SMA_20'] > latest['SMA_50']:
            signals.append("Bullish moving average alignment")
            strength += 1
        elif latest['Close'] < latest['SMA_20'] < latest['SMA_50']:
            signals.append("Bearish moving average alignment")
            strength -= 1
        
        # Volume confirmation
        if latest['Volume_Ratio'] > 1.5:
            signals.append("High volume confirms signal")
            strength += 0.5
        
        # Bollinger Bands
        if latest['Close'] < latest['BB_Lower']:
            signals.append("Price below lower Bollinger Band - oversold")
            strength += 1
        elif latest['Close'] > latest['BB_Upper']:
            signals.append("Price above upper Bollinger Band - overbought")
            strength -= 1
        
        # Overall signal
        if strength > 1:
            overall_signal = "strong_buy"
        elif strength > 0:
            overall_signal = "buy"
        elif strength < -1:
            overall_signal = "strong_sell"
        elif strength < 0:
            overall_signal = "sell"
        else:
            overall_signal = "hold"
        
        return {
            'overall_signal': overall_signal,
            'strength': strength,
            'individual_signals': signals
        }


class BlockchainAnalyzer:
    """Analyze blockchain performance and patterns"""
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.db_path = "data/blockchain_analytics.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize analytics database"""
        os.makedirs("data", exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_type TEXT NOT NULL,
                data TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def analyze_blockchain_performance(self) -> Dict:
        """Analyze overall blockchain performance"""
        try:
            stats = self.blockchain.get_blockchain_stats()
            
            # Transaction analysis
            total_transactions = 0
            transaction_types = {}
            daily_volumes = {}
            
            for block in self.blockchain.chain:
                for tx in block.transactions:
                    total_transactions += 1
                    
                    # Count transaction types
                    tx_type = getattr(tx, 'tx_type', 'transfer')
                    transaction_types[tx_type] = transaction_types.get(tx_type, 0) + 1
                    
                    # Daily volume analysis
                    date = datetime.fromtimestamp(tx.timestamp).date()
                    daily_volumes[date] = daily_volumes.get(date, 0) + tx.amount
            
            # Mining analysis
            mining_stats = self._analyze_mining_patterns()
            
            # Network health
            network_health = self._assess_network_health()
            
            return {
                'blockchain_stats': stats,
                'transaction_analysis': {
                    'total_transactions': total_transactions,
                    'transaction_types': transaction_types,
                    'daily_volumes': daily_volumes
                },
                'mining_stats': mining_stats,
                'network_health': network_health,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error in blockchain analysis: {e}")
            return {'error': str(e)}
    
    def _analyze_mining_patterns(self) -> Dict:
        """Analyze mining patterns and efficiency"""
        block_times = []
        difficulties = []
        
        for i in range(1, len(self.blockchain.chain)):
            current_block = self.blockchain.chain[i]
            previous_block = self.blockchain.chain[i-1]
            
            block_time = current_block.timestamp - previous_block.timestamp
            block_times.append(block_time)
            
            # Get difficulty from blockchain if available
            difficulty = getattr(current_block, 'difficulty', 4)
            difficulties.append(difficulty)
        
        avg_block_time = np.mean(block_times) if block_times else 0
        avg_difficulty = np.mean(difficulties) if difficulties else 4
        
        return {
            'average_block_time': avg_block_time,
            'average_difficulty': avg_difficulty,
            'total_blocks': len(self.blockchain.chain),
            'block_times': block_times[-10:]  # Last 10 block times
        }
    
    def _assess_network_health(self) -> Dict:
        """Assess overall network health"""
        health_score = 100
        issues = []
        
        # Check chain validity
        if not self.blockchain.is_chain_valid():
            health_score -= 50
            issues.append("Blockchain integrity compromised")
        
        # Check for recent activity
        if len(self.blockchain.chain) > 1:
            last_block = self.blockchain.chain[-1]
            time_since_last_block = time.time() - last_block.timestamp
            
            if time_since_last_block > 3600:  # 1 hour
                health_score -= 20
                issues.append("Low mining activity")
        
        # Check pending transactions
        if len(self.blockchain.pending_transactions) > 100:
            health_score -= 15
            issues.append("High pending transaction backlog")
        
        health_status = "excellent"
        if health_score < 70:
            health_status = "poor"
        elif health_score < 85:
            health_status = "fair"
        elif health_score < 95:
            health_status = "good"
        
        return {
            'health_score': health_score,
            'health_status': health_status,
            'issues': issues,
            'pending_transactions': len(self.blockchain.pending_transactions)
        }
    
    def generate_analytics_report(self) -> Dict:
        """Generate comprehensive analytics report"""
        try:
            # Blockchain analysis
            blockchain_analysis = self.analyze_blockchain_performance()
            
            # Market analysis for each company
            market_analyzer = MarketAnalyzer()
            market_analysis = {}
            
            for symbol in ['GOOGL', 'MSFT', 'CMCSA']:
                market_analysis[symbol] = market_analyzer.perform_comprehensive_analysis(symbol)
            
            # Portfolio analysis (if trading data exists)
            portfolio_analysis = self._analyze_portfolio_performance()
            
            # Generate insights and recommendations
            insights = self._generate_insights(blockchain_analysis, market_analysis, portfolio_analysis)
            
            report = {
                'report_timestamp': datetime.now().isoformat(),
                'blockchain_analysis': blockchain_analysis,
                'market_analysis': market_analysis,
                'portfolio_analysis': portfolio_analysis,
                'insights_and_recommendations': insights
            }
            
            # Cache the report
            self._cache_analysis('comprehensive_report', report)
            
            return report
            
        except Exception as e:
            logging.error(f"Error generating analytics report: {e}")
            return {'error': str(e)}
    
    def _analyze_portfolio_performance(self) -> Dict:
        """Analyze portfolio performance"""
        try:
            # This would integrate with the AI trader's portfolio data
            portfolio_data = {
                'total_value': 0,
                'profit_loss': 0,
                'win_rate': 0,
                'holdings': {}
            }
            
            # In a real implementation, this would pull from the AI trader's database
            return portfolio_data
            
        except Exception as e:
            logging.error(f"Error in portfolio analysis: {e}")
            return {'error': str(e)}
    
    def _generate_insights(self, blockchain_analysis: Dict, market_analysis: Dict, portfolio_analysis: Dict) -> Dict:
        """Generate actionable insights and recommendations"""
        insights = {
            'blockchain_insights': [],
            'market_insights': [],
            'portfolio_insights': [],
            'recommendations': []
        }
        
        # Blockchain insights
        if blockchain_analysis.get('network_health', {}).get('health_score', 0) < 85:
            insights['blockchain_insights'].append("Network health requires attention")
        
        # Market insights
        for symbol, analysis in market_analysis.items():
            if not analysis.get('error'):
                signal = analysis.get('trading_signals', {}).get('overall_signal', 'hold')
                if signal in ['strong_buy', 'strong_sell']:
                    insights['market_insights'].append(f"{symbol}: {signal.replace('_', ' ').title()} signal detected")
        
        # Recommendations
        insights['recommendations'].extend([
            "Monitor blockchain network health regularly",
            "Consider diversifying holdings across multiple companies",
            "Implement automated stop-loss mechanisms",
            "Review and adjust AI trading parameters based on market conditions"
        ])
        
        return insights
    
    def _cache_analysis(self, analysis_type: str, data: Dict):
        """Cache analysis results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analytics_cache (analysis_type, data)
            VALUES (?, ?)
        ''', (analysis_type, json.dumps(data)))
        
        conn.commit()
        conn.close()


class RealTimeTracker:
    """Real-time tracking and monitoring system"""
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.is_running = False
        self.tracking_thread = None
        self.callbacks = {}
    
    def start_tracking(self):
        """Start real-time tracking"""
        if self.is_running:
            return
        
        self.is_running = True
        self.tracking_thread = threading.Thread(target=self._tracking_loop, daemon=True)
        self.tracking_thread.start()
        
        logging.info("Real-time tracking started")
    
    def stop_tracking(self):
        """Stop real-time tracking"""
        self.is_running = False
        if self.tracking_thread:
            self.tracking_thread.join(timeout=10)
        
        logging.info("Real-time tracking stopped")
    
    def _tracking_loop(self):
        """Main tracking loop"""
        while self.is_running:
            try:
                # Track blockchain changes
                self._track_blockchain_changes()
                
                # Track market changes
                self._track_market_changes()
                
                # Track portfolio changes
                self._track_portfolio_changes()
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                logging.error(f"Error in tracking loop: {e}")
                time.sleep(30)  # Wait 30 seconds on error
    
    def _track_blockchain_changes(self):
        """Track blockchain changes and trigger callbacks"""
        # This would monitor for new blocks, transactions, etc.
        pass
    
    def _track_market_changes(self):
        """Track market changes and trigger alerts"""
        # This would monitor market conditions and trigger alerts
        pass
    
    def _track_portfolio_changes(self):
        """Track portfolio changes and performance"""
        # This would monitor portfolio performance and trigger alerts
        pass
    
    def register_callback(self, event_type: str, callback):
        """Register callback for specific events"""
        if event_type not in self.callbacks:
            self.callbacks[event_type] = []
        self.callbacks[event_type].append(callback)
    
    def trigger_callback(self, event_type: str, data: Any):
        """Trigger callbacks for specific events"""
        if event_type in self.callbacks:
            for callback in self.callbacks[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    logging.error(f"Error in callback for {event_type}: {e}")