```
                                 ╔════════════════════════════════════════════════════════════════╗
                                 ║                    🏦  LEDGERAPI  🏦                          ║
                                 ║            Enterprise-Grade Banking System                     ║
                                 ║                 Professional OOP Architecture                  ║
                                 ╚════════════════════════════════════════════════════════════════╝
```

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?style=for-the-badge&logo=sqlite)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)
![OOP](https://img.shields.io/badge/OOP-Architecture-yellow?style=for-the-badge)
![MIT License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**A production-ready banking system demonstrating advanced Python OOP, SQLite backend, comprehensive audit trails, and real-time transaction processing.**

[🚀 Live Demo](#live-demo) • [📋 Features](#-features) • [🛠️ Tech Stack](#️-tech-stack) • [⚙️ Architecture](#️-architecture) • [📦 Installation](#-installation)

</div>

---

## 🎯 Overview

**LedgerAPI** is a portfolio-ready, enterprise-grade banking system built with **Python OOP principles** and a robust **SQLite backend**. This project showcases professional software architecture, comprehensive audit trails, transaction processing, inter-account transfers, and an intuitive executive dashboard.

### Why LedgerAPI?
- ✅ **Production-Ready Code**: Enterprise-level architecture with best practices
- ✅ **Complete Audit Trail**: Every transaction logged with timestamps and user actions
- ✅ **Type-Safe OOP**: Leverages Python classes, inheritance, and encapsulation
- ✅ **Database Integrity**: SQLite with proper schema design and relationships
- ✅ **Professional UI**: Streamlit dashboard with real-time analytics
- ✅ **Portfolio Showcase**: Demonstrates skills in backend systems & data management

---

## 🚀 Live Demo

🌐 **[Visit the Live Application](https://ledgerapi-gtpxpjeyashd6tadofycb2.streamlit.app/)**

Experience the full banking system with:
- 📊 Live dashboard with account analytics
- 💰 Real-time transaction processing
- 📈 Account balance tracking
- 🔐 Secure account management

---

## ✨ Features

### 💳 Account Management
- Create and manage multiple account types (Savings, Checking, etc.)
- Track account balance, status, and account type
- View detailed account information
- Account activation/deactivation

### 💸 Transaction Processing
- Deposit funds into accounts
- Withdraw funds with balance validation
- Transfer money between accounts instantly
- Track transaction history with full details
- Real-time balance updates

### 📋 Comprehensive Audit System
- Complete audit trail for all operations
- Timestamp logging for every transaction
- User action tracking
- File-based audit logs (audit.log)
- Query transaction history by date, type, or amount

### 📊 Executive Dashboard
- Live bank overview statistics
- Total accounts, active accounts, and total balance
- Recent account activity
- Average account balance calculations
- Visual data representation with Plotly charts

### 🔐 Validation & Security
- Input validation for all operations
- Balance verification before transactions
- Account status checks
- Prevents overdrafts and invalid operations

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|----------|
| **Frontend** | Streamlit | Interactive web dashboard |
| **Backend** | Python 3.8+ | Core business logic |
| **Architecture** | OOP (Classes, Inheritance) | Professional code structure |
| **Database** | SQLite | Persistent data storage |
| **Audit Logging** | File-based logging | Transaction tracking |
| **Data Analysis** | Pandas | Data manipulation |
| **Visualization** | Plotly | Charts and graphs |

---

## ⚙️ Architecture

```
LedgerAPI/
├── app.py              # Streamlit dashboard & main application
├── bank.py             # Bank class (main controller)
├── account.py          # Account class (entity model)
├── transaction.py      # Transaction class (business logic)
├── audit.py            # AuditLogger class (audit trail system)
├── db.py               # Database helper class
├── menu.py             # CLI menu system
├── main.py             # Entry point
├── bank.db             # SQLite database
├── audit.log           # Audit trail log file
└── requirements.txt    # Python dependencies
```

### Class Hierarchy

```
📦 LedgerAPI
 ├── 🏦 Bank (Main Controller)
 ├── 💳 Account (Entity Model)
 │  └── Attributes: id, owner, type, balance, status
 ├── 💰 Transaction (Business Logic)
 │  └── Types: Deposit, Withdraw, Transfer
 ├── 📝 AuditLogger (Audit Trail)
 │  └── Logging: All operations with timestamps
 └── 🗄️  DB (Database Helper)
    └── SQLite Schema Management
```

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/mayank-goyal09/LedgerAPI.git
cd LedgerAPI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit application
streamlit run app.py

# Alternative: Run the CLI version
python main.py
```

### Requirements
```
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.14.0
```

---

## 💻 Usage

### Dashboard Operations

**Create a New Account**
```
1. Go to Dashboard → Select "Create Account"
2. Enter account holder name
3. Choose account type (Savings/Checking)
4. Initial deposit amount
```

**Make a Transaction**
```
1. Select Transaction Type (Deposit/Withdraw/Transfer)
2. Select Account
3. Enter Amount
4. Confirm operation
```

**View Account Details**
```
1. Dashboard shows all accounts
2. Click on any account row
3. View transaction history
4. See audit trail for that account
```

---

## 🏗️ Code Examples

### Creating an Account
```python
from bank import Bank
from account import Account

bank = Bank()
bank.create_account("John Doe", "SAVINGS", 5000)
```

### Processing a Transfer
```python
bank.transfer(from_account_id="ACC-001", 
              to_account_id="ACC-002", 
              amount=1000)
```

### Accessing Audit Trail
```python
audit_logs = bank.audit_logger.get_audit_trail()
for log in audit_logs:
    print(f"{log['timestamp']} - {log['action']}")
```

---

## 📊 Database Schema

### Accounts Table
```sql
CREATE TABLE accounts (
    id TEXT PRIMARY KEY,
    owner_name TEXT NOT NULL,
    account_type TEXT NOT NULL,
    balance REAL NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP
)
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id TEXT PRIMARY KEY,
    account_id TEXT,
    transaction_type TEXT,
    amount REAL,
    timestamp TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
)
```

---

## 🎨 Features in Action

### Dashboard Features
- 📊 **Bank Overview**: Total accounts, active accounts, total balance, average balance
- 💳 **Account Management**: Create, view, and manage accounts
- 💸 **Transactions**: Deposit, withdraw, and transfer funds
- 📈 **Analytics**: Visual representation of account data
- 🔍 **Search**: Find accounts and transactions easily

### Performance
- ⚡ Real-time updates
- 🚀 Fast transaction processing
- 💾 Efficient database queries
- 📁 Organized audit logging

---

## 🔒 Security Features

- ✅ Input validation for all operations
- ✅ Balance verification before transactions
- ✅ Account status validation
- ✅ Comprehensive audit logging
- ✅ Preventing overdrafts
- ✅ Unique account identifiers

---

## 📈 Project Statistics

| Metric | Value |
|--------|-------|
| **Lines of Code** | 500+ |
| **Classes** | 5 (Bank, Account, Transaction, AuditLogger, DB) |
| **Core Features** | 6+ |
| **Database Tables** | 2 |
| **OOP Concepts Used** | Inheritance, Encapsulation, Polymorphism |

---

## 🚀 Future Enhancements

- [ ] User authentication system
- [ ] Interest calculation and compound interest
- [ ] Loan management system
- [ ] Multi-currency support
- [ ] Advanced analytics and reporting
- [ ] Mobile app integration
- [ ] REST API endpoints
- [ ] Real-time notifications

---

## 📚 Learning Outcomes

This project demonstrates proficiency in:
- ✅ **Object-Oriented Programming**: Classes, inheritance, encapsulation
- ✅ **Database Design**: SQLite schema, relationships, queries
- ✅ **Backend Development**: Business logic and data validation
- ✅ **Frontend Development**: Streamlit dashboard creation
- ✅ **Software Architecture**: Professional project structure
- ✅ **Audit & Logging**: Comprehensive transaction tracking
- ✅ **Code Quality**: Best practices and clean code principles

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🤝 Connect

👨‍💻 **Created by**: Mayank Goyal

🔗 **Links**:
- GitHub: [@mayank-goyal09](https://github.com/mayank-goyal09)
- Portfolio: [Visit My Projects](https://github.com/mayank-goyal09)
- Project Dashboard: [LedgerAPI Live](https://ledgerapi-gtpxpjeyashd6tadofycb2.streamlit.app/)

---

<div align="center">

### ⭐ If this project helped you, please give it a star!

```
╔════════════════════════════════════════════════════════════════╗
║          Built with ❤️  and Professional OOP Design           ║
║              Ready for Production & Portfolio                  ║
╚════════════════════════════════════════════════════════════════╝
```

</div>
