import csv
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

# Avery 8160 layout specs
PAGE_WIDTH, PAGE_HEIGHT = letter

LABEL_WIDTH = 2.625 * inch      # 2-5/8"
LABEL_HEIGHT = 1.0 * inch       # 1"
LEFT_MARGIN = 0.1875 * inch     # 3/16"
TOP_MARGIN = 0.5 * inch
HORIZONTAL_GAP = 0.125 * inch   # 1/8"
VERTICAL_GAP = 0.0             # No vertical gap

LABELS_PER_ROW = 3
LABELS_PER_COL = 10


def make_label_text(row):
    """
    Build the multi-line address text for each label.
    CSV should contain: name, address, city, state, zip, country
    """
    name = row.get("Name", "").strip()
    addr = row.get("Address", "").strip()
    city = row.get("City", "").strip()
    state = row.get("State", "").strip()
    zipc = row.get("Zip", "").strip()
    country = row.get("Country", "").strip()

    line2 = f"{city}, {state} {zipc}".strip().strip(",")
    
    if country and country.lower() not in ("usa", "united states", "us"):
        return f"{name}\n{addr}\n{line2}\n{country}"
    else:
        return f"{name}\n{addr}\n{line2}"


def draw_label(c, x, y, text):
    """
    Draw text for a single label at the given coordinate.
    """
    c.saveState()
    c.setFont("Helvetica", 10)
    text_obj = c.beginText(x + 0.1*inch, y + LABEL_HEIGHT - 0.2*inch)

    for line in text.split("\n"):
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.restoreState()


def csv_to_avery_8160(csv_file, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)

    with open(csv_file, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        labels = list(reader)

    label_index = 0

    for row in labels:
        col = label_index % LABELS_PER_ROW
        r = (label_index // LABELS_PER_ROW) % LABELS_PER_COL

        x = LEFT_MARGIN + col * (LABEL_WIDTH + HORIZONTAL_GAP)
        y = PAGE_HEIGHT - TOP_MARGIN - ((r + 1) * LABEL_HEIGHT) - (r * VERTICAL_GAP)

        label_text = make_label_text(row)
        draw_label(c, x, y, label_text)

        label_index += 1

        # Start new page after 30 labels
        if label_index % (LABELS_PER_ROW * LABELS_PER_COL) == 0:
            c.showPage()

    c.save()
    print(f"Created {output_pdf}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python make_labels.py <input.csv> <output.pdf>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_pdf = sys.argv[2]

    csv_to_avery_8160(input_csv, output_pdf)
