# agent/loader.py
import os

def cargar_tickets_desde_txt() -> list[dict]:
    ruta_carpeta = os.path.join("data", "tickets")
    tickets = []
    for nombre_archivo in os.listdir(ruta_carpeta):
        if nombre_archivo.endswith(".txt"):
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            with open(ruta_completa, "r", encoding="utf-8") as archivo:
                contenido = archivo.read().strip()
                tickets.append({
                    "archivo": nombre_archivo,
                    "contenido": contenido
                })
    return tickets


