# frontend.py
import streamlit as st
import requests

st.set_page_config(page_title="Ecommerce Agent", page_icon="🛒")

st.title("🛒 Ecommerce Agent - Atención al Cliente")

st.markdown("""
Completa los campos como si fuera un mail de cliente. El sistema generará una respuesta profesional y empática.
""")

mail = st.text_input("From (email):")
subject = st.text_input("Subject:")
order = st.text_input("Order (opcional):")
store = st.text_input("Store (opcional):")
body = st.text_area("Mensaje:", height=100)

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