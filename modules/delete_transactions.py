import streamlit as st
import requests

from database.db import SUPABASE_URL
from utils.config import HEADERS

from utils.common import (
    get_transactions
)

from utils.logger import write_log


def show_delete():

    st.title("🗑 Delete Transactions")

    # --------------------------------------
    # ADMIN SECURITY
    # --------------------------------------

    if st.session_state["current_role"] != "ADMIN":

        st.error(
            "Only ADMIN users can delete transactions."
        )

        return

    transactions_df = get_transactions()

    if transactions_df.empty:

        st.info(
            "No transactions found."
        )

        return

    # --------------------------------------
    # SELECT TRANSACTION
    # --------------------------------------

    txn_display = [

        f"ID {row['id']} | "
        f"{row['txn_date']} | "
        f"{row['member_name']} | "
        f"{row['txn_type']} | "
        f"₹{row['amount']:,.2f}"

        for _, row in transactions_df.iterrows()

    ]

    selected_display = st.selectbox(
        "Select Transaction",
        txn_display
    )

    selected_index = txn_display.index(
        selected_display
    )

    selected = transactions_df.iloc[
        selected_index
    ]

    # --------------------------------------
    # PREVIEW
    # --------------------------------------

    st.subheader(
        "Transaction Details"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"Transaction ID : {selected['id']}"
        )

        st.write(
            f"Date : {selected['txn_date']}"
        )

        st.write(
            f"Member : {selected['member_name']}"
        )

        st.write(
            f"Type : {selected['txn_type']}"
        )

    with col2:

        st.write(
            f"Category : {selected['category']}"
        )

        st.write(
            f"Mode : {selected['payment_mode']}"
        )

        st.write(
            f"Amount : ₹{selected['amount']:,.2f}"
        )

        st.write(
            f"Remarks : {selected['remarks']}"
        )

    st.warning(
        """
        WARNING:

        Deleting a transaction will permanently remove it.

        This action cannot be undone.
        """
    )

    # --------------------------------------
    # CONFIRMATION
    # --------------------------------------

    confirm = st.checkbox(
        "I understand this action cannot be undone"
    )

    # --------------------------------------
    # DELETE
    # --------------------------------------

    if confirm:

        if st.button(
            "🗑 Permanently Delete Transaction"
        ):

            try:

                response = requests.delete(

                    f"{SUPABASE_URL}/rest/v1/transactions?id=eq.{selected['id']}",

                    headers=HEADERS

                )

                if response.status_code in [200, 204]:

                    # ----------------------------------
                    # AUDIT LOG
                    # ----------------------------------

                    write_log(

                        "DELETE",

                        "TRANSACTION",

                        st.session_state[
                            "current_member_name"
                        ],

                        int(selected["id"]),

                        f"""
                        Deleted Transaction

                        ID={selected['id']}

                        Member={selected['member_name']}

                        Type={selected['txn_type']}

                        Amount=₹{selected['amount']:,.2f}
                        """

                    )

                    st.success(
                        "Transaction Deleted Successfully"
                    )

                    st.rerun()

                else:

                    try:

                        error_message = (
                            response.json()
                        )

                    except:

                        error_message = (
                            response.text
                        )

                    st.error(
                        f"Delete Failed : "
                        f"{error_message}"
                    )

            except Exception as e:

                st.error(
                    f"Unexpected Error : {str(e)}"
                )

    else:

        st.info(
            "Tick the confirmation checkbox to enable deletion."
        )