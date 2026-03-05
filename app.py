import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Configuração da Página
st.set_page_config(page_title="Relatório de Vida", layout="centered")

# --- CONEXÃO COM GOOGLE SHEETS ---
def conecta_planilha():
    scope = ["https://www.googleapis.com", "https://www.googleapis.com"]
    # Aqui ele busca os dados do arquivo JSON que você colará no Streamlit depois
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    return client.open("Relatorio_Vida").sheet1

# --- DADOS DOS GRUPOS ---
dados_igreja = {
    "Grupo Ágape": {"lider": "João Silva", "rede": "Família"},
    "Grupo Betel": {"lider": "Maria Oliveira", "rede": "Jovens"},
    "Grupo Moriá": {"lider": "Pedro Santos", "rede": "Homens"}
}

# --- INTERFACE ---
st.title("⛪ Relatório de Vida")

with st.form("form_relatorio"):
    nome_grupo = st.selectbox("Selecione o Nome do Grupo", list(dados_igreja.keys()))
    
    # Campos Automáticos
    lider_grupo = dados_igreja[nome_grupo]["lider"]
    rede_grupo = dados_igreja[nome_grupo]["rede"]
    st.info(f"Líder: {lider_grupo} | Rede: {rede_grupo}")
    
    data = st.date_input("Data do Encontro").strftime('%d/%m/%Y')
    
    col1, col2 = st.columns(2)
    with col1:
        membros_grupo = st.number_input("Membros no Grupo", min_value=0)
        membros_culto = st.number_input("Membros no Culto", min_value=0)
        convidados = st.number_input("Convidados", min_value=0)
    with col2:
        criancas = st.number_input("Crianças (0-11)", min_value=0)
        ges = st.number_input("GEs", min_value=0)
        quilo_amor = st.number_input("Quilo do Amor (kg)", min_value=0.0)

    oferta = st.number_input("Oferta (R$)", min_value=0.0)
    discipulador = st.text_input("Discipulador")
    discipulado = st.selectbox("Fez Discipulado?", ["Sim", "Não"])
    obs = st.text_area("Observações")
    
    total = membros_grupo + convidados + criancas
    
    submit = st.form_submit_button("Enviar Relatório")

if submit:
    try:
        sheet = conecta_planilha()
        linha = [nome_grupo, lider_grupo, rede_grupo, data, oferta, obs, 
                 membros_grupo, membros_culto, convidados, criancas, 
                 quilo_amor, total, discipulador, discipulado, ges]
        sheet.append_row(linha)
        st.success("✅ Relatório enviado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao enviar: {e}")
