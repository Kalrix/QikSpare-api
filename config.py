import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "development")
MONGO_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "qikspare")
JWT_SECRET = os.getenv("JWT_SECRET")
