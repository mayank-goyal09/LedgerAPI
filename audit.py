

from datetime import datetime
from typing import List, Dict
import db

class AuditLogger:
    def __init__(self, logfile: str = "audit.log"):
        self.entries: List[Dict] = []
        self.logfile = logfile

    def log(self, action: str, account_id: str = "", amount: float = 0.0, status: str = "SUCCESS", message: str = ""):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action.upper(),
            "account_id": account_id,
            "amount": float(amount),
            "status": status.upper(),
            "message": message,
        }

        # 1) in memory
        self.entries.append(entry)

        # 2) to file
        line = (
            f"{entry['timestamp']} | {entry['action']} | {entry['account_id']} | "
            f"{entry['amount']} | {entry['status']} | {entry['message']}\n"
        )
        with open(self.logfile, "a", encoding="utf-8") as f:
            f.write(line)

        # 3) to DB
        db.insert_audit_entry(entry)


    def get_entries(self) -> List[Dict]:
        return list(self.entries)
