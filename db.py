# db.py

import sqlite3
from contextlib import contextmanager

DB_NAME = "bank.db"

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_id TEXT PRIMARY KEY,
            owner_name TEXT NOT NULL,
            account_type TEXT NOT NULL,
            balance REAL NOT NULL,
            status TEXT NOT NULL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            tx_id TEXT PRIMARY KEY,
            account_id TEXT NOT NULL,
            tx_type TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            message TEXT,
            timestamp TEXT NOT NULL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            account_id TEXT,
            amount REAL,
            status TEXT,
            message TEXT
        )
        """)

# db.py (add below init_db)

from typing import Dict

def save_account(account_dict: Dict):
    """Insert a new account row."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO accounts (account_id, owner_name, account_type, balance, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            account_dict["account_id"],
            account_dict["owner_name"],
            account_dict["account_type"],
            account_dict["balance"],
            account_dict["status"],
        ))


def update_account_balance(account_id: str, new_balance: float):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
        """, (new_balance, account_id))


def insert_transaction(tx_dict: Dict):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transactions (tx_id, account_id, tx_type, amount, status, message, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            tx_dict["tx_id"],
            tx_dict["account_id"],
            tx_dict["tx_type"],
            tx_dict["amount"],
            tx_dict["status"],
            tx_dict["message"],
            tx_dict["timestamp"],
        ))


def insert_audit_entry(entry: Dict):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO audit_log (timestamp, action, account_id, amount, status, message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entry["timestamp"],
            entry["action"],
            entry["account_id"],
            entry["amount"],
            entry["status"],
            entry["message"],
        ))

from typing import List, Dict

def fetch_all_accounts() -> List[Dict]:
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM accounts")
        rows = cur.fetchall()
        return [dict(row) for row in rows]


def fetch_transactions_for_account(account_id: str) -> List[Dict]:
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM transactions WHERE account_id = ? ORDER BY timestamp",
            (account_id,),
        )
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    
def close_account(account_id: str):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE accounts
            SET status = 'CLOSED'
            WHERE account_id = ?
        """, (account_id,))

def get_all_accounts_summary() -> List[Dict]:
    """Get summary of all accounts (id, owner, type, balance, status)."""
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT account_id, owner_name, account_type, balance, status 
            FROM accounts 
            ORDER BY account_id
        """)
        return [dict(row) for row in cur.fetchall()]

def get_recent_audit_logs(limit: int = 10) -> List[Dict]:
    """Get the most recent audit entries."""
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM audit_log 
            ORDER BY id DESC 
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cur.fetchall()]

