import streamlit as st
import requests
import pandas as pd

from database.db import SUPABASE_URL
from utils.config import HEADERS


def show_audit_logs():

    st.title("📜 Audit Logs")

    # ------------------------------------
    # ADMIN SECURITY
    # ------------------------------------

    if st.session_state["current_role"] != "ADMIN":

        st.error(
            "Only ADMIN users can view audit logs."
        )

        return

    # ------------------------------------
    # LOAD LOGS
    # ------------------------------------

    try:

        response = requests.get(

            f"{SUPABASE_URL}/rest/v1/audit_logs"
            "?select=*"
            "&order=id.desc",

            headers=HEADERS

        )

        if response.status_code != 200:

            st.error(
                f"Failed to load logs : {response.text}"
            )

            return

        logs_df = pd.DataFrame(
            response.json()
        )

        if logs_df.empty:

            st.info(
                "No audit logs found."
            )

            return

        # --------------------------------
        # FILTERS
        # --------------------------------

        st.subheader(
            "🔍 Filters"
        )

        col1, col2 = st.columns(2)

        with col1:

            action_filter = st.selectbox(
                "Action Type",
                ["ALL"] +
                sorted(
                    logs_df[
                        "action_type"
                    ].dropna().unique()
                )
            )

        with col2:

            module_filter = st.selectbox(
                "Module",
                ["ALL"] +
                sorted(
                    logs_df[
                        "module_name"
                    ].dropna().unique()
                )
            )

        filtered_df = logs_df.copy()

        if action_filter != "ALL":

            filtered_df = filtered_df[
                filtered_df[
                    "action_type"
                ] == action_filter
            ]

        if module_filter != "ALL":

            filtered_df = filtered_df[
                filtered_df[
                    "module_name"
                ] == module_filter
            ]

        # --------------------------------
        # SUMMARY
        # --------------------------------

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Logs",
                len(filtered_df)
            )

        with col2:

            st.metric(
                "Users Involved",
                filtered_df[
                    "user_name"
                ].nunique()
            )

        # --------------------------------
        # DISPLAY
        # --------------------------------

        st.divider()

        st.subheader(
            "📋 Audit Log Records"
        )

        st.dataframe(

            filtered_df[
                [
                    "id",
                    "action_type",
                    "module_name",
                    "user_name",
                    "record_id",
                    "description",
                    "created_at"
                ]
            ],

            use_container_width=True,
            hide_index=True

        )

        # --------------------------------
        # EXPORT
        # --------------------------------

        csv = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(

            label="⬇ Download Audit Logs",

            data=csv,

            file_name="audit_logs.csv",

            mime="text/csv"

        )

    except Exception as e:

        st.error(
            f"Unexpected Error : {str(e)}"
        )