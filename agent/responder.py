# agent/responder_ticket.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from config.settings import AZURE_API_VERSION,AZURE_DEPLOYMENT_NAME, AZURE_API_KEY, AZURE_ENDPOINT

llm = AzureChatOpenAI(
    deployment_name=AZURE_DEPLOYMENT_NAME,
    api_key=AZURE_API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version= AZURE_API_VERSION
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un agente de atención al cliente de una tienda online. Responde de forma clara, amable y profesional."),
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
""")
])

chain = prompt | llm

def generar_respuesta(ticket: str, info_pedido: dict) -> str:
    return chain.invoke({
        "ticket": ticket,
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
    }).content.strip()
