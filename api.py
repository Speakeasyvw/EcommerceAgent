from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.tools import (
    tool_buscar_pedido_por_id,
    tool_buscar_pedido_por_mail,
    tool_generar_respuesta,
    tool_escalar_a_humano,
)
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import AzureChatOpenAI
from config.settings import AZURE_API_KEY, AZURE_ENDPOINT, AZURE_DEPLOYMENT_NAME, AZURE_API_VERSION
import json


# --- MODELOS ---
class TicketRequest(BaseModel):
    ticket: str
class Respuesta(BaseModel):
    respuesta: str

# --- LLM Y AGENTE ---
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

IMPORTANTE: Cuando uses la herramienta GenerarRespuesta, asegúrate de que la respuesta incluya SIEMPRE, si están disponibles, el número de seguimiento (tracking), el producto y la fecha de compra. Si alguno de estos datos no está disponible, no lo menciones. El campo 'ticket' debe ser una copia literal del input recibido (incluyendo mail, subject, número de orden, tienda y mensaje original).

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
2. Buscar la información del pedido usando primero el número de orden.
   Si el número de orden no está presente, es "N/A", "0" o está vacío, busca el pedido usando el mail del cliente.
   Si tampoco hay mail, escala el caso a un humano.
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

# wrapper para pasar el ticket original de forma segura
def tool_generar_respuesta_wrapper(input_data):
    if isinstance(input_data, str):
        input_data = input_data.strip()
        if input_data.startswith("`") and input_data.endswith("`"):
            input_data = input_data[1:-1].strip()
        # reemplaza saltos de línea reales por '\n'
        input_data = input_data.replace('\r\n', '\\n').replace('\n', '\\n')
        try:
            input_data = json.loads(input_data)
        except Exception:
            try:
                input_data = eval(input_data)
            except Exception:
                return "Error: formato de entrada inválido para GenerarRespuesta."
    return tool_generar_respuesta(input_data)
tools = [
    Tool.from_function(tool_buscar_pedido_por_id, name="BuscarPedidoPorID", description="Busca un pedido por su número de orden."),
    Tool.from_function(tool_buscar_pedido_por_mail, name="BuscarPedidoPorMail", description="Busca un pedido por mail del cliente."),
    Tool.from_function(tool_generar_respuesta_wrapper, name="GenerarRespuesta", description="Genera una respuesta profesional y empática para el cliente usando el ticket y la info del pedido. Usa un string JSON con 'ticket' e 'info'."),
    Tool.from_function(tool_escalar_a_humano, name="EscalarAHumano", description="Escala el caso a un humano si no puede resolverse automáticamente."),
]


# --- FASTAPI ---
app = FastAPI(
    title="Ecommerce Agent API",
    description="API para responder tickets de atención al cliente de e-commerce.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# inicia el agente con las herramientas y el LLM
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    system_message=system_prompt
)

@app.post("/responder", response_model=Respuesta)
async def responder_ticket(ticket_req: TicketRequest):
    ticket = ticket_req.ticket
    ticket = ticket.replace('\r\n', '\\n').replace('\n', '\\n').strip()
    respuesta = agent.invoke({"input": {"ticket": ticket}})
    # si el output es un dict y tiene "intermediate_steps", busca la última Observation
    if isinstance(respuesta, dict):
        # busca la última Observation si existe
        steps = respuesta.get("intermediate_steps")
        if steps and isinstance(steps, list) and len(steps) > 0:
            # cada step es (AgentAction, Observation)
            last_obs = steps[-1][1]
            mensaje_final = last_obs
        elif "output" in respuesta:
            mensaje_final = respuesta["output"]
        else:
            mensaje_final = str(respuesta)
    else:
        mensaje_final = str(respuesta)
    return {"respuesta": mensaje_final}