#!/usr/bin/env python3
"""
DataCoin Android Edition
Mobile-optimized version for Android devices

Optimizations for Android:
- Lower mining difficulty
- Reduced memory usage
- Mobile-friendly data conversion rates
- Touch-optimized web interface
- Battery usage optimization
"""

import asyncio
import argparse
import time
import threading
import webbrowser
import sys
import os
import socket
from datetime import datetime
from contextlib import closing

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Android config if available
try:
    from android_config import get_android_config, is_android
    ANDROID_MODE = True
except ImportError:
    ANDROID_MODE = False
    def get_android_config():
        return {}
    def is_android():
        return False

from blockchain.core import Blockchain
from wallet.wallet import WalletManager
from data_engine.data_converter import DataConverter, DEFAULT_DATA_SOURCES
from api.main import app
import uvicorn

class DataCoinAndroidSystem:
    """Android-optimized DataCoin system controller"""
    
    def __init__(self):
        print("📱 Initializing DataCoin Android Edition...")
        
        # Get Android-specific configuration
        self.android_config = get_android_config()
        self.is_mobile = is_android()
        
        # Initialize core components with mobile optimizations
        self.blockchain = Blockchain()
        self.wallet_manager = WalletManager()
        self.data_converter = DataConverter(self.blockchain)
        
        # Apply mobile optimizations
        self._apply_mobile_optimizations()
        
        # Setup default data sources
        self._setup_data_sources()
        
        print("✅ DataCoin Android system initialized successfully!")
        if self.is_mobile:
            print("📱 Mobile optimizations applied")
    
    def _apply_mobile_optimizations(self):
        """Apply Android/mobile-specific optimizations"""
        
        # Reduce blockchain difficulty for mobile devices
        if self.is_mobile:
            self.blockchain.difficulty = self.android_config.get('mining_difficulty', 3)
        else:
            self.blockchain.difficulty = 3  # Default mobile-friendly difficulty
        
        # Optimize mining reward for mobile
        self.blockchain.mining_reward = 5  # Reduced from 10 for faster transactions
        
        # Adjust data conversion rate for mobile
        if hasattr(self.data_converter, 'calculator'):
            # More generous rates for mobile users
            self.data_converter.calculator.base_rate = 0.002  # Double the rate
            self.data_converter.calculator.quality_multipliers = {
                'high': 3.0,    # Increased from 2.0
                'medium': 1.5,  # Increased from 1.0
                'low': 0.8      # Increased from 0.5
            }
        
        print(f"⚙️ Mining difficulty set to: {self.blockchain.difficulty}")
        print(f"💰 Mining reward set to: {self.blockchain.mining_reward} DC")
        print(f"📊 Mobile-optimized conversion rates applied")
    
    def _setup_data_sources(self):
        """Setup mobile-friendly data sources"""
        # Add default sources with mobile-optimized weights
        mobile_sources = [
            {
                'source_id': 'mobile_news_api',
                'source_type': 'api',
                'url': 'https://jsonplaceholder.typicode.com/posts',
                'weight': 2.0  # Higher weight for mobile
            },
            {
                'source_id': 'mobile_github_api', 
                'source_type': 'api',
                'url': 'https://api.github.com/repositories',
                'weight': 2.5  # Higher weight for mobile
            },
            {
                'source_id': 'mobile_hackernews',
                'source_type': 'web',
                'url': 'https://news.ycombinator.com/',
                'weight': 1.8  # Higher weight for mobile
            }
        ]
        
        for source_config in mobile_sources:
            try:
                self.data_converter.add_data_source(**source_config)
            except Exception as e:
                print(f"⚠️ Could not add source {source_config['source_id']}: {e}")
    
    def find_free_port(self, start_port=8000):
        """Find a free port starting from start_port"""
        port = start_port
        while port < start_port + 100:  # Try 100 ports
            try:
                with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                port += 1
        return start_port  # Fallback
    
    def create_demo_scenario(self):
        """Create a mobile-optimized demonstration scenario"""
        print("\n📱 Creating mobile demo scenario...")
        
        # Create demo wallets
        alice_wallet = self.wallet_manager.create_wallet("mobile_alice")
        bob_wallet = self.wallet_manager.create_wallet("mobile_bob")
        miner_wallet = self.wallet_manager.create_wallet("mobile_miner")
        
        # Connect wallets to blockchain
        alice_wallet.connect_to_blockchain(self.blockchain)
        bob_wallet.connect_to_blockchain(self.blockchain)
        miner_wallet.connect_to_blockchain(self.blockchain)
        
        print(f"👤 Alice: {alice_wallet.address[:20]}...")
        print(f"👤 Bob: {bob_wallet.address[:20]}...")
        print(f"⛏️ Miner: {miner_wallet.address[:20]}...")
        
        # Quick data conversion (smaller amounts for mobile)
        print("\n🌐 Converting mobile data...")
        alice_wallet.convert_data_to_currency(1.0)  # 1 MB
        bob_wallet.convert_data_to_currency(0.5)    # 0.5 MB
        
        # Fast mobile mining
        print("\n⚡ Quick mobile mining...")
        miner_wallet.mine_block()
        
        # Mobile transaction
        print("\n💸 Mobile transaction...")
        alice_wallet.create_transaction(bob_wallet.address, 0.5, "mobile_transfer")
        
        # Final mobile mining
        print("\n⛏️ Final mobile mining...")
        miner_wallet.mine_block()
        
        # Display mobile-friendly stats
        stats = self.blockchain.get_blockchain_stats()
        print(f"\n📱 Mobile Demo Complete:")
        print(f"   Blocks: {stats['total_blocks']}")
        print(f"   Transactions: {stats['total_transactions']}")
        print(f"   Alice: {alice_wallet.get_balance():.3f} DC")
        print(f"   Bob: {bob_wallet.get_balance():.3f} DC")
        print(f"   Miner: {miner_wallet.get_balance():.3f} DC")
        
        return alice_wallet, bob_wallet, miner_wallet
    
    def start_mobile_server(self, host="0.0.0.0", port=None):
        """Start mobile-optimized API server"""
        
        if port is None:
            port = self.find_free_port()
        
        print(f"📱 Starting DataCoin mobile server...")
        print(f"🌐 Host: {host}")
        print(f"🔌 Port: {port}")
        print(f"📱 Mobile access: http://localhost:{port}")
        
        # Check for local network access
        try:
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(f"🔗 Network access: http://{local_ip}:{port}")
        except:
            print("🔗 Network access: Use device IP address")
        
        print(f"📖 API docs: http://localhost:{port}/docs")
        print(f"📱 PWA install: Open in Chrome and 'Add to Home Screen'")
        print()
        print("💡 Mobile tips:")
        print("   • Disable battery optimization for this app")
        print("   • Keep device connected to charger during mining")
        print("   • Use WiFi for better performance")
        print("   • Close other apps to free memory")
        print()
        print("🔴 Press Ctrl+C to stop server")
        print()
        
        # Configure uvicorn for mobile
        config = uvicorn.Config(
            app,
            host=host,
            port=port,
            log_level="warning",  # Reduce logs for mobile
            access_log=False,     # Disable access logs to save battery
            workers=1,            # Single worker for mobile
            reload=False          # Disable reload for stability
        )
        
        server = uvicorn.Server(config)
        server.run()

def show_mobile_help():
    """Show mobile-specific help"""
    print("""
📱 DataCoin Android Commands:
   --mobile-demo    Run mobile-optimized demonstration
   --mobile-server  Start mobile server (default)
   --quick-start    Fast setup for mobile devices
   --mobile-mine    Quick mining session
   --mobile-stats   Show mobile-friendly statistics
   --help           Show this help
   
📋 Mobile Setup:
   1. Install Termux from F-Droid
   2. Run: curl -sL [install-script] | bash
   3. Start: python android_main.py
   4. Open browser: http://localhost:[port]
   5. Add to home screen for app-like experience
   
⚡ Quick Commands:
   dc                    # Start DataCoin
   dc --mobile-demo      # Run demo
   dc --mobile-mine      # Mine blocks
   dc --mobile-stats     # View stats
    """)

def main():
    """Main entry point for Android DataCoin"""
    parser = argparse.ArgumentParser(
        description="DataCoin Android Edition - Mobile cryptocurrency system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
📱 Android Examples:
   python android_main.py                    # Start mobile server
   python android_main.py --mobile-demo      # Run demo
   python android_main.py --quick-start      # Fast setup
   python android_main.py --mobile-mine      # Quick mining
        """
    )
    
    parser.add_argument('--mobile-demo', action='store_true', help='Run mobile demonstration')
    parser.add_argument('--mobile-server', action='store_true', help='Start mobile server')
    parser.add_argument('--quick-start', action='store_true', help='Quick mobile setup')
    parser.add_argument('--mobile-mine', action='store_true', help='Quick mining session')
    parser.add_argument('--mobile-stats', action='store_true', help='Show mobile stats')
    parser.add_argument('--host', default='0.0.0.0', help='Server host (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, help='Server port (auto-detect if not specified)')
    
    args = parser.parse_args()
    
    # Show help if no arguments
    if not any(vars(args).values()):
        show_mobile_help()
        args.mobile_server = True
    
    try:
        # Initialize mobile system
        system = DataCoinAndroidSystem()
        
        if args.mobile_demo:
            print("\n📱 Running DataCoin mobile demonstration...")
            system.create_demo_scenario()
            print("\n🌐 Starting mobile server for exploration...")
            system.start_mobile_server(args.host, args.port)
            
        elif args.quick_start:
            print("\n⚡ DataCoin Quick Start for Mobile...")
            
            # Create a quick wallet
            wallet = system.wallet_manager.create_wallet("quick_mobile_wallet")
            wallet.connect_to_blockchain(system.blockchain)
            
            # Quick data conversion
            wallet.convert_data_to_currency(0.5)
            print(f"✅ Quick wallet created: {wallet.address[:20]}...")
            print(f"💰 Balance after data conversion: {wallet.get_balance():.6f} DC")
            
            # Start server
            system.start_mobile_server(args.host, args.port)
            
        elif args.mobile_mine:
            print("\n⛏️ Quick Mobile Mining Session...")
            
            # Create or load miner wallet
            wallet = system.wallet_manager.create_wallet("mobile_quick_miner")
            wallet.connect_to_blockchain(system.blockchain)
            
            # Add some transactions to mine
            wallet.convert_data_to_currency(1.0)
            
            # Mine a block
            print("🔄 Mining block... (mobile-optimized)")
            success = wallet.mine_block()
            
            if success:
                print(f"✅ Block mined successfully!")
                print(f"💰 New balance: {wallet.get_balance():.6f} DC")
            else:
                print("❌ Mining failed")
                
        elif args.mobile_stats:
            print("\n📊 DataCoin Mobile Statistics:")
            
            stats = system.blockchain.get_blockchain_stats()
            data_stats = system.data_converter.get_conversion_stats()
            
            print(f"""
📱 Mobile System Status:
   🔗 Blockchain Blocks: {stats['total_blocks']}
   💸 Total Transactions: {stats['total_transactions']}
   ⛏️ Mining Difficulty: {stats['current_difficulty']} (mobile-optimized)
   🌐 Data Converted: {stats['total_data_converted_mb']:.3f} MB
   📊 Data Sources: {data_stats['total_sources']}
   💰 Currency Generated: {data_stats['total_currency_generated']:.6f} DC
   🏢 Corporate Shares: {stats['corporate_shares']}
            """)
            
        else:
            # Default: start mobile server
            system.start_mobile_server(args.host, args.port)
            
    except KeyboardInterrupt:
        print("\n👋 DataCoin Android stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        if is_android():
            print("\n💡 Mobile troubleshooting:")
            print("   • Check internet connection")
            print("   • Restart Termux app")
            print("   • Free up device memory")
            print("   • Check battery optimization settings")
        sys.exit(1)

if __name__ == "__main__":
    main()