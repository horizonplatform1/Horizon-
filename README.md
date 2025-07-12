# 🪙 DataCoin - Digital Currency Powered by Internet Data

**DataCoin** is a revolutionary digital currency system that converts internet data into cryptocurrency. It features a complete blockchain implementation, secure wallet management, automated data collection, and corporate governance mechanisms for mining regulation.

## 🌟 Key Features

### 🔗 Blockchain Technology
- **Proof-of-Work Mining**: Secure consensus mechanism with adjustable difficulty
- **Transaction Processing**: Support for transfers, data conversions, and corporate shares
- **Immutable Ledger**: Cryptographically secure blockchain with SHA-256 hashing
- **Real-time Validation**: Automatic blockchain integrity checking

### 💼 Wallet System  
- **RSA Encryption**: 2048-bit key pairs for maximum security
- **Multiple Wallets**: Create and manage unlimited wallets
- **Transaction History**: Complete audit trail with SQLite storage
- **Balance Management**: Real-time balance calculation and updates

### 🌐 Data-to-Currency Conversion
- **Internet Data Mining**: Automatically collect data from web sources and APIs
- **Smart Valuation**: Quality-based currency conversion with multiple factors
- **Multiple Sources**: Support for web pages, APIs, RSS feeds, and social media
- **Automated Collection**: Scheduled data harvesting with configurable intervals

### 🏢 Corporate Regulation
- **Share-based Governance**: Purchase shares of Google, Microsoft, and NBC Universal
- **Mining Difficulty Control**: Share ownership influences mining parameters
- **Economic Balance**: Corporate control vs. decentralized mining incentives

### 🌐 Modern Interfaces
- **RESTful API**: Complete FastAPI implementation with OpenAPI documentation
- **Web Dashboard**: Beautiful, responsive web interface for all operations
- **Command Line**: Interactive CLI for power users and automation
- **Real-time Updates**: Live data refresh and notifications

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection (for data collection)
- 2GB RAM minimum
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/datacoin.git
   cd datacoin
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start DataCoin**
   ```bash
   python main.py
   ```
   
   This will automatically open your web browser with the DataCoin interface.

### Alternative Launch Options

```bash
# Run demonstration scenario
python main.py --demo

# Interactive command-line interface
python main.py --interactive

# API server only (no web interface)
python main.py --api-only

# Web interface (default)
python main.py --web
```

## 📖 Usage Guide

### 1. Creating Your First Wallet

**Via Web Interface:**
1. Open the DataCoin web interface
2. Navigate to "Wallet Management"
3. Enter a wallet name and click "Create Wallet"
4. Your wallet address and balance will be displayed

**Via CLI:**
```bash
DataCoin> create wallet my-wallet
✅ Wallet 'my-wallet' created with address: DC7a8f9b2c3d4e5f6789012345678901
```

### 2. Converting Data to Currency

**Automatic Data Collection:**
1. Select your wallet in the "Data Conversion" section
2. Click "Start Auto Conversion" to begin collecting data from configured sources
3. Data will be automatically converted to DataCoins based on quality and size

**Manual Data Conversion:**
1. Enter the amount of data (in MB) you want to convert
2. Click "Convert Data Manually"
3. DataCoins will be added to your wallet

### 3. Mining DataCoins

**Single Block Mining:**
1. Select a wallet for mining in the "Mining Control" section
2. Click "Mine One Block" to mine pending transactions
3. Receive mining rewards in your wallet

**Continuous Mining:**
1. Select your mining wallet
2. Click "Start Mining" to begin automatic block mining
3. Stop anytime with "Stop Mining"

### 4. Sending Transactions

1. Load your wallet in the "Wallet Management" section
2. Enter the recipient's wallet address
3. Specify the amount to send
4. Click "Send DataCoins"

### 5. Corporate Governance

1. Purchase shares of major corporations to influence mining
2. Higher share ownership can reduce mining difficulty
3. Create economic incentives and regulation mechanisms

## 🔧 API Documentation

DataCoin provides a comprehensive RESTful API. Once running, visit:
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

### Key Endpoints

```bash
# System Status
GET /system/health
GET /blockchain/stats

# Wallet Operations
POST /wallets/create
GET /wallets/{wallet_name}
POST /wallets/{wallet_name}/transaction

# Mining
POST /mining/start/{wallet_name}
POST /mining/mine/{wallet_name}
GET /mining/status

# Data Conversion
POST /data/convert/{wallet_name}
GET /data/sources
POST /data/auto-convert/start/{wallet_name}

# Corporate Shares
POST /wallets/{wallet_name}/shares
GET /corporate/shares
```

## 📁 Project Structure

```
datacoin/
├── blockchain/
│   └── core.py              # Blockchain implementation
├── wallet/
│   ├── wallet.py            # Wallet management
│   └── data/               # Wallet storage
├── data_engine/
│   └── data_converter.py    # Data collection and conversion
├── api/
│   └── main.py             # FastAPI server
├── frontend/
│   └── index.html          # Web interface
├── main.py                 # Main application
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🧪 Technical Details

### Blockchain Architecture
- **Block Structure**: Index, transactions, timestamp, nonce, hash, previous hash
- **Transaction Types**: Transfer, data conversion, mining reward, corporate shares
- **Proof of Work**: SHA-256 based with configurable difficulty
- **Consensus**: Longest valid chain rule

### Security Features
- **RSA 2048-bit**: Industry-standard encryption for wallet keys
- **SHA-256 Hashing**: Cryptographic security for all block hashes
- **Transaction Validation**: Multi-layer validation before block inclusion
- **SQLite Storage**: ACID-compliant data persistence

### Data Conversion Algorithm
```python
# Base conversion rate
base_value = data_size_mb * 0.001  # 1 MB = 0.001 DataCoins

# Quality multipliers
quality_score = calculate_quality(metrics)  # Based on content analysis
source_multiplier = get_source_weight(source_type)  # API vs web content
time_bonus = calculate_freshness(timestamp)  # Recent data is more valuable

final_value = base_value * quality_score * source_multiplier * time_bonus
```

### Corporate Governance Model
- **Share Cost**: 1000 DataCoins per share
- **Difficulty Adjustment**: 
  - High corporate control (>1000 shares): Easier mining
  - Low corporate control (<100 shares): Harder mining
- **Companies**: Google, Microsoft, NBC Universal

## 🎯 Example Scenarios

### Scenario 1: Basic Usage
```bash
# Create wallet
python main.py --interactive
DataCoin> create wallet alice
DataCoin> convert data
Data size (MB): 5.0
✅ Converted 5.0 MB to 0.005000 DataCoins

# Mine blocks
DataCoin> mine
⛏️ Mining block... (this may take a moment)
✅ Block mined successfully! Reward: 10 DC
```

### Scenario 2: Corporate Influence
```python
# Buy shares to influence mining
wallet.buy_corporate_shares("Google", 50)  # 50,000 DataCoins
blockchain.adjust_mining_difficulty()       # Easier mining due to corporate control
```

### Scenario 3: Automated Data Collection
```python
# Set up automatic data conversion
data_converter.start_auto_conversion("wallet_address", interval_minutes=30)
# System automatically collects data every 30 minutes
```

## 🔬 Advanced Configuration

### Custom Data Sources
```python
# Add custom data source
data_converter.add_data_source(
    source_id="custom_api",
    source_type="api",
    url="https://api.example.com/data",
    weight=1.5  # Higher value = more DataCoins
)
```

### Mining Difficulty
```python
# Manual difficulty adjustment
blockchain.difficulty = 6  # Higher = harder mining
blockchain.adjust_mining_difficulty()  # Based on corporate shares
```

### Conversion Rates
```python
# Modify conversion parameters
data_converter.calculator.base_rate = 0.002  # 1 MB = 0.002 DC
data_converter.calculator.quality_multipliers['high'] = 3.0  # High quality bonus
```

## 🐛 Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
pip install -r requirements.txt
python -m pip install --upgrade pip
```

**2. Port 8000 already in use**
```bash
# Kill existing process
sudo lsof -t -i:8000 | xargs kill -9

# Or use different port
uvicorn api.main:app --port 8001
```

**3. Data collection failures**
- Check internet connection
- Verify data source URLs are accessible
- Some sources may block automated requests

**4. Slow mining**
- Lower difficulty: `blockchain.difficulty = 2`
- Use faster hardware
- Mining is intentionally CPU-intensive for security

### Performance Optimization

**For Large Scale:**
- Use PostgreSQL instead of SQLite for wallets
- Implement Redis caching for API responses
- Deploy with Docker and load balancers
- Use dedicated mining nodes

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit: `git commit -am 'Add feature'`
5. Push: `git push origin feature-name`
6. Create a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black . && isort .

# Type checking
mypy .
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Satoshi Nakamoto** - For the original Bitcoin blockchain concept
- **FastAPI Team** - For the excellent web framework
- **Python Cryptography** - For secure encryption implementations
- **Open Source Community** - For the foundational libraries

## 📞 Support

- **Documentation**: http://localhost:8000/docs (when running)
- **Issues**: Create a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas

## 🔮 Roadmap

### Version 2.0 (Planned)
- [ ] WebSocket support for real-time updates
- [ ] Mobile app with React Native
- [ ] Machine learning for data quality assessment
- [ ] Multi-node network support
- [ ] Smart contracts functionality

### Version 3.0 (Future)
- [ ] Quantum-resistant encryption
- [ ] Cross-chain compatibility
- [ ] AI-powered data source discovery
- [ ] Governance token integration
- [ ] Professional exchange integration

---

**DataCoin** - *Converting the internet into currency, one byte at a time.* 🌐💰

Made with ❤️ by the DataCoin Team