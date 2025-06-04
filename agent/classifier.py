# agent/classifier.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from config.settings import AZURE_API_VERSION,AZURE_DEPLOYMENT_NAME, AZURE_API_KEY, AZURE_ENDPOINT

# Modelo LLM de Azure
llm = AzureChatOpenAI(
    deployment_name=AZURE_DEPLOYMENT_NAME,
    api_key=AZURE_API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version= AZURE_API_VERSION
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente que clasifica tickets de clientes de e-commerce."),
    ("human", """
Eres un sistema inteligente de atención al cliente para un e-commerce.

A continuación recibirás el contenido de un ticket de soporte enviado por un cliente. Tu tarea es **clasificar el ticket en una única intención principal**, seleccionando solo una de las siguientes categorías:

1. Consulta sobre procesamiento o envío del pedido  
2. Problema con el número de seguimiento (tracking)  
3. Solicitud de reembolso  
4. Solicitud de cambio o modificación del pedido  
5. Consulta general sobre el estado del pedido  
6. Producto dañado o defectuoso  
7. Entrega en dirección incorrecta  
8. Producto incorrecto o diferente al esperado  
9. Otra (si no corresponde a ninguna de las anteriores)

**Devuelve solamente el número y el nombre de la categoría. No agregues explicaciones ni repitas el contenido del ticket.**

TICKET:
---
{ticket}
---

Respuesta:
""")
])

chain = prompt | llm

def clasificar_ticket(ticket: str) -> str:
    respuesta = chain.invoke({"ticket": ticket})
    return respuesta.content.strip().lower()
