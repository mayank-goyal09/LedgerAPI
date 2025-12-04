import streamlit as st
from bank import Bank
import db

# ---------- Custom CSS for Brown-Grey Fintech Theme ----------
st.markdown("""
<style>
    /* Main background - Dark brown-grey gradient */
    .main {
        background: linear-gradient(135deg, #2C1B12 0%, #1A1A1A 50%, #2D2D2D 100%);
        color: #E8D5B7;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(232, 213, 183, 0.1);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    /* Gold accents for premium feel */
    .gold-accent {
        color: #D4AF37 !important;
        font-weight: 700;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #D4AF37, #B8860B);
        color: #1A1A1A;
        border-radius: 12px;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E140F 0%, #2A1F14 100%);
        border-right: 1px solid rgba(232, 213, 183, 0.1);
    }
    
    /* Metrics */
    .stMetric {
        background: rgba(44, 27, 18, 0.8);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(232, 213, 183, 0.2);
    }
    
    /* Footer */
    .footer {
        background: rgba(26, 26, 26, 0.9);
        padding: 2rem;
        text-align: center;
        border-top: 1px solid rgba(232, 213, 183, 0.1);
        margin-top: 3rem;
    }
    
    /* Form elements */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(232, 213, 183, 0.2);
        border-radius: 10px;
        color: #E8D5B7;
        padding: 0.75rem;
    }
    
    /* Dataframe */
    .dataframe {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        border: 1px solid rgba(232, 213, 183, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ---------- App Setup ----------
st.set_page_config(
    page_title="🏦 Mayank's Pro Bank System", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# DB & Bank init
db.init_db()
bank = Bank("MayankStreamlitBank")

# ---------- Hero Header ----------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center;'>
        <h1 class='gold-accent' style='font-size: 3.5rem; margin-bottom: 0;'>🏦 BANK COMMAND</h1>
        <p style='color: #B0A89A; font-size: 1.2rem; margin-top: 0;'>Professional Banking System with Audit Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- Enhanced Navigation ----------
with st.sidebar:
    st.markdown("<h2 class='gold-accent'>🚀 Control Panel</h2>", unsafe_allow_html=True)
    menu = st.selectbox("Select Operation", [
        "📊 Dashboard", "➕ Create Account", "💰 Deposit", 
        "💸 Withdraw", "🔍 Balance", "🔄 Transfer", 
        "📈 Transactions", "📋 Reports", "🕵️ Audit Trail"
    ], index=0)

# ---------- Enhanced Pages ----------
if menu == "📊 Dashboard":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("💎 Executive Dashboard")
    summary = bank.get_bank_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("🏦 Total Accounts", summary["total_accounts"])
    with col2: st.metric("✅ Active", summary["active_accounts"])
    with col3: st.metric("💵 Total Balance", f"₹{summary['total_balance']:.2f}")
    with col4: st.metric("📊 Avg Balance", f"₹{summary['avg_balance']:.2f}")
    
    st.markdown("### Recent Accounts")
    accounts = db.get_all_accounts_summary()
    if accounts is not None and len(accounts) > 0:
        st.dataframe(accounts, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "➕ Create Account":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("➕ Create New Account")
    with st.form("create_account", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1: owner = st.text_input("👤 Owner Name", placeholder="Enter full name")
        with col2: acc_type = st.selectbox("💳 Type", ["SAVINGS", "CURRENT"])
        initial = st.number_input("💰 Initial Deposit", min_value=0.0, value=0.0, step=500.0, 
                                 format="₹%.2f")
        submitted = st.form_submit_button("🚀 CREATE ACCOUNT", use_container_width=True)
    
    if 'submitted' in locals() and submitted:
        if not owner.strip():
            st.error("❌ Owner name required!")
        else:
            try:
                account = bank.create_account(owner.strip(), acc_type, initial)
                st.success(f"✅ **Account Created!** ID: <span class='gold-accent'>{account.account_id}</span>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "💰 Deposit":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("💰 Quick Deposit")
    with st.form("deposit", clear_on_submit=True):
        acc_id = st.text_input("📱 Account ID")
        amount = st.number_input("💵 Amount", min_value=0.01, step=100.0, format="₹%.2f")
        submitted = st.form_submit_button("💰 DEPOSIT", use_container_width=True)
    
    if 'submitted' in locals() and submitted:
        try:
            new_balance = bank.deposit(acc_id.strip(), amount)
            st.success(f"✅ **Deposited!** New Balance: <span class='gold-accent'>₹{new_balance:.2f}</span>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "💸 Withdraw":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("💸 Fast Withdraw")
    with st.form("withdraw", clear_on_submit=True):
        acc_id = st.text_input("📱 Account ID")
        amount = st.number_input("💵 Amount", min_value=0.01, step=100.0, format="₹%.2f")
        submitted = st.form_submit_button("💸 WITHDRAW", use_container_width=True)
    
    if 'submitted' in locals() and submitted:
        try:
            new_balance = bank.withdraw(acc_id.strip(), amount)
            st.success(f"✅ **Withdrawn!** New Balance: <span class='gold-accent'>₹{new_balance:.2f}</span>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "🔍 Balance":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("🔍 Instant Balance")
    col1, col2 = st.columns([3,1])
    with col1: acc_id = st.text_input("📱 Account ID")
    with col2: if st.button("🔍 CHECK", use_container_width=True):
        try:
            balance = bank.check_balance(acc_id.strip())
            st.success(f"💰 **Balance**: <span class='gold-accent'>₹{balance:.2f}</span>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "🔄 Transfer":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("🔄 Secure Transfer")
    with st.form("transfer", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1: from_id = st.text_input("📤 From Account")
        with col2: to_id = st.text_input("📥 To Account")
        amount = st.number_input("💵 Amount", min_value=0.01, step=100.0, format="₹%.2f")
        submitted = st.form_submit_button("🔄 TRANSFER", use_container_width=True)
    
    if 'submitted' in locals() and submitted:
        try:
            bank.transfer(from_id.strip(), to_id.strip(), amount)
            st.success(f"✅ **Transferred ₹{amount:.2f}!** From {from_id} → {to_id}", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📈 Transactions":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("📈 Transaction Ledger")
    col1, col2 = st.columns([3,1])
    with col1: acc_id = st.text_input("📱 Account ID")
    with col2: if st.button("📊 LOAD", use_container_width=True):
        tx_list = db.fetch_transactions_for_account(acc_id.strip())
        if tx_list is not None and len(tx_list) > 0:
            st.dataframe(tx_list, use_container_width=True, height=400)
        else:
            st.info("📭 No transactions found")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📋 Reports":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("📋 Analytics Reports")
    summary = bank.get_bank_summary()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🏦 Total Accounts", summary["total_accounts"])
        st.metric("✅ Active Accounts", summary["active_accounts"])
    with col2:
        st.metric("💵 Total Balance", f"₹{summary['total_balance']:.2f}")
        st.metric("📊 Avg Balance", f"₹{summary['avg_balance']:.2f}")
    
    if db.get_all_accounts_summary() is not None:
        st.subheader("🏛️ All Accounts")
        st.dataframe(db.get_all_accounts_summary(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "🕵️ Audit Trail":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("🕵️ Audit Intelligence")
    recent_audit = db.get_recent_audit_logs(100)
    if recent_audit is not None and len(recent_audit) > 0:
        st.dataframe(recent_audit, use_container_width=True, height=500)
    else:
        st.info("🔒 Clean audit trail - no suspicious activity!")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Premium Footer ----------
st.markdown("""
<div class="footer">
    <h3 style='color: #D4AF37; margin-bottom: 1rem;'>💖 Created with Love</h3>
    <p style='margin: 0.5rem 0; color: #B0A89A;'>Mayank Goyal | Data Scientist & ML Engineer</p>
    <div style='margin-top: 1rem;'>
        <a href='https://github.com/mayank-goyal09' target='_blank' style='margin: 0 1rem; color: #D4AF37; text-decoration: none; font-weight: 600;'>🌐 GitHub</a>
        <a href='https://linkedin.com/in/mayank-goyal09' target='_blank' style='margin: 0 1rem; color: #D4AF37; text-decoration: none; font-weight: 600;'>💼 LinkedIn</a>
    </div>
    <p style='margin-top: 1rem; font-size: 0.9rem; color: #6B5E4A;'>Professional Banking System | Built with Python + Streamlit + SQLite</p>
</div>
""", unsafe_allow_html=True)
