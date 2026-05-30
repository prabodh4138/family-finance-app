import streamlit as st
import pandas as pd
from io import BytesIO

from utils.common import (
    get_transactions,
    get_loans
)

def show_reports():

    st.title("📤 Reports")

    transactions_df = get_transactions()

    if not transactions_df.empty:

        buffer = BytesIO()

        with pd.ExcelWriter(
            buffer,
            engine="openpyxl"
        ) as writer:

            transactions_df.to_excel(
                writer,
                index=False
            )

        buffer.seek(0)

        st.download_button(

            "Download Transaction Report",

            buffer,

            "transactions.xlsx",

            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )

    loans_df = get_loans()

    if not loans_df.empty:

        loan_buffer = BytesIO()

        with pd.ExcelWriter(
            loan_buffer,
            engine="openpyxl"
        ) as writer:

            loans_df.to_excel(
                writer,
                index=False
            )

        loan_buffer.seek(0)

        st.download_button(

            "Download Loan Report",

            loan_buffer,

            "loans.xlsx",

            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )