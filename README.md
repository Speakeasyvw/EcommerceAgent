# EcommerceAgent

Sistema automatizado de atención al cliente para e-commerce usando IA y LLMs.

## Descripción

Este proyecto procesa tickets de clientes, clasifica la intención, recupera información de pedidos, genera respuestas automáticas personalizadas y guarda el historial de conversaciones.

## Arquitectura

- **Carga de tickets:** Lee archivos `.txt` desde `data/tickets/`.
- **Clasificación:** Determina la intención del ticket usando IA.
- **Extracción:** Obtiene datos clave (Order ID, email).
- **Base de datos:** Busca información del pedido en Excel.
- **Respuesta automática:** Usa Azure OpenAI para generar respuestas naturales.
- **Historial:** Guarda cada interacción en SQLite.

## Instalación

1. Clona el repositorio.
2. Instala dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Configura tus credenciales de Azure en `config/settings.py`.

## Uso

Procesa todos los tickets:
```
python main.py
```

Procesa solo 3 tickets (modo test):
```
python main.py  # y ajusta agent.procesar_tickets(n=3)
```

## Testing

Ejecuta los tests con:
```
pytest tests/
```

## Ejemplo de respuesta

> Hola [Cliente],  
> Gracias por tu consulta. Tu pedido está en proceso...  
> Saludos,  
> **Argo**

## Mejoras futuras

- Demo visual (Streamlit/Gradio)
- API REST (FastAPI)

