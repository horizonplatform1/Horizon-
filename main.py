#!/usr/bin/env python3
"""
DataCoin - A Real Digital Currency System
A comprehensive digital currency powered by internet data conversion

Features:
- Blockchain with proof-of-work mining
- Wallet management with RSA encryption
- Internet data to currency conversion
- Corporate share-based mining regulation
- RESTful API and web interface

Usage:
    python main.py [OPTIONS]

Options:
    --demo          Run demonstration scenario
    --api-only      Start only the API server
    --interactive   Start interactive command-line interface
    --web           Open web interface after starting API
"""

import asyncio
import argparse
import time
import threading
import webbrowser
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from blockchain.core import Blockchain
from wallet.wallet import WalletManager
from data_engine.data_converter import DataConverter, DEFAULT_DATA_SOURCES
from blockchain.ai_trader import AutomatedSharePurchaser
from blockchain.corporate_governance import CorporateGovernanceSystem
from blockchain.analytics_engine import BlockchainAnalyzer, MarketAnalyzer, RealTimeTracker
from api.main import app
import uvicorn
from blockchain.advanced_ai_system import AdvancedTradingAI, PredictiveAnalytics
from blockchain.advanced_governance import AdvancedCorporateGovernance
from blockchain.real_time_tracker import AdvancedRealTimeTracker

class DataCoinSystem:
    """Main DataCoin system controller"""
    
    def __init__(self):
        print("🪙 Initializing Advanced DataCoin System...")
        print("🔗 Setting up blockchain infrastructure...")
        
        # Core systems
        self.blockchain = Blockchain()
        self.wallet_manager = WalletManager()
        self.data_converter = DataConverter(self.blockchain)
        self.share_purchaser = AutomatedSharePurchaser(self.blockchain)
        self.governance_system = CorporateGovernanceSystem(self.blockchain)
        self.analyzer = BlockchainAnalyzer(self.blockchain)
        self.market_analyzer = MarketAnalyzer()
        self.tracker = RealTimeTracker(self.blockchain)
        
        # Advanced AI and automation systems
        print("🤖 Initializing Advanced AI Systems...")
        self.advanced_ai = AdvancedTradingAI(self.blockchain)
        self.predictive_analytics = PredictiveAnalytics(self.blockchain)
        
        # Advanced governance and legal systems
        print("⚖️  Initializing Advanced Governance Systems...")
        self.advanced_governance = AdvancedCorporateGovernance(self.blockchain)
        
        # Advanced real-time tracking and monitoring
        print("📊 Initializing Advanced Tracking Systems...")
        self.advanced_tracker = AdvancedRealTimeTracker(self.blockchain)
        
        print("✅ Advanced DataCoin System initialized successfully!")
        print("🚀 System ready with AI trading, governance monitoring, and real-time tracking")
        
        # Setup default data sources
        for source_config in DEFAULT_DATA_SOURCES:
            self.data_converter.add_data_source(**source_config)
        
        print("✅ DataCoin system initialized successfully!")
    
    def create_demo_scenario(self):
        """Create a comprehensive demonstration scenario with advanced features"""
        print("\n� Creating Advanced DataCoin Demo Scenario...")
        print("=" * 60)
        
        # Create demo wallets
        alice_wallet = self.wallet_manager.create_wallet("alice")
        bob_wallet = self.wallet_manager.create_wallet("bob")
        miner_wallet = self.wallet_manager.create_wallet("miner")
        ai_wallet = self.wallet_manager.create_wallet("ai_trader")
        
        # Connect wallets to blockchain
        alice_wallet.connect_to_blockchain(self.blockchain)
        bob_wallet.connect_to_blockchain(self.blockchain)
        miner_wallet.connect_to_blockchain(self.blockchain)
        ai_wallet.connect_to_blockchain(self.blockchain)
        
        print(f"👤 Alice wallet: {alice_wallet.address}")
        print(f"👤 Bob wallet: {bob_wallet.address}")
        print(f"⛏️ Miner wallet: {miner_wallet.address}")
        print(f"🤖 AI Trader wallet: {ai_wallet.address}")
        
        # Simulate data conversion for Alice and AI trader
        print("\n🌐 Simulating data conversion...")
        alice_wallet.convert_data_to_currency(5.0)  # 5 MB of data
        bob_wallet.convert_data_to_currency(3.5)    # 3.5 MB of data
        ai_wallet.convert_data_to_currency(10.0)    # 10 MB for AI trading
        
        # Mine the first block
        print("\n⛏️ Mining first block...")
        miner_wallet.mine_block()
        
        # Create some transactions
        print("\n💸 Creating transactions...")
        alice_wallet.create_transaction(bob_wallet.address, 0.001, "transfer")
        bob_wallet.create_transaction(alice_wallet.address, 0.0005, "transfer")
        alice_wallet.create_transaction(ai_wallet.address, 0.01, "transfer")  # Fund AI trader
        
        # Collect data from sources
        print("\n📊 Collecting data from sources...")
        for source_id in list(self.data_converter.sources.keys())[:2]:
            try:
                self.data_converter.collect_and_convert(source_id, alice_wallet.address)
                time.sleep(1)  # Brief delay between collections
            except Exception as e:
                print(f"⚠️ Could not collect from {source_id}: {e}")
        
        # Mine another block
        print("\n⛏️ Mining second block...")
        miner_wallet.mine_block()
        
        # Demonstrate AI Trading System
        print("\n🤖 Demonstrating AI Trading System...")
        print("   Training AI model with market data...")
        try:
            if self.advanced_ai.predictor.train_model():
                print("   ✅ AI model trained successfully")
            else:
                print("   ⚠️ AI model training failed, using defaults")
        except Exception as e:
            print(f"   ⚠️ AI training error: {e}")
        
        # Corporate shares demonstration with governance
        print("\n🏢 Demonstrating corporate shares and governance...")
        alice_wallet.buy_corporate_shares("Google", 1)
        bob_wallet.buy_corporate_shares("Microsoft", 1)
        
        # Simulate governance updates
        try:
            self.governance_system.update_share_ownership("GOOGL", alice_wallet.address, 1)
            self.governance_system.update_share_ownership("MSFT", bob_wallet.address, 1)
            print("   ✅ Governance tracking updated")
        except Exception as e:
            print(f"   ⚠️ Governance update error: {e}")
        
        # Start AI automated trading (brief demo)
        print("\n🤖 Starting AI automated trading (demo mode)...")
        try:
            # Don't actually start the continuous trading for demo
            print("   ✅ AI trading system initialized")
        except Exception as e:
            print(f"   ⚠️ AI trading error: {e}")
        
        # Generate analytics report
        print("\n📈 Generating Advanced Analytics Report...")
        try:
            analytics_report = self.analyzer.generate_analytics_report()
            if 'error' not in analytics_report:
                print("   ✅ Analytics report generated")
                print(f"   Network Health: {analytics_report['blockchain_analysis']['network_health']['health_status']}")
            else:
                print(f"   ⚠️ Analytics error: {analytics_report['error']}")
        except Exception as e:
            print(f"   ⚠️ Analytics generation error: {e}")
        
        # Start real-time tracking
        print("\n📡 Starting Real-time Tracking System...")
        try:
            self.tracker.start_tracking()
            print("   ✅ Real-time tracking activated")
        except Exception as e:
            print(f"   ⚠️ Tracking error: {e}")
        
        # Final mining and balance check
        print("\n⛏️ Final mining...")
        miner_wallet.mine_block()
        
        # Display final balances
        print("\n💰 Final Balances:")
        print(f"Alice: {alice_wallet.get_balance():.6f} DataCoins")
        print(f"Bob: {bob_wallet.get_balance():.6f} DataCoins")
        print(f"Miner: {miner_wallet.get_balance():.6f} DataCoins")
        print(f"AI Trader: {ai_wallet.get_balance():.6f} DataCoins")
        
        # Display blockchain stats
        stats = self.blockchain.get_blockchain_stats()
        print(f"\n📊 Blockchain Statistics:")
        print(f"Total Blocks: {stats['total_blocks']}")
        print(f"Total Transactions: {stats['total_transactions']}")
        print(f"Mining Difficulty: {stats['current_difficulty']}")
        print(f"Data Converted: {stats['total_data_converted_mb']:.3f} MB")
        print(f"Corporate Shares: {stats['corporate_shares']}")
        
        # Display AI trading status
        try:
            portfolio = self.advanced_ai.get_portfolio_summary()
            print(f"\n🤖 AI Trading Status:")
            print(f"Portfolio Value: ${portfolio['total_value']:.2f}")
            print(f"Holdings: {len(portfolio['holdings'])} companies")
            print(f"System Status: {'Running' if portfolio['is_running'] else 'Stopped'}")
        except Exception as e:
            print(f"   ⚠️ Portfolio summary error: {e}")
        
        # Display governance summary
        print(f"\n🏛️ Corporate Governance Summary:")
        companies = ['GOOGL', 'MSFT', 'CMCSA']
        for symbol in companies:
            try:
                shareholders = self.governance_system.get_major_shareholders(symbol)
                print(f"{symbol}: {len(shareholders)} major shareholders")
            except Exception as e:
                print(f"{symbol}: Error retrieving shareholders")
        
        print(f"\n✅ Advanced DataCoin System Demo Complete!")
        print(f"   • Blockchain: {len(self.blockchain.chain)} blocks")
        print(f"   • AI Trading: Initialized")
        print(f"   • Real-time Tracking: {'Active' if self.tracker.is_running else 'Inactive'}")
        print(f"   • Data Conversion: Active")
        print(f"   • Corporate Governance: Monitoring {len(companies)} companies")
        
        return alice_wallet, bob_wallet, miner_wallet, ai_wallet
    
    def interactive_cli(self):
        """Enhanced interactive command-line interface with advanced features"""
        current_wallet = None
        
        while True:
            print("\n" + "="*80)
            print("🪙 ADVANCED DATACOIN SYSTEM - Interactive Interface")
            print("="*80)
            print("📊 Status:", "🟢 ACTIVE" if current_wallet else "🔴 No wallet loaded")
            if current_wallet:
                print(f"💼 Wallet: {current_wallet.wallet_name}")
                print(f"💰 Balance: {self.blockchain.get_balance(current_wallet.public_key):.2f} DataCoin")
            
            # Enhanced menu with advanced features
            print("\n🔧 BASIC OPERATIONS:")
            print("1.  💼 Create Wallet")
            print("2.  📋 List Wallets") 
            print("3.  🔓 Load Wallet")
            print("4.  ⛏️  Mine Block")
            print("5.  💸 Send Transaction")
            print("6.  🔄 Convert Data to Currency")
            print("7.  📡 Collect Internet Data")
            print("8.  📈 Buy Company Shares")
            print("9.  🔗 Show Blockchain")
            
            print("\n🤖 AI & AUTOMATION:")
            print("10. 🧠 AI Trading System")
            print("11. 📊 Predictive Analytics")
            print("12. 🎯 Advanced Trading Decisions")
            print("13. 📈 Market Intelligence")
            
            print("\n⚖️  GOVERNANCE & LEGAL:")
            print("14. 🏛️  Corporate Governance")
            print("15. 📜 Legal Actions")
            print("16. 🔔 Board Notifications")
            print("17. 📋 Compliance Monitoring")
            
            print("\n📊 MONITORING & TRACKING:")
            print("18. 🎯 Real-Time Tracking")
            print("19. 📊 Analytics Dashboard")
            print("20. 📈 Portfolio Management")
            print("21. 🚨 Alert Management")
            
            print("\n🌐 SYSTEM MANAGEMENT:")
            print("22. 📊 System Status")
            print("23. 🛠️  API Server")
            print("24. ❓ Help")
            print("25. 🚪 Exit")
            
            choice = input("\n🎯 Enter your choice (1-25): ").strip()
            
            try:
                if choice == '1':
                    wallet_name = input("💼 Enter wallet name: ").strip()
                    self.create_wallet_cli(wallet_name)
                elif choice == '2':
                    self.list_wallets_cli()
                elif choice == '3':
                    wallet_name = input("💼 Enter wallet name: ").strip()
                    current_wallet = self.load_wallet_cli(wallet_name)
                elif choice == '4':
                    if current_wallet:
                        self.mine_block_cli(current_wallet)
                    else:
                        print("❌ Please load a wallet first")
                elif choice == '5':
                    if current_wallet:
                        self.send_transaction_cli(current_wallet)
                    else:
                        print("❌ Please load a wallet first")
                elif choice == '6':
                    if current_wallet:
                        self.convert_data_cli(current_wallet)
                    else:
                        print("❌ Please load a wallet first")
                elif choice == '7':
                    if current_wallet:
                        self.collect_data_cli(current_wallet)
                    else:
                        print("❌ Please load a wallet first")
                elif choice == '8':
                    if current_wallet:
                        self.buy_shares_cli(current_wallet)
                    else:
                        print("❌ Please load a wallet first")
                elif choice == '9':
                    self.show_blockchain_cli()
                elif choice == '10':
                    self.advanced_ai_trading_cli()
                elif choice == '11':
                    self.predictive_analytics_cli()
                elif choice == '12':
                    if current_wallet:
                        self.advanced_trading_decisions_cli(current_wallet)
                    else:
                        print("❌ Please load a wallet first")
                elif choice == '13':
                    self.market_intelligence_cli()
                elif choice == '14':
                    self.advanced_governance_cli()
                elif choice == '15':
                    self.legal_actions_cli()
                elif choice == '16':
                    self.board_notifications_cli()
                elif choice == '17':
                    self.compliance_monitoring_cli()
                elif choice == '18':
                    self.advanced_tracking_cli()
                elif choice == '19':
                    self.analytics_dashboard_cli()
                elif choice == '20':
                    self.portfolio_management_cli()
                elif choice == '21':
                    self.alert_management_cli()
                elif choice == '22':
                    self.system_status_cli()
                elif choice == '23':
                    self.start_api_server()
                elif choice == '24':
                    self.show_help()
                elif choice == '25':
                    print("👋 Goodbye! Exiting DataCoin system...")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n🛑 Operation cancelled by user")
            except Exception as e:
                print(f"❌ Error: {e}")
                logging.error(f"CLI error: {e}")

    def show_help(self):
        """Show available CLI commands"""
        print("""
📚 Available Commands:
    help                  - Show this help message
    status               - Show system status
    create wallet <name> - Create a new wallet
    list wallets         - List all wallets
    load wallet <name>   - Load a wallet
    balance              - Show current wallet balance
    mine                 - Mine a block with current wallet
    send                 - Send DataCoins to another address
    convert data         - Convert data to DataCoins
    collect data         - Collect data from sources
    buy shares           - Buy corporate shares
    blockchain           - Show blockchain information
    ai trading           - AI automated trading controls
    governance           - Corporate governance management
    analytics            - Advanced analytics and insights
    tracking             - Real-time tracking system
    portfolio            - Portfolio management and analysis
    exit                 - Exit the CLI
        """)
    
    def show_system_status(self):
        """Show system status"""
        stats = self.blockchain.get_blockchain_stats()
        data_stats = self.data_converter.get_conversion_stats()
        
        print(f"""
📊 System Status:
   Blockchain:
     • Total Blocks: {stats['total_blocks']}
     • Total Transactions: {stats['total_transactions']}
     • Mining Difficulty: {stats['current_difficulty']}
     • Pending Transactions: {stats['pending_transactions']}
     
   Data Conversion:
     • Total Sources: {data_stats['total_sources']}
     • Data Collected: {data_stats['total_data_collected_mb']:.3f} MB
     • Currency Generated: {data_stats['total_currency_generated']:.6f} DC
     • Conversion Rate: {data_stats['conversion_rate']:.6f} DC/MB
     
   Corporate Shares:
     • Google: {stats['corporate_shares']['Google']}
     • Microsoft: {stats['corporate_shares']['Microsoft']}
     • NBC Universal: {stats['corporate_shares']['NBC Universal']}
        """)
    
    def create_wallet_cli(self, wallet_name):
        """Create wallet via CLI"""
        wallet = self.wallet_manager.create_wallet(wallet_name)
        wallet.connect_to_blockchain(self.blockchain)
        print(f"✅ Wallet '{wallet_name}' created with address: {wallet.address}")
        return wallet
    
    def list_wallets_cli(self):
        """List wallets via CLI"""
        wallets = self.wallet_manager.list_wallets()
        if wallets:
            print("💼 Available Wallets:")
            for wallet in wallets:
                print(f"   • {wallet}")
        else:
            print("❌ No wallets found")
    
    def load_wallet_cli(self, wallet_name):
        """Load wallet via CLI"""
        wallet = self.wallet_manager.load_wallet(wallet_name)
        if wallet:
            wallet.connect_to_blockchain(self.blockchain)
            print(f"✅ Loaded wallet '{wallet_name}' with balance: {wallet.get_balance():.6f} DC")
            return wallet
        else:
            print(f"❌ Wallet '{wallet_name}' not found")
            return None
    
    def mine_block_cli(self, wallet):
        """Mine block via CLI"""
        if len(self.blockchain.pending_transactions) == 0:
            print("❌ No pending transactions to mine")
            return
        
        print("⛏️ Mining block... (this may take a moment)")
        success = wallet.mine_block()
        if success:
            print(f"✅ Block mined successfully! Reward: {self.blockchain.mining_reward} DC")
        else:
            print("❌ Mining failed")
    
    def send_transaction_cli(self, wallet):
        """Send transaction via CLI"""
        recipient = input("Recipient address: ").strip()
        try:
            amount = float(input("Amount: "))
            transaction = wallet.create_transaction(recipient, amount)
            if transaction:
                print(f"✅ Transaction sent! TX ID: {transaction.tx_id[:16]}...")
            else:
                print("❌ Transaction failed")
        except ValueError:
            print("❌ Invalid amount")
    
    def convert_data_cli(self, wallet):
        """Convert data via CLI"""
        try:
            data_size = float(input("Data size (MB): "))
            transaction = wallet.convert_data_to_currency(data_size)
            if transaction:
                print(f"✅ Converted {data_size} MB to {transaction.amount:.6f} DataCoins")
            else:
                print("❌ Data conversion failed")
        except ValueError:
            print("❌ Invalid data size")
    
    def collect_data_cli(self, wallet):
        """Collect data from sources via CLI"""
        sources = list(self.data_converter.sources.keys())
        if not sources:
            print("❌ No data sources available")
            return
        
        print("📊 Available data sources:")
        for i, source_id in enumerate(sources):
            print(f"   {i+1}. {source_id}")
        
        try:
            choice = int(input("Select source (number): ")) - 1
            if 0 <= choice < len(sources):
                source_id = sources[choice]
                transaction = self.data_converter.collect_and_convert(source_id, wallet.address)
                if transaction:
                    print(f"✅ Collected data from {source_id}")
                else:
                    print("❌ Data collection failed")
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Invalid input")
    
    def buy_shares_cli(self, wallet):
        """Buy corporate shares via CLI"""
        companies = ['Google', 'Microsoft', 'NBC Universal']
        print("🏢 Available companies:")
        for i, company in enumerate(companies):
            print(f"   {i+1}. {company}")
        
        try:
            choice = int(input("Select company (number): ")) - 1
            if 0 <= choice < len(companies):
                company = companies[choice]
                shares = int(input("Number of shares: "))
                success = wallet.buy_corporate_shares(company, shares)
                if success:
                    print(f"✅ Purchased {shares} shares of {company}")
                else:
                    print("❌ Share purchase failed")
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Invalid input")
    
    def show_blockchain_cli(self):
        """Show blockchain information via CLI"""
        print(f"\n🔗 Blockchain Information:")
        print(f"   Total Blocks: {len(self.blockchain.chain)}")
        
        if len(self.blockchain.chain) > 1:
            latest_block = self.blockchain.get_latest_block()
            print(f"   Latest Block Hash: {latest_block.hash}")
            print(f"   Latest Block Transactions: {len(latest_block.transactions)}")
            print(f"   Latest Block Timestamp: {datetime.fromtimestamp(latest_block.timestamp)}")
        
        if self.blockchain.pending_transactions:
            print(f"   Pending Transactions: {len(self.blockchain.pending_transactions)}")
        
        print(f"   Blockchain Valid: {self.blockchain.is_chain_valid()}")
    
    def advanced_ai_trading_cli(self):
        """Advanced AI trading system interface"""
        print("\n🤖 Advanced AI Trading System")
        print("="*50)
        
        print("1. 🧠 Train AI Models")
        print("2. 🚀 Start Automated Trading")
        print("3. 🛑 Stop Automated Trading")
        print("4. 📊 AI Performance Summary")
        print("5. 🔄 Market Intelligence")
        print("6. 🎯 Single Trading Decision")
        print("7. 🔙 Back to Main Menu")
        
        choice = input("\n🎯 Enter choice: ").strip()
        
        try:
            if choice == '1':
                print("🧠 Training AI models for all companies...")
                results = self.advanced_ai.train_ai_models()
                print("📊 Training Results:")
                for company, success in results.items():
                    status = "✅ Success" if success else "❌ Failed"
                    print(f"  {company}: {status}")
                    
            elif choice == '2':
                wallet_address = input("💼 Enter wallet address for trading: ").strip()
                if wallet_address:
                    self.advanced_ai.start_automated_trading(wallet_address)
                    print("🚀 Advanced AI trading system started!")
                else:
                    print("❌ Please provide a valid wallet address")
                    
            elif choice == '3':
                self.advanced_ai.stop_automated_trading()
                print("🛑 Advanced AI trading system stopped")
                
            elif choice == '4':
                summary = self.advanced_ai.get_ai_performance_summary()
                print("📊 AI Performance Summary:")
                print(f"  Total Decisions: {summary.get('total_decisions', 0)}")
                print(f"  Average Confidence: {summary.get('average_confidence', 0):.2%}")
                print(f"  Average Expected Return: {summary.get('average_expected_return', 0):.2%}")
                print(f"  AI Models Trained: {summary.get('ai_models_trained', 0)}/3")
                print(f"  Trading Active: {'🟢 Yes' if summary.get('trading_active') else '🔴 No'}")
                
                if summary.get('recent_decisions'):
                    print("\n📈 Recent Decisions:")
                    for decision in summary['recent_decisions']:
                        print(f"  {decision[0]}: {decision[1]} ({decision[2]} decisions, {decision[3]:.2%} confidence)")
                        
            elif choice == '5':
                company = input("📈 Enter company symbol (GOOGL/MSFT/CMCSA): ").strip().upper()
                if company in ['GOOGL', 'MSFT', 'CMCSA']:
                    intelligence = self.advanced_ai.gather_market_intelligence(company)
                    print(f"📊 Market Intelligence for {company}:")
                    print(f"  Overall Sentiment: {intelligence.overall_sentiment:.2f}")
                    print(f"  News Sentiment: {intelligence.news_sentiment.get(company, 0):.2f}")
                    print(f"  Social Sentiment: {intelligence.social_media_sentiment.get(company, 0):.2f}")
                else:
                    print("❌ Invalid company symbol")
                    
            elif choice == '6':
                company = input("📈 Enter company symbol (GOOGL/MSFT/CMCSA): ").strip().upper()
                balance = float(input("💰 Enter available balance: "))
                
                if company in ['GOOGL', 'MSFT', 'CMCSA']:
                    decision = self.advanced_ai.make_trading_decision(company, balance)
                    print(f"\n🎯 AI Trading Decision for {company}:")
                    print(f"  Action: {decision.action}")
                    print(f"  Shares Recommended: {decision.shares_recommended}")
                    print(f"  Confidence: {decision.confidence:.2%}")
                    print(f"  Risk Assessment: {decision.risk_assessment}")
                    print(f"  Expected Return: {decision.expected_return:.2%}")
                    print(f"  Time Horizon: {decision.time_horizon}")
                    print(f"  Market Sentiment: {decision.market_sentiment:.2f}")
                    print("  Reasoning:")
                    for reason in decision.reasoning:
                        print(f"    • {reason}")
                else:
                    print("❌ Invalid company symbol")
                    
        except Exception as e:
            print(f"❌ Error in AI trading system: {e}")
            logging.error(f"AI trading CLI error: {e}")

    def predictive_analytics_cli(self):
        """Predictive analytics interface"""
        print("\n📊 Predictive Analytics System")
        print("="*50)
        
        print("1. 🎯 Optimal Acquisition Strategy")
        print("2. 📈 Market Impact Forecast")
        print("3. 🔮 Price Prediction")
        print("4. 📊 Risk Analysis")
        print("5. 🔙 Back to Main Menu")
        
        choice = input("\n🎯 Enter choice: ").strip()
        
        try:
            if choice == '1':
                company = input("📈 Enter company symbol (GOOGL/MSFT/CMCSA): ").strip().upper()
                holdings = int(input("📊 Current holdings: "))
                capital = float(input("💰 Available capital: "))
                
                if company in ['GOOGL', 'MSFT', 'CMCSA']:
                    strategy = self.predictive_analytics.predict_optimal_acquisition_strategy(
                        company, holdings, capital
                    )
                    print(f"\n🎯 Optimal Strategy for {company}:")
                    print(f"  Strategy: {strategy.get('strategy', 'UNKNOWN')}")
                    print(f"  Recommended Shares: {strategy.get('recommended_shares', 0)}")
                    print(f"  Confidence: {strategy.get('confidence', 0):.2%}")
                    print(f"  Current Price: ${strategy.get('current_price', 0):.2f}")
                    print(f"  Volatility: {strategy.get('volatility', 0):.2%}")
                    print(f"  Momentum: {strategy.get('momentum', 0):.2%}")
                    print(f"  Reasoning: {strategy.get('reasoning', 'N/A')}")
                else:
                    print("❌ Invalid company symbol")
                    
            elif choice == '2':
                company = input("📈 Enter company symbol (GOOGL/MSFT/CMCSA): ").strip().upper()
                shares = int(input("📊 Acquisition size (shares): "))
                
                if company in ['GOOGL', 'MSFT', 'CMCSA']:
                    impact = self.predictive_analytics.forecast_market_impact(shares, company)
                    print(f"\n📈 Market Impact Forecast for {shares:,} shares of {company}:")
                    print(f"  Ownership Percentage: {impact.get('ownership_percentage', 0):.4f}%")
                    print(f"  Market Reaction: {impact.get('market_reaction', 'UNKNOWN')}")
                    print(f"  Expected Price Impact: {impact.get('expected_price_impact', 0):.2%}")
                    print(f"  Regulatory Attention: {'🟡 Yes' if impact.get('regulatory_attention') else '🟢 No'}")
                    print(f"  Takeover Speculation: {'🔴 Yes' if impact.get('takeover_speculation') else '🟢 No'}")
                else:
                    print("❌ Invalid company symbol")
                    
        except Exception as e:
            print(f"❌ Error in predictive analytics: {e}")
            logging.error(f"Predictive analytics CLI error: {e}")

    def advanced_governance_cli(self):
        """Advanced corporate governance interface"""
        print("\n⚖️  Advanced Corporate Governance System")
        print("="*50)
        
        print("1. 🏛️  Start Governance Monitoring")
        print("2. 🛑 Stop Governance Monitoring")
        print("3. 📜 Execute Corporate Action")
        print("4. 📊 Governance Dashboard")
        print("5. 🔔 Send Board Notification")
        print("6. 📋 Compliance Status")
        print("7. 🔙 Back to Main Menu")
        
        choice = input("\n🎯 Enter choice: ").strip()
        
        try:
            if choice == '1':
                self.advanced_governance.start_governance_monitoring()
                print("🏛️  Advanced governance monitoring started!")
                
            elif choice == '2':
                self.advanced_governance.stop_governance_monitoring()
                print("🛑 Advanced governance monitoring stopped")
                
            elif choice == '3':
                print("\n📜 Available Corporate Actions:")
                print("1. 📋 Takeover Notice")
                print("2. 🗳️  Proxy Fight")
                print("3. ⚖️  Shareholder Lawsuit")
                
                action_choice = input("Select action (1-3): ").strip()
                company = input("📈 Enter company symbol (GOOGL/MSFT/CMCSA): ").strip().upper()
                initiator = input("💼 Enter initiator address: ").strip()
                
                if company in ['GOOGL', 'MSFT', 'CMCSA'] and initiator:
                    if action_choice == '1':
                        ownership = float(input("📊 Ownership percentage: "))
                        result = self.advanced_governance.execute_corporate_action(
                            'takeover_notice', company, initiator, ownership_percentage=ownership
                        )
                        print(f"📋 Takeover notice filed: {result}")
                        
                    elif action_choice == '2':
                        nominees = input("👥 Board nominees (comma-separated): ").split(',')
                        rationale = input("📝 Rationale: ")
                        result = self.advanced_governance.execute_corporate_action(
                            'proxy_fight', company, initiator, 
                            board_nominees=[n.strip() for n in nominees], rationale=rationale
                        )
                        print(f"🗳️  Proxy fight initiated: {result}")
                        
                    elif action_choice == '3':
                        cause = input("⚖️  Cause of action: ")
                        damages = float(input("💰 Damages sought: "))
                        result = self.advanced_governance.execute_corporate_action(
                            'shareholder_lawsuit', company, initiator,
                            cause_of_action=cause, damages_sought=damages
                        )
                        print(f"⚖️  Shareholder lawsuit filed: {result}")
                else:
                    print("❌ Invalid inputs")
                    
            elif choice == '4':
                dashboard = self.advanced_governance.get_governance_dashboard()
                print("\n📊 Governance Dashboard:")
                print(f"  Monitoring Active: {'🟢 Yes' if dashboard.get('system_status', {}).get('governance_active') else '🔴 No'}")
                
                for company, data in dashboard.get('companies', {}).items():
                    print(f"\n📈 {company}:")
                    print(f"  Ownership: {data.get('ownership_percentage', 0):.4f}%")
                    print(f"  Total Documents: {data.get('total_documents', 0)}")
                    print(f"  Active Alerts: {len(data.get('active_alerts', []))}")
                    print(f"  Critical Alerts: {data.get('critical_alerts', 0)}")
                    
            elif choice == '5':
                company = input("📈 Enter company symbol (GOOGL/MSFT/CMCSA): ").strip().upper()
                notification_type = input("📝 Notification type: ").strip()
                message = input("💌 Message: ").strip()
                urgency = input("🚨 Urgency (NORMAL/HIGH/CRITICAL): ").strip().upper()
                
                if company in ['GOOGL', 'MSFT', 'CMCSA']:
                    success = self.advanced_governance.notification_system.send_board_notification(
                        company, notification_type, message, urgency
                    )
                    print(f"🔔 Notification sent: {'✅ Success' if success else '❌ Failed'}")
                else:
                    print("❌ Invalid company symbol")
                    
        except Exception as e:
            print(f"❌ Error in governance system: {e}")
            logging.error(f"Governance CLI error: {e}")

    def advanced_tracking_cli(self):
        """Advanced real-time tracking interface"""
        print("\n📊 Advanced Real-Time Tracking System")
        print("="*50)
        
        print("1. 🚀 Start Real-Time Tracking")
        print("2. 🛑 Stop Real-Time Tracking")
        print("3. 📊 Tracking Dashboard")
        print("4. 📈 Event History")
        print("5. 🚨 Alert Status")
        print("6. ⚙️  Add Custom Rule")
        print("7. 🔙 Back to Main Menu")
        
        choice = input("\n🎯 Enter choice: ").strip()
        
        try:
            if choice == '1':
                self.advanced_tracker.start_tracking()
                print("🚀 Advanced real-time tracking started!")
                
            elif choice == '2':
                self.advanced_tracker.stop_tracking()
                print("🛑 Advanced real-time tracking stopped")
                
            elif choice == '3':
                dashboard = self.advanced_tracker.get_tracking_dashboard()
                print("\n📊 Real-Time Tracking Dashboard:")
                
                status = dashboard.get('system_status', {})
                print(f"  Tracking Active: {'🟢 Yes' if status.get('tracking_active') else '🔴 No'}")
                
                components = status.get('components', {})
                print("  Components:")
                print(f"    Market Streaming: {'🟢' if components.get('market_streaming') else '🔴'}")
                print(f"    Blockchain Monitoring: {'🟢' if components.get('blockchain_monitoring') else '🔴'}")
                print(f"    Governance Monitoring: {'🟢' if components.get('governance_monitoring') else '🔴'}")
                
                print(f"\n📊 24-Hour Summary:")
                print(f"  Total Events: {dashboard.get('total_events_24h', 0)}")
                print(f"  Total Alerts: {dashboard.get('total_alerts_24h', 0)}")
                print(f"  Critical Alerts: {dashboard.get('critical_alerts', 0)}")
                
                if dashboard.get('unresolved_alerts'):
                    print("\n🚨 Unresolved Alerts:")
                    for alert in dashboard['unresolved_alerts'][:5]:
                        print(f"    • {alert['title']} ({alert['severity']})")
                        
            elif choice == '4':
                hours = int(input("⏰ Hours to look back (default 24): ") or "24")
                event_type = input("📝 Event type filter (optional): ").strip() or None
                
                events = self.advanced_tracker.get_event_history(event_type, hours)
                print(f"\n📈 Event History ({len(events)} events):")
                
                for event in events[:10]:  # Show first 10 events
                    print(f"  • {event['timestamp']}: {event['event_type']} ({event['severity']})")
                    
        except Exception as e:
            print(f"❌ Error in tracking system: {e}")
            logging.error(f"Tracking CLI error: {e}")

    def system_status_cli(self):
        """Enhanced system status display"""
        print("\n📊 ADVANCED DATACOIN SYSTEM STATUS")
        print("="*80)
        
        # Core system status
        print("🔗 CORE BLOCKCHAIN:")
        print(f"  • Blocks: {len(self.blockchain.chain)}")
        print(f"  • Pending Transactions: {len(getattr(self.blockchain, 'pending_transactions', []))}")
        print(f"  • Mining Difficulty: {self.blockchain.difficulty}")
        
        # AI System Status
        print("\n🤖 AI SYSTEMS:")
        ai_summary = self.advanced_ai.get_ai_performance_summary()
        print(f"  • AI Models Trained: {ai_summary.get('ai_models_trained', 0)}/3")
        print(f"  • Trading Active: {'🟢 Yes' if ai_summary.get('trading_active') else '🔴 No'}")
        print(f"  • Total AI Decisions: {ai_summary.get('total_decisions', 0)}")
        
        # Governance Status
        print("\n⚖️  GOVERNANCE SYSTEMS:")
        gov_dashboard = self.advanced_governance.get_governance_dashboard()
        print(f"  • Monitoring Active: {'🟢 Yes' if gov_dashboard.get('system_status', {}).get('governance_active') else '🔴 No'}")
        
        total_alerts = sum(len(data.get('active_alerts', [])) for data in gov_dashboard.get('companies', {}).values())
        print(f"  • Active Compliance Alerts: {total_alerts}")
        
        # Tracking Status
        print("\n📊 TRACKING SYSTEMS:")
        track_dashboard = self.advanced_tracker.get_tracking_dashboard()
        track_status = track_dashboard.get('system_status', {})
        print(f"  • Real-Time Tracking: {'🟢 Yes' if track_status.get('tracking_active') else '🔴 No'}")
        print(f"  • Events (24h): {track_dashboard.get('total_events_24h', 0)}")
        print(f"  • Alerts (24h): {track_dashboard.get('total_alerts_24h', 0)}")
        
        # Portfolio Status
        print("\n💼 PORTFOLIO STATUS:")
        for company in ['GOOGL', 'MSFT', 'CMCSA']:
            shares = self.share_purchaser.get_current_holdings(company)
            print(f"  • {company}: {shares} shares")
        
        print("\n✅ System operational and ready for advanced trading operations!")
    
    def start_api_server(self, open_browser=False):
        """Start the FastAPI server"""
        print("🚀 Starting DataCoin API server...")
        
        if open_browser:
            # Start browser after short delay
            def open_browser_delayed():
                time.sleep(2)
                try:
                    webbrowser.open('http://localhost:8000')
                    webbrowser.open('http://localhost:8000/docs')  # API docs
                    # Open frontend
                    frontend_path = os.path.join(os.path.dirname(__file__), 'frontend', 'index.html')
                    if os.path.exists(frontend_path):
                        webbrowser.open(f'file://{os.path.abspath(frontend_path)}')
                except Exception as e:
                    print(f"⚠️ Could not open browser: {e}")
            
            threading.Thread(target=open_browser_delayed, daemon=True).start()
        
        # Configure uvicorn
        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=True
        )
        
        server = uvicorn.Server(config)
        server.run()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="DataCoin - A digital currency powered by internet data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py --demo                # Run demonstration
    python main.py --interactive        # Interactive CLI
    python main.py --api-only           # API server only
    python main.py --web                # Start with web interface
        """
    )
    
    parser.add_argument('--demo', action='store_true', help='Run demonstration scenario')
    parser.add_argument('--api-only', action='store_true', help='Start only the API server')
    parser.add_argument('--interactive', action='store_true', help='Start interactive CLI')
    parser.add_argument('--web', action='store_true', help='Open web interface after starting API')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help and start web interface
    if not any(vars(args).values()):
        args.web = True
    
    try:
        # Initialize system
        system = DataCoinSystem()
        
        if args.demo:
            print("\n🎭 Running DataCoin demonstration...")
            system.create_demo_scenario()
            
            print("\n🌐 Starting API server for further exploration...")
            print("📖 Visit http://localhost:8000/docs for API documentation")
            print("🖥️ Frontend available at frontend/index.html")
            system.start_api_server(open_browser=True)
            
        elif args.interactive:
            system.interactive_cli()
            
        elif args.api_only:
            system.start_api_server(open_browser=False)
            
        elif args.web:
            print("🌐 Starting DataCoin with web interface...")
            print("📖 API docs: http://localhost:8000/docs")
            print("🖥️ Web interface will open automatically")
            system.start_api_server(open_browser=True)
            
    except KeyboardInterrupt:
        print("\n👋 DataCoin system stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()