import logging

from ..repositories import get_repository
from ._validacion import POLIZA_RE, PRODUCTO_RE, error, normalizar

logger = logging.getLogger(__name__)

_CAMPOS_POLIZA = (
    "numero_poliza",
    "codigo_producto",
    "estado",
    "fecha_inicio",
    "fecha_fin",
    "prima_mensual",
)


def consultar_poliza(numero_poliza: str) -> dict:
    """Consulta el estado y vigencia de una póliza.

    Args:
        numero_poliza: Número de póliza con formato POL-XXXXXXXX (8 dígitos).

    Returns:
        dict con status y los datos de la póliza, o error_message.
    """
    numero = normalizar(numero_poliza)
    if not POLIZA_RE.match(numero):
        return error("Número de póliza inválido. El formato esperado es POL- seguido de 8 dígitos.")

    try:
        poliza = get_repository().obtener_poliza(numero)
    except Exception:
        logger.exception("Error consultando póliza %s", numero)
        return error("No fue posible consultar la póliza en este momento.")

    if poliza is None:
        return error(f"No se encontró la póliza {numero}.")

    # No se expone el titular ni otros datos personales.
    return {"status": "success", "poliza": {k: poliza.get(k) for k in _CAMPOS_POLIZA}}


def listar_coberturas(codigo_producto: str) -> dict:
    """Lista las coberturas de un producto.

    Args:
        codigo_producto: Código del producto, p. ej. AUTO-PLUS.

    Returns:
        dict con status, nombre del producto y coberturas, o error_message.
    """
    codigo = normalizar(codigo_producto)
    if not codigo or len(codigo) > 40 or not PRODUCTO_RE.match(codigo):
        return error("Código de producto inválido.")

    try:
        producto = get_repository().obtener_coberturas(codigo)
    except Exception:
        logger.exception("Error consultando coberturas de %s", codigo)
        return error("No fue posible consultar las coberturas en este momento.")

    if producto is None:
        return error(f"No se encontró el producto {codigo}.")

    return {
        "status": "success",
        "codigo_producto": codigo,
        "nombre": producto.get("nombre"),
        "coberturas": producto.get("coberturas", []),
    }
