from modules.invoices.invoice_models import InvoiceCreate, InvoiceItem


def compute_invoice_totals(invoice: InvoiceCreate) -> InvoiceCreate:
    sub_total = 0.0
    total_gst = 0.0
    grand_total = 0.0

    for item in invoice.items:
        price = item.unitPrice * item.quantity
        discount = item.discountAmount or (price * (item.discountPercent / 100))
        taxable = price - discount
        gst_amount = taxable * (item.gst / 100)
        total = taxable + gst_amount

        # Set calculated fields in item
        item.totalPriceBeforeTax = taxable
        item.totalTaxAmount = gst_amount
        item.totalAmount = total

        sub_total += taxable
        total_gst += gst_amount
        grand_total += total

    grand_total += invoice.deliveryCharge or 0
    grand_total += invoice.platformFee or 0

    invoice.subTotal = round(sub_total, 2)
    invoice.totalGst = round(total_gst, 2)
    invoice.grandTotal = round(grand_total, 2)

    return invoice
