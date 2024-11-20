import streamlit as st
import pymupdf
import tempfile
import zipfile
import os
import shutil
import streamlit_pdf_viewer as pdf_viewer

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🎈 Rotar PDF")
st.write(
    "Carga tu archivo PDF y modifica la rotación."
)

col1, col2 = st.columns(2)

with col1:
    uploaded_pdf= st.file_uploader(label="Cargar PDF",type=["pdf"],key="uploaded_pdf",accept_multiple_files=False)

    st.write(st.session_state)
    st.write("hola")

# with col2:
    if uploaded_pdf:
        binary_data = st.session_state["uploaded_pdf"].getvalue()
        # st.write(binary_data)
        pdf_viewer(input=binary_data,width=500)


