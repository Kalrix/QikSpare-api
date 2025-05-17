from database import connect_to_mongo_sync, get_database
from bson import ObjectId
from datetime import datetime
import hashlib

def hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()

def main():
    connect_to_mongo_sync()
    db = get_database()

    admin_data = {
        "_id": ObjectId(),
        "full_name": "Himanshu Nehra",
        "phone": "9873313311",
        "email": "admin2@qikspare.com",
        "role": "admin",
        "pin": hash_pin("0000"),
        "created_at": datetime.utcnow()
    }

    db["users"].insert_one(admin_data)
    print("✅ Admin created:", admin_data)

if __name__ == "__main__":
    main()
