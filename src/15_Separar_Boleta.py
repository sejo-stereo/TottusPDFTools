import streamlit as st
import pymupdf
import io
from pathlib import Path
import zipfile
import datetime

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🖨 Separar Boletas")

st.markdown("""
    1. Cargar el PDF.
    2. Click en "Separar PDF"
""")

def separar_boleta(pdf):
    doc = pymupdf.open(stream=pdf.read(),filetype="pdf")
    zip_buffer = io.BytesIO()

    rect = [10, 110, 250, 110] # rect del DNI

    with zipfile.ZipFile(zip_buffer,"w",zipfile.ZIP_DEFLATED) as zip_file:
        # Crear nuevos documentos según las páginas agrupadas
        for i in range(len(doc)):
            page = doc[i]
            text = page.get_textbox(rect=rect).strip()
            new_filename = f"{text} Boleta.pdf"
            pdf_buffer = io.BytesIO()
            new_doc = pymupdf.open()  # Crear un PDF vacío

            new_doc.insert_pdf(doc, from_page=i, to_page=i)
            new_doc.save(pdf_buffer)
            pdf_buffer.seek(0)
            zip_file.writestr(new_filename,pdf_buffer.getvalue())  

    zip_buffer.seek(0)

    st.download_button(
        label="Descargar Boletas",
        data=zip_buffer,
        file_name="Descargas.zip",
        mime="application/zip"
    )  

uploaded_pdf = st.file_uploader("Cargar PDF",type=["pdf"],accept_multiple_files=False)
if uploaded_pdf:
    if st.button("Firmar"):
        separar_boleta(uploaded_pdf)