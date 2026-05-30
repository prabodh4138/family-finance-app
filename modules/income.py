import streamlit as st
import requests

from utils.timezone import today_ist

from database.db import SUPABASE_URL
from utils.config import HEADERS

from utils.common import (
    get_members
)

from utils.logger import write_log


def show_income():

    st.title("💰 Income Entry")

    members_df = get_members()

    if members_df.empty:

        st.warning(
            "No members available"
        )

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

    with st.form("income_form"):

        txn_date = st.date_input(
            "Transaction Date",
            value=today_ist()
        )

        member_name = st.selectbox(
            "Member",
            members_df["member_name"]
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
            "💾 Save Income"
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

            payload = {

                "member_id":
                int(member["id"]),

                "member_name":
                member_name,

                "txn_date":
                str(txn_date),

                "txn_type":
                "INCOME",

                "category":
                "INCOME",

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

                # -----------------------------------
                # AUDIT LOG
                # -----------------------------------

                write_log(

                    "CREATE",

                    "INCOME",

                    st.session_state[
                        "current_member_name"
                    ],

                    None,

                    f"Income ₹{amount:,.2f} "
                    f"| Mode={payment_mode}"

                )

                st.success(
                    "Income Saved Successfully"
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