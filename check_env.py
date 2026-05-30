from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path, override=True)

print(os.getenv("SUPABASE_URL"))