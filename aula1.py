import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, time

# Configuração da página
st.set_page_config(page_title="Mapa Cirúrgico Oficial", layout="centered")

st.title("🏥 Reserva de Sala Cirúrgica")

# 1. LINK CORRETO DA PLANILHA (Link principal)
url_oficial = "https://docs.google.com/spreadsheets/d/1-w1V1UfEfwxRAMd_gw9n3D0u5lZgDyzFGBGxNNsRAzc/edit#gid=0"

# 2. LIGANDO A CONEXÃO (O que faltava!)
conn = st.connection("gsheets", type=GSheetsConnection)

# FORMULÁRIO
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

# AÇÃO DE SALVAR
if botao:
    # Cálculo do gatilho de 7 dias
    data_gatilho = data_cir + pd.Timedelta(days=7)
    
    # Organizando os dados
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

    try:
        # Lendo e atualizando
        existentes = conn.read(spreadsheet=url_oficial)
        atualizado = pd.concat([existentes, dados_novos], ignore_index=True)
        conn.update(spreadsheet=url_oficial, data=atualizado)
        st.success("🚀 Reserva salva na planilha da gestora!")
        st.balloons()
    except Exception as e:
        st.error(f"Erro técnico: {e}")
        st.error("DICA: Verifique se a planilha está como 'EDITOR' para 'Qualquer pessoa com o link'.")
