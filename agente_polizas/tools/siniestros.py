import logging

from ..repositories import get_repository
from ._validacion import SINIESTRO_RE, error, normalizar

logger = logging.getLogger(__name__)

_CAMPOS_SINIESTRO = (
    "numero_siniestro",
    "numero_poliza",
    "estado",
    "fecha_reporte",
    "ultima_actualizacion",
)


def consultar_estado_siniestro(numero_siniestro: str) -> dict:
    """Consulta el estado de un siniestro.

    Args:
        numero_siniestro: Número de siniestro con formato SIN-XXXXXXXX (8 dígitos).

    Returns:
        dict con status y el estado del siniestro, o error_message.
    """
    numero = normalizar(numero_siniestro)
    if not SINIESTRO_RE.match(numero):
        return error(
            "Número de siniestro inválido. El formato esperado es SIN- seguido de 8 dígitos."
        )

    try:
        siniestro = get_repository().obtener_siniestro(numero)
    except Exception:
        logger.exception("Error consultando siniestro %s", numero)
        return error("No fue posible consultar el siniestro en este momento.")

    if siniestro is None:
        return error(f"No se encontró el siniestro {numero}.")

    return {"status": "success", "siniestro": {k: siniestro.get(k) for k in _CAMPOS_SINIESTRO}}
