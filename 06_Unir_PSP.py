import pandas as pd
import streamlit as st
import tempfile
import os

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🖇 Unir PSP")
st.write(
    "Carga tus archivos excel PSP y procesa para unirlos."
)

max_rows = st.number_input(label="Nro Máximo de Filas",min_value=1,max_value=9_000,value=200,step=1)

uploaded_files = st.file_uploader(label="Upload files",type=["xlsx","xlsb"],accept_multiple_files=True)

def remove_file():
    os.remove("PSP Consolidado.xlsx")

def unir_PSP(files,maxrows):
    dfs = []
    for file in files:
        data = pd.read_excel(file,skiprows=3,sheet_name="PSP SMALL",nrows=maxrows,dtype="object",usecols="M:BQ")
        dfs.append(data)
    dataset = pd.concat(dfs,ignore_index=True)
    final_dataset =dataset[dataset["UNIDAD"] != "<<SELECCIONA OPCION>>"].dropna(how="all")
    final_dataset.to_excel("PSP Consolidado.xlsx",index=False)

    with open("PSP Consolidado.xlsx", "rb") as fp:
            btn = st.download_button(
                label="Descargar archivos",
                data=fp,
                file_name="PSP Consolidado.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                on_click=remove_file)


if uploaded_files and max_rows > 0:
     if st.button("Unir PSP"):
          unir_PSP(uploaded_files,maxrows=max_rows)