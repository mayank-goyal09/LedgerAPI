# menu.py

from bank import Bank      # make sure Bank class is in bank.py
import db


def get_positive_float(prompt: str) -> float:
    """Read a float > 0 from the user."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value <= 0:
                print("Amount must be greater than zero. Try again.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_non_negative_float(prompt: str) -> float:
    """Read a float >= 0 from the user (for initial deposits)."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value < 0:
                print("Amount cannot be negative. Try again.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_menu_choice() -> str:
    choice = input("Enter choice: ").strip()
    return choice


def run_cli():
    bank = Bank("ProjectBank")

    while True:
        print("\n=== BANK SYSTEM MENU ===")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Show Audit Trail (in-memory)")
        print("6. Show Transactions for Account")
        print("7. Close Account")
        print("8. Bank Reports Dashboard")
        print("9. Transfer Between Accounts")
        print("0. Exit")

        choice = get_menu_choice()

        if choice == "1":
            owner = input("Owner name: ").strip()
            acc_type = input("Account type (SAVINGS/CURRENT): ").strip() or "SAVINGS"
            initial = get_non_negative_float("Initial deposit (0 allowed): ")
            account = bank.create_account(owner, acc_type, initial)
            print(f"✅ Account created with ID: {account.account_id}")

        elif choice == "2":
            acc_id = input("Account ID: ").strip()
            amount = get_positive_float("Amount to deposit: ")
            try:
                new_balance = bank.deposit(acc_id, amount)
                print(f"✅ Deposit successful. New balance: {new_balance}")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif choice == "3":
            acc_id = input("Account ID: ").strip()
            amount = get_positive_float("Amount to withdraw: ")
            try:
                new_balance = bank.withdraw(acc_id, amount)
                print(f"✅ Withdrawal successful. New balance: {new_balance}")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif choice == "4":
            acc_id = input("Account ID: ").strip()
            try:
                balance = bank.check_balance(acc_id)
                print(f"💰 Balance for {acc_id}: {balance}")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif choice == "5":
            print("\n--- AUDIT TRAIL ---")
            for entry in bank.audit.get_entries():
                print(entry)

        elif choice == "6":
            acc_id = input("Account ID: ").strip()
            tx_list = db.fetch_transactions_for_account(acc_id)
            if not tx_list:
                print("No transactions found for this account.")
            else:
                print(f"\n--- Transactions for {acc_id} ---")
                for tx in tx_list:
                    print(
                        f"{tx['timestamp']} | {tx['tx_type']} | {tx['amount']} | "
                        f"{tx['status']} | {tx['message']}"
                    )

        elif choice == "7":
            acc_id = input("Account ID: ").strip()
            try:
                bank.close_account(acc_id)
                print(f"✅ Account {acc_id} closed.")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif choice == "8":
            print("\n=== BANK REPORTS DASHBOARD ===")

            # Total bank stats
            summary = bank.get_bank_summary()
            print(f"📊 Total Accounts: {summary['total_accounts']}")
            print(f"✅ Active Accounts: {summary['active_accounts']}")
            print(f"💰 Total Balance: ${summary['total_balance']:,.2f}")
            print(f"📈 Avg Balance: ${summary['avg_balance']:,.2f}")

            # All accounts table
            accounts = db.get_all_accounts_summary()
            if accounts:
                print("\n--- ALL ACCOUNTS ---")
                print(f"{'ID':<12} {'Owner':<15} {'Type':<10} {'Balance':<12} {'Status'}")
                print("-" * 65)
                for acc in accounts:
                    print(
                        f"{acc['account_id']:<12} {acc['owner_name']:<15} "
                        f"{acc['account_type']:<10} ${acc['balance']:<11.2f} {acc['status']}"
                    )

            # Recent audit
            recent_audit = db.get_recent_audit_logs(5)
            if recent_audit:
                print("\n--- RECENT AUDIT (last 5) ---")
                for entry in recent_audit:
                    print(
                        f"{entry['timestamp'][:19]} | {entry['action']:<12} | "
                        f"{entry['account_id']:<12} | {entry['status']}"
                    )

        elif choice == "9":
            from_id = input("From Account ID: ").strip()
            to_id = input("To Account ID: ").strip()
            amount = get_positive_float("Amount to transfer: ")
            try:
                bank.transfer(from_id, to_id, amount)
                print(f"✅ Transferred {amount} from {from_id} to {to_id}.")
            except Exception as e:
                print(f"❌ Error: {e}")

        elif choice == "0":
            print("👋 Exiting. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please try again.")
