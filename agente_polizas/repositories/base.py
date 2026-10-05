from abc import ABC, abstractmethod
from typing import Any


class PolizaRepository(ABC):
    """Acceso a pólizas, productos y siniestros."""

    @abstractmethod
    def obtener_poliza(self, numero_poliza: str) -> dict[str, Any] | None: ...

    @abstractmethod
    def obtener_coberturas(self, codigo_producto: str) -> dict[str, Any] | None: ...

    @abstractmethod
    def obtener_siniestro(self, numero_siniestro: str) -> dict[str, Any] | None: ...
