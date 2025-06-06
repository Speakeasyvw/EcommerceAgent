class EcommerceAgent:
    def __init__(self, loader, classifier, db, responder, historial):
        self.loader = loader
        self.classifier = classifier
        self.db = db
        self.responder = responder
        self.historial = historial

    def procesar_tickets(self, n=None):
        tickets = self.loader()
        if n is not None:
            tickets = tickets[:n]
        for ticket in tickets:
            contenido = ticket["contenido"]
            intencion = self.classifier(contenido)
            print(f"{ticket['archivo']} => Intención: {intencion}")

            order_id = self.db['extraer_order_id'](contenido)
            info = self.db['buscar_pedido_por_id'](order_id) if order_id else None
            if not info:
                mail = self.db['extraer_mail'](contenido)
                info = self.db['buscar_pedido_por_mail'](mail) if mail else None

            if info:
                print(f"→ Cliente: {info['cliente']}")
                print(f"→ Mail: {info['mail']}")
                print(f"→ Fecha: {info['fecha_pedido']}")
                print(f"→ Carrier: {info['carrier']}")
                print(f"→ Tienda: {info['store']}")
                historial = self.historial['obtener_historial'](info['mail'])
                respuesta = self.responder(contenido, info, historial)
                print("\nRespuesta sugerida para el cliente:\n")
                print(respuesta)
                self.historial['guardar_historial'](info['mail'], contenido, respuesta)
            else:
                print("→ No se encontró información del pedido.")
            print("-" * 40)