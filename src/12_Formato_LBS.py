import streamlit as st
import pymupdf
import io
from pathlib import Path

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
    filename = Path(pdf.name).stem
    for page in doc:
        page.insert_image(
            rect = (100,550,200,850),
            # filename = firma,
            stream = img_buffer,
            overlay = True,
            keep_proportion = True
        )
    pdf_buffer = io.BytesIO()
    doc.save(pdf_buffer)
    pdf_buffer.seek(0)
    img_buffer.seek(0)

    st.download_button(
        label="Descargar PDF Firmado",
        data=pdf_buffer,
        file_name=f"{filename}_firmado.pdf",
        mime="application/pdf"
    )

    

uploaded_pdf = st.file_uploader("Cargar PDF",type=["pdf"],accept_multiple_files=False)
uploaded_firma = st.file_uploader("Cargar Firma",type=["png","jpg","jpge"],accept_multiple_files=False)

if uploaded_pdf and uploaded_firma:
    if st.button("Firmar"):
        firmar(uploaded_pdf,uploaded_firma)