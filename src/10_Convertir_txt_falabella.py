import pandas as pd
import streamlit as st
import os
import numpy as np

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("📎 Convertir TXT Falabella")
st.write("Carga el TXT de Falabella y se mostrar una tabla para exportar")


uploader = st.file_uploader(label="Cargar",accept_multiple_files=True,type=["txt"])

def remove_file():
     os.remove("DataFalabella.xlsx")


def procesar_txt(txt_files):
    to_concat = []
    for txt_file in txt_files:
        fecha = txt_file.name.split("_")[3]
        empresa = txt_file.name.split("_")[5]
        glosa = txt_file.name.split("_")[6][:-4]
        id_operacion = txt_file.name.split("_")[0]
        df = pd.read_fwf(txt_file,colspecs=([3,23],[23,63],[65,78],[78,80],[121,124],[124,136]),skiprows=1,header=None,encoding="ISO-8859-1")\
        .rename(columns={0:"Cuenta",1:"Nombres",2:"Entero",3:"Decimal",4:"TipoDoc",5:"NroDoc"})
        df["Importe"] = round(df["Entero"] + (df["Decimal"] / 100),2)
        df = df.drop(columns=["Entero","Decimal"])
        # df["NRO_SOLICITUD"] = nro_solicitud
        # df["ESTADO"] = estado
        df["FECHA"] = pd.to_datetime(fecha).strftime("%d/%m/%Y")
        df["EMPRESA"] = empresa
        df["GLOSA"] = glosa
        df["NRO OPERACION"] = id_operacion
        df["Cuenta"] = df["Cuenta"].astype(str)    # df["ARCHIVO"] = txt_file
        # df["NroDoc"] = df.apply(lambda x: x["NroDoc"].zfill(8) if x["TipoDoc"] == "DNI" else x["NroDoc"].zfill(10))
        df["NroDoc"] = np.where(df["TipoDoc"] == "DNI",df["NroDoc"].astype(str).str.zfill(8),df["NroDoc"].astype(str).str.zfill(10))
        to_concat.append(df)
    
    data = pd.concat(to_concat,ignore_index=True)
    st.dataframe(data)
    xlsx = data.to_excel("DataFalabella.xlsx",index=False)

    with open("DataFalabella.xlsx", "rb") as fp:
            btn = st.download_button(
                label="Descargar archivos",
                data=fp,
                file_name="DataFalabella.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                on_click=remove_file)

    
if st.button(label="Procesar"):
    procesar_txt(uploader)

