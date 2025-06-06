# agent/database.py

import pandas as pd

# Carga única de la base
df = pd.read_excel("data/master_flee.xlsx", sheet_name="Sheet1")

# Limpiamos nombres de columnas por si tienen espacios
df.columns = df.columns.str.strip()

def buscar_pedido_por_id(order_id: str) -> dict | None:
    if not order_id:
        return None
    order_id = str(order_id).strip().upper()
    df["# Order"] = df["# Order"].astype(str).str.strip().str.upper()
    fila = df[df["# Order"] == order_id]
    if fila.empty:
        return None
    datos = fila.iloc[0]
    return {
        "estado_pedido": datos.get("Order Status"),
        "subestado": datos.get("Order Sub Status"),
        "cliente": datos.get("Name"),
        "mail": datos.get("Mail"),
        "descripcion_producto": datos.get("Item Description") or datos.get("Description"),
        "fecha_pedido": str(datos.get("Order Date")),
        "carrier": datos.get("Carrier"),
        "tracking": datos.get("Tracking #"),
        "delivery_date": str(datos.get("Delivery date")),
        "store": datos.get("Store"),
        "country": datos.get("Country"),
        "order_id": datos.get("# Order"),
        "store_order": datos.get("Store Order"),
        "po_number": datos.get("PO #"),
        "po_date": str(datos.get("PO Date")),
        "order_price": datos.get("Order Price"),
        "unit_price": datos.get("Unit Price"),
        "supplier": datos.get("Supplier"),
        "lead_time": datos.get("Lead time"),
        "order_status": datos.get("Order Status"),
        "order_sub_status": datos.get("Order Sub Status")
    }

def buscar_pedido_por_mail(mail: str) -> dict | None:
    if not mail:
        return None
    mail = mail.strip().lower()
    df["Mail"] = df["Mail"].astype(str).str.strip().str.lower()
    fila = df[df["Mail"] == mail]
    if fila.empty:
        return None
    datos = fila.iloc[0]
    return {
        "estado_pedido": datos.get("Order Status"),
        "subestado": datos.get("Order Sub Status"),
        "cliente": datos.get("Name"),
        "mail": datos.get("Mail"),
        "descripcion_producto": datos.get("Item Description") or datos.get("Description"),
        "fecha_pedido": str(datos.get("Order Date")),
        "carrier": datos.get("Carrier"),
        "tracking": datos.get("Tracking #"),
        "delivery_date": str(datos.get("Delivery date")),
        "store": datos.get("Store"),
        "country": datos.get("Country"),
        "order_id": datos.get("# Order"),
        "store_order": datos.get("Store Order"),
        "po_number": datos.get("PO #"),
        "po_date": str(datos.get("PO Date")),
        "order_price": datos.get("Order Price"),
        "unit_price": datos.get("Unit Price"),
        "supplier": datos.get("Supplier"),
        "lead_time": datos.get("Lead time"),
        "order_status": datos.get("Order Status"),
        "order_sub_status": datos.get("Order Sub Status")
    }

import re

def extraer_order_id(texto: str) -> str | None:
    import re
    # Busca patrones tipo #12345
    match = re.search(r"#(\w+)", texto)
    if match:
        return match.group(1)
    # Busca patrones tipo Order: 123456, Pedido: H8, SB47185, TC6353, etc.
    match = re.search(r"(?:Order|Pedido)[^\w]?[:\s]*([A-Za-z0-9\-]+)", texto, re.IGNORECASE)
    if match:
        return match.group(1)
    # Solo acepta cadenas con al menos un número y no palabras comunes
    posibles = re.findall(r"\b([A-Za-z0-9\-]{2,})\b", texto)
    palabras_ignoradas = {
        "ticket", "from", "subject", "hello", "please", "order", "pedido", "thanks", "thank", "was", "arrive", "the", "and", "with", "for", "that", "have", "your", "you", "can", "let", "know", "when", "should", "expect", "week", "not", "been", "updated", "tracking", "number", "isn", "t", "updating", "my", "package", "on", "in", "details"
    }
    for posible in posibles:
        if any(char.isdigit() for char in posible) and posible.lower() not in palabras_ignoradas:
            return posible
    return None

def extraer_mail(texto: str) -> str | None:
    """Extrae el primer mail que encuentre en el texto."""
    match = re.search(r'[\w\.-]+@[\w\.-]+', texto)
    return match.group(0) if match else None

    