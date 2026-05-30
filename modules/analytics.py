import streamlit as st
import pandas as pd
import plotly.express as px

from utils.common import (
    get_transactions,
    get_loans
)

def show_analytics():

    st.title("📊 Analytics Dashboard")

    df = get_transactions()

    if df.empty:

        st.info("No transaction data")

        return

    expense_df = df[
        df["txn_type"] == "EXPENSE"
    ]

    income_df = df[
        df["txn_type"] == "INCOME"
    ]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Expense",
            f"₹ {expense_df['amount'].sum():,.2f}"
        )

    with col2:

        st.metric(
            "Income",
            f"₹ {income_df['amount'].sum():,.2f}"
        )

    with col3:

        st.metric(
            "Savings",
            f"₹ {(income_df['amount'].sum()-expense_df['amount'].sum()):,.2f}"
        )

    st.divider()

    category_df = expense_df.groupby(
        "category"
    )["amount"].sum().reset_index()

    fig = px.pie(
        category_df,
        names="category",
        values="amount",
        hole=0.4
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    loans_df = get_loans()

    if not loans_df.empty:

        loan_summary = loans_df.groupby(
            "loan_type"
        )["loan_amount"].sum().reset_index()

        fig2 = px.bar(
            loan_summary,
            x="loan_type",
            y="loan_amount"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )