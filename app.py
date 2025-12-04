import streamlit as st
from bank import Bank
import db


# ---------- Page config ----------
st.set_page_config(
    page_title="Mayank's Bank - Pro Banking System",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------- Custom CSS (brown-grey theme) ----------
st.markdown(
    """
<style>
/* Global app background */
.stApp {
    background: linear-gradient(135deg, #2C1B12 0%, #1A1A1A 40%, #2D2D2D 100%);
    color: #E8D5B7;
}

/* Main content container */
.main > div {
    padding-top: 1rem;
}

/* Glass card container */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(232, 213, 183, 0.15);
    border-radius: 18px;
    padding: 1.8rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.45);
}

/* Gold accent text */
.gold-accent {
    color: #D4AF37 !important;
    font-weight: 700;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E140F 0%, #2A1F14 100%);
    border-right: 1px solid rgba(232, 213, 183, 0.1);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(45deg, #D4AF37, #B8860B);
    color: #1A1A1A !important;
    border-radius: 12px;
    border: none;
    padding: 0.4rem 1.2rem;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(212, 175, 55, 0.35);
    transition: all 0.2s ease-in-out;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 22px rgba(212, 175, 55, 0.5);
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > select {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(232, 213, 183, 0.25);
    border-radius: 10px;
    color: #E8D5B7;
}

/* Dataframe styling wrapper */
[data-testid="stDataFrame"] {
    background: rgba(0, 0, 0, 0.15);
    border-radius: 12px;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(44, 27, 18, 0.8);
    border-radius: 14px;
    padding: 0.6rem 0.8rem;
    border: 1px solid rgba(232, 213, 183, 0.25);
}

/* Footer */
.footer {
    background: rgba(10, 10, 10, 0.95);
    padding: 1.5rem;
    text-align: center;
    border-top: 1px solid rgba(232, 213, 183, 0.2);
    margin-top: 2.5rem;
}
</style>
    """,
    unsafe_allow_html=True,
)


# ---------- DB + Bank init ----------
db.init_db()
bank = Bank("Mayank's Bank")


# ---------- Hero header ----------
hero_col1, hero_col2, hero_col3 = st.columns([1, 2, 1])
with hero_col2:
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 1rem;">
            <h1 class="gold-accent" style="font-size: 3rem; margin-bottom: 0.2rem;">
                🏦 Mayank's Bank
            </h1>
            <p style="color: #B0A89A; font-size: 1.05rem; margin-top: 0;">
                Professional Banking System with Audit Trails & SQLite Backend
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Sidebar navigation ----------
with st.sidebar:
    st.markdown(
        "<h2 class='gold-accent'>🚀 Control Panel</h2>",
        unsafe_allow_html=True,
    )
    menu = st.selectbox(
        "Choose operation",
        [
            "📊 Dashboard",
            "➕ Create Account",
            "💰 Deposit",
            "💸 Withdraw",
            "🔍 Check Balance",
            "🔄 Transfer",
            "📈 Transactions",
            "📋 Reports",
            "🕵️ Audit Trail",
        ],
    )


# ---------- Pages ----------

# Dashboard
if menu == "📊 Dashboard":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("📊 Bank Overview")

    summary = bank.get_bank_summary()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Accounts", summary["total_accounts"])
    with c2:
        st.metric("Active Accounts", summary["active_accounts"])
    with c3:
        st.metric("Total Balance", f"₹{summary['total_balance']:.2f}")
    with c4:
        st.metric("Average Balance", f"₹{summary['avg_balance']:.2f}")

    st.markdown("### Recent Accounts")
    accounts = db.get_all_accounts_summary()
    if accounts is not None and len(accounts) > 0:
        st.dataframe(accounts, use_container_width=True)
    else:
        st.info("No accounts yet. Create the first one from the sidebar.")
    st.markdown("</div>", unsafe_allow_html=True)


# Create Account
elif menu == "➕ Create Account":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("➕ Create New Account")

    with st.form("create_account_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            owner = st.text_input("👤 Owner name", placeholder="Enter full name")
        with col2:
            acc_type = st.selectbox("💳 Account type", ["SAVINGS", "CURRENT"])
        initial = st.number_input(
            "💰 Initial deposit",
            min_value=0.0,
            value=0.0,
            step=500.0,
            format="%.2f",
        )
        submitted = st.form_submit_button("🚀 Create account", use_container_width=True)

    if submitted:
        if not owner.strip():
            st.error("Owner name is required.")
        else:
            try:
                account = bank.create_account(owner.strip(), acc_type, initial)
                st.success(
                    f"✅ Account created! ID: "
                    f"<span class='gold-accent'>{account.account_id}</span>",
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"❌ Error: {e}")
    st.markdown("</div>", unsafe_allow_html=True)


# Deposit
elif menu == "💰 Deposit":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("💰 Deposit")

    with st.form("deposit_form", clear_on_submit=True):
        acc_id = st.text_input("🏦 Account ID")
        amount = st.number_input(
            "Amount",
            min_value=0.01,
            step=100.0,
            format="%.2f",
        )
        submitted = st.form_submit_button("💰 Deposit", use_container_width=True)

    if submitted:
        try:
            new_balance = bank.deposit(acc_id.strip(), amount)
            st.success(
                f"✅ Deposit successful. New balance: "
                f"<span class='gold-accent'>₹{new_balance:.2f}</span>",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"❌ Error: {e}")
    st.markdown("</div>", unsafe_allow_html=True)


# Withdraw
elif menu == "💸 Withdraw":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("💸 Withdraw")

    with st.form("withdraw_form", clear_on_submit=True):
        acc_id = st.text_input("🏦 Account ID")
        amount = st.number_input(
            "Amount",
            min_value=0.01,
            step=100.0,
            format="%.2f",
        )
        submitted = st.form_submit_button("💸 Withdraw", use_container_width=True)

    if submitted:
        try:
            new_balance = bank.withdraw(acc_id.strip(), amount)
            st.success(
                f"✅ Withdrawal successful. New balance: "
                f"<span class='gold-accent'>₹{new_balance:.2f}</span>",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"❌ Error: {e}")
    st.markdown("</div>", unsafe_allow_html=True)


# Check Balance
elif menu == "🔍 Check Balance":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("🔍 Check Balance")

    col1, col2 = st.columns([3, 1])
    with col1:
        acc_id = st.text_input("🏦 Account ID")
    with col2:
        check_btn = st.button("🔍 Check", use_container_width=True)

    if check_btn:
        try:
            balance = bank.check_balance(acc_id.strip())
            st.success(
                f"💰 Balance for <span class='gold-accent'>{acc_id}</span>: "
                f"<span class='gold-accent'>₹{balance:.2f}</span>",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"❌ Error: {e}")
    st.markdown("</div>", unsafe_allow_html=True)


# Transfer
elif menu == "🔄 Transfer":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("🔄 Transfer Between Accounts")

    with st.form("transfer_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            from_id = st.text_input("📤 From Account ID")
        with c2:
            to_id = st.text_input("📥 To Account ID")
        amount = st.number_input(
            "Amount",
            min_value=0.01,
            step=100.0,
            format="%.2f",
        )
        submitted = st.form_submit_button("🔄 Transfer", use_container_width=True)

    if submitted:
        try:
            bank.transfer(from_id.strip(), to_id.strip(), amount)
            st.success(
                f"✅ Transferred ₹{amount:.2f} from "
                f"<span class='gold-accent'>{from_id}</span> "
                f"to <span class='gold-accent'>{to_id}</span>.",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"❌ Error: {e}")
    st.markdown("</div>", unsafe_allow_html=True)


# Transactions
elif menu == "📈 Transactions":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("📈 Transaction History")

    acc_id = st.text_input("🏦 Account ID")
    if st.button("📊 Load transactions"):
        tx_list = db.fetch_transactions_for_account(acc_id.strip())
        if tx_list is not None and len(tx_list) > 0:
            st.dataframe(tx_list, use_container_width=True, height=400)
        else:
            st.info("No transactions found for this account.")
    st.markdown("</div>", unsafe_allow_html=True)


# Reports
elif menu == "📋 Reports":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("📋 Bank Reports")

    summary = bank.get_bank_summary()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Accounts", summary["total_accounts"])
        st.metric("Active Accounts", summary["active_accounts"])
    with col2:
        st.metric("Total Balance", f"₹{summary['total_balance']:.2f}")
        st.metric("Average Balance", f"₹{summary['avg_balance']:.2f}")

    st.markdown("### All Accounts")
    accounts = db.get_all_accounts_summary()
    if accounts is not None and len(accounts) > 0:
        st.dataframe(accounts, use_container_width=True)
    else:
        st.info("No accounts available yet.")
    st.markdown("</div>", unsafe_allow_html=True)


# Audit Trail
elif menu == "🕵️ Audit Trail":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("🕵️ Audit Trail")

    recent_audit = db.get_recent_audit_logs(100)
    if recent_audit is not None and len(recent_audit) > 0:
        st.dataframe(recent_audit, use_container_width=True, height=450)
    else:
        st.info("No audit entries yet.")
    st.markdown("</div>", unsafe_allow_html=True)


# ---------- Footer ----------
st.markdown(
    """
<div class="footer">
    <h4 style="color: #D4AF37; margin-bottom: 0.4rem;">
        💖 created with love by mayank goyal · data scientist
    </h4>
    <div style="margin-top: 0.4rem;">
        <a href="https://github.com/mayank-goyal09" target="_blank"
           style="margin: 0 0.8rem; color: #D4AF37; text-decoration: none; font-weight: 600;">
           🌐 GitHub
        </a>
        <a href="www.linkedin.com/in/mayank-goyal-4b8756363" target="_blank"
           style="margin: 0 0.8rem; color: #D4AF37; text-decoration: none; font-weight: 600;">
           💼 LinkedIn
        </a>
    </div>
    <p style="margin-top: 0.5rem; font-size: 0.85rem; color: #8D7F6A;">
        Mayank's Bank · Python · Streamlit · SQLite · OOP Banking Engine with Audit Logging
    </p>
</div>
    """,
    unsafe_allow_html=True,
)
