import requests
import pandas as pd

from database.db import SUPABASE_URL
from utils.config import HEADERS


def get_members():

    url = f"{SUPABASE_URL}/rest/v1/members?select=*"

    response = requests.get(
        url,
        headers=HEADERS
    )

    return pd.DataFrame(response.json())


def get_categories():

    url = f"{SUPABASE_URL}/rest/v1/categories?select=*"

    response = requests.get(
        url,
        headers=HEADERS
    )

    return pd.DataFrame(response.json())


def get_transactions():

    url = (
        f"{SUPABASE_URL}/rest/v1/transactions"
        "?select=*&order=id.desc"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    return pd.DataFrame(response.json())


def get_loans():

    url = (
        f"{SUPABASE_URL}/rest/v1/loans"
        "?select=*&order=id.desc"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    return pd.DataFrame(response.json())