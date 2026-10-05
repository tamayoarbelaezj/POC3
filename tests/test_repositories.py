from unittest.mock import MagicMock

from agente_polizas.repositories.firestore_repo import FirestorePolizaRepository
from agente_polizas.repositories.memory_repo import InMemoryPolizaRepository


def test_memoria_devuelve_poliza_existente():
    repo = InMemoryPolizaRepository()
    poliza = repo.obtener_poliza("POL-00000001")
    assert poliza["estado"] == "VIGENTE"


def test_memoria_devuelve_none_si_no_existe():
    repo = InMemoryPolizaRepository()
    assert repo.obtener_poliza("POL-99999999") is None
    assert repo.obtener_coberturas("NO-EXISTE") is None
    assert repo.obtener_siniestro("SIN-99999999") is None


def test_memoria_no_comparte_estado_mutable():
    repo = InMemoryPolizaRepository()
    poliza = repo.obtener_poliza("POL-00000001")
    poliza["estado"] = "MODIFICADA"
    assert repo.obtener_poliza("POL-00000001")["estado"] == "VIGENTE"


def test_memoria_con_datos_personalizados():
    repo = InMemoryPolizaRepository(polizas={"POL-12345678": {"estado": "VIGENTE"}})
    assert repo.obtener_poliza("POL-12345678") == {"estado": "VIGENTE"}
    assert repo.obtener_poliza("POL-00000001") is None


def _cliente_firestore(existe: bool, datos: dict | None = None):
    snapshot = MagicMock()
    snapshot.exists = existe
    snapshot.to_dict.return_value = datos
    client = MagicMock()
    client.collection.return_value.document.return_value.get.return_value = snapshot
    return client


def test_firestore_lee_documento():
    client = _cliente_firestore(True, {"numero_poliza": "POL-00000001"})
    repo = FirestorePolizaRepository(collection="polizas_test", client=client)

    assert repo.obtener_poliza("POL-00000001") == {"numero_poliza": "POL-00000001"}
    client.collection.assert_called_with("polizas_test")
    client.collection.return_value.document.assert_called_with("POL-00000001")


def test_firestore_documento_inexistente():
    repo = FirestorePolizaRepository(client=_cliente_firestore(False))
    assert repo.obtener_siniestro("SIN-00000001") is None
    assert repo.obtener_coberturas("AUTO-PLUS") is None
