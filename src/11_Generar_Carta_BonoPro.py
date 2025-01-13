import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import io
import pandas as pd
from datetime import date
import os
import streamlit as st
import tempfile
import zipfile
import shutil

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🖨 Generar Cartas de Bono Pro")
st.write(
    "Carga el archivo Excel con la data y genera las cargas de Bono Pro."
)

#Variables
# formato_file = "assets//asistencia//PLANTILLA CARTAS BONOPRO.pdf"
today_text = date.today().strftime("%d/%m/%Y")
output_zip = 'CartasBonoPro.zip'

def remove_zip_file():
    os.remove(f"{output_zip}.zip")

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)

def create_table_from_df(dataframe,x_coord,y_coord):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Convert DataFrame to list of lists
    data = [dataframe.columns.to_list()] + dataframe.values.tolist()

    table = Table(data)

    row_height = 7
    num_rows = len(data)
    row_heights = [row_height] * num_rows

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 0),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0,0), (-1,0), 6),
        ('FONTSIZE', (0,1), (-1,-1), 6),
        ('ROWHEIGHTS', (0, 0), (-1, -1), row_heights)
    ])
    table.setStyle(style)

    table_width, table_height = table.wrap(0, 0)

    adjusted_x = x_coord
    adjusted_y = y_coord - table_height  # Subtract table height to position the top-left corner

    table.drawOn(can, adjusted_x, adjusted_y)

    # table.wrapOn(can, 0, 0)
    # table.drawOn(can, 150, 295)  # Adjust the position as needed
    can.save()

    packet.seek(0)
    return packet

def generar_cartas_asistencia(data_file,title_text,dia_respuesta_text):
    temp_folder = tempfile.TemporaryDirectory()

    df_data = pd.read_excel(data_file,dtype=object,sheet_name="data")[["COD_TRABAJADOR","DESC_UNIDAD","FECHA","TIPO AUSENTISMO","DIAS TRABAJADOS","DIAS AUSENTISMO","NRO DOC","NOMBRES"]]
    df_data['FECHA'] = pd.to_datetime(df_data.FECHA, format='%d-%m-%Y')
    df_data['FECHA'] = df_data['FECHA'].dt.strftime('%d-%m-%Y')
    list_trabajadores = df_data[["NOMBRES","NRO DOC","DIAS TRABAJADOS","DIAS AUSENTISMO"]].drop_duplicates()

    for i,j in list_trabajadores.iterrows():
        nombres = j["NOMBRES"]
        # unidad = j["DESC_UNIDAD"]
        dni = j["NRO DOC"]
        dias_trabajados = j["DIAS TRABAJADOS"]
        dias_ausentismo = j["DIAS AUSENTISMO"]
        # output_excel = f"output\FORMATO_{nombres}.xlsx"
        output_pdf = os.path.join(temp_folder.name,f"{dni} {nombres}.pdf")
        # output_pdf = f"{temp_folder.name}\\{dni} {nombres}.pdf"
        print(output_pdf)

        # template_file.seek(0)
        # doc = fitz.open(stream=template_file.read(),filetype="pdf")
        formato_file = "assets//asistencia//PLANTILLA CARTAS BONOPRO.pdf"
        doc = fitz.open(formato_file)
        page = doc[0]

        page_width = page.rect.width
        font = fitz.Font("Helvetica-Bold")
        text_width = font.text_length(title_text, fontsize=11)
        x = (page_width - text_width) / 2
        page.insert_text((x, 89), title_text, fontsize=11, fontname="Helvetica-Bold", color=(0, 0, 0))

        page.insert_text((35, 110), f"Hola {nombres}", fontsize=9, color=(0,0,0),fontname="Helvetica-Bold")
        # page.insert_text((395, 161), f"Unidad: {unidad}", fontsize=8, color=(0,0,0),fontname="Helvetica-Bold")
        page.insert_text((35, 125), f"Para el cálculo del Bono Pro, un factor importante son tus días laborados del periodo, por lo que mediante esta carta te comunicamos", fontsize=8, color=(0,0,0),fontname="Helvetica")
        page.insert_text((35, 135), f"que este mes cuentas con {dias_trabajados} días laborados y con {dias_ausentismo} días de ausentismo detallados:", fontsize=8, color=(0,0,0),fontname="Helvetica")
        page.insert_text((35, 712), f"Cualquier consulta u observación podrás revisarla con el área de Gestión Humana de tu unidad hasta el {dia_respuesta_text}.", fontsize=8, color=(0,0,0),fontname="Helvetica")
        page.insert_text((35, 735), f"Fecha de emisión: {today_text}", fontsize=7, color=(0,0,0),fontname="Helvetica")

        df_to_paste = df_data[df_data["NOMBRES"] == nombres][["FECHA","TIPO AUSENTISMO"]]
        # data_list = [df_to_paste.columns.tolist()] + df_to_paste.values.tolist()
        # if len(df_to_paste) > 31:
        
        packet_1 = create_table_from_df(df_to_paste[:31],x_coord=100,y_coord=680)
        table_pdf_1 = fitz.open("pdf", packet_1.read())
        page.show_pdf_page(fitz.Rect(0, 0, page.rect.width, page.rect.height), table_pdf_1, 0)

        if len(df_to_paste) > 31:
            packet_2 = create_table_from_df(df_to_paste[31:],x_coord=300,y_coord=680)
            table_pdf_2 = fitz.open("pdf", packet_2.read())
            page.show_pdf_page(fitz.Rect(0, 0, page.rect.width, page.rect.height), table_pdf_2, 0)
        
        # Save the modified PDF to a new file
        doc.save(output_pdf)
        doc.close()

    shutil.make_archive(output_zip,"zip",temp_folder.name)
        
    with open(f"{output_zip}.zip", "rb") as fp:
        btn = st.download_button(
            label="Descargar archivos",
            data=fp,
            file_name=f"{output_zip}.zip",
            mime="application/zip",
            on_click=remove_zip_file)

col1,col2 = st.columns(2)

with col1:
    # template_file = st.file_uploader(label="Cargar plantilla PDF",type="pdf",accept_multiple_files=False)
    title_text = st.text_input(label="Título de la carta",value="",placeholder="CARTA DE DÍAS LABORADOS - DICIEMBRE 2024")
    dia_respuesta_text = st.text_input(label="Fecha máxima de respuesta",value="",placeholder="13 de enero de 2025")


with col2:
    data_file = st.file_uploader(label="Cargar Excel",type=["xlsx","xlsb","xlsm"],accept_multiple_files=False)
    if data_file:
        if st.button("Generar Cartas Bono Pro"):
            generar_cartas_asistencia(data_file,title_text,dia_respuesta_text)