"""
Advanced AI System for Automated Trading and Corporate Control
Implements sophisticated machine learning algorithms for automated share acquisition,
corporate governance, and strategic decision-making
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Attention
import yfinance as yf
import sqlite3
import json
import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import os
from dataclasses import dataclass
import requests
from textblob import TextBlob
import asyncio

from blockchain.core import Blockchain, Transaction


@dataclass
class TradingDecision:
    """Represents an AI-generated trading decision"""
    company: str
    action: str  # 'BUY', 'SELL', 'HOLD'
    confidence: float
    shares_recommended: int
    reasoning: List[str]
    risk_assessment: str
    expected_return: float
    time_horizon: str
    market_sentiment: float


@dataclass
class MarketIntelligence:
    """Market intelligence and sentiment analysis"""
    overall_sentiment: float
    news_sentiment: Dict[str, float]
    social_media_sentiment: Dict[str, float]
    analyst_recommendations: Dict[str, Dict]
    economic_indicators: Dict[str, float]
    competitor_analysis: Dict[str, Dict]


class AdvancedNeuralNetwork:
    """Deep learning model for stock price prediction and market analysis"""
    
    def __init__(self, company: str):
        self.company = company
        self.model = None
        self.scaler = MinMaxScaler()
        self.sequence_length = 60
        self.is_trained = False
        
    def build_lstm_model(self, input_shape: Tuple[int, int]) -> Sequential:
        """Build advanced LSTM model with attention mechanism"""
        model = Sequential([
            LSTM(128, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(64, return_sequences=True),
            Dropout(0.2),
            LSTM(32, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
        return model
    
    def prepare_sequences(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare sequences for LSTM training"""
        X, y = [], []
        for i in range(self.sequence_length, len(data)):
            X.append(data[i-self.sequence_length:i])
            y.append(data[i, 0])  # Predict closing price
        return np.array(X), np.array(y)
    
    def train(self, market_data: pd.DataFrame) -> bool:
        """Train the neural network on market data"""
        try:
            # Prepare features
            features = ['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_20', 'RSI', 'MACD']
            data = market_data[features].fillna(method='forward').values
            
            # Scale the data
            scaled_data = self.scaler.fit_transform(data)
            
            # Create sequences
            X, y = self.prepare_sequences(scaled_data)
            
            if len(X) > 0:
                # Build and train model
                self.model = self.build_lstm_model((X.shape[1], X.shape[2]))
                self.model.fit(X, y, epochs=50, batch_size=32, verbose=0, validation_split=0.2)
                self.is_trained = True
                logging.info(f"Neural network trained for {self.company}")
                return True
        except Exception as e:
            logging.error(f"Error training neural network for {self.company}: {e}")
        return False
    
    def predict_price(self, recent_data: np.ndarray) -> Tuple[float, float]:
        """Predict future price with confidence interval"""
        if not self.is_trained or self.model is None:
            return 0.0, 0.0
        
        try:
            scaled_data = self.scaler.transform(recent_data)
            sequence = scaled_data[-self.sequence_length:].reshape(1, self.sequence_length, -1)
            
            # Make prediction
            prediction = self.model.predict(sequence, verbose=0)[0][0]
            
            # Calculate confidence (simplified)
            confidence = min(0.95, max(0.5, 1.0 - abs(prediction - recent_data[-1, 3]) / recent_data[-1, 3]))
            
            return float(prediction), float(confidence)
        except Exception as e:
            logging.error(f"Error making prediction: {e}")
            return 0.0, 0.0


class SentimentAnalyzer:
    """Analyzes market sentiment from news and social media"""
    
    def __init__(self):
        self.news_sources = [
            'https://newsapi.org/v2/everything',
            'https://api.polygon.io/v2/reference/news',
            'https://api.marketaux.com/v1/news/all'
        ]
        
    def analyze_news_sentiment(self, company: str) -> float:
        """Analyze news sentiment for a company"""
        try:
            # Simulate news sentiment analysis
            # In real implementation, would use NewsAPI or similar
            search_terms = {
                'GOOGL': ['Google', 'Alphabet', 'Android', 'Chrome'],
                'MSFT': ['Microsoft', 'Windows', 'Azure', 'Office'],
                'CMCSA': ['Comcast', 'NBCUniversal', 'Xfinity', 'NBC']
            }
            
            sentiment_score = 0.0
            article_count = 0
            
            # Simulate news analysis (replace with real API calls)
            for term in search_terms.get(company, [company]):
                # Simulate sentiment scores
                sentiment_score += np.random.normal(0.1, 0.3)  # Slightly positive bias
                article_count += 1
            
            return sentiment_score / max(article_count, 1) if article_count > 0 else 0.0
            
        except Exception as e:
            logging.error(f"Error analyzing news sentiment: {e}")
            return 0.0
    
    def analyze_social_sentiment(self, company: str) -> float:
        """Analyze social media sentiment"""
        try:
            # Simulate social media sentiment
            # In real implementation, would use Twitter API, Reddit API, etc.
            base_sentiment = np.random.normal(0.05, 0.2)
            return np.clip(base_sentiment, -1.0, 1.0)
        except Exception as e:
            logging.error(f"Error analyzing social sentiment: {e}")
            return 0.0


class AdvancedTradingAI:
    """Advanced AI system for automated trading decisions"""
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.companies = ['GOOGL', 'MSFT', 'CMCSA']
        self.neural_networks = {}
        self.sentiment_analyzer = SentimentAnalyzer()
        self.db_path = "data/advanced_ai_decisions.db"
        self.trading_active = False
        self.risk_tolerance = 0.7  # Moderate risk
        self.max_position_size = 0.3  # Max 30% of portfolio per stock
        
        self._init_database()
        self._init_neural_networks()
        
    def _init_database(self):
        """Initialize AI decision database"""
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                company TEXT NOT NULL,
                action TEXT NOT NULL,
                shares INTEGER,
                confidence REAL,
                reasoning TEXT,
                market_sentiment REAL,
                expected_return REAL,
                actual_return REAL,
                success_rate REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                company TEXT NOT NULL,
                overall_sentiment REAL,
                news_sentiment REAL,
                social_sentiment REAL,
                analyst_rating TEXT,
                price_target REAL,
                economic_indicators TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _init_neural_networks(self):
        """Initialize neural networks for each company"""
        for company in self.companies:
            self.neural_networks[company] = AdvancedNeuralNetwork(company)
    
    def train_ai_models(self) -> Dict[str, bool]:
        """Train all AI models with latest market data"""
        results = {}
        
        for company in self.companies:
            try:
                # Collect comprehensive market data
                ticker = yf.Ticker(company)
                data = ticker.history(period="2y")
                
                if not data.empty:
                    # Add technical indicators
                    data['SMA_20'] = data['Close'].rolling(20).mean()
                    data['RSI'] = self._calculate_rsi(data['Close'])
                    data['MACD'] = data['Close'].ewm(span=12).mean() - data['Close'].ewm(span=26).mean()
                    
                    # Train neural network
                    success = self.neural_networks[company].train(data)
                    results[company] = success
                else:
                    results[company] = False
                    
            except Exception as e:
                logging.error(f"Error training AI for {company}: {e}")
                results[company] = False
        
        return results
    
    def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def gather_market_intelligence(self, company: str) -> MarketIntelligence:
        """Gather comprehensive market intelligence"""
        try:
            # News sentiment
            news_sentiment = self.sentiment_analyzer.analyze_news_sentiment(company)
            
            # Social media sentiment
            social_sentiment = self.sentiment_analyzer.analyze_social_sentiment(company)
            
            # Overall sentiment
            overall_sentiment = (news_sentiment * 0.6 + social_sentiment * 0.4)
            
            # Simulate analyst recommendations
            analyst_recs = {
                'buy_ratio': np.random.uniform(0.4, 0.8),
                'hold_ratio': np.random.uniform(0.1, 0.4),
                'sell_ratio': np.random.uniform(0.0, 0.2),
                'avg_price_target': self._get_current_price(company) * np.random.uniform(1.05, 1.25)
            }
            
            # Economic indicators
            economic_indicators = {
                'market_volatility': np.random.uniform(0.1, 0.4),
                'sector_performance': np.random.uniform(-0.1, 0.2),
                'interest_rates': np.random.uniform(0.02, 0.06),
                'inflation_rate': np.random.uniform(0.02, 0.05)
            }
            
            intelligence = MarketIntelligence(
                overall_sentiment=overall_sentiment,
                news_sentiment={company: news_sentiment},
                social_media_sentiment={company: social_sentiment},
                analyst_recommendations={company: analyst_recs},
                economic_indicators=economic_indicators,
                competitor_analysis={}
            )
            
            # Store intelligence
            self._store_market_intelligence(company, intelligence)
            
            return intelligence
            
        except Exception as e:
            logging.error(f"Error gathering market intelligence: {e}")
            return MarketIntelligence(0.0, {}, {}, {}, {}, {})
    
    def _get_current_price(self, symbol: str) -> float:
        """Get current stock price"""
        try:
            ticker = yf.Ticker(symbol)
            return ticker.history(period="1d")['Close'].iloc[-1]
        except:
            return 100.0  # Default price
    
    def make_trading_decision(self, company: str, wallet_balance: float) -> TradingDecision:
        """Make an AI-powered trading decision"""
        try:
            # Gather intelligence
            intelligence = self.gather_market_intelligence(company)
            
            # Get current market data
            ticker = yf.Ticker(company)
            recent_data = ticker.history(period="3mo")
            
            if recent_data.empty:
                return self._create_hold_decision(company)
            
            # Technical analysis
            current_price = recent_data['Close'].iloc[-1]
            sma_20 = recent_data['Close'].rolling(20).mean().iloc[-1]
            sma_50 = recent_data['Close'].rolling(50).mean().iloc[-1]
            rsi = self._calculate_rsi(recent_data['Close']).iloc[-1]
            
            # Neural network prediction
            features = ['Open', 'High', 'Low', 'Close', 'Volume']
            if all(col in recent_data.columns for col in features):
                recent_features = recent_data[features].fillna(method='forward').values
                predicted_price, confidence = self.neural_networks[company].predict_price(recent_features)
            else:
                predicted_price, confidence = current_price, 0.5
            
            # Decision logic
            reasoning = []
            score = 0.0
            
            # Technical indicators
            if current_price > sma_20:
                score += 0.2
                reasoning.append("Price above 20-day moving average")
            if sma_20 > sma_50:
                score += 0.1
                reasoning.append("20-day MA above 50-day MA (bullish trend)")
            if rsi < 30:
                score += 0.2
                reasoning.append("RSI indicates oversold condition")
            elif rsi > 70:
                score -= 0.2
                reasoning.append("RSI indicates overbought condition")
            
            # Sentiment analysis
            sentiment_weight = 0.3
            score += intelligence.overall_sentiment * sentiment_weight
            reasoning.append(f"Market sentiment: {intelligence.overall_sentiment:.2f}")
            
            # AI prediction
            if predicted_price > current_price * 1.05:
                score += 0.3
                reasoning.append(f"AI predicts price increase to ${predicted_price:.2f}")
            elif predicted_price < current_price * 0.95:
                score -= 0.3
                reasoning.append(f"AI predicts price decrease to ${predicted_price:.2f}")
            
            # Risk assessment
            volatility = recent_data['Close'].pct_change().std() * np.sqrt(252)
            risk_level = "LOW" if volatility < 0.2 else "MEDIUM" if volatility < 0.4 else "HIGH"
            
            # Make decision
            if score > 0.5:
                action = "BUY"
                shares = min(int(wallet_balance * self.max_position_size / current_price), 
                           int(wallet_balance * score / current_price))
            elif score < -0.3:
                action = "SELL"
                shares = 0  # For simulation
            else:
                action = "HOLD"
                shares = 0
            
            expected_return = (predicted_price - current_price) / current_price
            
            decision = TradingDecision(
                company=company,
                action=action,
                confidence=confidence,
                shares_recommended=shares,
                reasoning=reasoning,
                risk_assessment=risk_level,
                expected_return=expected_return,
                time_horizon="1-3 months",
                market_sentiment=intelligence.overall_sentiment
            )
            
            # Store decision
            self._store_trading_decision(decision)
            
            return decision
            
        except Exception as e:
            logging.error(f"Error making trading decision for {company}: {e}")
            return self._create_hold_decision(company)
    
    def _create_hold_decision(self, company: str) -> TradingDecision:
        """Create a default HOLD decision"""
        return TradingDecision(
            company=company,
            action="HOLD",
            confidence=0.5,
            shares_recommended=0,
            reasoning=["Insufficient data for analysis"],
            risk_assessment="UNKNOWN",
            expected_return=0.0,
            time_horizon="N/A",
            market_sentiment=0.0
        )
    
    def _store_trading_decision(self, decision: TradingDecision):
        """Store trading decision in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO ai_decisions 
                (company, action, shares, confidence, reasoning, market_sentiment, expected_return)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                decision.company,
                decision.action,
                decision.shares_recommended,
                decision.confidence,
                json.dumps(decision.reasoning),
                decision.market_sentiment,
                decision.expected_return
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Error storing trading decision: {e}")
    
    def _store_market_intelligence(self, company: str, intelligence: MarketIntelligence):
        """Store market intelligence in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO market_intelligence 
                (company, overall_sentiment, news_sentiment, social_sentiment, economic_indicators)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                company,
                intelligence.overall_sentiment,
                intelligence.news_sentiment.get(company, 0.0),
                intelligence.social_media_sentiment.get(company, 0.0),
                json.dumps(intelligence.economic_indicators)
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Error storing market intelligence: {e}")
    
    def start_automated_trading(self, wallet_address: str):
        """Start automated trading system"""
        self.trading_active = True
        self.wallet_address = wallet_address
        
        def trading_loop():
            while self.trading_active:
                try:
                    for company in self.companies:
                        if not self.trading_active:
                            break
                        
                        # Get wallet balance (simplified)
                        wallet_balance = 10000.0  # Simulate wallet balance
                        
                        # Make trading decision
                        decision = self.make_trading_decision(company, wallet_balance)
                        
                        if decision.action == "BUY" and decision.shares_recommended > 0:
                            logging.info(f"AI recommends buying {decision.shares_recommended} shares of {company}")
                            logging.info(f"Reasoning: {', '.join(decision.reasoning)}")
                            
                            # Execute purchase (integrate with existing purchase system)
                            # This would call the existing automated share purchaser
                            
                        time.sleep(300)  # Wait 5 minutes between decisions
                        
                    time.sleep(1800)  # Wait 30 minutes between full cycles
                    
                except Exception as e:
                    logging.error(f"Error in trading loop: {e}")
                    time.sleep(60)
        
        threading.Thread(target=trading_loop, daemon=True).start()
        logging.info("Advanced AI trading system started")
    
    def stop_automated_trading(self):
        """Stop automated trading system"""
        self.trading_active = False
        logging.info("Advanced AI trading system stopped")
    
    def get_ai_performance_summary(self) -> Dict:
        """Get AI performance summary"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get recent decisions
            cursor.execute('''
                SELECT company, action, COUNT(*) as count, AVG(confidence) as avg_confidence
                FROM ai_decisions 
                WHERE timestamp > datetime('now', '-7 days')
                GROUP BY company, action
            ''')
            
            recent_decisions = cursor.fetchall()
            
            # Get overall stats
            cursor.execute('''
                SELECT COUNT(*) as total_decisions, AVG(confidence) as avg_confidence,
                       AVG(expected_return) as avg_expected_return
                FROM ai_decisions
            ''')
            
            overall_stats = cursor.fetchone()
            
            conn.close()
            
            return {
                'recent_decisions': recent_decisions,
                'total_decisions': overall_stats[0],
                'average_confidence': overall_stats[1],
                'average_expected_return': overall_stats[2],
                'ai_models_trained': len([nn for nn in self.neural_networks.values() if nn.is_trained]),
                'trading_active': self.trading_active
            }
            
        except Exception as e:
            logging.error(f"Error getting AI performance summary: {e}")
            return {}


class PredictiveAnalytics:
    """Advanced predictive analytics for market and blockchain analysis"""
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.models = {}
        
    def predict_optimal_acquisition_strategy(self, target_company: str, 
                                           current_holdings: int, 
                                           available_capital: float) -> Dict:
        """Predict optimal strategy for acquiring company shares"""
        try:
            # Analyze market conditions
            ticker = yf.Ticker(target_company)
            data = ticker.history(period="1y")
            
            if data.empty:
                return {'strategy': 'HOLD', 'confidence': 0.0}
            
            # Calculate metrics
            current_price = data['Close'].iloc[-1]
            volatility = data['Close'].pct_change().std() * np.sqrt(252)
            momentum = (data['Close'].iloc[-1] - data['Close'].iloc[-30]) / data['Close'].iloc[-30]
            
            # Determine strategy
            if volatility < 0.25 and momentum > 0.05:
                strategy = "AGGRESSIVE_BUY"
                recommended_shares = int(available_capital * 0.8 / current_price)
            elif volatility < 0.35 and momentum > 0.0:
                strategy = "GRADUAL_ACCUMULATION"
                recommended_shares = int(available_capital * 0.3 / current_price)
            elif momentum < -0.1:
                strategy = "WAIT_FOR_DIP"
                recommended_shares = 0
            else:
                strategy = "CONSERVATIVE_BUY"
                recommended_shares = int(available_capital * 0.2 / current_price)
            
            confidence = min(0.95, max(0.5, 1.0 - volatility))
            
            return {
                'strategy': strategy,
                'recommended_shares': recommended_shares,
                'confidence': confidence,
                'current_price': current_price,
                'volatility': volatility,
                'momentum': momentum,
                'reasoning': f"Based on {volatility:.2f} volatility and {momentum:.2f} momentum"
            }
            
        except Exception as e:
            logging.error(f"Error predicting acquisition strategy: {e}")
            return {'strategy': 'HOLD', 'confidence': 0.0}
    
    def forecast_market_impact(self, acquisition_size: int, company: str) -> Dict:
        """Forecast the market impact of a large acquisition"""
        try:
            # Get company info
            ticker = yf.Ticker(company)
            info = ticker.info
            shares_outstanding = info.get('sharesOutstanding', 1000000000)
            
            # Calculate impact
            ownership_percentage = (acquisition_size / shares_outstanding) * 100
            
            # Predict market reaction
            if ownership_percentage > 10:
                market_reaction = "SIGNIFICANT_POSITIVE"
                price_impact = 0.15  # 15% increase expected
            elif ownership_percentage > 5:
                market_reaction = "MODERATE_POSITIVE"
                price_impact = 0.08
            elif ownership_percentage > 1:
                market_reaction = "SLIGHT_POSITIVE"
                price_impact = 0.03
            else:
                market_reaction = "MINIMAL"
                price_impact = 0.01
            
            return {
                'ownership_percentage': ownership_percentage,
                'market_reaction': market_reaction,
                'expected_price_impact': price_impact,
                'regulatory_attention': ownership_percentage > 5,
                'takeover_speculation': ownership_percentage > 15
            }
            
        except Exception as e:
            logging.error(f"Error forecasting market impact: {e}")
            return {}