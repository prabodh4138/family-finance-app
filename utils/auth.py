import streamlit as st
import requests

from database.db import (
    SUPABASE_URL,
    SUPABASE_KEY
)

from utils.config import HEADERS


def login_screen():

    if st.session_state.get("logged_in"):

        return True

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown(
            """
            <h1 style='text-align:center'>
            🏠 Family Finance ERP
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        email = st.text_input("📧 Email")

        password = st.text_input(
            "🔑 Password",
            type="password"
        )

        login_button = st.button(
            "Login",
            use_container_width=True
        )

    if login_button:

        auth_url = (
            f"{SUPABASE_URL}"
            "/auth/v1/token?grant_type=password"
        )

        auth_headers = {
            "apikey": SUPABASE_KEY,
            "Content-Type": "application/json"
        }

        auth_data = {
            "email": email,
            "password": password
        }

        auth_response = requests.post(
            auth_url,
            headers=auth_headers,
            json=auth_data
        )

        if auth_response.status_code == 200:

            auth_result = auth_response.json()

            user_id = auth_result["user"]["id"]

            role_url = (
                f"{SUPABASE_URL}/rest/v1/app_users"
                f"?select=*"
                f"&auth_user_id=eq.{user_id}"
            )

            role_response = requests.get(
                role_url,
                headers=HEADERS
            )

            role_data = role_response.json()

            if len(role_data) == 0:

                st.error(
                    "User role not assigned"
                )

                return False

            st.session_state["logged_in"] = True

            st.session_state["user_id"] = user_id

            st.session_state["current_role"] = (
                role_data[0]["role"]
            )

            st.session_state["current_member_id"] = (
                role_data[0]["member_id"]
            )

            st.session_state["current_member_name"] = (
                role_data[0]["member_name"]
            )

            st.rerun()

        else:

            st.error(
                "Invalid Email or Password"
            )

    return False