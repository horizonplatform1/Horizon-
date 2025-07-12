#!/data/data/com.termux/files/usr/bin/bash

# DataCoin Android Installation Script for Termux
# This script installs DataCoin on Android using Termux

echo "🪙 DataCoin Android Installer"
echo "=============================="
echo ""
echo "📱 Installing DataCoin on Android via Termux..."
echo ""

# Update Termux packages
echo "📦 Updating Termux packages..."
pkg update -y
pkg upgrade -y

# Install required packages
echo "🔧 Installing required packages..."
pkg install -y python python-pip git openssh openssl sqlite

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
pip install cryptography requests fastapi uvicorn beautifulsoup4 schedule numpy

# Create DataCoin directory
echo "📁 Setting up DataCoin directory..."
cd ~
mkdir -p datacoin
cd datacoin

# Download DataCoin files (in real scenario, this would clone from git)
echo "📥 Setting up DataCoin files..."

# Create a minimal requirements file for Android
cat > requirements.txt << 'EOF'
cryptography
requests
fastapi
uvicorn
beautifulsoup4
schedule
numpy
EOF

# Create Android-optimized main launcher
cat > android_launcher.py << 'EOF'
#!/usr/bin/env python3
"""
DataCoin Android Launcher
Optimized for Android/Termux environment
"""

import os
import sys
import signal
import threading
import time
import socket
from contextlib import closing

def find_free_port():
    """Find a free port for the server"""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def check_termux():
    """Check if running in Termux"""
    return 'com.termux' in os.environ.get('PREFIX', '')

def main():
    print("🪙 DataCoin Android Edition")
    print("==========================")
    print()
    
    if check_termux():
        print("📱 Running in Termux environment")
    else:
        print("⚠️  Not detected as Termux - some features may not work")
    
    print("🚀 Starting DataCoin system...")
    
    # Import main DataCoin system
    try:
        from main import DataCoinSystem
    except ImportError as e:
        print(f"❌ Error importing DataCoin: {e}")
        print("💡 Make sure all files are in place and dependencies installed")
        return 1
    
    # Initialize system
    try:
        system = DataCoinSystem()
        
        # Find free port
        port = find_free_port()
        print(f"🌐 Starting server on port {port}")
        print(f"📱 Access via: http://localhost:{port}")
        print(f"📖 API docs: http://localhost:{port}/docs")
        print()
        print("💡 To access from other devices on same network:")
        print(f"   Use your device IP instead of localhost")
        print()
        print("🔴 Press Ctrl+C to stop")
        print()
        
        # Start API server
        import uvicorn
        from api.main import app
        
        config = uvicorn.Config(
            app,
            host="0.0.0.0",  # Allow external connections
            port=port,
            log_level="info"
        )
        
        server = uvicorn.Server(config)
        server.run()
        
    except KeyboardInterrupt:
        print("\n👋 DataCoin stopped")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
EOF

chmod +x android_launcher.py

# Create Android-specific configuration
cat > android_config.py << 'EOF'
"""
Android-specific configuration for DataCoin
"""

import os
import tempfile

# Android/Termux specific paths
ANDROID_DATA_DIR = os.path.expanduser("~/datacoin_data")
ANDROID_TEMP_DIR = tempfile.gettempdir()

# Ensure data directory exists
os.makedirs(ANDROID_DATA_DIR, exist_ok=True)

# Android configuration
ANDROID_CONFIG = {
    'data_dir': ANDROID_DATA_DIR,
    'temp_dir': ANDROID_TEMP_DIR,
    'max_workers': 2,  # Limit workers on mobile
    'mining_difficulty': 3,  # Easier mining on mobile
    'auto_save_interval': 30,  # More frequent saves
    'mobile_optimized': True
}

def get_android_config():
    """Get Android-optimized configuration"""
    return ANDROID_CONFIG

def is_android():
    """Check if running on Android"""
    return 'com.termux' in os.environ.get('PREFIX', '') or \
           'ANDROID_ROOT' in os.environ or \
           'ANDROID_DATA' in os.environ
EOF

# Create startup script
cat > start_datacoin.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash

echo "🪙 Starting DataCoin on Android..."
echo ""

# Check if we're in the right directory
if [ ! -f "android_launcher.py" ]; then
    echo "❌ DataCoin files not found in current directory"
    echo "💡 Please cd to the datacoin directory first"
    exit 1
fi

# Check for Python
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install with: pkg install python"
    exit 1
fi

# Start DataCoin
echo "🚀 Launching DataCoin..."
python android_launcher.py
EOF

chmod +x start_datacoin.sh

# Create quick access script
cat > dc << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/datacoin && ./start_datacoin.sh
EOF

chmod +x dc

# Move quick access to PATH
mkdir -p ~/.local/bin
cp dc ~/.local/bin/
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

echo ""
echo "✅ DataCoin Android installation complete!"
echo ""
echo "🚀 To start DataCoin:"
echo "   cd ~/datacoin && ./start_datacoin.sh"
echo "   OR simply type: dc"
echo ""
echo "📱 First time setup:"
echo "   1. Open Termux"
echo "   2. Type 'dc' and press Enter"
echo "   3. Open browser and go to http://localhost:<port>"
echo "   4. Create your first wallet and start mining!"
echo ""
echo "💡 Tips for Android:"
echo "   • Keep Termux running in background"
echo "   • Use 'termux-wake-lock' to prevent sleep"
echo "   • Lower mining difficulty for better mobile performance"
echo ""
echo "🔗 Access from other devices:"
echo "   Find your Android IP and use http://<android-ip>:<port>"
echo ""
EOF