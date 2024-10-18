import streamlit as st

pages = [
    st.Page("01_Unir_PDF.py",title="Unir PDF",icon=":material/close_fullscreen:"),
    st.Page("02_Separar_PDF.py",title="Separar PDF",icon=":material/add:")
]

pg = st.navigation(pages)
pg.run()