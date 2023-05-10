import locale 

import csv

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from datetime import datetime

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Register the font with ReportLab
pdfmetrics.registerFont(TTFont('RobotoMono', './fonts/RobotoMono-Regular.ttf'))
pdfmetrics.registerFont(TTFont('RobotoMono-Bold', './fonts/RobotoMono-Bold.ttf'))
pdfmetrics.registerFont(TTFont('RobotoMono-Medium', './fonts/RobotoMono-Medium.ttf'))

pdfmetrics.registerFont(TTFont('Inconsolata', './fonts/Inconsolata-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Inconsolata-Bold', './fonts/Inconsolata-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Inconsolata-Medium', './fonts/Inconsolata-SemiBold.ttf'))

# Sets the current Time of Month & Year
today = datetime.now()
currentMonth = today.strftime("%b")
currentYear = today.strftime('%Y')


def create_apartment_tables(apartment_data, meter_readings_table_width, notes_table_width, billing_details_table_width):
    previous_meter_reading = float(apartment_data[2])
    current_meter_reading = float(apartment_data[3])
    units_used = round((current_meter_reading - previous_meter_reading))
    unit_price = 160
    unit_price_formatted = f"Ksh {locale.format_string('%d', unit_price, grouping=True)}"
    water_bill = round((units_used * unit_price))
    garbage_fee = 300
    total_bill = water_bill + garbage_fee
    total_bill_formatted = f"Ksh {locale.format_string('%d', total_bill, grouping=True)}"
    house_number = apartment_data[1].upper()

    # Define the meter readings table data
    meter_readings_data = [
        ["Meter Readings", "Amount"],
        ["Previous Meter Reading", previous_meter_reading],
        ["Current Meter Reading", current_meter_reading],
        ["Units Used", units_used],
        ["Unit Price", unit_price_formatted],
    ]

    # Define the notes table data
    notes_data = [
        ["House Number:" + " " + house_number ],
        [currentMonth + ", " + currentYear ],
        ["Graceland Apartments"],
        [""],
        [""],
    ]

    # Define the billing details table data
    billing_details_data = [
        ["Description", "Amount"],
        ["Water Bill", water_bill],
        ["Garbage Fee", garbage_fee],
        [""],
        ["Total Bill", total_bill_formatted],
    ]


    # Create Table objects with the data
    meter_readings_table = Table(meter_readings_data)
    notes_table = Table(notes_data)
    billing_details_table = Table(billing_details_data)
    

    # Set table styles
    meter_readings_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Inconsolata-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 1), (-1, -1), "Inconsolata")
            ]
        )
    )

    notes_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Inconsolata-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 1), (-1, -1), "Inconsolata")
            ]
        )
    )

    billing_details_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Inconsolata-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Inconsolata"),
                ("FONTNAME", (0, -1), (-1, -1), "RobotoMono-Bold"),  # Apply bold font to the last row
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    

    # Set the width of each table
    meter_readings_table._argW[0] = meter_readings_table_width * 2/3
    meter_readings_table._argW[1] = meter_readings_table_width / 3
    notes_table._argW[0] = notes_table_width
    billing_details_table._argW[0] = billing_details_table_width / 2
    billing_details_table._argW[1] = billing_details_table_width / 2


    

    return [meter_readings_table, notes_table, billing_details_table,]


# Read the CSV file
meter_readings_file = "meter_readings.csv"

with open(meter_readings_file, newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    next(csvreader)  # Skip header row
    meter_readings_data = [row for row in csvreader]

# Create a Canvas object for the PDF
c = canvas.Canvas(currentMonth + ", " + currentYear + " Graceland Water Invoices.pdf", pagesize=A4)

# Define the margins
left_margin = 0.2 * inch
right_margin = A4[0] - 0.2 * inch
top_margin = A4[1] - 0.2 * inch
bottom_margin = 0.2 * inch

# Calculate the available width for the tables
available_width = right_margin - left_margin

num_apartments_per_page = 7
vertical_spacing = 0.27 * inch

# Set the width of each table
meter_readings_table_width = available_width / 3
notes_table_width = available_width / 3
billing_details_table_width = available_width / 3




for i, apartment_data in enumerate(meter_readings_data):
    if i % num_apartments_per_page == 0 and i != 0:
        c.showPage()  # Move to the next page after every 7 apartments

    # Create tables for the current apartment
    tables = create_apartment_tables(apartment_data, meter_readings_table_width, notes_table_width, billing_details_table_width,)

    # Calculate the height of the tallest table
    table_heights = [t.wrapOn(c, available_width, top_margin)[1] for t in tables]
    max_table_height = max(table_heights)

    # Calculate the vertical offset for the current apartment
    vertical_offset = top_margin - (i % num_apartments_per_page) * (max_table_height + vertical_spacing)

   # Draw the tables on the canvas with the calculated vertical offset and adjusted starting positions
    tables[0].drawOn(c, left_margin, vertical_offset - table_heights[0])
    tables[1].drawOn(c, left_margin + meter_readings_table_width, vertical_offset - table_heights[1])
    tables[2].drawOn(c, left_margin + meter_readings_table_width + notes_table_width, vertical_offset - table_heights[2])



# Save the canvas as a PDF
c.save()

