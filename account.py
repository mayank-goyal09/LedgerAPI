

class Account:
    def __init__(self, account_id: str, owner_name: str, account_type: str = "SAVINGS", initial_balance: float = 0.0):
        self.account_id = account_id
        self.owner_name = owner_name
        self.account_type = account_type.upper()
        self.balance = float(initial_balance)
        self.status = "ACTIVE"

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        return self.balance

    def get_balance(self) -> float:
        return self.balance

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "owner_name": self.owner_name,
            "account_type": self.account_type,
            "balance": self.balance,
            "status": self.status,
        }
