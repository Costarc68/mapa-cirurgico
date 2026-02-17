import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, time

# Configuração da página
st.set_page_config(page_title="Mapa Cirúrgico Oficial", layout="centered")

st.title("🏥 Reserva de Sala Cirúrgica")

# Conexão com a sua planilha (Link que você enviou)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1-w1V1UfEfwxRAMd_gw9n3D0u5lZgDyzFGBGxNNsRAzc/export?format=csv"
# 1. FORMULÁRIO
with st.form("form_final", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        medico = st.selectbox("Cirurgião", ["DR. RIVAS", "DR. VAGNER"])
        paciente = st.text_input("Nome do Paciente").upper()
        data_cir = st.date_input("Data da Cirurgia", format="DD/MM/YYYY")
    with col2:
        convenio = st.text_input("Convênio").upper()
        procedimento = st.text_input("Procedimento").upper()
        horario = st.time_input("Horário", value=time(7, 0))
    
    opme = st.selectbox("OPME?", ["Não", "Sim"])
    obs = st.text_area("Observações para Gestão")
    
    botao = st.form_submit_button("✅ CONFIRMAR RESERVA")

# 2. AÇÃO DE SALVAR
if botao:
    # Cálculo do gatilho de 7 dias
    data_gatilho = data_cir + pd.Timedelta(days=7)
    
    # Organizando os dados para a planilha
    dados_novos = pd.DataFrame([{
        "Data Registro": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Cirurgião": medico,
        "Paciente": paciente,
        "Data Cirurgia": data_cir.strftime("%d/%m/%Y"),
        "Convênio": convenio,
        "Procedimento": procedimento,
        "Gatilho 7 Dias": data_gatilho.strftime("%d/%m/%Y"),
        "Observação": obs
    }])

    # Lendo dados existentes e adicionando o novo
    try:
        existentes = conn.read(spreadsheet=url)
        atualizado = pd.concat([existentes, dados_novos], ignore_index=True)
        conn.update(spreadsheet=url, data=atualizado)
        st.success("🚀 Reserva salva na planilha da gestora!")
        st.balloons()
    except:

        st.error("Erro ao conectar. Verifique se a planilha está como 'Editor' para todos.")
