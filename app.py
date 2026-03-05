import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Conectando com a planilha usando os Secrets do Streamlit
scope = ["https://www.googleapis.com", "https://www.googleapis.com"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)

# Abre a planilha pelo nome
sheet = client.open("Nome da Sua Planilha").sheet1

# No final do seu código, dentro do botão de envio:
if st.button("Enviar Relatório"):
    dados = [
        nome_grupo, lider_grupo, rede, str(data), oferta, observacao,
        membros_grupo, membros_culto, convidados, criancas, 
        quilo_amor, total_presentes, discipulador, discipulado, ges
    ]
    sheet.append_row(dados)
    st.success("Dados salvos no Excel com sucesso!")
