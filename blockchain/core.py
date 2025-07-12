import hashlib
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import threading

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, data_value: float = 0, tx_type: str = "transfer"):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.data_value = data_value  # Value derived from internet data
        self.tx_type = tx_type  # "transfer", "data_mining", "corporate_regulation"
        self.timestamp = time.time()
        self.tx_id = self.generate_tx_id()
    
    def generate_tx_id(self) -> str:
        """Generate unique transaction ID"""
        tx_string = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}{self.data_value}"
        return hashlib.sha256(tx_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        return {
            'tx_id': self.tx_id,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'data_value': self.data_value,
            'tx_type': self.tx_type,
            'timestamp': self.timestamp
        }
    
    def is_valid(self) -> bool:
        """Validate transaction"""
        if self.amount < 0:
            return False
        if self.sender == self.recipient:
            return False
        return True

class Block:
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate block hash using SHA-256"""
        block_string = json.dumps({
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """Mine block with proof of work"""
        target = "0" * difficulty
        start_time = time.time()
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            
            # Add mining progress feedback
            if self.nonce % 10000 == 0:
                elapsed = time.time() - start_time
                print(f"Mining block {self.index}... Nonce: {self.nonce}, Time: {elapsed:.2f}s")
        
        print(f"Block {self.index} mined! Hash: {self.hash}")
    
    def to_dict(self) -> Dict:
        return {
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'hash': self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.difficulty = 4  # Mining difficulty
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = 10  # Coins rewarded for mining
        self.corporate_shares = {
            'Google': 0,
            'Microsoft': 0,
            'NBC Universal': 0
        }
        self.data_conversion_rate = 0.001  # 1 MB = 0.001 coins
        self.create_genesis_block()
        self.lock = threading.Lock()
    
    def create_genesis_block(self) -> None:
        """Create the first block in the chain"""
        genesis_transaction = Transaction("genesis", "system", 0, 0, "genesis")
        genesis_block = Block(0, [genesis_transaction], "0")
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Add a transaction to pending transactions"""
        with self.lock:
            if transaction.is_valid():
                self.pending_transactions.append(transaction)
                return True
            return False
    
    def mine_pending_transactions(self, mining_reward_address: str) -> Block:
        """Mine pending transactions and add to blockchain"""
        # Add mining reward transaction
        reward_transaction = Transaction(
            "system", 
            mining_reward_address, 
            self.mining_reward, 
            0, 
            "mining_reward"
        )
        self.pending_transactions.append(reward_transaction)
        
        # Create new block
        new_block = Block(
            len(self.chain),
            self.pending_transactions,
            self.get_latest_block().hash
        )
        
        # Mine the block
        new_block.mine_block(self.difficulty)
        
        # Add to chain and clear pending transactions
        with self.lock:
            self.chain.append(new_block)
            self.pending_transactions = []
        
        return new_block
    
    def get_balance(self, address: str) -> float:
        """Get balance for a given address"""
        balance = 0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount
        
        return balance
    
    def convert_data_to_currency(self, data_size_mb: float, converter_address: str) -> Transaction:
        """Convert internet data to digital currency"""
        currency_amount = data_size_mb * self.data_conversion_rate
        
        # Create data conversion transaction
        conversion_transaction = Transaction(
            "data_network",
            converter_address,
            currency_amount,
            data_size_mb,
            "data_conversion"
        )
        
        self.add_transaction(conversion_transaction)
        return conversion_transaction
    
    def buy_corporate_shares(self, company: str, shares: int, buyer_address: str) -> bool:
        """Simulate buying corporate shares to regulate mining"""
        if company not in self.corporate_shares:
            return False
        
        # Calculate cost (simplified)
        cost = shares * 1000  # 1000 coins per share
        
        if self.get_balance(buyer_address) >= cost:
            # Create share purchase transaction
            share_transaction = Transaction(
                buyer_address,
                f"corporate_{company}",
                cost,
                shares,
                "share_purchase"
            )
            
            self.add_transaction(share_transaction)
            self.corporate_shares[company] += shares
            return True
        return False
    
    def adjust_mining_difficulty(self) -> None:
        """Adjust mining difficulty based on corporate share ownership"""
        total_shares = sum(self.corporate_shares.values())
        
        if total_shares > 1000:  # High corporate control
            self.difficulty = max(2, self.difficulty - 1)  # Easier mining
        elif total_shares < 100:  # Low corporate control
            self.difficulty = min(6, self.difficulty + 1)  # Harder mining
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if current block references previous block
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_blockchain_stats(self) -> Dict:
        """Get comprehensive blockchain statistics"""
        total_transactions = sum(len(block.transactions) for block in self.chain)
        total_data_converted = sum(
            tx.data_value for block in self.chain 
            for tx in block.transactions 
            if tx.tx_type == "data_conversion"
        )
        
        return {
            'total_blocks': len(self.chain),
            'total_transactions': total_transactions,
            'current_difficulty': self.difficulty,
            'total_data_converted_mb': total_data_converted,
            'corporate_shares': self.corporate_shares,
            'pending_transactions': len(self.pending_transactions)
        }