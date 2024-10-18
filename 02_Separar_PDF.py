import streamlit as st
import pymupdf
import tempfile
import zipfile
import os
import shutil

st.title("🎈 Separar PDF")
st.write(
    "Carga tu archivo PDF y procesa para separarlos."
)

uploaded_file= st.file_uploader(label="Upload file",type=["pdf"],accept_multiple_files=False)

def remove_zip():
     os.remove("Descargas.zip")

def separar_pdf(uploaded_file):
    temp_folder = tempfile.TemporaryDirectory()
    doc = pymupdf.open(stream=uploaded_file.read(),filetype="pdf")
    for i,page in enumerate(doc):
        temp_doc = pymupdf.open()
        temp_doc.insert_pdf(doc,from_page=i,to_page=i)
        temp_doc.save(os.path.join(temp_folder.name,f"{uploaded_file.name}_{i+1}.pdf"))
        temp_doc.close()

    shutil.make_archive("Descargas","zip",temp_folder.name)
    with open("Descargas.zip", "rb") as fp:
            btn = st.download_button(
                label="Descargar ZIP",
                data=fp,
                file_name="Descargas.zip",
                mime="application/zip",
                on_click=remove_zip)

if st.button("Separar PDF"):
    separar_pdf(uploaded_file)

