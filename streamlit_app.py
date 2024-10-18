import streamlit as st

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


pages = [
    st.Page("01_Unir_PDF.py",title="Unir PDF",icon=":material/close_fullscreen:"),
    st.Page("02_Separar_PDF.py",title="Separar PDF",icon=":material/add:"),
    st.Page("03_Convertir_PDF.py",title="Convertir PDF a Word")
]

pg = st.navigation(pages)
pg.run()