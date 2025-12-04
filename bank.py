# bank_system.py

from uuid import uuid4
from typing import Dict

from account import Account
from transaction import Transaction
from audit import AuditLogger
import db


class Bank:
    """Core banking service managing accounts, transactions, and audit logging."""

    def __init__(self, name: str = "MyBank"):
        self.name = name
        self.accounts: Dict[str, Account] = {}
        self.transactions: Dict[str, Transaction] = {}
        self.audit = AuditLogger()

        # load existing accounts from DB into memory
        self.load_accounts_from_db()

    def _generate_account_id(self) -> str:
        return "ACC-" + uuid4().hex[:8].upper()

    def _generate_tx_id(self) -> str:
        return "TX-" + uuid4().hex[:10].upper()

    def create_account(
        self,
        owner_name: str,
        account_type: str = "SAVINGS",
        initial_balance: float = 0.0,
    ) -> Account:
        account_id = self._generate_account_id()
        account = Account(account_id, owner_name, account_type, initial_balance)
        self.accounts[account_id] = account

        # save to DB
        db.save_account(account.to_dict())

        # audit + initial tx
        self.audit.log("CREATE_ACCOUNT", account_id, initial_balance, "SUCCESS", f"Owner={owner_name}")

        if initial_balance > 0:
            tx_id = self._generate_tx_id()
            tx = Transaction(tx_id, account_id, "DEPOSIT", initial_balance, "SUCCESS", "Initial deposit")
            self.transactions[tx_id] = tx
            db.insert_transaction(tx.to_dict())

        return account

    def get_account(self, account_id: str) -> Account:
        if account_id not in self.accounts:
            self.audit.log("GET_ACCOUNT", account_id, 0.0, "FAILED", "Account not found")
            raise KeyError(f"Account {account_id} not found.")
        return self.accounts[account_id]

    def deposit(self, account_id: str, amount: float) -> float:
        account = self.get_account(account_id)
        if account.status != "ACTIVE":
            self.audit.log("DEPOSIT", account_id, amount, "FAILED", "Account not active")
            raise ValueError("Account is not active.")

        tx_id = self._generate_tx_id()
        try:
            new_balance = account.deposit(amount)

            # update DB balance
            db.update_account_balance(account_id, new_balance)

            # transaction record
            tx = Transaction(tx_id, account_id, "DEPOSIT", amount, "SUCCESS", f"New balance={new_balance}")
            self.transactions[tx_id] = tx
            db.insert_transaction(tx.to_dict())

            self.audit.log("DEPOSIT", account_id, amount, "SUCCESS", f"New balance={new_balance}")
            return new_balance
        except Exception as e:
            self.audit.log("DEPOSIT", account_id, amount, "FAILED", str(e))
            tx = Transaction(tx_id, account_id, "DEPOSIT", amount, "FAILED", str(e))
            self.transactions[tx_id] = tx
            db.insert_transaction(tx.to_dict())
            raise

    def withdraw(self, account_id: str, amount: float) -> float:
        account = self.get_account(account_id)
        if account.status != "ACTIVE":
            self.audit.log("WITHDRAW", account_id, amount, "FAILED", "Account not active")
            raise ValueError("Account is not active.")

        tx_id = self._generate_tx_id()
        try:
            new_balance = account.withdraw(amount)

            # update DB balance
            db.update_account_balance(account_id, new_balance)

            # transaction record
            tx = Transaction(tx_id, account_id, "WITHDRAW", amount, "SUCCESS", f"New balance={new_balance}")
            self.transactions[tx_id] = tx
            db.insert_transaction(tx.to_dict())

            self.audit.log("WITHDRAW", account_id, amount, "SUCCESS", f"New balance={new_balance}")
            return new_balance
        except Exception as e:
            self.audit.log("WITHDRAW", account_id, amount, "FAILED", str(e))
            tx = Transaction(tx_id, account_id, "WITHDRAW", amount, "FAILED", str(e))
            self.transactions[tx_id] = tx
            db.insert_transaction(tx.to_dict())
            raise

    def check_balance(self, account_id: str) -> float:
        account = self.get_account(account_id)
        balance = account.get_balance()
        self.audit.log("BALANCE_CHECK", account_id, 0.0, "SUCCESS", f"Balance={balance}")
        return balance

    def load_accounts_from_db(self):
        """Load all accounts from the database into memory (self.accounts)."""
        records = db.fetch_all_accounts()
        for rec in records:
            acc = Account(
                rec["account_id"],
                rec["owner_name"],
                rec["account_type"],
                rec["balance"],
            )
            acc.status = rec["status"]
            self.accounts[acc.account_id] = acc

    def close_account(self, account_id: str):
        """Mark an account as CLOSED in memory, DB, and audit trail."""
        account = self.get_account(account_id)
        if account.status == "CLOSED":
            self.audit.log("CLOSE_ACCOUNT", account_id, 0.0, "FAILED", "Already closed")
            raise ValueError("Account is already closed.")

        account.status = "CLOSED"
        db.close_account(account_id)
        self.audit.log("CLOSE_ACCOUNT", account_id, 0.0, "SUCCESS", "Account closed")


    def get_bank_summary(self) -> Dict:
        """Return summary stats for the entire bank."""
        total_accounts = len(self.accounts)
        total_balance = sum(acc.get_balance() for acc in self.accounts.values())
        active_accounts = sum(1 for acc in self.accounts.values() if acc.status == "ACTIVE")
        
        return {
            "total_accounts": total_accounts,
            "active_accounts": active_accounts,
            "total_balance": total_balance,
            "avg_balance": total_balance / total_accounts if total_accounts > 0 else 0
        }
    

    def transfer(self, from_account_id: str, to_account_id: str, amount: float):
        """Transfer amount from one account to another as an atomic operation."""
        if from_account_id == to_account_id:
            raise ValueError("Cannot transfer to the same account.")

        # Get accounts
        from_acc = self.get_account(from_account_id)
        to_acc = self.get_account(to_account_id)

        # Status checks
        if from_acc.status != "ACTIVE":
            self.audit.log("TRANSFER", from_account_id, amount, "FAILED", "Source account not active")
            raise ValueError("Source account is not active.")
        if to_acc.status != "ACTIVE":
            self.audit.log("TRANSFER", to_account_id, amount, "FAILED", "Destination account not active")
            raise ValueError("Destination account is not active.")

        # Generate transaction IDs
        tx_out_id = self._generate_tx_id()
        tx_in_id = self._generate_tx_id()

        try:
            # 1) Withdraw from source
            new_from_balance = from_acc.withdraw(amount)
            db.update_account_balance(from_account_id, new_from_balance)

            tx_out = Transaction(
                tx_out_id,
                from_account_id,
                "TRANSFER_OUT",
                amount,
                "SUCCESS",
                f"To {to_account_id}, new balance={new_from_balance}",
            )
            self.transactions[tx_out_id] = tx_out
            db.insert_transaction(tx_out.to_dict())

            # 2) Deposit to destination
            new_to_balance = to_acc.deposit(amount)
            db.update_account_balance(to_account_id, new_to_balance)

            tx_in = Transaction(
                tx_in_id,
                to_account_id,
                "TRANSFER_IN",
                amount,
                "SUCCESS",
                f"From {from_account_id}, new balance={new_to_balance}",
            )
            self.transactions[tx_in_id] = tx_in
            db.insert_transaction(tx_in.to_dict())

            # 3) Audit
            self.audit.log(
                "TRANSFER",
                from_account_id,
                amount,
                "SUCCESS",
                f"From {from_account_id} to {to_account_id}",
            )

        except Exception as e:
            # One side failed: record failed transfer
            self.audit.log(
                "TRANSFER",
                from_account_id,
                amount,
                "FAILED",
                f"Error: {e}",
            )
            # Note: for full ACID, you'd wrap DB work in an explicit SQL transaction.
            raise

