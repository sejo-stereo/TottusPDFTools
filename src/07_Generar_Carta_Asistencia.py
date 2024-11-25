import fitz
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import io
import pandas as pd
from datetime import date
import os
import zipfile
import streamlit as st
import tempfile

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🖨 Generar Cartas de Indicencia")
st.write(
    "Carga el archivo Excel con la data y genera las cargas de incidencias."
)

# Coordenadas PDF
table_coord_X, table_coord_Y = [125,400]
nombre_coords = [125,161]
unidad_coords = [395,161]
fecha_coords = [395,171]
fecha_emision_coords = [110,710]

#Variables
formato_file = "assets//asistencia//FormatoCartaAsistencia.pdf"
today_text = date.today().strftime("%d/%m/%Y")
output_zip = 'CartasIncidencias.zip'


data_file = st.file_uploader(label="Cargar Excel",type=["xlsx","xlsb"],accept_multiple_files=False)

def remove_zip_file():
    os.remove(output_zip)


def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)

def create_table_from_df(dataframe):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    data = [dataframe.columns.to_list()] + dataframe.values.tolist() #Convertir dataframe

    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 0),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0,0), (-1,0), 6),
        ('FONTSIZE', (0,1), (-1,-1), 6)
    ])
    table.setStyle(style)

    table_width, table_height = table.wrap(0, 0)

    table.drawOn(can, table_coord_X, (table_coord_Y - table_height))

    can.save()

    packet.seek(0)
    return packet

def generar_cartas_asistencia(data_file):

    temp_folder = tempfile.TemporaryDirectory()

    df_data = pd.read_excel(data_file,dtype=object)[["NRO DOC","DESC_UNIDAD","NOMBRES","FECHA","INICIO TEORICO","FIN TEORICO","INICIO REAL","FIN REAL","TIPO INCIDENCIA"]]
    df_data['FECHA'] = pd.to_datetime(df_data.FECHA, format='%d-%m-%Y').dt.strftime('%d-%m-%Y')
    lista_trabajadores = df_data[["NOMBRES","DESC_UNIDAD","NRO DOC"]].drop_duplicates()

    for i,j in lista_trabajadores.iterrows():
        # Variables trabajadores
        nombres = j["NOMBRES"]
        unidad = j["DESC_UNIDAD"]
        dni = j["NRO DOC"]
        # output_pdf = os.path.join("pdf_output", f"{dni} {nombres}.pdf")
        output_pdf = os.path.join(temp_folder.name, f"{dni}.pdf")
        df_to_paste = df_data[df_data["NOMBRES"] == nombres].drop(columns=["NOMBRES","DESC_UNIDAD","NRO DOC"])

        # Main
        doc = fitz.open(formato_file)

        packet = create_table_from_df(df_to_paste)
        table_pdf = fitz.open("pdf", packet.read())

        # Seleccionar página e ingresar datos al pdf
        page = doc[0]
        page.insert_text(nombre_coords, nombres, fontsize=8, color=(0,0,0),fontname="Helvetica-Bold")
        page.insert_text(unidad_coords, f"Unidad: {unidad}", fontsize=8, color=(0,0,0),fontname="Helvetica-Bold")
        page.insert_text(fecha_coords, f"Fecha: {today_text}", fontsize=8, color=(0,0,0),fontname="Helvetica-Bold")
        page.insert_text(fecha_emision_coords, f"Fecha de emisión: {today_text}", fontsize=7, color=(0,0,0),fontname="Helvetica")

        #Pegar la tabla en el pdf.
        page.show_pdf_page(fitz.Rect(0, 0, page.rect.width, page.rect.height), table_pdf, 0)

        doc.save(output_pdf)

    zip_folder(temp_folder.name, output_zip)
        
    with open(output_zip, "rb") as fp:
        btn = st.download_button(
            label="Descargar archivos",
            data=fp,
            file_name=output_zip,
            mime="application/zip",
            on_click=remove_zip_file)



if data_file:
    if st.button("Generar Cartas"):
        generar_cartas_asistencia(data_file)