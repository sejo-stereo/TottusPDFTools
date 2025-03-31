import streamlit as st
import pymupdf
import io
from pathlib import Path
import zipfile
import datetime

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



def separar_documentos(pdf,tipo_documento):
    rects = {"Boleta":[42, 110, 211, 117],"Liquidación":[94, 128, 354, 131]}
    document_rect = rects[tipo_documento]
    doc = pymupdf.open(stream=pdf.read(),filetype="pdf")
    zip_buffer = io.BytesIO()

    text_to_pages = {}

    # agrupa las páginas por el DNI 
    for i in range(len(doc)):
        page = doc[i]
        text = page.get_textbox(rect=document_rect).strip()

        if text in text_to_pages:
            text_to_pages[text].append(i)
        else:
            text_to_pages[text] = [i]

    with zipfile.ZipFile(zip_buffer,"w",zipfile.ZIP_DEFLATED) as zip_file:
        # Crear nuevos documentos según las páginas agrupadas
        for text, pages in text_to_pages.items():
            new_filename = f"{text} {tipo_documento}.pdf"
            pdf_buffer = io.BytesIO()
            new_doc = pymupdf.open()  # Crear un PDF vacío

            for page_num in pages:
                new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
            
            new_doc.save(pdf_buffer)
            pdf_buffer.seek(0)
            zip_file.writestr(new_filename,pdf_buffer.getvalue())  

    zip_buffer.seek(0)

    st.download_button(
        label="Descargar PDFs Separados",
        data=zip_buffer,
        file_name="Descargas.zip",
        mime="application/zip"
    )  
st.title("✂️ Separar Documentos Nómina")

st.markdown("""
    1. Seleccionar el tipo de documento a separar.
    2. Cargar el PDF.
    3. Click en "Separar PDF"
""")

tipo_documento = st.selectbox("Seleccione el tipo de documento a separar",options=["Boleta","Liquidación"])
uploaded_pdf = st.file_uploader("Cargar PDF",type=["pdf"],accept_multiple_files=False)
if uploaded_pdf and tipo_documento:
    if st.button("Separar Documentos"):
        separar_documentos(uploaded_pdf,tipo_documento)