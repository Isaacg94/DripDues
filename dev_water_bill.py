import csv
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

UNIT_PRICE = 160
GARBAGE_CHARGE = 300
INPUT_FILE = 'meter_readings.csv'
OUTPUT_FILE = 'invoices.pdf'

# Add this function to create invoices in a PDF file
def create_invoice_pdf(invoices):
    # Define the page size and adjust the margins
    page_width, page_height = A4
    c = Canvas(OUTPUT_FILE, pagesize=(page_width, page_height))

    # Define the colors and font for the invoice
    red_color = (0.8, 0, 0)
    blue_color = (0, 0.2, 0.6)
    c.setFillColor(red_color)
    c.setStrokeColor(blue_color)
    c.setFont("Helvetica-Bold", 16)

    section_height = page_height / 4

    for i, invoice in enumerate(invoices):
        # Move to a new page after every 4 invoices
        if i % 4 == 0 and i > 0:
            c.showPage()

        # Calculate the vertical offset for the current invoice
        offset = section_height * (i % 4)

        # Draw the invoice
        c.drawString(inch, page_height - inch - offset, f"Graceland Apartments")
        c.setFillColor(blue_color)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(inch, page_height - inch * 1.5 - offset, f"House Number: {invoice['house']}  Month: {invoice['month']}")
        c.setFillColor(red_color)
        c.setFont("Helvetica", 12)
        c.drawString(inch, page_height - inch * 2 - offset, f"Previous Reading: {invoice['previous']}  Current Reading: {invoice['current']}")
        c.drawString(inch, page_height - inch * 2.5 - offset, f"Units Used: {invoice['units_used']}  Total Used: {invoice['total_used']:.2f}")
        c.drawString(inch, page_height - inch * 3 - offset, f"Garbage Charge: {GARBAGE_CHARGE}  Total Bill: {invoice['total_bill']:.2f}")

    c.save()

def calculate_bill(previous, current):
    units_used = current - previous
    total_used = units_used * UNIT_PRICE
    total_bill = total_used + GARBAGE_CHARGE
    return units_used, total_used, total_bill

def read_meter_readings():
    invoices = []

    with open(INPUT_FILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            month, house, previous, current = row['Month'], row['House'], float(row['Previous']), float(row['Current'])
            units_used, total_used, total_bill = calculate_bill(previous, current)

            # Save the invoice data
            invoice = {
                'month': month,
                'house': house,
                'previous': previous,
                'current': current,
                'units_used': units_used,
                'total_used': total_used,
                'total_bill': total_bill
            }
            invoices.append(invoice)

    # Create the PDF with the invoices
    create_invoice_pdf(invoices)

if __name__ == '__main__':
    read_meter_readings()
