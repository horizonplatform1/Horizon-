"""
AI-Powered Automated Share Trading System
Automatically purchases and manages corporate shares using machine learning
"""

import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Optional, Tuple
import logging
import time
import threading
from datetime import datetime, timedelta
import sqlite3
import json

from blockchain.core import Blockchain, Transaction

class SharePredictor:
    """AI model for predicting share prices and optimal purchase timing"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.companies = ['GOOGL', 'MSFT', 'CMCSA']  # Google, Microsoft, NBCUniversal (Comcast)
        
    def collect_market_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Collect historical market data for a company"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            # Add technical indicators
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['RSI'] = self.calculate_rsi(data['Close'])
            data['Volatility'] = data['Close'].rolling(window=20).std()
            data['Price_Change'] = data['Close'].pct_change()
            
            return data
        except Exception as e:
            logging.error(f"Error collecting data for {symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """Prepare features for machine learning model"""
        features = ['Open', 'High', 'Low', 'Volume', 'SMA_20', 'SMA_50', 
                   'RSI', 'Volatility', 'Price_Change']
        
        feature_data = data[features].dropna()
        return self.scaler.fit_transform(feature_data)
    
    def train_model(self) -> bool:
        """Train the AI model on historical data"""
        try:
            all_data = []
            all_targets = []
            
            for symbol in self.companies:
                data = self.collect_market_data(symbol)
                if data.empty:
                    continue
                
                features = self.prepare_features(data)
                # Predict next day's closing price
                targets = data['Close'].shift(-1).dropna().values
                
                # Align features and targets
                min_len = min(len(features), len(targets))
                features = features[:min_len]
                targets = targets[:min_len]
                
                all_data.extend(features)
                all_targets.extend(targets)
            
            if len(all_data) > 0:
                X = np.array(all_data)
                y = np.array(all_targets)
                
                self.model.fit(X, y)
                self.is_trained = True
                logging.info("AI trading model trained successfully")
                return True
            
        except Exception as e:
            logging.error(f"Error training model: {e}")
        
        return False
    
    def predict_optimal_purchase(self, symbol: str) -> Tuple[bool, float, str]:
        """Predict if now is optimal time to purchase shares"""
        if not self.is_trained:
            self.train_model()
        
        try:
            data = self.collect_market_data(symbol, period="3mo")
            if data.empty:
                return False, 0.0, "No data available"
            
            current_features = self.prepare_features(data)
            if len(current_features) == 0:
                return False, 0.0, "Insufficient data for prediction"
            
            # Use latest data point for prediction
            latest_features = current_features[-1:].reshape(1, -1)
            predicted_price = self.model.predict(latest_features)[0]
            current_price = data['Close'].iloc[-1]
            
            # Calculate potential profit
            profit_potential = (predicted_price - current_price) / current_price
            
            # Decision logic
            should_buy = profit_potential > 0.02  # Expect at least 2% profit
            confidence = min(abs(profit_potential) * 100, 100)  # Convert to percentage
            
            reason = f"Predicted price: ${predicted_price:.2f}, Current: ${current_price:.2f}, Potential profit: {profit_potential*100:.2f}%"
            
            return should_buy, confidence, reason
            
        except Exception as e:
            logging.error(f"Error predicting for {symbol}: {e}")
            return False, 0.0, f"Prediction error: {e}"


class AutomatedSharePurchaser:
    """Automated system for purchasing corporate shares"""
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.predictor = SharePredictor()
        self.db_path = "data/ai_trading.db"
        self.is_running = False
        self.purchase_thread = None
        self.companies = {
            'GOOGL': {'name': 'Google', 'max_shares': 1000000, 'priority': 1},
            'MSFT': {'name': 'Microsoft', 'max_shares': 1000000, 'priority': 2},
            'CMCSA': {'name': 'NBCUniversal', 'max_shares': 1000000, 'priority': 3}
        }
        self._init_database()
        
    def _init_database(self):
        """Initialize trading database"""
        import os
        os.makedirs("data", exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchase_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                shares_purchased INTEGER NOT NULL,
                price_per_share REAL NOT NULL,
                total_cost REAL NOT NULL,
                buyer_address TEXT NOT NULL,
                prediction_confidence REAL NOT NULL,
                reasoning TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                blockchain_tx_id TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS share_holdings (
                symbol TEXT PRIMARY KEY,
                total_shares INTEGER DEFAULT 0,
                average_cost REAL DEFAULT 0.0,
                current_value REAL DEFAULT 0.0,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def get_current_share_price(self, symbol: str) -> float:
        """Get current market price for a share"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                return float(data['Close'].iloc[-1])
        except Exception as e:
            logging.error(f"Error getting price for {symbol}: {e}")
        
        # Fallback to simulated prices for demo
        prices = {'GOOGL': 150.0, 'MSFT': 380.0, 'CMCSA': 45.0}
        return prices.get(symbol, 100.0)
    
    def calculate_purchase_amount(self, symbol: str, confidence: float, wallet_balance: float) -> int:
        """Calculate optimal number of shares to purchase"""
        max_shares = self.companies[symbol]['max_shares']
        current_holdings = self.get_current_holdings(symbol)
        
        # Don't exceed maximum holdings
        remaining_capacity = max_shares - current_holdings
        if remaining_capacity <= 0:
            return 0
        
        # Calculate purchase based on confidence and available funds
        price_per_share = self.get_current_share_price(symbol)
        max_affordable = int(wallet_balance * 0.1 / price_per_share)  # Use 10% of wallet
        
        # Scale by confidence
        confidence_factor = confidence / 100.0
        target_shares = int(max_affordable * confidence_factor)
        
        return min(target_shares, remaining_capacity, 1000)  # Cap at 1000 shares per purchase
    
    def execute_purchase(self, symbol: str, shares: int, buyer_address: str, 
                        confidence: float, reasoning: str) -> Optional[str]:
        """Execute the actual share purchase"""
        try:
            price_per_share = self.get_current_share_price(symbol)
            total_cost = shares * price_per_share
            
            # Create blockchain transaction for share purchase
            tx = Transaction(
                sender=buyer_address,
                recipient="CORPORATE_TREASURY",
                amount=total_cost,
                tx_type="corporate_share_purchase"
            )
            
            # Add custom data for share purchase
            tx.share_data = {
                'symbol': symbol,
                'shares': shares,
                'price_per_share': price_per_share,
                'confidence': confidence,
                'reasoning': reasoning
            }
            
            # Add to blockchain
            if self.blockchain.add_transaction(tx):
                # Record in database
                self._record_purchase(symbol, shares, price_per_share, total_cost, 
                                    buyer_address, confidence, reasoning, tx.tx_id)
                
                # Update share holdings
                self._update_holdings(symbol, shares, price_per_share)
                
                logging.info(f"Successfully purchased {shares} shares of {symbol} for {total_cost} DataCoins")
                return tx.tx_id
            
        except Exception as e:
            logging.error(f"Error executing purchase of {symbol}: {e}")
        
        return None
    
    def _record_purchase(self, symbol: str, shares: int, price_per_share: float, 
                        total_cost: float, buyer_address: str, confidence: float, 
                        reasoning: str, tx_id: str):
        """Record purchase in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO purchase_history 
            (symbol, shares_purchased, price_per_share, total_cost, buyer_address, 
             prediction_confidence, reasoning, blockchain_tx_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (symbol, shares, price_per_share, total_cost, buyer_address, 
              confidence, reasoning, tx_id))
        
        conn.commit()
        conn.close()
    
    def _update_holdings(self, symbol: str, new_shares: int, price_per_share: float):
        """Update current share holdings"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current holdings
        cursor.execute('SELECT total_shares, average_cost FROM share_holdings WHERE symbol = ?', (symbol,))
        result = cursor.fetchone()
        
        if result:
            current_shares, current_avg_cost = result
            total_shares = current_shares + new_shares
            
            # Calculate new average cost
            total_cost = (current_shares * current_avg_cost) + (new_shares * price_per_share)
            new_avg_cost = total_cost / total_shares if total_shares > 0 else 0
            
            cursor.execute('''
                UPDATE share_holdings 
                SET total_shares = ?, average_cost = ?, last_updated = CURRENT_TIMESTAMP
                WHERE symbol = ?
            ''', (total_shares, new_avg_cost, symbol))
        else:
            # Insert new holding
            cursor.execute('''
                INSERT INTO share_holdings (symbol, total_shares, average_cost)
                VALUES (?, ?, ?)
            ''', (symbol, new_shares, price_per_share))
        
        conn.commit()
        conn.close()
    
    def get_current_holdings(self, symbol: str) -> int:
        """Get current number of shares held for a symbol"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT total_shares FROM share_holdings WHERE symbol = ?', (symbol,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else 0
    
    def automated_purchase_cycle(self, buyer_address: str):
        """Main automated purchase cycle"""
        while self.is_running:
            try:
                wallet_balance = self.blockchain.get_balance(buyer_address)
                
                if wallet_balance < 100:  # Minimum balance required
                    time.sleep(300)  # Wait 5 minutes
                    continue
                
                # Check each company for purchase opportunities
                for symbol in self.companies.keys():
                    should_buy, confidence, reasoning = self.predictor.predict_optimal_purchase(symbol)
                    
                    if should_buy and confidence > 70:  # High confidence threshold
                        shares_to_buy = self.calculate_purchase_amount(symbol, confidence, wallet_balance)
                        
                        if shares_to_buy > 0:
                            tx_id = self.execute_purchase(symbol, shares_to_buy, buyer_address, 
                                                        confidence, reasoning)
                            
                            if tx_id:
                                print(f"🤖 AI Trader: Purchased {shares_to_buy} shares of {symbol}")
                                print(f"   Confidence: {confidence:.1f}% | Reason: {reasoning}")
                                
                                # Update wallet balance
                                wallet_balance = self.blockchain.get_balance(buyer_address)
                
                # Wait before next cycle (check every 5 minutes)
                time.sleep(300)
                
            except Exception as e:
                logging.error(f"Error in automated purchase cycle: {e}")
                time.sleep(60)  # Wait 1 minute on error
    
    def start_automated_purchasing(self, buyer_address: str):
        """Start the automated purchasing system"""
        if self.is_running:
            return False
        
        self.is_running = True
        self.purchase_thread = threading.Thread(
            target=self.automated_purchase_cycle, 
            args=(buyer_address,),
            daemon=True
        )
        self.purchase_thread.start()
        
        logging.info("Automated share purchasing system started")
        return True
    
    def stop_automated_purchasing(self):
        """Stop the automated purchasing system"""
        self.is_running = False
        if self.purchase_thread:
            self.purchase_thread.join(timeout=10)
        
        logging.info("Automated share purchasing system stopped")
    
    def get_portfolio_summary(self) -> Dict:
        """Get comprehensive portfolio summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get holdings
        cursor.execute('SELECT * FROM share_holdings')
        holdings = cursor.fetchall()
        
        # Get recent purchases
        cursor.execute('''
            SELECT * FROM purchase_history 
            ORDER BY timestamp DESC LIMIT 10
        ''')
        recent_purchases = cursor.fetchall()
        
        conn.close()
        
        total_portfolio_value = 0
        portfolio = {}
        
        for holding in holdings:
            symbol, shares, avg_cost, _, last_updated = holding
            current_price = self.get_current_share_price(symbol)
            current_value = shares * current_price
            total_cost = shares * avg_cost
            profit_loss = current_value - total_cost
            
            portfolio[symbol] = {
                'shares': shares,
                'average_cost': avg_cost,
                'current_price': current_price,
                'current_value': current_value,
                'profit_loss': profit_loss,
                'profit_loss_percent': (profit_loss / total_cost * 100) if total_cost > 0 else 0
            }
            
            total_portfolio_value += current_value
        
        return {
            'total_value': total_portfolio_value,
            'holdings': portfolio,
            'recent_purchases': recent_purchases,
            'is_running': self.is_running
        }