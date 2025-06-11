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
- **Demo visual:** Incluye una interfaz visual para probar el sistema.

## Instalación

1. Clona el repositorio.
2. Configura tus credenciales de Azure en `config/settings.py`.
3. Abrir terminal y ejecutar: python -m venv env
4. Activar el env: env/scripts/activate 
-----
 Si nos da un error por falta de autorización ejecutamos como administrador 
el siguiente comando en el PowerShell de Windows:

Set-ExecutionPolicy RemoteSigned -Scope LocalMachine

luego apretamos "s" para confirmar
Luego repetimos el paso 4
-----
5. Instala dependencias:
   ```
   pip install -r requirements.txt
   ```
---
 - Recuerden poner su Api Key en un archivo .env .
 - Recuerden tambien setear sus variables de entorno en la consola de siguiente forma, reemplazando con los correspondientes valores.
   
 $env:AZURE_API_KEY="AZURE API KEY"
 $env:AZURE_DEPLOYMENT_NAME="DEPLOYMENT NAME"
 $env:AZURE_ENDPOINT="AZURE ENDPOINT"
 $env:AZURE_API_VERSION="API VERSION"
 
---

## Uso

Procesa todos los tickets:
```
python main.py
```

Procesa solo 3 tickets (modo test):
```
python main.py  # y ajusta agent.procesar_tickets(n=3)
```

## API REST

Levanta el servidor FastAPI:
```
uvicorn api:app --reload
```
Envía tickets vía POST a `/responder`:
```json
{
  "ticket": "From: cliente@email.com\nSubject: Consulta\nOrder: 12345\nStore: Tienda\nMensaje del cliente..."
}
```

## Demo visual

Ejecuta la demo visual:
```
python frontend.py
```
Accede a la interfaz en tu navegador para probar el sistema de manera interactiva.

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

- Integración multicanal (email, WhatsApp)
- Mejoras en la extracción de datos y clasificación
- Panel de administración web

- Mejorar agente con contexto sobre politicas de empresa
- Mejorar contexto con fechas de consultas, casos mas reales
- En caso de escalar el caso, enviar un mail/aviso a tal agente real automaticamente

---
Dudas o sugerencias? Porfavor abrir un issue o pull request
