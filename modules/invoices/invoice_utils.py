from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import DESCENDING

async def generate_invoice_number(collection: AsyncIOMotorCollection) -> str:
    today_str = datetime.utcnow().strftime("%Y%m%d")
    prefix = f"INV-{today_str}"

    try:
        last_invoice = await collection.find_one(
            {"invoiceNumber": {"$regex": f"^{prefix}-"}},
            sort=[("createdAt", DESCENDING)]
        )

        if last_invoice and "invoiceNumber" in last_invoice:
            parts = last_invoice["invoiceNumber"].split("-")
            last_number = int(parts[-1]) if parts[-1].isdigit() else 0
            next_number = f"{last_number + 1:03d}"
        else:
            next_number = "001"

    except Exception as e:
        print("⚠️ Error generating invoice number:", str(e))
        next_number = "001"

    return f"{prefix}-{next_number}"

def serialize_invoice(invoice: dict) -> dict:
    return {
        **invoice,
        "id": str(invoice.get("_id")),
        "_id": str(invoice.get("_id")),  # Optional: only if you want to preserve _id too
    }
