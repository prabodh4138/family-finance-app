import streamlit as st

from utils.auth import login_screen

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="🏠 Family Finance ERP",
    page_icon="🏠",
    layout="wide"
)

# =====================================================
# LOGIN
# =====================================================

if not login_screen():
    st.stop()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🏠 Family Finance ERP")

    st.markdown("---")

    st.write(
        f"👤 {st.session_state.get('current_member_name', '')}"
    )

    st.write(
        f"🔑 {st.session_state.get('current_role', '')}"
    )

    st.markdown("---")

    menu_options = [

        "Dashboard",

        "Expense Entry",

        "Income Entry",

        "Transfer",

        "Loan Management",

        "Loan Repayment",

        "Analytics",

        "Reports",

        "Delete Transactions"

    ]

    # ------------------------------------------
    # ADMIN ONLY MENUS
    # ------------------------------------------

    if st.session_state.get("current_role") == "ADMIN":

        menu_options.extend([

            "Audit Logs"

        ])

    menu_options.append("Logout")

    menu = st.radio(
        "Navigation",
        menu_options
    )

# =====================================================
# ROUTER
# =====================================================

if menu == "Dashboard":

    from modules.dashboard import show_dashboard

    show_dashboard()

# =====================================================

elif menu == "Expense Entry":

    from modules.expense import show_expense

    show_expense()

# =====================================================

elif menu == "Income Entry":

    from modules.income import show_income

    show_income()

# =====================================================

elif menu == "Transfer":

    from modules.transfer import show_transfer

    show_transfer()

# =====================================================

elif menu == "Loan Management":

    from modules.loans import show_loans

    show_loans()

# =====================================================

elif menu == "Loan Repayment":

    from modules.repayment import show_repayment

    show_repayment()

# =====================================================

elif menu == "Analytics":

    from modules.analytics import show_analytics

    show_analytics()

# =====================================================

elif menu == "Reports":

    from modules.reports import show_reports

    show_reports()

# =====================================================

elif menu == "Delete Transactions":

    from modules.delete_transactions import show_delete

    show_delete()

# =====================================================

elif menu == "Audit Logs":

    from modules.audit_logs import (
        show_audit_logs
    )

    show_audit_logs()

# =====================================================

elif menu == "Logout":

    st.session_state.clear()

    st.success(
        "Logged out successfully."
    )

    st.rerun()