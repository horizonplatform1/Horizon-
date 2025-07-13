"""
Corporate Governance System
Manages corporate share ownership, board notifications, and legal actions
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import json
import logging
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import os
from dataclasses import dataclass

from blockchain.core import Blockchain, Transaction


@dataclass
class BoardMember:
    """Represents a board member of a company"""
    name: str
    email: str
    title: str
    company: str
    phone: Optional[str] = None
    

@dataclass
class LegalAction:
    """Represents a legal action taken regarding corporate governance"""
    action_id: str
    action_type: str  # 'takeover_notice', 'shareholder_meeting', 'legal_challenge'
    company: str
    description: str
    status: str
    filing_date: datetime
    deadline: Optional[datetime] = None
    

class CorporateGovernanceSystem:
    """Manages corporate governance and legal actions"""
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.db_path = "data/corporate_governance.db"
        self.companies = {
            'GOOGL': {
                'name': 'Google LLC',
                'full_name': 'Alphabet Inc.',
                'board_members': [
                    BoardMember('Sundar Pichai', 'board@alphabet.com', 'CEO', 'GOOGL'),
                    BoardMember('Ruth Porat', 'board@alphabet.com', 'CFO', 'GOOGL'),
                    BoardMember('Larry Page', 'board@alphabet.com', 'Co-Founder', 'GOOGL'),
                    BoardMember('Sergey Brin', 'board@alphabet.com', 'Co-Founder', 'GOOGL')
                ],
                'total_shares': 13000000000,  # Approximate total shares
                'governance_threshold': 0.05  # 5% for major governance actions
            },
            'MSFT': {
                'name': 'Microsoft Corporation',
                'full_name': 'Microsoft Corporation',
                'board_members': [
                    BoardMember('Satya Nadella', 'board@microsoft.com', 'CEO', 'MSFT'),
                    BoardMember('Amy Hood', 'board@microsoft.com', 'CFO', 'MSFT'),
                    BoardMember('John W. Thompson', 'board@microsoft.com', 'Chairman', 'MSFT'),
                    BoardMember('Reid Hoffman', 'board@microsoft.com', 'Board Member', 'MSFT')
                ],
                'total_shares': 7500000000,
                'governance_threshold': 0.05
            },
            'CMCSA': {
                'name': 'NBCUniversal Media LLC',
                'full_name': 'Comcast Corporation',
                'board_members': [
                    BoardMember('Brian Roberts', 'board@comcast.com', 'CEO', 'CMCSA'),
                    BoardMember('Jeff Shell', 'board@nbcuniversal.com', 'CEO NBCUniversal', 'CMCSA'),
                    BoardMember('Mike Cavanagh', 'board@comcast.com', 'CFO', 'CMCSA'),
                    BoardMember('Dana Strong', 'board@comcast.com', 'President', 'CMCSA')
                ],
                'total_shares': 4500000000,
                'governance_threshold': 0.05
            }
        }
        
        self._init_database()
        self._init_email_config()
        
    def _init_database(self):
        """Initialize corporate governance database"""
        os.makedirs("data", exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Share ownership tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS share_ownership (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                owner_address TEXT NOT NULL,
                shares_owned INTEGER NOT NULL,
                ownership_percentage REAL NOT NULL,
                voting_rights BOOLEAN DEFAULT TRUE,
                acquisition_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Board notifications
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS board_notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                notification_type TEXT NOT NULL,
                message TEXT NOT NULL,
                recipient_email TEXT NOT NULL,
                sent_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                delivery_status TEXT DEFAULT 'pending'
            )
        ''')
        
        # Legal actions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS legal_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action_id TEXT UNIQUE NOT NULL,
                action_type TEXT NOT NULL,
                symbol TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL,
                filing_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                deadline DATETIME,
                resolution TEXT,
                documents TEXT
            )
        ''')
        
        # Voting records
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voting_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                proposal_id TEXT NOT NULL,
                voter_address TEXT NOT NULL,
                shares_voted INTEGER NOT NULL,
                vote_choice TEXT NOT NULL,
                vote_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def _init_email_config(self):
        """Initialize email configuration for notifications"""
        # In a real system, these would be environment variables
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "datacoin.governance@gmail.com"
        self.sender_password = "your_app_password"  # Use app password for Gmail
        
    def calculate_ownership_percentage(self, symbol: str, shares: int) -> float:
        """Calculate ownership percentage for a given number of shares"""
        total_shares = self.companies[symbol]['total_shares']
        return (shares / total_shares) * 100
    
    def update_share_ownership(self, symbol: str, owner_address: str, shares_purchased: int):
        """Update share ownership records"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if owner already has shares
        cursor.execute('''
            SELECT shares_owned FROM share_ownership 
            WHERE symbol = ? AND owner_address = ?
        ''', (symbol, owner_address))
        
        result = cursor.fetchone()
        
        if result:
            # Update existing ownership
            new_total = result[0] + shares_purchased
            ownership_pct = self.calculate_ownership_percentage(symbol, new_total)
            
            cursor.execute('''
                UPDATE share_ownership 
                SET shares_owned = ?, ownership_percentage = ?, last_updated = CURRENT_TIMESTAMP
                WHERE symbol = ? AND owner_address = ?
            ''', (new_total, ownership_pct, symbol, owner_address))
        else:
            # Create new ownership record
            ownership_pct = self.calculate_ownership_percentage(symbol, shares_purchased)
            
            cursor.execute('''
                INSERT INTO share_ownership 
                (symbol, owner_address, shares_owned, ownership_percentage)
                VALUES (?, ?, ?, ?)
            ''', (symbol, owner_address, shares_purchased, ownership_pct))
        
        conn.commit()
        conn.close()
        
        # Check if this triggers any governance actions
        self._check_governance_triggers(symbol, owner_address, shares_purchased)
    
    def _check_governance_triggers(self, symbol: str, owner_address: str, shares_purchased: int):
        """Check if share purchase triggers governance actions"""
        current_ownership = self.get_ownership_percentage(symbol, owner_address)
        threshold = self.companies[symbol]['governance_threshold']
        
        # Major shareholder notification (5% threshold)
        if current_ownership >= threshold * 100:
            self._trigger_major_shareholder_notice(symbol, owner_address, current_ownership)
        
        # Potential takeover notice (25% threshold)
        if current_ownership >= 25.0:
            self._trigger_takeover_notice(symbol, owner_address, current_ownership)
        
        # Majority control notice (51% threshold)
        if current_ownership >= 51.0:
            self._trigger_majority_control_notice(symbol, owner_address, current_ownership)
    
    def _trigger_major_shareholder_notice(self, symbol: str, owner_address: str, ownership_pct: float):
        """Trigger major shareholder notification to board"""
        company = self.companies[symbol]
        
        message = f"""
        MAJOR SHAREHOLDER NOTIFICATION
        
        Company: {company['full_name']} ({symbol})
        
        We hereby notify the Board of Directors that wallet address {owner_address} 
        has acquired {ownership_pct:.2f}% ownership stake in the company.
        
        This acquisition triggers the major shareholder disclosure requirements.
        
        Please acknowledge receipt of this notification within 5 business days.
        
        DataCoin Governance System
        """
        
        self._send_board_notification(symbol, "major_shareholder", message)
        self._file_legal_action(symbol, "major_shareholder_notice", 
                               f"Major shareholder notification for {ownership_pct:.2f}% stake")
    
    def _trigger_takeover_notice(self, symbol: str, owner_address: str, ownership_pct: float):
        """Trigger takeover notice to board and regulators"""
        company = self.companies[symbol]
        
        message = f"""
        POTENTIAL TAKEOVER NOTICE
        
        Company: {company['full_name']} ({symbol})
        
        URGENT: Wallet address {owner_address} has acquired {ownership_pct:.2f}% 
        ownership stake in the company, potentially indicating a takeover attempt.
        
        This acquisition requires immediate board review and potential shareholder meeting.
        
        Recommended actions:
        1. Emergency board meeting within 48 hours
        2. Review of anti-takeover provisions
        3. Shareholder communication plan
        4. Legal counsel consultation
        
        Please respond immediately.
        
        DataCoin Governance System
        """
        
        self._send_board_notification(symbol, "takeover_notice", message)
        self._file_legal_action(symbol, "takeover_notice", 
                               f"Potential takeover notice for {ownership_pct:.2f}% stake")
    
    def _trigger_majority_control_notice(self, symbol: str, owner_address: str, ownership_pct: float):
        """Trigger majority control notice"""
        company = self.companies[symbol]
        
        message = f"""
        MAJORITY CONTROL ACHIEVED
        
        Company: {company['full_name']} ({symbol})
        
        CRITICAL: Wallet address {owner_address} has achieved majority control 
        with {ownership_pct:.2f}% ownership stake.
        
        This triggers immediate governance changes and legal requirements:
        
        1. Mandatory tender offer to remaining shareholders
        2. Board composition review
        3. SEC filing requirements
        4. Shareholder rights plan activation
        
        Legal counsel must be engaged immediately.
        
        DataCoin Governance System
        """
        
        self._send_board_notification(symbol, "majority_control", message)
        self._file_legal_action(symbol, "majority_control", 
                               f"Majority control achieved with {ownership_pct:.2f}% stake")
    
    def _send_board_notification(self, symbol: str, notification_type: str, message: str):
        """Send notification to board members"""
        company = self.companies[symbol]
        
        for board_member in company['board_members']:
            try:
                # Create email message
                msg = MIMEMultipart()
                msg['From'] = self.sender_email
                msg['To'] = board_member.email
                msg['Subject'] = f"DataCoin Governance Alert - {company['full_name']}"
                
                # Add message body
                body = f"Dear {board_member.name},\n\n{message}"
                msg.attach(MIMEText(body, 'plain'))
                
                # Send email (simulation - in production, use real SMTP)
                print(f"📧 Board Notification Sent to {board_member.name} ({board_member.email})")
                print(f"   Subject: DataCoin Governance Alert - {company['full_name']}")
                print(f"   Type: {notification_type}")
                
                # Record notification in database
                self._record_notification(symbol, notification_type, message, board_member.email)
                
            except Exception as e:
                logging.error(f"Failed to send notification to {board_member.email}: {e}")
    
    def _record_notification(self, symbol: str, notification_type: str, message: str, recipient: str):
        """Record notification in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO board_notifications 
            (symbol, notification_type, message, recipient_email, delivery_status)
            VALUES (?, ?, ?, ?, ?)
        ''', (symbol, notification_type, message, recipient, 'sent'))
        
        conn.commit()
        conn.close()
    
    def _file_legal_action(self, symbol: str, action_type: str, description: str):
        """File a legal action record"""
        action_id = f"{symbol}_{action_type}_{int(time.time())}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO legal_actions 
            (action_id, action_type, symbol, description, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (action_id, action_type, symbol, description, 'filed'))
        
        conn.commit()
        conn.close()
        
        print(f"⚖️  Legal Action Filed: {action_type} for {symbol}")
        print(f"   Action ID: {action_id}")
        print(f"   Description: {description}")
    
    def get_ownership_percentage(self, symbol: str, owner_address: str) -> float:
        """Get current ownership percentage for an address"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ownership_percentage FROM share_ownership 
            WHERE symbol = ? AND owner_address = ?
        ''', (symbol, owner_address))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else 0.0
    
    def get_major_shareholders(self, symbol: str, min_percentage: float = 1.0) -> List[Dict]:
        """Get list of major shareholders"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT owner_address, shares_owned, ownership_percentage, last_updated
            FROM share_ownership 
            WHERE symbol = ? AND ownership_percentage >= ?
            ORDER BY ownership_percentage DESC
        ''', (symbol, min_percentage))
        
        results = cursor.fetchall()
        conn.close()
        
        shareholders = []
        for result in results:
            shareholders.append({
                'address': result[0],
                'shares': result[1],
                'percentage': result[2],
                'last_updated': result[3]
            })
        
        return shareholders
    
    def create_shareholder_proposal(self, symbol: str, proposer_address: str, 
                                  proposal_text: str, voting_deadline: datetime) -> str:
        """Create a shareholder proposal for voting"""
        proposal_id = f"{symbol}_PROP_{int(time.time())}"
        
        # Check if proposer has sufficient shares (typically 1% minimum)
        ownership_pct = self.get_ownership_percentage(symbol, proposer_address)
        if ownership_pct < 1.0:
            raise ValueError("Insufficient shares to create proposal (minimum 1% required)")
        
        # In a real system, this would create a formal proposal and voting mechanism
        print(f"📋 Shareholder Proposal Created: {proposal_id}")
        print(f"   Company: {symbol}")
        print(f"   Proposer: {proposer_address} ({ownership_pct:.2f}% ownership)")
        print(f"   Proposal: {proposal_text}")
        print(f"   Voting Deadline: {voting_deadline}")
        
        return proposal_id
    
    def get_governance_summary(self, symbol: str) -> Dict:
        """Get comprehensive governance summary for a company"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get ownership distribution
        cursor.execute('''
            SELECT COUNT(*) as total_owners, 
                   SUM(shares_owned) as total_shares_held,
                   MAX(ownership_percentage) as max_ownership
            FROM share_ownership 
            WHERE symbol = ?
        ''', (symbol,))
        
        ownership_stats = cursor.fetchone()
        
        # Get recent notifications
        cursor.execute('''
            SELECT notification_type, COUNT(*) as count
            FROM board_notifications 
            WHERE symbol = ? 
            GROUP BY notification_type
        ''', (symbol,))
        
        notifications = cursor.fetchall()
        
        # Get legal actions
        cursor.execute('''
            SELECT action_type, status, COUNT(*) as count
            FROM legal_actions 
            WHERE symbol = ?
            GROUP BY action_type, status
        ''', (symbol,))
        
        legal_actions = cursor.fetchall()
        
        conn.close()
        
        return {
            'company': self.companies[symbol],
            'ownership_stats': {
                'total_owners': ownership_stats[0] if ownership_stats else 0,
                'total_shares_held': ownership_stats[1] if ownership_stats else 0,
                'max_ownership': ownership_stats[2] if ownership_stats else 0
            },
            'major_shareholders': self.get_major_shareholders(symbol),
            'notifications': notifications,
            'legal_actions': legal_actions
        }
    
    def simulate_legal_challenge(self, symbol: str, challenger_address: str, 
                               challenge_type: str, description: str) -> str:
        """Simulate filing a legal challenge"""
        action_id = f"{symbol}_CHALLENGE_{int(time.time())}"
        
        legal_actions = {
            'board_composition': 'Challenge to current board composition and governance',
            'merger_opposition': 'Opposition to proposed merger or acquisition',
            'shareholder_rights': 'Assertion of shareholder rights and privileges',
            'proxy_contest': 'Contest for proxy voting control',
            'derivative_suit': 'Derivative lawsuit on behalf of corporation'
        }
        
        full_description = f"{legal_actions.get(challenge_type, 'Legal challenge')}: {description}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO legal_actions 
            (action_id, action_type, symbol, description, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (action_id, challenge_type, symbol, full_description, 'filed'))
        
        conn.commit()
        conn.close()
        
        print(f"⚖️  Legal Challenge Filed: {action_id}")
        print(f"   Type: {challenge_type}")
        print(f"   Company: {symbol}")
        print(f"   Challenger: {challenger_address}")
        print(f"   Description: {full_description}")
        
        # Notify board of legal challenge
        self._send_board_notification(symbol, "legal_challenge", 
                                     f"Legal challenge filed: {full_description}")
        
        return action_id