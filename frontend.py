import streamlit as st
import requests

st.set_page_config(page_title="Ecommerce Agent", page_icon="🛒")

# Paleta de colores
gris_oscuro = "#23272f"
gris_medio = "#353b48"
azul = "#1a4d6e"
blanco = "#f8fafc"
verde = "#2ecc71"

# Estilos personalizados
st.markdown(f"""
    <style>
    .main {{
        background-color: {gris_oscuro};
    }}
    .stTextInput, .stTextArea {{
        margin-bottom: 0.1rem !important;
    }}
    div[data-testid="stTextInput"] label, div[data-testid="stTextArea"] label {{
        color: {verde};
        font-weight: 600;
        font-size: 1.05rem;
    }}
    .stTextInput input {{
        background-color: {gris_medio};
        color: {blanco};
        border-radius: 6px;
        border: 1.5px solid {azul};
        font-size: 1rem;
    }}
    .stTextArea textarea {{
        background-color: {gris_medio};
        color: {blanco};
        border-radius: 6px;
        border: 1.5px solid {azul};
        min-height: 140px;
        font-size: 1.08rem;
    }}
    .stButton button {{
        background-color: {azul};
        color: {blanco};
        border-radius: 6px;
        font-weight: bold;
        font-size: 1.08rem;
        border: none;
        padding: 0.5rem 1.5rem;
    }}
    .stButton button:hover {{
        background-color: {verde};
        color: {gris_oscuro};
    }}
    .stMarkdown, .stCaption, .stAlert {{
        color: {blanco};
    }}
    </style>
""", unsafe_allow_html=True)

st.title("🛒 Argo - Agente de Atención al Cliente")

st.markdown(
    f'<div style="color:{blanco};font-size:1.1rem;">'
    "Completa los campos como si fuera un mail de cliente. El sistema generará una respuesta profesional y empática."
    "</div>",
    unsafe_allow_html=True
)

# Formulario compacto
col1, col2 = st.columns(2)
with col1:
    mail = st.text_input("From (email):", key="mail")
    order = st.text_input("Order (opcional):", key="order")
with col2:
    subject = st.text_input("Subject:", key="subject")
    store = st.text_input("Store (opcional):", key="store")

body = st.text_area("Mensaje:", height=180, key="body")

respuesta_final = ""

if st.button("Enviar"):
    if not (mail and subject and body):
        st.warning("Por favor, completa al menos email, subject y mensaje.")
    else:
        ticket = f"From: {mail}\nSubject: {subject}\n"
        if order:
            ticket += f"Order: {order}\n"
        if store:
            ticket += f"Store: {store}\n"
        ticket += f"\"{body}\""
        with st.spinner("Procesando..."):
            try:
                response = requests.post(
                    "http://localhost:8000/responder",
                    json={"ticket": ticket},
                    timeout=60
                )
                if response.status_code == 200:
                    data = response.json()
                    respuesta_final = data['respuesta']
                    st.success("Respuesta del agente:")
                    st.text_area("Respuesta lista para el cliente:", value=respuesta_final, height=200)
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Error de conexión: {e}")

st.markdown("---")
st.caption("Desarrollado por tu equipo de IA ✨")
hide_st_style = """
             <style>
             #MainMenu {visibility: hidden;}
             footer {visibility: hidden;}
             header {visibility: hidden;}
             </style>
             """
st.markdown(hide_st_style, unsafe_allow_html=True)