import streamlit as st
import pandas as pd

from utils.common import (
    get_members,
    get_transactions
)

def show_dashboard():

    st.title("📊 Dashboard")

    members_df = get_members()

    if st.session_state["current_role"] == "MEMBER":

        members_df = members_df[
            members_df["id"] ==
            st.session_state["current_member_id"]
        ]

    if members_df.empty:

        st.warning("No members found")
        return

    total_cash = members_df["cash_balance"].sum()

    total_upi = members_df["upi_balance"].sum()

    total_balance = members_df["total_balance"].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Total Cash",
            f"₹ {total_cash:,.2f}"
        )

    with col2:
        st.metric(
            "📱 Total UPI",
            f"₹ {total_upi:,.2f}"
        )

    with col3:
        st.metric(
            "💰 Total Balance",
            f"₹ {total_balance:,.2f}"
        )

    st.divider()

    st.subheader("👨‍👩‍👧 Member Balances")

    st.dataframe(
        members_df[
            [
                "member_name",
                "cash_balance",
                "upi_balance",
                "total_balance"
            ]
        ],
        use_container_width=True
    )

    st.divider()

    transactions_df = get_transactions()

    if not transactions_df.empty:

        if st.session_state["current_role"] == "MEMBER":

            transactions_df = transactions_df[
                transactions_df["member_id"] ==
                st.session_state["current_member_id"]
            ]

        st.subheader("📒 Recent Transactions")

        st.dataframe(
            transactions_df.head(50),
            use_container_width=True
        )