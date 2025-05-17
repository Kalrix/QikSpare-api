from fastapi import APIRouter, HTTPException, Body, Depends, Query
from typing import Optional
from datetime import datetime
from bson import ObjectId
from pymongo.collection import Collection
from pymongo import DESCENDING

from modules.invoices.invoice_models import InvoiceCreate
from modules.invoices.invoice_utils import generate_invoice_number, serialize_invoice
from modules.invoices.invoice_service import compute_invoice_totals
from database import get_database
from motor.motor_asyncio import AsyncIOMotorCollection


router = APIRouter(prefix="/api/invoices", tags=["Invoices"])

# -------------------------------------
# MongoDB collection accessor
# -------------------------------------
def get_invoice_collection() -> Collection:
    db = get_database()
    return db["invoices"]


# -------------------------------------
# Create Invoice
# -------------------------------------
@router.post("/create")
async def create_invoice(
    data: InvoiceCreate = Body(...),
    collection: Collection = Depends(get_invoice_collection)
):
    invoice_data = compute_invoice_totals(data)
    invoice_dict = invoice_data.dict()

    invoice_dict["createdAt"] = datetime.utcnow()
    invoice_dict["updatedAt"] = datetime.utcnow()
    invoice_dict["invoiceNumber"] = await generate_invoice_number(collection)
    invoice_dict["isDeleted"] = False

    result = await collection.insert_one(invoice_dict)
    return {
        "message": "Invoice created",
        "invoice_id": str(result.inserted_id),
        "invoiceNumber": invoice_dict["invoiceNumber"]
    }


# -------------------------------------
# List Invoices with Filtering
# -------------------------------------
@router.get("/list")
async def list_invoices(
    status: Optional[str] = Query(None),
    garageId: Optional[str] = Query(None),
    from_date: Optional[str] = Query(None),  # Format: YYYY-MM-DD
    to_date: Optional[str] = Query(None),    # Format: YYYY-MM-DD
    collection: Collection = Depends(get_invoice_collection)
):
    filters = {"isDeleted": False}

    if status:
        filters["status"] = status
    if garageId:
        filters["garageId"] = garageId
    if from_date or to_date:
        filters["createdAt"] = {}
        if from_date:
            filters["createdAt"]["$gte"] = datetime.fromisoformat(from_date)
        if to_date:
            filters["createdAt"]["$lte"] = datetime.fromisoformat(to_date)

    cursor = collection.find(filters).sort("createdAt", DESCENDING)
    invoices = await cursor.to_list(length=1000)  # Limit to 1000 for safety

    return [serialize_invoice(inv) for inv in invoices]


# -------------------------------------
# Get One Invoice by ID
# -------------------------------------
@router.get("/{invoice_id}")
async def get_invoice(
    invoice_id: str,
    collection: Collection = Depends(get_invoice_collection)
):
    try:
        obj_id = ObjectId(invoice_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid invoice ID")

    invoice = await collection.find_one({"_id": obj_id, "isDeleted": False})
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return serialize_invoice(invoice)


# -------------------------------------
# Update Invoice
# -------------------------------------
@router.patch("/update/{invoice_id}")
async def update_invoice(
    invoice_id: str,
    update_data: dict = Body(...),
    collection: Collection = Depends(get_invoice_collection)
):
    try:
        obj_id = ObjectId(invoice_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid invoice ID")

    update_data["updatedAt"] = datetime.utcnow()

    result = await collection.update_one(
        {"_id": obj_id, "isDeleted": False},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Invoice not found or deleted")

    return {"message": "Invoice updated"}


# -------------------------------------
# Soft Delete Invoice
# -------------------------------------
@router.delete("/delete/{invoice_id}")
async def delete_invoice(
    invoice_id: str,
    collection: Collection = Depends(get_invoice_collection)
):
    try:
        obj_id = ObjectId(invoice_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid invoice ID")

    result = await collection.delete_one({"_id": obj_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return {"message": "Invoice hard deleted"}
