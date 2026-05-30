import requests

url = "https://maqujrsyrwrlirjodgoi.supabase.co"

try:
    response = requests.get(url)

    print(response.status_code)
    print(response.text)

except Exception as e:
    print(e)