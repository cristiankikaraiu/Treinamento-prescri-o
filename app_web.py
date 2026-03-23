import streamlit as st
import json
import random

# Configuração da página para parecer um App
st.set_page_config(page_title="Simulador de Prescrição", page_icon="💊")

# Estilo para ficar com cara de App Moderno
st.markdown("""
    <style>
    .main { background-color: #121212; color: white; }
    div.stButton > button { width: 100%; border-radius: 10px; height: 3em; background-color: #1f6aa5; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Carregar os dados
def carregar_dados():
    try:
        with open('dados.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

dados = carregar_dados()

if not dados:
    st.error("Erro: arquivo dados.json não encontrado!")
else:
    # Sorteio do caso (salva na sessão para não mudar ao digitar)
    if 'caso' not in st.session_state:
        st.session_state.caso = random.choice(dados)

    st.title("🩺 Treino de Prescrição")
    st.subheader(st.session_state.caso['pergunta'])

    # Campos de entrada
    med = st.text_input("Medicamento e Dosagem", placeholder="Ex: Dipirona 500 mg/ml...")
    qtd = st.text_input("Quantidade", placeholder="Ex: 1 ampola")
    intervalo = st.text_input("Intervalo", placeholder="Ex: 6/6h")
    adm = st.text_input("Quanto administrar", placeholder="Ex: 01 ampola")
    dil = st.text_input("Diluição", placeholder="Ex: 18ml de SF")

    if st.button("VERIFICAR RESPOSTA"):
        # Gabarito vs Resposta (tudo em minúsculo e sem espaços sobrando)
        resp = [med.strip().lower(), qtd.strip().lower(), intervalo.strip().lower(), adm.strip().lower(), dil.strip().lower()]
        gab = [st.session_state.caso['medicamento'].lower(), st.session_state.caso['quantidade'].lower(), 
               st.session_state.caso['intervalo'].lower(), st.session_state.caso['administrar'].lower(), 
               st.session_state.caso['diluicao'].lower()]

        if resp == gab:
            st.success("✅ CORRETO! Prescrição impecável.")
        else:
            st.error(f"❌ INCORRETO!")
            st.info(f"**Gabarito:**\n\n{st.session_state.caso['medicamento']}\n\nQtd: {st.session_state.caso['quantidade']} | Int: {st.session_state.caso['intervalo']}\n\nAdm: {st.session_state.caso['administrar']} em {st.session_state.caso['diluicao']}")

    if st.button("PRÓXIMO CASO"):
        st.session_state.caso = random.choice(dados)
        st.rerun()