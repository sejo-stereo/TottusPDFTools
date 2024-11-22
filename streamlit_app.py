import streamlit as st

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


pages = {
    "GENERAL":
    [
    st.Page("01_Unir_PDF.py",title="Unir PDF",icon="🖇",url_path="general_unir_pdf"),
    st.Page("02_Separar_PDF.py",title="Separar PDF",icon="✂",url_path="general_separar_pdf"),
    st.Page("03_Convertir_PDF.py",title="Convertir PDF a Word",icon="📑",url_path="general_word_to_pdf"),
    # st.Page("04_Rotar_PDF.py",title="Rotar PDF")
    st.Page("05_Imagen_a_pdf.py",title="Convertir Imagen a PDF",icon="📸",url_path="general_img_to_pdf")
    ],
    "PIL":[
        st.Page("06_Unir_PSP.py",title="Unir archivos PSP",icon="🖇",url_path="PIL_unir_PSP")    
    ],
    "ASISTENCIA":[],
}

pg = st.navigation(pages)
pg.run()