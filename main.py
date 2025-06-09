from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import AzureChatOpenAI
from agent.tools import (
    tool_buscar_pedido_por_id,
    tool_buscar_pedido_por_mail,
    tool_generar_respuesta,
    tool_escalar_a_humano,
)
from agent.loader import cargar_tickets_desde_txt
from agent.historial import inicializar_db
from config.settings import AZURE_API_KEY, AZURE_ENDPOINT, AZURE_DEPLOYMENT_NAME, AZURE_API_VERSION

import sys

# inicializa la base de datos si es necesario
inicializar_db()

llm = AzureChatOpenAI(
    deployment_name=AZURE_DEPLOYMENT_NAME,
    api_key=AZURE_API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version=AZURE_API_VERSION
)

system_prompt = """
Eres un agente de atención al cliente para un e-commerce.
Responde siempre de manera profesional, empática y clara, como lo haría un agente humano experimentado.
Agradece la consulta, ofrece ayuda y muestra comprensión ante problemas o demoras.
Nunca inventes información: si no tienes datos suficientes, escala el caso a un humano.

SIEMPRE que uses la herramienta GenerarRespuesta, el campo 'ticket' debe ser una copia literal del input recibido (incluyendo mail, subject, número de orden, tienda y mensaje original). Si el input recibido es:

From: chrismcdaniel1976@hotmail.com
Subject: Question about my order
Order: 216408
Store: Balma Home [US]
"Hello, I just placed an order and Id like to confirm the expected processing time before it ships. Can you provide some details?"

entonces el campo 'ticket' debe ser exactamente ese texto, sin modificar ni resumir.

Tienes acceso a las siguientes herramientas:
- BuscarPedidoPorID: Busca información de un pedido usando el número de orden.
- BuscarPedidoPorMail: Busca información de un pedido usando el mail del cliente.
- GenerarRespuesta: Redacta una respuesta profesional y empática para el cliente usando el ticket y la información del pedido.
  Cuando uses esta herramienta, pásale un string JSON o un diccionario Python con los campos 'ticket' e 'info', donde:
    - 'ticket' debe contener el **texto completo del ticket** (no un número ni un identificador).
    - 'info' es el resultado de la búsqueda del pedido (puede ser un diccionario con los datos relevantes).
- EscalarAHumano: Escala el caso a un humano si no puedes resolverlo automáticamente.

Tu objetivo es:
1. Analizar el ticket y extraer los datos relevantes (número de orden, mail, etc).
2. Buscar la información del pedido usando primero el número de orden, luego el mail.
3. Si encuentras la información, usa GenerarRespuesta para responder al cliente.
4. Si no puedes resolver el caso, usa EscalarAHumano.
5. Sé claro, profesional y empático en todas las respuestas.

IMPORTANTE: Cuando uses la herramienta GenerarRespuesta, el campo 'ticket' debe ser exactamente el texto completo del ticket recibido como input, sin modificar ni resumir. NUNCA pongas solo un número, ID, mail, subject o resumen. Si tienes dudas, copia literalmente el texto del ticket recibido.

Ejemplo de uso correcto de GenerarRespuesta:
Input recibido:
From: Kaz115@hotmail.co.uk
Subject: When will my order arrive?
"Hi, I ordered the Premium 5 in 1 Hair Styler, and I need to know when it will arrive. Could you please give me an estimated delivery date?"

Llamada correcta a la tool:
{
  "ticket": "From: Kaz115@hotmail.co.uk\nSubject: When will my order arrive?\n\"Hi, I ordered the Premium 5 in 1 Hair Styler, and I need to know when it will arrive. Could you please give me an estimated delivery date?\"",
  "info": {
    "estado_pedido": "Purchased",
    "cliente": "Karen Leadbitter",
    "mail": "Kaz115@hotmail.co.uk",
    "descripcion_producto": "Premium 5 in 1 Hair Styler Pro with Hot Brush and Dryer Functions",
    "carrier": "Cainiao",
    "tracking": "LP00705094419884",
    "delivery_date": "2025-08-01 00:00:00",
    "order_id": "5960"
  }
}

ADVERTENCIA: Si el campo 'ticket' no es el texto completo del ticket recibido como input (incluyendo mail, subject, número de orden, tienda y mensaje original), RECHAZA la acción y corrígelo antes de llamar a la herramienta. NUNCA uses solo un número, ID, mail, subject o resumen.

Ejemplo INCORRECTO:
{
  "ticket": "216408",
  "info": { ... }
}
Corrección:
{
  "ticket": "From: chrismcdaniel1976@hotmail.com\nSubject: Question about my order\nOrder: 216408\nStore: Balma Home [US]\n\"Hello, I just placed an order and I’d like to confirm the expected processing time before it ships. Can you provide some details?\"",
  "info": { ... }
}
"""

# variable global para guardar el ticket original
last_ticket_input = None

def tool_generar_respuesta_wrapper(input_data):
    global last_ticket_input
    return tool_generar_respuesta(input_data, original_ticket=last_ticket_input)

# define las tools
tools = [
    Tool.from_function(tool_buscar_pedido_por_id, name="BuscarPedidoPorID", description="Busca un pedido por su número de orden."),
    Tool.from_function(tool_buscar_pedido_por_mail, name="BuscarPedidoPorMail", description="Busca un pedido por mail del cliente."),
    Tool.from_function(tool_generar_respuesta_wrapper, name="GenerarRespuesta", description="Genera una respuesta profesional y empática para el cliente usando el ticket y la info del pedido. Usa un string JSON con 'ticket' e 'info'."),
    Tool.from_function(tool_escalar_a_humano, name="EscalarAHumano", description="Escala el caso a un humano si no puede resolverse automáticamente."),
]

# inicia el agente
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    system_message=system_prompt
)

# carga los tickets y prueba los primeros 3
tickets = cargar_tickets_desde_txt()
for idx, ticket_dict in enumerate(tickets[:3], 1):
    mail = ticket_dict.get("mail") or ""
    subject = ticket_dict.get("subject") or ""
    body = ticket_dict["contenido"]
    ticket = f"From: {mail}\nSubject: {subject}\n{body}"
    print(f"\n--- Ticket #{idx} ---\n{ticket}\n")
    last_ticket_input = ticket 
    try:
        respuesta = agent.invoke(ticket)
        print(f"Respuesta:\n{respuesta}\n{'-'*40}")
    except Exception as e:
        print(f"Error procesando el ticket #{idx}: {e}", file=sys.stderr)