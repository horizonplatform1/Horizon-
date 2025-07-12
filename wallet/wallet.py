import hashlib
import json
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from typing import Dict, List, Optional
import base64
import sqlite3
from datetime import datetime

from blockchain.core import Transaction, Blockchain

class Wallet:
    def __init__(self, wallet_name: str = None):
        self.wallet_name = wallet_name or f"wallet_{int(datetime.now().timestamp())}"
        self.private_key = None
        self.public_key = None
        self.address = None
        self.transactions_history: List[Dict] = []
        self.blockchain: Optional[Blockchain] = None
        
        # Initialize wallet database
        self.db_path = f"wallet/data/{self.wallet_name}.db"
        self._ensure_directory()
        self._init_database()
        
        # Generate keys if new wallet
        if not self._load_existing_wallet():
            self._generate_keys()
            self._save_wallet()
    
    def _ensure_directory(self):
        """Ensure wallet data directory exists"""
        os.makedirs("wallet/data", exist_ok=True)
    
    def _init_database(self):
        """Initialize wallet database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tx_id TEXT UNIQUE,
                sender TEXT,
                recipient TEXT,
                amount REAL,
                data_value REAL,
                tx_type TEXT,
                timestamp REAL,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallet_info (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _generate_keys(self):
        """Generate RSA key pair for wallet"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        
        # Generate wallet address from public key
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Create address hash
        address_hash = hashlib.sha256(public_pem).hexdigest()
        self.address = f"DC{address_hash[:32]}"  # DC prefix for DataCoin
    
    def _save_wallet(self):
        """Save wallet to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Serialize keys
        private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Save wallet info
        wallet_data = [
            ('wallet_name', self.wallet_name),
            ('address', self.address),
            ('private_key', base64.b64encode(private_pem).decode()),
            ('public_key', base64.b64encode(public_pem).decode())
        ]
        
        cursor.executemany(
            'INSERT OR REPLACE INTO wallet_info (key, value) VALUES (?, ?)',
            wallet_data
        )
        
        conn.commit()
        conn.close()
    
    def _load_existing_wallet(self) -> bool:
        """Load existing wallet from database"""
        if not os.path.exists(self.db_path):
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT key, value FROM wallet_info')
        wallet_data = dict(cursor.fetchall())
        
        if 'private_key' not in wallet_data:
            conn.close()
            return False
        
        # Load keys
        try:
            private_pem = base64.b64decode(wallet_data['private_key'])
            self.private_key = serialization.load_pem_private_key(
                private_pem, password=None, backend=default_backend()
            )
            
            public_pem = base64.b64decode(wallet_data['public_key'])
            self.public_key = serialization.load_pem_public_key(
                public_pem, backend=default_backend()
            )
            
            self.address = wallet_data['address']
            self.wallet_name = wallet_data['wallet_name']
            
            conn.close()
            return True
        except Exception as e:
            print(f"Error loading wallet: {e}")
            conn.close()
            return False
    
    def connect_to_blockchain(self, blockchain: Blockchain):
        """Connect wallet to blockchain network"""
        self.blockchain = blockchain
    
    def get_balance(self) -> float:
        """Get current wallet balance"""
        if not self.blockchain:
            return 0.0
        return self.blockchain.get_balance(self.address)
    
    def create_transaction(self, recipient: str, amount: float, tx_type: str = "transfer") -> Optional[Transaction]:
        """Create a new transaction"""
        if not self.blockchain:
            print("Wallet not connected to blockchain")
            return None
        
        # Check balance
        if self.get_balance() < amount:
            print(f"Insufficient balance. Current: {self.get_balance()}, Required: {amount}")
            return None
        
        # Create transaction
        transaction = Transaction(
            sender=self.address,
            recipient=recipient,
            amount=amount,
            tx_type=tx_type
        )
        
        # Add to blockchain
        if self.blockchain.add_transaction(transaction):
            self._record_transaction(transaction)
            return transaction
        else:
            print("Failed to add transaction to blockchain")
            return None
    
    def _record_transaction(self, transaction: Transaction):
        """Record transaction in wallet database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO transactions 
            (tx_id, sender, recipient, amount, data_value, tx_type, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            transaction.tx_id,
            transaction.sender,
            transaction.recipient,
            transaction.amount,
            transaction.data_value,
            transaction.tx_type,
            transaction.timestamp
        ))
        
        conn.commit()
        conn.close()
    
    def get_transaction_history(self) -> List[Dict]:
        """Get transaction history for this wallet"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT tx_id, sender, recipient, amount, data_value, tx_type, timestamp, status
            FROM transactions
            ORDER BY timestamp DESC
        ''')
        
        transactions = []
        for row in cursor.fetchall():
            transactions.append({
                'tx_id': row[0],
                'sender': row[1],
                'recipient': row[2],
                'amount': row[3],
                'data_value': row[4],
                'tx_type': row[5],
                'timestamp': row[6],
                'status': row[7]
            })
        
        conn.close()
        return transactions
    
    def mine_block(self) -> bool:
        """Mine a new block and receive reward"""
        if not self.blockchain:
            print("Wallet not connected to blockchain")
            return False
        
        try:
            print(f"Mining block for wallet {self.address}...")
            new_block = self.blockchain.mine_pending_transactions(self.address)
            print(f"Successfully mined block {new_block.index}!")
            return True
        except Exception as e:
            print(f"Mining failed: {e}")
            return False
    
    def convert_data_to_currency(self, data_size_mb: float) -> Optional[Transaction]:
        """Convert internet data to digital currency"""
        if not self.blockchain:
            print("Wallet not connected to blockchain")
            return None
        
        transaction = self.blockchain.convert_data_to_currency(data_size_mb, self.address)
        if transaction:
            self._record_transaction(transaction)
            print(f"Converted {data_size_mb} MB to {transaction.amount} DataCoins")
        return transaction
    
    def buy_corporate_shares(self, company: str, shares: int) -> bool:
        """Buy corporate shares to influence mining regulation"""
        if not self.blockchain:
            print("Wallet not connected to blockchain")
            return False
        
        success = self.blockchain.buy_corporate_shares(company, shares, self.address)
        if success:
            print(f"Successfully purchased {shares} shares of {company}")
        else:
            print(f"Failed to purchase shares of {company}")
        return success
    
    def export_wallet_data(self) -> Dict:
        """Export wallet data for backup"""
        return {
            'wallet_name': self.wallet_name,
            'address': self.address,
            'balance': self.get_balance(),
            'transaction_count': len(self.get_transaction_history())
        }
    
    def get_wallet_stats(self) -> Dict:
        """Get comprehensive wallet statistics"""
        transactions = self.get_transaction_history()
        
        total_sent = sum(tx['amount'] for tx in transactions if tx['sender'] == self.address)
        total_received = sum(tx['amount'] for tx in transactions if tx['recipient'] == self.address)
        data_converted = sum(tx['data_value'] for tx in transactions if tx['tx_type'] == 'data_conversion')
        
        return {
            'address': self.address,
            'balance': self.get_balance(),
            'total_transactions': len(transactions),
            'total_sent': total_sent,
            'total_received': total_received,
            'data_converted_mb': data_converted,
            'wallet_name': self.wallet_name
        }

class WalletManager:
    """Manage multiple wallets"""
    
    def __init__(self):
        self.wallets: Dict[str, Wallet] = {}
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Ensure wallet directory exists"""
        os.makedirs("wallet/data", exist_ok=True)
    
    def create_wallet(self, wallet_name: str) -> Wallet:
        """Create a new wallet"""
        if wallet_name in self.wallets:
            print(f"Wallet {wallet_name} already exists")
            return self.wallets[wallet_name]
        
        wallet = Wallet(wallet_name)
        self.wallets[wallet_name] = wallet
        print(f"Created new wallet: {wallet_name} with address: {wallet.address}")
        return wallet
    
    def load_wallet(self, wallet_name: str) -> Optional[Wallet]:
        """Load existing wallet"""
        if wallet_name in self.wallets:
            return self.wallets[wallet_name]
        
        try:
            wallet = Wallet(wallet_name)
            self.wallets[wallet_name] = wallet
            return wallet
        except Exception as e:
            print(f"Failed to load wallet {wallet_name}: {e}")
            return None
    
    def list_wallets(self) -> List[str]:
        """List all available wallets"""
        wallet_files = []
        data_dir = "wallet/data"
        
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.endswith('.db'):
                    wallet_files.append(file.replace('.db', ''))
        
        return wallet_files
    
    def get_wallet(self, wallet_name: str) -> Optional[Wallet]:
        """Get wallet by name"""
        return self.wallets.get(wallet_name)