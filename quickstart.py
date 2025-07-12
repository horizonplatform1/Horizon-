#!/usr/bin/env python3
"""
DataCoin Quick Start Script

This script tests the basic functionality of the DataCoin system
and provides a quick demonstration of core features.
"""

import sys
import time
import traceback

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from blockchain.core import Blockchain, Transaction, Block
        print("✅ Blockchain core imported successfully")
        
        from wallet.wallet import Wallet, WalletManager
        print("✅ Wallet system imported successfully")
        
        from data_engine.data_converter import DataConverter
        print("✅ Data engine imported successfully")
        
        from api.main import app
        print("✅ API module imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try: pip install -r requirements.txt")
        return False

def test_blockchain():
    """Test basic blockchain functionality"""
    print("\n🔗 Testing blockchain...")
    
    try:
        from blockchain.core import Blockchain, Transaction
        
        # Create blockchain
        blockchain = Blockchain()
        print(f"✅ Blockchain created with {len(blockchain.chain)} block(s)")
        
        # Test transaction
        tx = Transaction("alice", "bob", 1.0)
        print(f"✅ Transaction created: {tx.tx_id[:16]}...")
        
        # Add transaction
        blockchain.add_transaction(tx)
        print(f"✅ Transaction added to pending pool")
        
        # Test validation
        is_valid = blockchain.is_chain_valid()
        print(f"✅ Blockchain validation: {is_valid}")
        
        return True
    except Exception as e:
        print(f"❌ Blockchain test failed: {e}")
        traceback.print_exc()
        return False

def test_wallet():
    """Test wallet functionality"""
    print("\n💼 Testing wallet system...")
    
    try:
        from wallet.wallet import WalletManager
        from blockchain.core import Blockchain
        
        # Create wallet manager and blockchain
        wallet_manager = WalletManager()
        blockchain = Blockchain()
        
        # Create test wallet
        wallet = wallet_manager.create_wallet("test_wallet")
        wallet.connect_to_blockchain(blockchain)
        
        print(f"✅ Wallet created: {wallet.address[:20]}...")
        print(f"✅ Initial balance: {wallet.get_balance()} DataCoins")
        
        return True
    except Exception as e:
        print(f"❌ Wallet test failed: {e}")
        traceback.print_exc()
        return False

def test_data_conversion():
    """Test data conversion functionality"""
    print("\n🌐 Testing data conversion...")
    
    try:
        from data_engine.data_converter import DataConverter
        from blockchain.core import Blockchain
        
        # Create components
        blockchain = Blockchain()
        data_converter = DataConverter(blockchain)
        
        print(f"✅ Data converter created with {len(data_converter.sources)} sources")
        
        # Test conversion stats
        stats = data_converter.get_conversion_stats()
        print(f"✅ Conversion stats retrieved: {stats['total_sources']} sources")
        
        return True
    except Exception as e:
        print(f"❌ Data conversion test failed: {e}")
        traceback.print_exc()
        return False

def test_complete_flow():
    """Test a complete DataCoin flow"""
    print("\n🚀 Testing complete DataCoin flow...")
    
    try:
        from blockchain.core import Blockchain
        from wallet.wallet import WalletManager
        from data_engine.data_converter import DataConverter
        
        # Initialize system
        blockchain = Blockchain()
        wallet_manager = WalletManager()
        data_converter = DataConverter(blockchain)
        
        # Create wallets
        alice = wallet_manager.create_wallet("alice_test")
        bob = wallet_manager.create_wallet("bob_test")
        miner = wallet_manager.create_wallet("miner_test")
        
        # Connect to blockchain
        alice.connect_to_blockchain(blockchain)
        bob.connect_to_blockchain(blockchain)
        miner.connect_to_blockchain(blockchain)
        
        print(f"✅ Created wallets: Alice, Bob, Miner")
        
        # Simulate data conversion
        alice.convert_data_to_currency(2.0)  # 2 MB
        print(f"✅ Alice converted 2 MB to DataCoins")
        
        # Mine a block
        miner.mine_block()
        print(f"✅ Miner mined a block")
        
        # Check balances
        alice_balance = alice.get_balance()
        miner_balance = miner.get_balance()
        
        print(f"✅ Alice balance: {alice_balance:.6f} DC")
        print(f"✅ Miner balance: {miner_balance:.6f} DC")
        
        # Create transaction
        if alice_balance > 0.001:
            alice.create_transaction(bob.address, 0.001)
            print(f"✅ Alice sent 0.001 DC to Bob")
            
            # Mine another block
            miner.mine_block()
            print(f"✅ Transaction mined in new block")
            
            # Final balances
            print(f"✅ Final balances:")
            print(f"   Alice: {alice.get_balance():.6f} DC")
            print(f"   Bob: {bob.get_balance():.6f} DC")
            print(f"   Miner: {miner.get_balance():.6f} DC")
        
        # Show blockchain stats
        stats = blockchain.get_blockchain_stats()
        print(f"✅ Blockchain: {stats['total_blocks']} blocks, {stats['total_transactions']} transactions")
        
        return True
    except Exception as e:
        print(f"❌ Complete flow test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🪙 DataCoin Quick Start Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Blockchain", test_blockchain),
        ("Wallet", test_wallet),
        ("Data Conversion", test_data_conversion),
        ("Complete Flow", test_complete_flow),
    ]
    
    passed = 0
    failed = 0
    
    start_time = time.time()
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} test encountered an error: {e}")
            failed += 1
    
    end_time = time.time()
    
    print("\n" + "=" * 50)
    print(f"🏁 Test Results:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   ⏱️ Total time: {end_time - start_time:.2f} seconds")
    
    if failed == 0:
        print("\n🎉 All tests passed! DataCoin is ready to use.")
        print("\n💡 Next steps:")
        print("   1. Run 'python main.py --demo' for a demonstration")
        print("   2. Run 'python main.py --web' to start the web interface")
        print("   3. Run 'python main.py --interactive' for CLI mode")
        print("   4. Visit http://localhost:8000/docs for API documentation")
        return 0
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please check the errors above.")
        print("\n💡 Common solutions:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Check Python version: python --version (requires 3.8+)")
        print("   3. Ensure all files are in place")
        return 1

if __name__ == "__main__":
    sys.exit(main())