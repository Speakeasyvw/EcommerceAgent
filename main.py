# main.py

from agent.loader import cargar_tickets_desde_txt
from agent.classifier import clasificar_ticket
from agent.database import buscar_pedido_por_id, buscar_pedido_por_mail, extraer_order_id, extraer_mail
from agent.responder import generar_respuesta
from agent.historial import inicializar_db, guardar_historial, obtener_historial
import sys

inicializar_db()
tickets = cargar_tickets_desde_txt()

if tickets:
    for ticket in tickets[:3]:  # Procesar solo los primeros 3 tickets
        contenido = ticket["contenido"]
        intencion = clasificar_ticket(contenido)
        print(f"{ticket['archivo']} => Intención: {intencion}")

        order_id = extraer_order_id(contenido)
        print(f"Order ID extraído: {order_id}")
        info = buscar_pedido_por_id(order_id) if order_id else None

        if info:
            print(f"→ Pedido encontrado por Order ID: {order_id}")
        else:
            mail = extraer_mail(contenido)
            print(f"Mail extraído: {mail}")
            info = buscar_pedido_por_mail(mail) if mail else None
            if info:
                print(f"→ Pedido encontrado por mail: {mail}")
            else:
                print("→ No se encontró información del pedido.")

        if info:
            print(f"→ Estado: {info['estado_pedido']}")
            print(f"→ Producto: {info['descripcion_producto']}")
            print(f"→ Cliente: {info['cliente']}")
            print(f"→ Mail: {info['mail']}")
            print(f"→ Fecha: {info['fecha_pedido']}")
            print(f"→ Carrier: {info['carrier']}")
            print(f"→ Tienda: {info['store']}")
            # Generar y mostrar respuesta automática
            respuesta = generar_respuesta(contenido, info)
            print("\nRespuesta sugerida para el cliente:\n")
            print(respuesta)
            # Guardar historial
            guardar_historial(info['mail'], contenido, respuesta)
        print("-" * 40)
    print("Procesamiento de tickets finalizado.")
    sys.exit(0)
else:
    print("No hay tickets para procesar.")
    sys.exit(0)

#Para consultar el historial de un cliente específico
#mail_consulta = input("Ingrese el mail del cliente para consultar su historial: ").strip().lower()
#if info:
    ## ...existing prints y guardar_historial...
   #historial = obtener_historial(info['mail'])
    #print("\nHistorial de conversaciones con este cliente:")
    #for fecha, ticket, respuesta in historial:
    #    print(f"\nFecha: {fecha}\nTicket: {ticket}\nRespuesta: {respuesta}\n{'-'*20}")