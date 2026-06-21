import re
from datetime import date

def validar_dni(dni: str) -> bool:
    """Validación básica: 7-8 dígitos, opcional letra (pero aquí solo números)."""
    return bool(re.fullmatch(r"\d{7,8}", dni))

def validar_email(email: str) -> bool:
    return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))

def validar_telefono(telefono: str) -> bool:
    """Teléfono: 9-15 dígitos, opcional '+' al inicio."""
    return bool(re.fullmatch(r"\+?\d{9,15}", telefono))

def validar_nombre(nombre: str) -> bool:
    """Nombre no vacío y sin números (simplificado)."""
    return bool(nombre.strip() and not any(c.isdigit() for c in nombre))

def input_no_vacio(mensaje: str) -> str:
    """Solicita entrada hasta que no esté vacía."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Este campo no puede estar vacío.")

def input_fecha(mensaje: str) -> date:
    """Solicita fecha en formato YYYY-MM-DD."""
    while True:
        fecha_str = input(mensaje).strip()
        try:
            return date.fromisoformat(fecha_str)
        except ValueError:
            print("Formato inválido. Use AAAA-MM-DD (ej: 2026-06-11)")