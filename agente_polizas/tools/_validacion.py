import re

POLIZA_RE = re.compile(r"^POL-\d{8}$")
SINIESTRO_RE = re.compile(r"^SIN-\d{8}$")
PRODUCTO_RE = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)*$")


def normalizar(valor: str | None) -> str:
    return (valor or "").strip().upper()


def error(mensaje: str) -> dict:
    return {"status": "error", "error_message": mensaje}
