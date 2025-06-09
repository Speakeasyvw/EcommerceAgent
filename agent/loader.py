# agent/loader.py
import os

def parse_ticket_mail(texto: str) -> dict:
    import re
    lines = texto.splitlines()
    mail = None
    subject = None
    body_lines = []
    for line in lines:
        if line.lower().startswith("from:"):
            match = re.search(r'[\w\.-]+@[\w\.-]+', line)
            if match:
                mail = match.group(0)
        elif line.lower().startswith("subject:"):
            subject = line.split(":", 1)[1].strip()
        elif not line.lower().startswith("ticket"):
            body_lines.append(line)
    body = "\n".join(body_lines).strip()
    return {
        "mail": mail,
        "subject": subject,
        "body": body
    }

def cargar_tickets_desde_txt() -> list[dict]:
    ruta_carpeta = os.path.join("data", "tickets")
    tickets = []
    for nombre_archivo in os.listdir(ruta_carpeta):
        if nombre_archivo.endswith(".txt"):
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            with open(ruta_completa, "r", encoding="utf-8") as archivo:
                contenido = archivo.read().strip()
                # aplica el parser para mails/CRM
                parsed = parse_ticket_mail(contenido)
                tickets.append({
                    "archivo": nombre_archivo,
                    "contenido": parsed["body"],   # solo el cuerpo del mensaje
                    "mail": parsed["mail"],        # mail extraído (si existe)
                    "subject": parsed["subject"]   # asunto extraído (si existe)
                })
    return tickets