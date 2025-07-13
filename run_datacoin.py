#!/usr/bin/env python3
"""
Advanced DataCoin System Launcher
Quick startup script for the enhanced blockchain system
"""

import sys
import os

def main():
    print("🪙 " + "="*60)
    print("🪙 DATACOIN ADVANCED BLOCKCHAIN SYSTEM")
    print("🪙 " + "="*60)
    print()
    print("🚀 Features Available:")
    print("   🤖 Advanced AI Trading with Neural Networks")
    print("   ⚖️  Corporate Governance & Legal Actions")
    print("   📊 Real-Time Tracking & Monitoring")
    print("   💼 Portfolio Management & Analytics")
    print("   🌐 Web Dashboard & CLI Interface")
    print()
    
    print("📋 Startup Options:")
    print("   1. 🎮 Interactive CLI Mode")
    print("   2. 🌐 Web API Server")
    print("   3. 📊 Enhanced Dashboard")
    print("   4. 🎭 Demo Mode")
    print("   5. 🚪 Exit")
    print()
    
    choice = input("🎯 Select startup mode (1-5): ").strip()
    
    try:
        from main import DataCoinSystem
        system = DataCoinSystem()
        
        if choice == "1":
            print("🎮 Starting Interactive CLI...")
            system.interactive_cli()
        elif choice == "2":
            print("🌐 Starting Web API Server...")
            system.start_api_server(open_browser=True)
        elif choice == "3":
            print("📊 Starting Enhanced Dashboard...")
            print("ℹ️  Run: streamlit run blockchain/enhanced_dashboard.py")
        elif choice == "4":
            print("🎭 Running Demo Mode...")
            system.create_demo_scenario()
        elif choice == "5":
            print("👋 Goodbye!")
            return
        else:
            print("❌ Invalid choice")
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("ℹ️  Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ System Error: {e}")

if __name__ == "__main__":
    main()