import pandas as pd
import streamlit as st
import os
import numpy as np

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("📎 Convertir TXT Falabella")
st.write("Carga el TXT de Falabella y se mostrar una tabla para exportar")


uploader = st.file_uploader(label="Cargar",accept_multiple_files=False,type=["txt"])


def procesar_txt(txt_file):
    fecha = txt_file.name.split("_")[3]
    df = pd.read_fwf(txt_file,colspecs=([3,23],[23,63],[65,78],[78,80],[121,124],[124,136]),skiprows=1,header=None,encoding="ISO-8859-1")\
    .rename(columns={0:"Cuenta",1:"Nombres",2:"Entero",3:"Decimal",4:"TipoDoc",5:"NroDoc"})
    df["Importe"] = round(df["Entero"] + (df["Decimal"] / 100),2)
    df = df.drop(columns=["Entero","Decimal"])
    # df["NRO_SOLICITUD"] = nro_solicitud
    # df["ESTADO"] = estado
    df["FECHA"] = pd.to_datetime(fecha).strftime("%d/%m/%Y")
    df["Cuenta"] = df["Cuenta"].astype(str)    # df["ARCHIVO"] = txt_file
    # df["NroDoc"] = df.apply(lambda x: x["NroDoc"].zfill(8) if x["TipoDoc"] == "DNI" else x["NroDoc"].zfill(10))
    df["NroDoc"] = np.where(df["TipoDoc"] == "DNI",df["NroDoc"].astype(str).str.zfill(8),df["NroDoc"].astype(str).str.zfill(10))
    st.dataframe(df)

if st.button(label="Procesar"):
    procesar_txt(uploader)

