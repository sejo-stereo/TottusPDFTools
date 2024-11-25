import streamlit as st
import os
import tempfile
import pymupdf
import shutil

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


options = {
    pymupdf.PDF_PERM_PRINT:"Imprimir",
    pymupdf.PDF_PERM_MODIFY:"Editar",
    pymupdf.PDF_PERM_COPY:"Copiar",
    pymupdf.PDF_PERM_ANNOTATE:"Comentar",
    # pymupdf.PDF_PERM_ACCESSIBILITY:"Imprimir documento",
    pymupdf.PDF_PERM_ASSEMBLE:"Modificar",
}

def remove_zip():
     os.remove("Descargas.zip")

def proteger_pdfs(files,owner_password,user_password,perms):
    temp_folder = tempfile.TemporaryDirectory()

    perms_2 = 0
    for valor in perms:
        perms_2 |= valor

    for file in files:
        doc = pymupdf.open(stream=file.read(),filetype="pdf")
        doc.save(
            os.path.join(temp_folder.name,file.name),
            encryption = pymupdf.PDF_ENCRYPT_AES_256,
            owner_pw =owner_password,
            user_pw = user_password,
            permissions=perms_2
        )
    shutil.make_archive("Descargas","zip",temp_folder.name)

    with open("Descargas.zip", "rb") as fp:
                    btn = st.download_button(
                        label="Descargar archivos protegidos.",
                        data=fp,
                        file_name="Descargas.zip",
                        mime="application/zip",
                        on_click=remove_zip)
    

st.title("🔐 Proteger PDF")
st.write(
    "Carga tus archivos PDF, asigna contraseña y protegelos."
)

col1,col2 = st.columns(2)

with col1:
    uploaded_pdfs = st.file_uploader(label="Cargar PDF",key="uploaded_pdfs",accept_multiple_files=True,type=["pdf"])

with col2:
    owner_password_input = st.text_input(label="Contraseña Administrador",key="owner_password",type="password")
    user_password_input = st.text_input(label="Contraseña Usuario",key="user_password",type="password")
    selection = st.segmented_control(
        "Selecciona los permisos que quieres habiltiar:",
        options = options.keys(),
        format_func=lambda option: options[option],
        selection_mode="multi",
        default=[pymupdf.PDF_PERM_PRINT,pymupdf.PDF_PERM_MODIFY,pymupdf.PDF_PERM_COPY,pymupdf.PDF_PERM_ANNOTATE,pymupdf.PDF_PERM_ASSEMBLE]
    )

    if st.button("Procesar"):
        proteger_pdfs(uploaded_pdfs,owner_password=owner_password_input,user_password=user_password_input,perms=selection)
