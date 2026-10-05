import copy
from typing import Any

from .base import PolizaRepository

# Datos ficticios para desarrollo local y pruebas.
_POLIZAS = {
    "POL-00000001": {
        "numero_poliza": "POL-00000001",
        "titular": "Cliente Prueba Uno",
        "codigo_producto": "AUTO-PLUS",
        "estado": "VIGENTE",
        "fecha_inicio": "2026-01-15",
        "fecha_fin": "2027-01-14",
        "prima_mensual": 185000,
    },
    "POL-00000002": {
        "numero_poliza": "POL-00000002",
        "titular": "Cliente Prueba Dos",
        "codigo_producto": "HOGAR-BASICO",
        "estado": "CANCELADA",
        "fecha_inicio": "2024-03-01",
        "fecha_fin": "2025-02-28",
        "prima_mensual": 62000,
    },
    "POL-00000003": {
        "numero_poliza": "POL-00000003",
        "titular": "Cliente Prueba Tres",
        "codigo_producto": "VIDA-INDIVIDUAL",
        "estado": "EN_MORA",
        "fecha_inicio": "2025-06-10",
        "fecha_fin": "2026-06-09",
        "prima_mensual": 98000,
    },
}

_PRODUCTOS = {
    "AUTO-PLUS": {
        "codigo_producto": "AUTO-PLUS",
        "nombre": "Auto Plus (demo)",
        "coberturas": [
            {"nombre": "Responsabilidad civil extracontractual", "limite": 2000000000},
            {"nombre": "Pérdida total por daños", "limite": "100% valor comercial"},
            {"nombre": "Hurto", "limite": "100% valor comercial"},
            {"nombre": "Asistencia en viaje", "limite": "Incluida"},
        ],
    },
    "HOGAR-BASICO": {
        "codigo_producto": "HOGAR-BASICO",
        "nombre": "Hogar Básico (demo)",
        "coberturas": [
            {"nombre": "Incendio y anexos", "limite": 300000000},
            {"nombre": "Daños por agua", "limite": 20000000},
        ],
    },
    "VIDA-INDIVIDUAL": {
        "codigo_producto": "VIDA-INDIVIDUAL",
        "nombre": "Vida Individual (demo)",
        "coberturas": [
            {"nombre": "Muerte por cualquier causa", "limite": 150000000},
            {"nombre": "Incapacidad total y permanente", "limite": 150000000},
        ],
    },
}

_SINIESTROS = {
    "SIN-00000001": {
        "numero_siniestro": "SIN-00000001",
        "numero_poliza": "POL-00000001",
        "estado": "EN_EVALUACION",
        "fecha_reporte": "2026-08-20",
        "descripcion": "Choque simple en parqueadero",
        "ultima_actualizacion": "2026-09-02",
    },
    "SIN-00000002": {
        "numero_siniestro": "SIN-00000002",
        "numero_poliza": "POL-00000003",
        "estado": "PAGADO",
        "fecha_reporte": "2025-11-03",
        "descripcion": "Reclamación de prueba",
        "ultima_actualizacion": "2025-12-15",
    },
}


class InMemoryPolizaRepository(PolizaRepository):
    def __init__(
        self,
        polizas: dict[str, dict] | None = None,
        productos: dict[str, dict] | None = None,
        siniestros: dict[str, dict] | None = None,
    ) -> None:
        self._polizas = copy.deepcopy(polizas if polizas is not None else _POLIZAS)
        self._productos = copy.deepcopy(productos if productos is not None else _PRODUCTOS)
        self._siniestros = copy.deepcopy(siniestros if siniestros is not None else _SINIESTROS)

    def obtener_poliza(self, numero_poliza: str) -> dict[str, Any] | None:
        return copy.deepcopy(self._polizas.get(numero_poliza))

    def obtener_coberturas(self, codigo_producto: str) -> dict[str, Any] | None:
        return copy.deepcopy(self._productos.get(codigo_producto))

    def obtener_siniestro(self, numero_siniestro: str) -> dict[str, Any] | None:
        return copy.deepcopy(self._siniestros.get(numero_siniestro))
