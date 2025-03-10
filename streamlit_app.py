import streamlit as st

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.write(f"Desarrollado por José Melgarejo.")


pages = {
    "GENERAL":
    [
    st.Page("src//01_Unir_PDF.py",title="Unir PDF",icon="🖇",url_path="general_unir_pdf"),
    st.Page("src//02_Separar_PDF.py",title="Separar PDF",icon="✂",url_path="general_separar_pdf"),
    st.Page("src//03_Convertir_PDF.py",title="Convertir PDF a Word",icon="📑",url_path="general_word_to_pdf"),
    # st.Page("04_Rotar_PDF.py",title="Rotar PDF")
    st.Page("src//05_Imagen_a_pdf.py",title="Convertir Imagen a PDF",icon="📸",url_path="general_img_to_pdf"),
    st.Page("src//09_Proteger_PDF.py",title="Proteger PDF",icon="🔐",url_path="general_proteger_pdf")
    
    ],
    "PIL":[
        st.Page("src//06_Unir_PSP.py",title="Consolidar archivos PSP",icon="🖇",url_path="pil_consolidar_PSP")    
    ],
    "ASISTENCIA":[
        st.Page("src//07_Generar_Carta_Asistencia.py",title="Generar Cartas Incidencias",icon="🖨",url_path="asistencia_generar_cartas_incidencia"),
        st.Page("src//08_Unir_Pestanas_Marcas.py",title="Unir Pestañas de Marcas",icon="📎",url_path="asistencia_consolidar_pestanas_marcas"),
        st.Page("src//11_Generar_Carta_BonoPro.py",title="Generar Cartas Bono Pro",icon="🖨",url_path="asistencia_generar_cartas_bonopro"),
          
    ],
    "CONTABILIDAD":[
        st.Page("src//10_Convertir_txt_falabella.py",title="Convertir TXT Falabella",icon="🖨",url_path="contabilidad_convertir_txt_falabella"),  
    ],
    "NOMINA":[
        st.Page("src//12_Formato_LBS.py",title="Firmar Documentos",icon="🖨",url_path="nomina_firmar_pdf"),  
    ]
}

pg = st.navigation(pages)
pg.run()