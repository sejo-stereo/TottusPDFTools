import streamlit as st
import pymupdf
import tempfile
import zipfile
import os
import shutil

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🎈 Separar PDF")
st.write(
    "Carga tu archivo PDF y procesa para separarlos."
)

uploaded_file= st.file_uploader(label="Upload file",type=["pdf"],accept_multiple_files=False)
rename_flag = st.checkbox("Quiere renombrar sus archivos?")
if rename_flag:
    #  position = st.number_input("Posición Clave",step=1,min_value=1)
     positions = st.slider("Posiciones Clave",step=1,min_value=1,max_value=50,value=(1,1))
    #  start_pos = positions[0]
    #  end_pos = positions[1]
    #  st.write(start_pos,end_pos)


def remove_zip():
     os.remove("Descargas.zip")

def separar_pdf(uploaded_file):
    temp_folder = tempfile.TemporaryDirectory()
    doc = pymupdf.open(stream=uploaded_file.read(),filetype="pdf")
    for i,page in enumerate(doc):
        temp_doc = pymupdf.open()
        temp_doc.insert_pdf(doc,from_page=i,to_page=i)
        if rename_flag:
            name_words = []
            start_pos = positions[0]
            end_pos = positions[1]
            text = page.get_text(sort=True)
            words = text.split("\n")
            for v in range(start_pos,end_pos+1):
                key_word = words[v-1]
                name_words.append(key_word)
            name_words_concat = " ".join(name_words)
            st.write(words)
            pdf_name = f"{name_words_concat}.pdf"
        else:
             pdf_name = f"{uploaded_file.name}_{i+1}.pdf"
        temp_doc.save(os.path.join(temp_folder.name,pdf_name))
        temp_doc.close()

    shutil.make_archive("Descargas","zip",temp_folder.name)
    with open("Descargas.zip", "rb") as fp:
            btn = st.download_button(
                label="Descargar ZIP",
                data=fp,
                file_name="Descargas.zip",
                mime="application/zip",
                on_click=remove_zip)
if uploaded_file:
    if st.button("Separar PDF"):
        separar_pdf(uploaded_file)

