import streamlit as st
import requests

from utils.timezone import today_ist

from database.db import SUPABASE_URL
from utils.config import HEADERS

from utils.common import (
get_members,
get_loans
)

from utils.logger import write_log

def show_loans():

st.title("🏦 Loan Management")

members_df = get_members()

if members_df.empty:

    st.warning(
        "No members available"
    )

    return

# -------------------------------------
# ROLE FILTER
# -------------------------------------

if st.session_state["current_role"] == "MEMBER":

    members_df = members_df[
        members_df["id"]
        ==
        st.session_state["current_member_id"]
    ]

# -------------------------------------
# LOAN ENTRY FORM
# -------------------------------------

with st.form("loan_form"):

    loan_type = st.selectbox(

        "Loan Type",

        [
            "LOAN_GIVEN",
            "LOAN_TAKEN"
        ]

    )

    member_name = st.selectbox(

        "Family Member",

        members_df["member_name"]

    )

    counterparty_name = st.text_input(
        "Borrower / Lender Name"
    )

    counterparty_type = st.selectbox(

        "Counterparty Type",

        [
            "BANK",
            "RELATIVE",
            "FRIEND",
            "OUTSIDER",
            "FINANCE_COMPANY"
        ]

    )

    payment_mode = st.selectbox(

        "Payment Mode",

        [
            "CASH",
            "UPI"
        ]

    )

    loan_amount = st.number_input(

        "Loan Amount",

        min_value=1.0,

        step=1.0

    )

    interest_rate = st.number_input(

        "Interest Rate (%)",

        min_value=0.0,

        value=0.0

    )

    emi_amount = st.number_input(

        "EMI Amount",

        min_value=0.0,

        value=0.0

    )

    due_date = st.date_input(

        "Due Date",

        value=today_ist()

    )

    remarks = st.text_input(
        "Remarks"
    )

    submit = st.form_submit_button(
        "💾 Save Loan"
    )

# -------------------------------------
# SAVE LOAN
# -------------------------------------

if submit:

    try:

        if not counterparty_name.strip():

            st.error(
                "Borrower / Lender Name is required"
            )

            return

        member = members_df[

            members_df["member_name"]

            ==

            member_name

        ].iloc[0]

        payload = {

            "loan_type":
            loan_type,

            "member_id":
            int(member["id"]),

            "member_name":
            member_name,

            "counterparty_name":
            counterparty_name.strip(),

            "counterparty_type":
            counterparty_type,

            "loan_date":
            str(today_ist()),

            "payment_mode":
            payment_mode,

            "loan_amount":
            loan_amount,

            "paid_amount":
            0,

            "pending_amount":
            loan_amount,

            "interest_rate":
            interest_rate,

            "emi_amount":
            emi_amount,

            "due_date":
            str(due_date),

            "remarks":
            remarks,

            "loan_status":
            "ACTIVE"

        }

        response = requests.post(

            f"{SUPABASE_URL}/rest/v1/loans",

            headers=HEADERS,

            json=payload

        )

        if response.status_code in [200, 201]:

            write_log(

                "CREATE",

                "LOAN",

                st.session_state[
                    "current_member_name"
                ],

                None,

                f"{loan_type} | "
                f"{counterparty_name} | "
                f"₹{loan_amount:,.2f}"

            )

            st.success(
                "Loan Saved Successfully"
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

# -------------------------------------
# LOAN REGISTER
# -------------------------------------

st.divider()

st.subheader(
    "📒 Loan Register"
)

loans_df = get_loans()

if loans_df.empty:

    st.info(
        "No loan records found"
    )

    return

if st.session_state["current_role"] == "MEMBER":

    loans_df = loans_df[

        loans_df["member_id"]

        ==

        st.session_state[
            "current_member_id"
        ]

    ]

st.dataframe(

    loans_df,

    use_container_width=True

)

# -------------------------------------
# SUMMARY
# -------------------------------------

st.divider()

total_given = loans_df[

    loans_df["loan_type"]

    ==

    "LOAN_GIVEN"

]["loan_amount"].sum()

total_taken = loans_df[

    loans_df["loan_type"]

    ==

    "LOAN_TAKEN"

]["loan_amount"].sum()

active_amount = loans_df[

    loans_df["loan_status"]

    ==

    "ACTIVE"

]["pending_amount"].sum()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        "Loan Given",

        f"₹ {total_given:,.2f}"

    )

with col2:

    st.metric(

        "Loan Taken",

        f"₹ {total_taken:,.2f}"

    )

with col3:

    st.metric(

        "Outstanding",

        f"₹ {active_amount:,.2f}"

    )

