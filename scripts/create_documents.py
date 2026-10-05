from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path


# Project मधील documents folder
DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "documents"

DOCUMENTS_DIR.mkdir(exist_ok=True)


def create_pdf(filename, title, lines):
    """
    Creates a simple text-based PDF.
    """
    file_path = DOCUMENTS_DIR / filename

    c = canvas.Canvas(str(file_path), pagesize=A4)

    width, height = A4
    y = height - 60

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, title)

    y -= 35

    # Body
    c.setFont("Helvetica", 11)

    for line in lines:
        if y < 60:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = height - 60

        c.drawString(50, y, line)
        y -= 20

    c.save()

    print(f"Created: {file_path}")


# ---------------------------------------------------------
# 1. Supplier Invoice 01
# ---------------------------------------------------------

create_pdf(
    "supplier_invoice_01.pdf",
    "SMARTSTOCK SUPPLIER INVOICE",
    [
        "Invoice Number: INV-001",
        "Supplier: MedSupply Pvt Ltd",
        "Invoice Date: 15 December 2025",
        "",
        "Medicine: Paracetamol 500mg",
        "Quantity: 1000 tablets",
        "Current Unit Price: Rs. 2.50",
        "Total Amount: Rs. 2500",
        "",
        "Previous Purchase Details:",
        "Previous Unit Price: Rs. 2.30",
        "Previous Purchase Date: 10 November 2025",
        "",
        "Payment Terms: 30 days",
        "Document Type: Supplier Invoice",
    ],
)


# ---------------------------------------------------------
# 2. Supplier Invoice 02
# ---------------------------------------------------------

create_pdf(
    "supplier_invoice_02.pdf",
    "SMARTSTOCK SUPPLIER INVOICE",
    [
        "Invoice Number: INV-002",
        "Supplier: HealthCare Distributors",
        "Invoice Date: 20 January 2026",
        "",
        "Medicine: Paracetamol 500mg",
        "Quantity: 1500 tablets",
        "Current Unit Price: Rs. 2.60",
        "Total Amount: Rs. 3900",
        "",
        "Previous Purchase Details:",
        "Previous Unit Price: Rs. 2.40",
        "Previous Purchase Date: 18 December 2025",
        "",
        "Payment Terms: 30 days",
        "Document Type: Supplier Invoice",
    ],
)


# ---------------------------------------------------------
# 3. Medicine Policy
# ---------------------------------------------------------

create_pdf(
    "medicine_policy.pdf",
    "SMARTSTOCK MEDICINE STORAGE POLICY",
    [
        "1. Medicines must be stored according to manufacturer instructions.",
        "",
        "2. Temperature-sensitive medicines must be kept within",
        "   the recommended temperature range.",
        "",
        "3. Expired medicines must not be issued to patients.",
        "",
        "4. Medicines approaching expiry should be identified",
        "   during inventory review.",
        "",
        "5. Stock records should be updated regularly.",
        "",
        "6. Pharmacy staff should verify medicine condition",
        "   before dispensing.",
    ],
)


# ---------------------------------------------------------
# 4. Procurement Policy
# ---------------------------------------------------------

create_pdf(
    "procurement_policy.pdf",
    "SMARTSTOCK PROCUREMENT POLICY",
    [
        "1. Reorder recommendations must be reviewed by",
        "   authorised pharmacy staff.",
        "",
        "2. Supplier information must be verified before",
        "   placing an order.",
        "",
        "3. Previous supplier invoices may be consulted",
        "   when reviewing historical prices.",
        "",
        "4. Procurement orders require human approval",
        "   before dispatch.",
        "",
        "5. Supplier communication should contain medicine",
        "   name, quantity and relevant purchase details.",
    ],
)


print("")
print("===================================")
print("All SmartStock PDFs created!")
print("===================================")