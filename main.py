# main.py
from agent.loader import cargar_tickets_desde_txt
from agent.classifier import clasificar_ticket
from agent.database import buscar_pedido_por_id, buscar_pedido_por_mail, extraer_order_id, extraer_mail
from agent.responder import generar_respuesta
from agent.historial import inicializar_db, guardar_historial, obtener_historial
from agent.ecommerce_agent import EcommerceAgent
import sys

inicializar_db()

# instancia el agente con los módulos/funciones necesarias
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
# procesa los tickets. El para n indica el numero de tickets a procesar
agent.procesar_tickets(n=1)