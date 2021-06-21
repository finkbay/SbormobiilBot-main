import os

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

django_token = os.getenv("DJANGO_TOKEN")

sqlite3_file = 'E:/pract/SbormobiilBot-main/tgadmin/db.sqlite3'
