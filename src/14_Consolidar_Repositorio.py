import pandas as pd
import streamlit as st
import os
import io
import pathlib

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("📎 Consolidar Repositorios")

data_files = st.file_uploader(label="Cargar Excel",type=["xlsx","xlsb"],accept_multiple_files=True)

def consolidar_repositorios(files):
    excel_buffer = io.BytesIO()
    dfs = []
    for file in files:
        da = pd.read_excel(file,sheet_name="Plantilla RRHH",skiprows=3,dtype="object")
        da = da.dropna(how="all")
        da["NombreArchivo"] = file.name
        dfs.append(da)

    df = pd.concat(dfs,ignore_index=True)

    with pd.ExcelWriter(excel_buffer,engine="openpyxl") as writer:
        df.to_excel(writer,sheet_name="Repositorio",index=False)

    st.download_button(
        label="Descargar Excel",
        data=excel_buffer,
        file_name="output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if st.button("Procesar"):
    consolidar_repositorios(data_files)