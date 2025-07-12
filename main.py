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
from api.main import app
import uvicorn

class DataCoinSystem:
    """Main DataCoin system controller"""
    
    def __init__(self):
        print("🪙 Initializing DataCoin System...")
        
        # Initialize core components
        self.blockchain = Blockchain()
        self.wallet_manager = WalletManager()
        self.data_converter = DataConverter(self.blockchain)
        
        # Setup default data sources
        for source_config in DEFAULT_DATA_SOURCES:
            self.data_converter.add_data_source(**source_config)
        
        print("✅ DataCoin system initialized successfully!")
    
    def create_demo_scenario(self):
        """Create a demonstration scenario with sample data"""
        print("\n🎭 Creating demonstration scenario...")
        
        # Create demo wallets
        alice_wallet = self.wallet_manager.create_wallet("alice")
        bob_wallet = self.wallet_manager.create_wallet("bob")
        miner_wallet = self.wallet_manager.create_wallet("miner")
        
        # Connect wallets to blockchain
        alice_wallet.connect_to_blockchain(self.blockchain)
        bob_wallet.connect_to_blockchain(self.blockchain)
        miner_wallet.connect_to_blockchain(self.blockchain)
        
        print(f"👤 Alice wallet: {alice_wallet.address}")
        print(f"👤 Bob wallet: {bob_wallet.address}")
        print(f"⛏️ Miner wallet: {miner_wallet.address}")
        
        # Simulate data conversion for Alice
        print("\n🌐 Simulating data conversion...")
        alice_wallet.convert_data_to_currency(5.0)  # 5 MB of data
        bob_wallet.convert_data_to_currency(3.5)    # 3.5 MB of data
        
        # Mine the first block
        print("\n⛏️ Mining first block...")
        miner_wallet.mine_block()
        
        # Create some transactions
        print("\n💸 Creating transactions...")
        alice_wallet.create_transaction(bob_wallet.address, 0.001, "transfer")
        bob_wallet.create_transaction(alice_wallet.address, 0.0005, "transfer")
        
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
        
        # Corporate shares demonstration
        print("\n🏢 Demonstrating corporate shares...")
        alice_wallet.buy_corporate_shares("Google", 1)
        
        # Final mining and balance check
        print("\n⛏️ Final mining...")
        miner_wallet.mine_block()
        
        # Display final balances
        print("\n💰 Final Balances:")
        print(f"Alice: {alice_wallet.get_balance():.6f} DataCoins")
        print(f"Bob: {bob_wallet.get_balance():.6f} DataCoins")
        print(f"Miner: {miner_wallet.get_balance():.6f} DataCoins")
        
        # Display blockchain stats
        stats = self.blockchain.get_blockchain_stats()
        print(f"\n📊 Blockchain Statistics:")
        print(f"Total Blocks: {stats['total_blocks']}")
        print(f"Total Transactions: {stats['total_transactions']}")
        print(f"Mining Difficulty: {stats['current_difficulty']}")
        print(f"Data Converted: {stats['total_data_converted_mb']:.3f} MB")
        print(f"Corporate Shares: {stats['corporate_shares']}")
        
        return alice_wallet, bob_wallet, miner_wallet
    
    def interactive_cli(self):
        """Interactive command-line interface"""
        print("\n🖥️ DataCoin Interactive CLI")
        print("Type 'help' for available commands or 'exit' to quit")
        
        current_wallet = None
        
        while True:
            try:
                command = input("\nDataCoin> ").strip().lower()
                
                if command == 'exit' or command == 'quit':
                    break
                elif command == 'help':
                    self.show_help()
                elif command == 'status':
                    self.show_system_status()
                elif command.startswith('create wallet'):
                    wallet_name = command.split(' ', 2)[2] if len(command.split(' ', 2)) > 2 else input("Wallet name: ")
                    current_wallet = self.create_wallet_cli(wallet_name)
                elif command == 'list wallets':
                    self.list_wallets_cli()
                elif command.startswith('load wallet'):
                    wallet_name = command.split(' ', 2)[2] if len(command.split(' ', 2)) > 2 else input("Wallet name: ")
                    current_wallet = self.load_wallet_cli(wallet_name)
                elif command == 'balance':
                    if current_wallet:
                        print(f"Balance: {current_wallet.get_balance():.6f} DataCoins")
                    else:
                        print("❌ No wallet loaded")
                elif command == 'mine':
                    if current_wallet:
                        self.mine_block_cli(current_wallet)
                    else:
                        print("❌ No wallet loaded")
                elif command.startswith('send'):
                    if current_wallet:
                        self.send_transaction_cli(current_wallet)
                    else:
                        print("❌ No wallet loaded")
                elif command == 'convert data':
                    if current_wallet:
                        self.convert_data_cli(current_wallet)
                    else:
                        print("❌ No wallet loaded")
                elif command == 'collect data':
                    if current_wallet:
                        self.collect_data_cli(current_wallet)
                    else:
                        print("❌ No wallet loaded")
                elif command == 'buy shares':
                    if current_wallet:
                        self.buy_shares_cli(current_wallet)
                    else:
                        print("❌ No wallet loaded")
                elif command == 'blockchain':
                    self.show_blockchain_cli()
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n👋 Goodbye!")
    
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