import streamlit as st
import pymupdf
import io
from pathlib import Path
import zipfile
import datetime

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🖨 Firmar PDF")

st.markdown("""
    1. Cargar el PDF.
    2. Cargar la firma.
    3. Ya esta configurado la posición de la firma, solo debe hacer click en "Firmar".
""")

def firmar(pdf,firma):
    doc = pymupdf.open(stream=pdf.read(),filetype="pdf")
    img_buffer = io.BytesIO(firma.read())
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer,"w",zipfile.ZIP_DEFLATED) as zip_file:
        # filename = Path(pdf.name).stem
        for page_number in range(len(doc)):
            page = doc[page_number]
            temp_doc = pymupdf.open()
            pdf_buffer = io.BytesIO()

            words = page.get_text("words",sort=True)
            dni = None
            for i,word in enumerate(words):
                text = word[4]
                if text == "DNI":
                    dni = words[i+2][4]
                    # print(dni)
                    break
            page.insert_image(
                rect = (100,550,200,860),
                # filename = firma,
                stream = img_buffer,
                overlay = True,
                keep_proportion = True
            )
            temp_doc.insert_pdf(doc, from_page=page_number, to_page=page_number)
            temp_doc.save(pdf_buffer)
            pdf_buffer.seek(0)
            img_buffer.seek(0)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            zip_file.writestr(f"{dni} Liquidación Beneficios Sociales {timestamp}.pdf",pdf_buffer.getvalue())  

    zip_buffer.seek(0)

    st.download_button(
        label="Descargar PDFs Firmados",
        data=zip_buffer,
        file_name="Descargas.zip",
        mime="application/zip"
    )  

uploaded_pdf = st.file_uploader("Cargar PDF",type=["pdf"],accept_multiple_files=False)
uploaded_firma = st.file_uploader("Cargar Firma",type=["png","jpg","jpge"],accept_multiple_files=False)

if uploaded_pdf and uploaded_firma:
    if st.button("Firmar"):
        firmar(uploaded_pdf,uploaded_firma)