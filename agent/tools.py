import json
from agent.database import buscar_pedido_por_id, buscar_pedido_por_mail
from agent.responder import generar_respuesta

def tool_buscar_pedido_por_id(order_id: str) -> str:
    info = buscar_pedido_por_id(order_id)
    return str(info) if info else "No se encontró el pedido por ID."

def tool_buscar_pedido_por_mail(mail: str) -> str:
    mail_normalizado = mail.strip().lower()
    info = buscar_pedido_por_mail(mail_normalizado)
    return str(info) if info else "No se encontró el pedido por mail."

def tool_generar_respuesta_wrapper(input_data):
    if isinstance(input_data, str):
        input_data = input_data.strip()
        if input_data.startswith("`") and input_data.endswith("`"):
            input_data = input_data[1:-1].strip()
        try:
            input_data = json.loads(input_data)
        except Exception:
            return "Error: formato de entrada inválido para GenerarRespuesta. Debe ser JSON válido."
    return tool_generar_respuesta(input_data)

def tool_generar_respuesta(input_data):
    if isinstance(input_data, dict):
        ticket = input_data.get("ticket")
        info = input_data.get("info")
    else:
        data = json.loads(input_data)
        ticket = data.get("ticket")
        info = data.get("info")
    if not ticket:
        return "Error: el campo 'ticket' no puede ser vacío."
    if isinstance(info, str):
        try:
            info = json.loads(info)
        except Exception:
            return "No se pudo procesar la información del pedido."
    return generar_respuesta(ticket, info, None)

def tool_escalar_a_humano(ticket: str) -> str:
    return "Este caso requiere intervención humana. Se ha escalado a soporte."