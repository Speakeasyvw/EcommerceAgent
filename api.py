from fastapi import FastAPI, Request
from agent.loader import cargar_tickets_desde_txt
from agent.classifier import clasificar_ticket
from agent.database import buscar_pedido_por_id, buscar_pedido_por_mail, extraer_order_id, extraer_mail
from agent.responder import generar_respuesta
from agent.historial import inicializar_db, guardar_historial, obtener_historial
from agent.ecommerce_agent import EcommerceAgent
from pydantic import BaseModel

class TicketRequest(BaseModel):
    ticket: str
inicializar_db()

agent = EcommerceAgent(
    loader=cargar_tickets_desde_txt,
    classifier=clasificar_ticket,
    db={
        'buscar_pedido_por_id': buscar_pedido_por_id,
        'buscar_pedido_por_mail': buscar_pedido_por_mail,
        'extraer_order_id': extraer_order_id,
        'extraer_mail': extraer_mail
    },
    responder=generar_respuesta,
    historial={
        'obtener_historial': obtener_historial,
        'guardar_historial': guardar_historial
    }
)

app = FastAPI()

@app.post("/responder")
async def responder_ticket(request: TicketRequest):
    try:
        ticket = request.ticket
        order_id = agent.db['extraer_order_id'](ticket)
        info = agent.db['buscar_pedido_por_id'](order_id) if order_id else None
        if not info:
            mail = agent.db['extraer_mail'](ticket)
            info = agent.db['buscar_pedido_por_mail'](mail) if mail else None
        if not info:
            return {"error": "No se encontró información del pedido para el ticket."}
        historial = agent.historial['obtener_historial'](info['mail'])
        respuesta = agent.responder(ticket, info, historial)
        return {"respuesta": respuesta}
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {"error": str(e)}