from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import threading
import time

from blockchain.core import Blockchain, Transaction
from wallet.wallet import Wallet, WalletManager
from data_engine.data_converter import DataConverter, DEFAULT_DATA_SOURCES

# Pydantic models for API requests/responses
class TransactionCreate(BaseModel):
    recipient: str
    amount: float
    tx_type: str = "transfer"

class WalletCreate(BaseModel):
    wallet_name: str

class DataSourceCreate(BaseModel):
    source_id: str
    source_type: str
    url: str
    weight: float = 1.0

class SharePurchase(BaseModel):
    company: str
    shares: int

class DataConversion(BaseModel):
    data_size_mb: float

class TransactionResponse(BaseModel):
    tx_id: str
    sender: str
    recipient: str
    amount: float
    data_value: float
    tx_type: str
    timestamp: float

class WalletResponse(BaseModel):
    wallet_name: str
    address: str
    balance: float
    transaction_count: int

class BlockchainStats(BaseModel):
    total_blocks: int
    total_transactions: int
    current_difficulty: int
    total_data_converted_mb: float
    corporate_shares: Dict[str, int]
    pending_transactions: int

# Initialize the digital currency system
app = FastAPI(
    title="DataCoin API",
    description="RESTful API for DataCoin - A digital currency powered by internet data",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
blockchain = Blockchain()
wallet_manager = WalletManager()
data_converter = DataConverter(blockchain)

# Initialize default data sources
for source_config in DEFAULT_DATA_SOURCES:
    data_converter.add_data_source(**source_config)

# Background mining thread
mining_active = False
mining_thread = None

def background_mining():
    """Background mining process"""
    global mining_active
    while mining_active:
        try:
            # Get a default mining wallet
            mining_wallet = wallet_manager.create_wallet("system_miner")
            mining_wallet.connect_to_blockchain(blockchain)
            
            if len(blockchain.pending_transactions) > 0:
                mining_wallet.mine_block()
                time.sleep(30)  # Wait 30 seconds between mining attempts
            else:
                time.sleep(10)  # Wait 10 seconds if no pending transactions
        except Exception as e:
            print(f"Mining error: {e}")
            time.sleep(60)

# Blockchain endpoints
@app.get("/", response_model=Dict)
async def root():
    """Root endpoint with system information"""
    return {
        "name": "DataCoin API",
        "version": "1.0.0",
        "description": "A digital currency powered by internet data conversion",
        "features": [
            "Blockchain with proof-of-work mining",
            "Wallet management with RSA encryption", 
            "Internet data to currency conversion",
            "Corporate share-based mining regulation",
            "Real-time transaction processing"
        ],
        "endpoints": {
            "blockchain": "/blockchain/",
            "wallets": "/wallets/",
            "data_conversion": "/data/",
            "mining": "/mining/"
        }
    }

@app.get("/blockchain/stats", response_model=BlockchainStats)
async def get_blockchain_stats():
    """Get comprehensive blockchain statistics"""
    stats = blockchain.get_blockchain_stats()
    return BlockchainStats(**stats)

@app.get("/blockchain/blocks")
async def get_blocks(limit: int = 10):
    """Get recent blocks"""
    blocks = blockchain.chain[-limit:] if len(blockchain.chain) > limit else blockchain.chain
    return [block.to_dict() for block in blocks]

@app.get("/blockchain/block/{block_index}")
async def get_block(block_index: int):
    """Get specific block by index"""
    if block_index < 0 or block_index >= len(blockchain.chain):
        raise HTTPException(status_code=404, detail="Block not found")
    
    return blockchain.chain[block_index].to_dict()

@app.get("/blockchain/validate")
async def validate_blockchain():
    """Validate the entire blockchain"""
    is_valid = blockchain.is_chain_valid()
    return {"valid": is_valid}

@app.get("/blockchain/pending")
async def get_pending_transactions():
    """Get pending transactions"""
    return [tx.to_dict() for tx in blockchain.pending_transactions]

# Wallet endpoints
@app.post("/wallets/create", response_model=WalletResponse)
async def create_wallet(wallet_data: WalletCreate):
    """Create a new wallet"""
    wallet = wallet_manager.create_wallet(wallet_data.wallet_name)
    wallet.connect_to_blockchain(blockchain)
    
    return WalletResponse(
        wallet_name=wallet.wallet_name,
        address=wallet.address,
        balance=wallet.get_balance(),
        transaction_count=len(wallet.get_transaction_history())
    )

@app.get("/wallets", response_model=List[str])
async def list_wallets():
    """List all available wallets"""
    return wallet_manager.list_wallets()

@app.get("/wallets/{wallet_name}", response_model=WalletResponse)
async def get_wallet(wallet_name: str):
    """Get wallet information"""
    wallet = wallet_manager.load_wallet(wallet_name)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    wallet.connect_to_blockchain(blockchain)
    
    return WalletResponse(
        wallet_name=wallet.wallet_name,
        address=wallet.address,
        balance=wallet.get_balance(),
        transaction_count=len(wallet.get_transaction_history())
    )

@app.get("/wallets/{wallet_name}/balance")
async def get_wallet_balance(wallet_name: str):
    """Get wallet balance"""
    wallet = wallet_manager.load_wallet(wallet_name)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    wallet.connect_to_blockchain(blockchain)
    return {"balance": wallet.get_balance()}

@app.get("/wallets/{wallet_name}/transactions")
async def get_wallet_transactions(wallet_name: str):
    """Get wallet transaction history"""
    wallet = wallet_manager.load_wallet(wallet_name)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    return wallet.get_transaction_history()

@app.get("/wallets/{wallet_name}/stats")
async def get_wallet_stats(wallet_name: str):
    """Get comprehensive wallet statistics"""
    wallet = wallet_manager.load_wallet(wallet_name)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    wallet.connect_to_blockchain(blockchain)
    return wallet.get_wallet_stats()

@app.post("/wallets/{wallet_name}/transaction", response_model=TransactionResponse)
async def create_transaction(wallet_name: str, transaction_data: TransactionCreate):
    """Create a new transaction"""
    wallet = wallet_manager.load_wallet(wallet_name)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    wallet.connect_to_blockchain(blockchain)
    
    transaction = wallet.create_transaction(
        transaction_data.recipient,
        transaction_data.amount,
        transaction_data.tx_type
    )
    
    if not transaction:
        raise HTTPException(status_code=400, detail="Transaction failed")
    
    return TransactionResponse(**transaction.to_dict())

@app.post("/wallets/{wallet_name}/shares")
async def buy_corporate_shares(wallet_name: str, share_data: SharePurchase):
    """Buy corporate shares to influence mining regulation"""
    wallet = wallet_manager.load_wallet(wallet_name)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    wallet.connect_to_blockchain(blockchain)
    
    success = wallet.buy_corporate_shares(share_data.company, share_data.shares)
    
    if not success:
        raise HTTPException(status_code=400, detail="Share purchase failed")
    
    return {
        "success": True,
        "company": share_data.company,
        "shares": share_data.shares,
        "total_shares": blockchain.corporate_shares[share_data.company]
    }

# Mining endpoints
@app.post("/mining/start/{wallet_name}")
async def start_mining(wallet_name: str, background_tasks: BackgroundTasks):
    """Start mining with specified wallet"""
    global mining_active, mining_thread
    
    if mining_active:
        return {"message": "Mining already active"}
    
    wallet = wallet_manager.load_wallet(wallet_name)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    wallet.connect_to_blockchain(blockchain)
    
    mining_active = True
    mining_thread = threading.Thread(target=background_mining, daemon=True)
    mining_thread.start()
    
    return {"message": f"Mining started with wallet {wallet_name}"}

@app.post("/mining/stop")
async def stop_mining():
    """Stop mining process"""
    global mining_active
    
    mining_active = False
    return {"message": "Mining stopped"}

@app.get("/mining/status")
async def get_mining_status():
    """Get mining status"""
    return {
        "active": mining_active,
        "difficulty": blockchain.difficulty,
        "pending_transactions": len(blockchain.pending_transactions),
        "mining_reward": blockchain.mining_reward
    }

@app.post("/mining/mine/{wallet_name}")
async def mine_single_block(wallet_name: str):
    """Mine a single block"""
    wallet = wallet_manager.load_wallet(wallet_name)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    wallet.connect_to_blockchain(blockchain)
    
    if len(blockchain.pending_transactions) == 0:
        raise HTTPException(status_code=400, detail="No pending transactions to mine")
    
    success = wallet.mine_block()
    
    if not success:
        raise HTTPException(status_code=400, detail="Mining failed")
    
    return {
        "success": True,
        "block_index": len(blockchain.chain) - 1,
        "reward": blockchain.mining_reward
    }

# Data conversion endpoints
@app.get("/data/sources")
async def get_data_sources():
    """Get all data sources"""
    return data_converter.get_source_list()

@app.post("/data/sources")
async def add_data_source(source_data: DataSourceCreate):
    """Add a new data source"""
    success = data_converter.add_data_source(
        source_data.source_id,
        source_data.source_type,
        source_data.url,
        source_data.weight
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add data source")
    
    return {"success": True, "source_id": source_data.source_id}

@app.post("/data/convert/{wallet_name}")
async def convert_data_manual(wallet_name: str, conversion_data: DataConversion):
    """Manually convert data to currency"""
    wallet = wallet_manager.load_wallet(wallet_name)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    wallet.connect_to_blockchain(blockchain)
    
    transaction = wallet.convert_data_to_currency(conversion_data.data_size_mb)
    
    if not transaction:
        raise HTTPException(status_code=400, detail="Data conversion failed")
    
    return TransactionResponse(**transaction.to_dict())

@app.post("/data/collect/{source_id}/{wallet_name}")
async def collect_from_source(source_id: str, wallet_name: str):
    """Collect data from specific source and convert to currency"""
    wallet = wallet_manager.load_wallet(wallet_name)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    wallet.connect_to_blockchain(blockchain)
    
    transaction = data_converter.collect_and_convert(source_id, wallet.address)
    
    if not transaction:
        raise HTTPException(status_code=400, detail="Data collection failed")
    
    return TransactionResponse(**transaction.to_dict())

@app.post("/data/auto-convert/start/{wallet_name}")
async def start_auto_conversion(wallet_name: str, interval_minutes: int = 60):
    """Start automatic data conversion"""
    wallet = wallet_manager.load_wallet(wallet_name)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    data_converter.start_auto_conversion(wallet.address, interval_minutes)
    
    return {
        "message": f"Auto conversion started for wallet {wallet_name}",
        "interval_minutes": interval_minutes
    }

@app.post("/data/auto-convert/stop")
async def stop_auto_conversion():
    """Stop automatic data conversion"""
    data_converter.stop_auto_conversion()
    return {"message": "Auto conversion stopped"}

@app.get("/data/stats")
async def get_conversion_stats():
    """Get data conversion statistics"""
    return data_converter.get_conversion_stats()

# Corporate regulation endpoints
@app.get("/corporate/shares")
async def get_corporate_shares():
    """Get current corporate share ownership"""
    return blockchain.corporate_shares

@app.post("/corporate/adjust-difficulty")
async def adjust_mining_difficulty():
    """Manually adjust mining difficulty based on corporate shares"""
    old_difficulty = blockchain.difficulty
    blockchain.adjust_mining_difficulty()
    new_difficulty = blockchain.difficulty
    
    return {
        "old_difficulty": old_difficulty,
        "new_difficulty": new_difficulty,
        "corporate_shares": blockchain.corporate_shares
    }

# System control endpoints
@app.post("/system/reset")
async def reset_system():
    """Reset the entire system (for development/testing)"""
    global blockchain, data_converter, mining_active
    
    # Stop any running processes
    mining_active = False
    data_converter.stop_auto_conversion()
    
    # Recreate blockchain
    blockchain = Blockchain()
    data_converter = DataConverter(blockchain)
    
    # Re-add default data sources
    for source_config in DEFAULT_DATA_SOURCES:
        data_converter.add_data_source(**source_config)
    
    return {"message": "System reset successfully"}

@app.get("/system/health")
async def health_check():
    """System health check"""
    return {
        "status": "healthy",
        "blockchain_valid": blockchain.is_chain_valid(),
        "total_blocks": len(blockchain.chain),
        "total_wallets": len(wallet_manager.list_wallets()),
        "data_sources": len(data_converter.sources),
        "mining_active": mining_active,
        "auto_conversion_active": data_converter.is_running
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)