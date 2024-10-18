import streamlit as st
import pymupdf
import tempfile
import zipfile
import os
import shutil
from pdf2docx import parse

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🎈 Convertir PDF a WORD")
st.write(
    "Carga tu archivo PDF y conviertelos a WORD."
)

uploaded_file= st.file_uploader(label="Upload file",type=["pdf"],accept_multiple_files=False)

def convertir_docx(file):
    file_name = file.name
    temp_folder = tempfile.TemporaryDirectory()
    temp_pdf_name = os.path.join(temp_folder.name,"tempfile.pdf")
    temp_docx_name = os.path.join(temp_folder.name,f"{file_name[:-4]}.docx")
    doc = pymupdf.open(stream=file.read(),filetype="pdf")
    doc.save(temp_pdf_name)
    doc.close()
    file_name = file.name
    parse(temp_pdf_name,temp_docx_name)

    with open(temp_docx_name, "rb") as fp:
            btn = st.download_button(
                label="Descargar Word",
                data=fp,
                file_name=f"{file_name[:-4]}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                # on_click=remove_zip)
                )

if st.button("Procesar"):
    convertir_docx(uploaded_file)