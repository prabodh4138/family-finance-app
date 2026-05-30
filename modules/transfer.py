import streamlit as st
import requests

from database.db import SUPABASE_URL
from utils.config import HEADERS

from utils.common import get_members
from utils.logger import write_log
from utils.timezone import today_ist


def show_transfer():

    st.title("🔄 Family Member Transfer")

    members_df = get_members()

    if members_df.empty:

        st.warning(
            "No members available"
        )

        return

    # =====================================
    # FROM MEMBER
    # =====================================

    member_names = members_df[
        "member_name"
    ].tolist()

    from_member = st.selectbox(
        "From Member",
        member_names
    )

    from_row = members_df[
        members_df["member_name"] == from_member
    ].iloc[0]

    # =====================================
    # BALANCE PREVIEW
    # =====================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Cash Balance",
            f"₹ {float(from_row['cash_balance']):,.2f}"
        )

    with col2:

        st.metric(
            "UPI Balance",
            f"₹ {float(from_row['upi_balance']):,.2f}"
        )

    with col3:

        st.metric(
            "Total Balance",
            f"₹ {float(from_row['total_balance']):,.2f}"
        )

    # =====================================
    # TO MEMBER OPTIONS
    # =====================================

    to_member_options = [

        member

        for member in member_names

        if member != from_member

    ]

    # =====================================
    # FORM
    # =====================================

    with st.form("transfer_form"):

        transfer_date = st.date_input(
            "Transfer Date",
            value=today_ist()
        )

        to_member = st.selectbox(
            "To Member",
            to_member_options
        )

        payment_mode = st.selectbox(
            "Payment Mode",
            [
                "CASH",
                "UPI"
            ]
        )

        amount = st.number_input(
            "Transfer Amount",
            min_value=1.0,
            step=1.0
        )

        remarks = st.text_input(
            "Remarks"
        )

        submit = st.form_submit_button(
            "🔄 Transfer"
        )

    # =====================================
    # SAVE
    # =====================================

    if submit:

        try:

            to_row = members_df[
                members_df["member_name"] == to_member
            ].iloc[0]

            # ------------------------------
            # BALANCE VALIDATION
            # ------------------------------

            if payment_mode == "CASH":

                available_balance = float(
                    from_row["cash_balance"]
                )

            else:

                available_balance = float(
                    from_row["upi_balance"]
                )

            if amount > available_balance:

                st.error(
                    f"Insufficient {payment_mode} Balance"
                )

                return

            payload = {

                "transfer_date":
                str(transfer_date),

                "from_member_id":
                int(from_row["id"]),

                "from_member_name":
                from_member,

                "to_member_id":
                int(to_row["id"]),

                "to_member_name":
                to_member,

                "payment_mode":
                payment_mode,

                "amount":
                amount,

                "remarks":
                remarks

            }

            response = requests.post(

                f"{SUPABASE_URL}/rest/v1/member_transfers",

                headers=HEADERS,

                json=payload

            )

            if response.status_code in [200, 201]:

                write_log(

                    "TRANSFER",

                    "MEMBER_TRANSFER",

                    st.session_state.get(
                        "current_member_name",
                        "SYSTEM"
                    ),

                    None,

                    f"{from_member} → {to_member} | ₹{amount:,.2f} | {payment_mode}"

                )

                st.success(
                    "Transfer Successful"
                )

                st.rerun()

            else:

                st.error(
                    response.text
                )

        except Exception as e:

            st.error(
                f"Unexpected Error : {str(e)}"
            )

    # =====================================
    # MEMBER BALANCES
    # =====================================

    st.divider()

    st.subheader(
        "👨‍👩‍👧 Current Family Balances"
    )

    st.dataframe(

        members_df[
            [
                "member_name",
                "cash_balance",
                "upi_balance",
                "total_balance"
            ]
        ],

        use_container_width=True,
        hide_index=True

    )