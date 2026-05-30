import streamlit as st
import requests

from utils.timezone import today_ist

from database.db import SUPABASE_URL
from utils.config import HEADERS

from utils.common import (
    get_members,
    get_categories
)

from utils.logger import write_log


def show_expense():

    st.title("💸 Expense Entry")

    members_df = get_members()

    categories_df = get_categories()

    if members_df.empty:

        st.warning("No members available")

        return

    if categories_df.empty:

        st.warning("No categories available")

        return

    # ---------------------------------------
    # MEMBER SECURITY
    # ---------------------------------------

    if st.session_state["current_role"] == "MEMBER":

        members_df = members_df[
            members_df["id"] ==
            st.session_state["current_member_id"]
        ]

    # ---------------------------------------
    # FORM
    # ---------------------------------------

    with st.form("expense_form"):

        txn_date = st.date_input(
            "Transaction Date",
            value=today_ist()
        )

        member_name = st.selectbox(
            "Member",
            members_df["member_name"]
        )

        category = st.selectbox(
            "Category",
            categories_df["category_name"]
        )

        payment_mode = st.selectbox(
            "Payment Mode",
            [
                "CASH",
                "UPI"
            ]
        )

        amount = st.number_input(
            "Amount",
            min_value=1.0,
            step=1.0
        )

        remarks = st.text_input(
            "Remarks"
        )

        submit = st.form_submit_button(
            "💾 Save Expense"
        )

    # ---------------------------------------
    # SAVE
    # ---------------------------------------

    if submit:

        try:

            member = members_df[
                members_df["member_name"] ==
                member_name
            ].iloc[0]

            # -------------------------------
            # BALANCE VALIDATION
            # -------------------------------

            if payment_mode == "CASH":

                if amount > float(
                    member["cash_balance"]
                ):

                    st.error(
                        "Insufficient Cash Balance"
                    )

                    return

            if payment_mode == "UPI":

                if amount > float(
                    member["upi_balance"]
                ):

                    st.error(
                        "Insufficient UPI Balance"
                    )

                    return

            payload = {

                "member_id":
                int(member["id"]),

                "member_name":
                member_name,

                "txn_date":
                str(txn_date),

                "txn_type":
                "EXPENSE",

                "category":
                category,

                "payment_mode":
                payment_mode,

                "amount":
                amount,

                "remarks":
                remarks

            }

            response = requests.post(

                f"{SUPABASE_URL}/rest/v1/transactions",

                headers=HEADERS,

                json=payload

            )

            if response.status_code in [200, 201]:

                # ---------------------------
                # AUDIT LOG
                # ---------------------------

                write_log(

                    "CREATE",

                    "EXPENSE",

                    st.session_state[
                        "current_member_name"
                    ],

                    None,

                    f"Expense ₹{amount:,.2f} "
                    f"| Category={category} "
                    f"| Mode={payment_mode}"

                )

                st.success(
                    "Expense Saved Successfully"
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
                    f"Save Failed : "
                    f"{error_message}"
                )

        except Exception as e:

            st.error(
                f"Unexpected Error : {str(e)}"
            )