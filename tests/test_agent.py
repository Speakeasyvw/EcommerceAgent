
import pytest
from agent.database import extraer_order_id, extraer_mail
from agent.classifier import clasificar_ticket

def test_extraer_order_id():
    texto = "Hola, mi número de pedido es #12345 y quiero saber el estado."
    assert extraer_order_id(texto) == "12345"

def test_extraer_mail():
    texto = "Mi correo es cliente@ejemplo.com, por favor avísenme."
    assert extraer_mail(texto) == "cliente@ejemplo.com"

def test_clasificar_ticket():
    texto = "¿Cuándo llega mi pedido?"
    resultado = clasificar_ticket(texto)
    assert any(palabra in resultado for palabra in ["envío", "procesamiento", "estado"])