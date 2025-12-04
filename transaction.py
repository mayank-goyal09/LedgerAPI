

from datetime import datetime

class Transaction:
    def __init__(self, tx_id: str, account_id: str, tx_type: str, amount: float, status: str = "SUCCESS", message: str = ""):
        self.tx_id = tx_id
        self.account_id = account_id
        self.tx_type = tx_type.upper()      # DEPOSIT / WITHDRAW / TRANSFER
        self.amount = float(amount)
        self.status = status.upper()        # SUCCESS / FAILED
        self.message = message
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "tx_id": self.tx_id,
            "account_id": self.account_id,
            "tx_type": self.tx_type,
            "amount": self.amount,
            "status": self.status,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
        }
