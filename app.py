import streamlit as st
from fpdf import FPDF

# Titel & Farben
titles = [
    ("Titel 1", "#E63946"),
    ("Titel 2", "#F1A208"),
    ("Titel 3", "#A8DADC"),
    ("Titel 4", "#457B9D"),
    ("Titel 5", "#1D3557"),
    ("Titel 6", "#2A9D8F"),
    ("Titel 7", "#E76F51"),
    ("Titel 8", "#6D597A"),
    ("Titel 9", "#FFB703"),
]

# Funktion zur Umrechnung Hex → RGB (für fpdf)
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_styled_grid_pdf(inputs, styles):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(False)

    box_width = 99
    box_height = 70

    for i in range(3):  # rows
        for j in range(3):  # cols
            idx = i * 3 + j
            x = j * box_width
            y = i * box_height

            # Box-Stil aus styles[] holen
            style = styles[idx]
            title = style["title"].replace("\\n", "\n")  # \n im String zu echtem Umbruch
            color = style["title_color"]
            font_size = style.get("font_size", 12)

            # Rechteck zeichnen
            pdf.rect(x, y, box_width, box_height)

            # Titel-Stil
            r, g, b = hex_to_rgb(color)
            pdf.set_text_color(r, g, b)
            
            # Unterstrichen + Fett, Schriftgröße evtl. abhängig von idx
            if idx == 4:
                pdf.set_font("Arial", style='BU', size=18)  # Box 5: fett + unterstrichen + größer
            else:
                pdf.set_font("Arial", style='BU', size=16)

            # Titel zeichnen (mit multi_cell wegen \n)
            pdf.set_xy(x + 2, y + 2)
            pdf.multi_cell(w=box_width - 4, h=7, txt=title, align='C')

            # Text (schwarz)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", size=style["font_size"])
            pdf.set_xy(x + 2, y + 20)  # weiter unten nach Titel
            line_height = style["font_size"] * 0.6
            pdf.multi_cell(w=box_width - 4, h=line_height, txt=inputs[idx], align='L')

    return pdf.output(dest='S').encode('latin1')


# Streamlit UI
st.title("3×3 PDF Raster mit farbigen Titeln")

inputs = []
for i, (title, _) in enumerate(titles):
    user_input = st.text_area(f"Text für {title}:", key=f"text_{i}")
    inputs.append(user_input)

if st.button("PDF generieren"):
    pdf_bytes = create_styled_grid_pdf(inputs)
    st.download_button("Download PDF", pdf_bytes, file_name="raster.pdf", mime="application/pdf")
