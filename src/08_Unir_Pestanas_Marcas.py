import pandas as pd
import streamlit as st
import os

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("📎 Consolidar pestañas de un archivo de marcas")
st.write(
    "Carga el archivo Excel para consolidar todas las pestañas. Las pestañas deben contar con la misma estructura de encabezados"   
)

data_file = st.file_uploader(label="Cargar Excel",type=["xlsx","xlsb"],accept_multiple_files=False)

def remove_file():
     os.remove("Consolidado.xlsx")

def consolidar_pestanas(file):
    xls = pd.ExcelFile(file)
    sheets = xls.sheet_names
    sheets = [sheet for sheet in sheets if sheet not in ["apoyo","INDICE"]]

    dfs = []
    for sheet in sheets:
        df = pd.read_excel(xls,sheet_name=sheet,skiprows=2,usecols="A:O")
        dfs.append(df)

    alldf = pd.concat(dfs,ignore_index=True)
    alldf = alldf.dropna(how="all")
    alldf.to_excel(f"Consolidado.xlsx",index=False)

    with open("Consolidado.xlsx", "rb") as fp:
            btn = st.download_button(
                label="Descargar archivos",
                data=fp,
                file_name="Consolidado.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                on_click=remove_file)


if data_file:
    if st.button("Consolidar"):
        consolidar_pestanas(data_file)