import logging
from typing import Any

from .base import PolizaRepository

logger = logging.getLogger(__name__)


class FirestorePolizaRepository(PolizaRepository):
    """Lee de Firestore: <coleccion>, productos y siniestros."""

    def __init__(
        self,
        project: str | None = None,
        collection: str = "polizas",
        productos_collection: str = "productos",
        siniestros_collection: str = "siniestros",
        client: Any = None,
    ) -> None:
        if client is None:
            from google.cloud import firestore

            client = firestore.Client(project=project)
        self._client = client
        self._polizas = collection
        self._productos = productos_collection
        self._siniestros = siniestros_collection

    def _get(self, collection: str, doc_id: str) -> dict[str, Any] | None:
        snapshot = self._client.collection(collection).document(doc_id).get()
        if not snapshot.exists:
            return None
        return snapshot.to_dict()

    def obtener_poliza(self, numero_poliza: str) -> dict[str, Any] | None:
        return self._get(self._polizas, numero_poliza)

    def obtener_coberturas(self, codigo_producto: str) -> dict[str, Any] | None:
        return self._get(self._productos, codigo_producto)

    def obtener_siniestro(self, numero_siniestro: str) -> dict[str, Any] | None:
        return self._get(self._siniestros, numero_siniestro)
