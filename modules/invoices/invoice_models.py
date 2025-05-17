from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PartyInfo(BaseModel):
    userId: str
    name: str
    address: str
    phone: str
    email: Optional[str] = ""
    gstin: Optional[str] = ""


class InvoiceItem(BaseModel):
    partName: str
    modelNo: str
    category: str
    unitPrice: float
    quantity: int
    discountAmount: float = 0.0
    discountPercent: float = 0.0
    gst: float = 0.0
    totalPriceBeforeTax: Optional[float] = 0.0
    totalTaxAmount: Optional[float] = 0.0
    totalAmount: Optional[float] = 0.0


class InvoiceCreate(BaseModel):
    invoiceType: str  # "customer" or "platform"
    buyer: Optional[PartyInfo] = None
    seller: PartyInfo
    items: List[InvoiceItem]

    # Charges
    deliveryCharge: Optional[float] = 0.0
    platformFee: Optional[float] = 0.0
    deliveryChargeGst: Optional[float] = 0.0  # GST % on delivery
    platformFeeGst: Optional[float] = 0.0     # GST % on platform

    # Payment
    paymentMode: str
    paymentStatus: Optional[str] = "unpaid"  # unpaid, partial, paid
    paidAmount: Optional[float] = 0.0
    paymentDate: Optional[datetime] = None
    transactionId: Optional[str] = None

    # Invoice meta
    invoiceDate: str  # ISO format
    invoiceNumber: Optional[str] = None
    referenceNumber: Optional[str] = None
    createdBy: Optional[str] = None
    garageId: Optional[str] = None
    notes: Optional[str] = ""

    # Summary
    subTotal: Optional[float] = 0.0           # total before GST
    totalGst: Optional[float] = 0.0           # GST from item rows
    additionalGst: Optional[float] = 0.0      # GST from delivery/platform
    grandTotal: Optional[float] = 0.0         # sum of all

    # Assets
    invoicePdfUrl: Optional[str] = None
    signatureUrl: Optional[str] = None

    # System fields
    createdAt: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updatedAt: Optional[datetime] = None
    status: Optional[str] = "draft"           # draft, paid, cancelled, etc.
    version: Optional[int] = 1
    isDeleted: Optional[bool] = False
