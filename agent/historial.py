import sqlite3

DB_PATH = "historial_clientes.db"

def inicializar_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mail TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ticket TEXT,
        respuesta TEXT
    )
    """)
    conn.commit()
    conn.close()

def guardar_historial(mail, ticket, respuesta):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO historial (mail, ticket, respuesta) VALUES (?, ?, ?)",
        (mail, ticket, respuesta)
    )
    conn.commit()
    conn.close()

def obtener_historial(mail):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, ticket, respuesta FROM historial WHERE mail = ? ORDER BY fecha", (mail,))
    historial = cursor.fetchall()
    conn.close()
    return historial