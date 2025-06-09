# agent/responder_ticket.py
import time
import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from config.settings import AZURE_API_VERSION,AZURE_DEPLOYMENT_NAME, AZURE_API_KEY, AZURE_ENDPOINT

# Config logging básico
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filename="logs_azure_openai.txt",  # guarda en archivo
    filemode="a"  # append
)

llm = AzureChatOpenAI(
    deployment_name=AZURE_DEPLOYMENT_NAME,
    api_key=AZURE_API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version= AZURE_API_VERSION,
    temperature=0.3,  # temperatura baja para respuestas más coherentes y formales
    max_tokens=750  # aumentar el límite de tokens en caso de necesitar respuestas más detalladas
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un agente de atención al cliente de una tienda online llamado Argo. Responde de forma clara, amable y profesional. Firma siempre como 'Argo'."),
    ("human", """
Este es un ticket de un cliente:

"{ticket}"

Estos son los datos del pedido:

- Cliente: {cliente}
- Estado: {estado}
- Subestado: {subestado}
- Fecha del pedido: {fecha}
- Producto: {producto}
- Precio total: {precio_total}
- Precio unitario: {precio_unitario}
- Transportista: {carrier}
- Tracking: {tracking}
- Fecha de entrega estimada: {delivery_date}
- Tienda: {tienda}
- País: {pais}
- Proveedor: {proveedor}
- Lead time: {lead_time}
- Nota interna: {nota}

Redacta una respuesta natural al cliente en base a su consulta y estos datos. Sé empático si hay algún problema, y no repitas la información literal del ticket.
Firma siempre como 'Argo' al final de la respuesta.
""")
])

chain = prompt | llm

def generar_respuesta(ticket: str, info_pedido: dict, historial: list = None) -> str:
    historial_texto = ""
    if historial:
        for fecha, ticket_ant, respuesta_ant in historial[-3:]:
            historial_texto += f"\n[Historial]\nCliente: {ticket_ant}\nAgente: {respuesta_ant}\n"
    payload = {
        "ticket": ticket + historial_texto,
        "cliente": info_pedido.get("cliente"),
        "estado": info_pedido.get("estado_pedido"),
        "subestado": info_pedido.get("subestado"),
        "fecha": info_pedido.get("fecha_pedido"),
        "producto": info_pedido.get("descripcion_producto"),
        "precio_total": info_pedido.get("order_price"),
        "precio_unitario": info_pedido.get("unit_price"),
        "carrier": info_pedido.get("carrier"),
        "tracking": info_pedido.get("tracking"),
        "delivery_date": info_pedido.get("delivery_date"),
        "tienda": info_pedido.get("store"),
        "pais": info_pedido.get("country"),
        "proveedor": info_pedido.get("supplier"),
        "lead_time": info_pedido.get("lead_time"),
        "nota": info_pedido.get("note"),
    }
    start = time.time()
    respuesta = chain.invoke(payload)
    end = time.time()
    logging.info(f"Tiempo de respuesta Azure OpenAI: {end - start:.2f} segundos")

    # --- BLOQUE EXTRA: Forzar inclusión de datos clave ---
    extras = []
    if info_pedido.get("tracking") and info_pedido.get("tracking") != "-":
        extras.append(f"Número de seguimiento: {info_pedido['tracking']}")
    if info_pedido.get("descripcion_producto"):
        extras.append(f"Producto: {info_pedido['descripcion_producto']}")
    if info_pedido.get("fecha_pedido"):
        extras.append(f"Fecha de compra: {info_pedido['fecha_pedido']}")
    if extras:
        respuesta_final = respuesta.content.strip() + "\n\n" + "\n".join(extras)
    else:
        respuesta_final = respuesta.content.strip()
    return respuesta_final

