import streamlit as st
from fpdf import FPDF

monate = [
    'Jänner','Februar','März','April','Mai','Juni',
    'Juli','August','September','Oktober','November','Dezember'
]

# Pre-Set Überschriften
titel = [
"Fantasie, Kreativität und\nkünstlerisches Gestalten",
"Musik",
"Motorik",
"Sprache, Kommunikation\nund Medien",
"",
"Körper, Umwelt und\nGesundheit",
"Soziales und Gesundheit",
"Wahrnehmung, Emotion und\nKognition",
"Mathematik,\nNaturwissenschaft und\nTechnik"
]

# Pre-Set Farben
farben = [
"#C00798",
"#932ECE",
"#47E3FF",
"#93FF2F",
"",
"#239B89",
"#FF8800",
"#198628",
"#D9E900"
]
# Funktion zur Umrechnung Hex → RGB (für fpdf)
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# PDF erzeugen
def create_grid_pdf(monat, titel, farben):
    pdf = FPDF(orientation='L', unit= 'mm', format= 'A4')
    pdf.add_page() # erzeugt überhaupt erste Seite
    pdf.set_auto_page_break(False) # keine automatischen neuen Seiten

    box_width = 91 # mm
    box_height = 62 # mm

    page_width = 273 # mm
    page_height = 210 #mm

    for i in range(3): #row
        for j in range(3): #col
            indx = i*3 + j
            x = j * box_width
            y =  i * box_height

            # Offset für Druck kreieren
            x = x+12 
            y= y+12

            # Box zeichnen
            pdf.rect(x,y,box_width, box_height)

            # Überschriften und Monat schreiben
            if indx == 4:
                pdf.set_xy(x+2, y + (box_height-8)/2)
                pdf.set_font('Helvetica', size=40, style='B')
                pdf.set_text_color(0,0,0)
                pdf.multi_cell(w= box_width-4, h=8, txt=monat, align= 'C')
            else:
                pdf.set_xy(x+2, y+2) # 2mm Padding
                pdf.set_font('Helvetica', size=18, style='BU')
                r, g, b = hex_to_rgb(farben[indx])
                pdf.set_text_color(r, g, b)
                pdf.multi_cell(w= box_width-4, h=8, txt=titel[indx], align= 'C')
            
            # Inhalt / Text einfügen
            if indx == 4:
                pass
            else:
                pdf.set_xy(x+2, y+25) # 2mm Padding
                pdf.set_font('Helvetica', size=14)
                r, g, b = hex_to_rgb(farben[indx])
                pdf.set_text_color(r, g, b)
                pdf.multi_cell(w= box_width-4, h=8, txt=input_data[indx], align= 'C')

    return pdf.output(dest='S').encode('latin1')


# UI auf Streamlit
st.title('Lotus Generator')
st.subheader('Monat eingeben')
monat = st.selectbox('Monat auswählen', monate)

input_data=[]
for i in range(len(titel)):
    if i ==4:
        pass
    input = st.text_area(titel[i])
    input_data.append(input)

if st.button("PDF generieren"):
    pdf_bytes = create_grid_pdf(monat,titel,farben)
    st.download_button("Download PDF", pdf_bytes, file_name="raster.pdf", mime="application/pdf")