import streamlit as st
import requests

from utils.timezone import today_ist

from database.db import SUPABASE_URL
from utils.config import HEADERS

from utils.common import (
    get_loans
)

from utils.logger import write_log


def show_repayment():

    st.title("💳 Loan Repayment")

    loans_df = get_loans()

    if loans_df.empty:

        st.info(
            "No loan records found"
        )

        return

    # --------------------------------------
    # MEMBER FILTER
    # --------------------------------------

    if st.session_state["current_role"] == "MEMBER":

        loans_df = loans_df[
            loans_df["member_id"] ==
            st.session_state["current_member_id"]
        ]

    active_loans = loans_df[
        loans_df["loan_status"] == "ACTIVE"
    ]

    if active_loans.empty:

        st.info(
            "No active loans found"
        )

        return

    # --------------------------------------
    # LOAN SELECTION
    # --------------------------------------

    loan_display = [

        f"ID {row['id']} | "
        f"{row['counterparty_name']} | "
        f"Pending ₹{row['pending_amount']:,.2f}"

        for _, row in active_loans.iterrows()

    ]

    selected_display = st.selectbox(
        "Select Active Loan",
        loan_display
    )

    selected_index = loan_display.index(
        selected_display
    )

    selected = active_loans.iloc[
        selected_index
    ]

    st.info(

        f"""
Member : {selected['member_name']}

Counterparty : {selected['counterparty_name']}

Loan Type : {selected['loan_type']}

Pending Amount : ₹{selected['pending_amount']:,.2f}
        """

    )

    # --------------------------------------
    # FORM
    # --------------------------------------

    payment_date = st.date_input(
        "Payment Date",
        value=today_ist()
    )

    repayment_amount = st.number_input(
        "Repayment Amount",
        min_value=1.0,
        step=1.0
    )

    payment_mode = st.selectbox(
        "Payment Mode",
        [
            "CASH",
            "UPI"
        ]
    )

    remarks = st.text_input(
        "Remarks"
    )

    # --------------------------------------
    # SAVE
    # --------------------------------------

    if st.button("💾 Save Repayment"):

        try:

            pending_amount = float(
                selected["pending_amount"]
            )

            if repayment_amount > pending_amount:

                st.error(
                    f"""
Repayment amount cannot exceed
pending amount.

Pending Amount:
₹ {pending_amount:,.2f}
                    """
                )

                return

            payload = {

                "loan_id":
                int(selected["id"]),

                "member_id":
                int(selected["member_id"]),

                "member_name":
                selected["member_name"],

                "counterparty_name":
                selected["counterparty_name"],

                "payment_date":
                str(payment_date),

                "payment_type":
                "LOAN_REPAYMENT",

                "payment_mode":
                payment_mode,

                "amount":
                repayment_amount,

                "remarks":
                remarks

            }

            response = requests.post(

                f"{SUPABASE_URL}/rest/v1/loan_transactions",

                headers=HEADERS,

                json=payload

            )

            if response.status_code in [200, 201]:

                # ----------------------------------
                # AUDIT LOG
                # ----------------------------------

                write_log(

                    "REPAYMENT",

                    "LOAN",

                    st.session_state[
                        "current_member_name"
                    ],

                    int(selected["id"]),

                    f"""
Loan Repayment

₹{repayment_amount:,.2f}

Counterparty:
{selected['counterparty_name']}
                    """

                )

                st.success(
                    "Repayment Saved Successfully"
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

    # --------------------------------------
    # ACTIVE LOAN SUMMARY
    # --------------------------------------

    st.divider()

    total_pending = active_loans[
        "pending_amount"
    ].sum()

    total_paid = active_loans[
        "paid_amount"
    ].sum()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Outstanding Amount",
            f"₹ {total_pending:,.2f}"
        )

    with col2:

        st.metric(
            "Recovered Amount",
            f"₹ {total_paid:,.2f}"
        )
