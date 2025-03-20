import pandas as pd
import streamlit as st
import os
import io
import pathlib

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("📎 Generar archivo de carga a GeoVictoria")
# st.write(
#     "Carga el archivo Excel para consolidar todas las pestañas. Las pestañas deben contar con la misma estructura de encabezados"   
# )

file_turnos = "assets/asistencia/TurnosGeovictoria.xlsx"

fecha_inicio  = st.date_input("Ingrese la fecha de inicio",value="default_value_today",format="DD/MM/YYYY")
data_file = st.file_uploader(label="Cargar Excel",type=["xlsx","xlsb"],accept_multiple_files=False)

def generate_dias(date_input):
    date_to_replace = {}
    for i in range(15):
        dia = f"Dia_{i+1}"
        # print(dia)
        date_to_replace[dia] = pd.to_datetime(date_input) + pd.Timedelta(days=i)
    return date_to_replace
    

def generate_output(excel_file,date_input,turnos_file):
    output_buffer = io.BytesIO()
    filename = pathlib.Path(excel_file.name).stem
    df_base = pd.read_excel(excel_file,dtype="object",skiprows=7,sheet_name="JEFE SECCION")
    df_base = df_base.rename(columns={"LUN":"Dia_1","MAR":"Dia_2","MIE":"Dia_3",
                        "JUE":"Dia_4","VIE":"Dia_5","SAB":"Dia_6",
                        "DOM":"Dia_7","LUN.1":"Dia_8","MAR.1":"Dia_9",
                        "MIE.1":"Dia_10","JUE.1":"Dia_11","VIE.1":"Dia_12",
                        "SAB.1":"Dia_13","DOM.1":"Dia_14"})
    df_base = df_base.dropna(subset="TIENDA")
    df_turnos = pd.read_excel(turnos_file,dtype="object")
    columnas = df_base.columns
    cols_fijas = columnas[:9]
    cols_query_1 = columnas[:16]
    cols_query_2 = list(columnas[:9]) + list(columnas[19:26])
    query_df_1 = df_base[cols_query_1]
    query_df_2 = df_base[cols_query_2]
    query_1_melt = query_df_1.melt(id_vars=cols_fijas,value_vars=["Dia_1","Dia_2","Dia_3","Dia_4","Dia_5","Dia_6","Dia_7"])
    query_2_melt = query_df_2.melt(id_vars=cols_fijas,value_vars=["Dia_8","Dia_9","Dia_10","Dia_11","Dia_12","Dia_13","Dia_14"])
    query_melted = pd.concat([query_1_melt,query_2_melt],axis=0,ignore_index=True)
    query_final = query_melted.merge(right=df_turnos,how="left",left_on="value",right_on="Turno_Lista").drop(columns=["Turno_Lista"])
    query_final["variable"] = query_final["variable"].replace(generate_dias(date_input))
    query_final["DIA"] = query_final["variable"].dt.day
    query_final["MES"] = query_final["variable"].dt.month
    query_final["ANNO"] = query_final["variable"].dt.year
    query_final = query_final.dropna(subset=["value"])
    query_export = query_final[["TRABAJADOR","ID_Turno","DIA","MES","ANNO"]]
    query_export = query_export.rename(columns={"TRABAJADOR":"DNI","ID_Turno":"ID Turno","DIA":"Dia","MES":"Mes","ANNO":"Año"})
    query_export["ID Centro de Costo"] = None

    with pd.ExcelWriter(output_buffer,engine="openpyxl") as writer:
        query_export.to_excel(writer, index=False, sheet_name='Sheet1')

    st.download_button(
        label="Descargar Excel Carga",
        data=output_buffer,
        file_name="output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
if st.button("Procesar"):
    generate_output(data_file,fecha_inicio,file_turnos)