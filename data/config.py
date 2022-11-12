import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))

admins = [
    33180657,
    456954476
]

ip = os.getenv("ip")
db_host = ip  # Если вы запускаете базу не через докер!
# db_host = "db"  # Если вы запускаете базу через докер и у вас в services стоит название базы db


aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

banned_users = [
    123421342,
    432412341
]

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{db_host}/{DATABASE}"
