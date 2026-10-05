import pytest

from agente_polizas.repositories import factory
from agente_polizas.tools import consultar_estado_siniestro, consultar_poliza, listar_coberturas


def test_consultar_poliza_ok():
    resultado = consultar_poliza("POL-00000001")
    assert resultado["status"] == "success"
    assert resultado["poliza"]["estado"] == "VIGENTE"
    assert resultado["poliza"]["codigo_producto"] == "AUTO-PLUS"


def test_consultar_poliza_no_expone_titular():
    resultado = consultar_poliza("POL-00000001")
    assert "titular" not in resultado["poliza"]


def test_consultar_poliza_normaliza_entrada():
    assert consultar_poliza("  pol-00000002 ")["status"] == "success"


@pytest.mark.parametrize(
    "valor", ["", "POL-123", "POL-123456789", "PO-00000001", "00000001", "POL-0000000A", None]
)
def test_consultar_poliza_formato_invalido(valor):
    resultado = consultar_poliza(valor)
    assert resultado["status"] == "error"
    assert "formato" in resultado["error_message"]


def test_consultar_poliza_inexistente():
    resultado = consultar_poliza("POL-99999999")
    assert resultado["status"] == "error"
    assert "No se encontró" in resultado["error_message"]


def test_consultar_poliza_error_repositorio(monkeypatch):
    class RepoRoto:
        def obtener_poliza(self, numero):
            raise RuntimeError("timeout")

    monkeypatch.setattr("agente_polizas.tools.polizas.get_repository", lambda: RepoRoto())
    resultado = consultar_poliza("POL-00000001")
    assert resultado["status"] == "error"
    assert "timeout" not in resultado["error_message"]


def test_listar_coberturas_ok():
    resultado = listar_coberturas("AUTO-PLUS")
    assert resultado["status"] == "success"
    assert len(resultado["coberturas"]) == 4


@pytest.mark.parametrize("valor", ["", "auto plus", "AUTO_PLUS", "X" * 50, "../polizas"])
def test_listar_coberturas_codigo_invalido(valor):
    assert listar_coberturas(valor)["status"] == "error"


def test_listar_coberturas_inexistente():
    assert listar_coberturas("SALUD-TOTAL")["status"] == "error"


def test_consultar_siniestro_ok():
    resultado = consultar_estado_siniestro("SIN-00000001")
    assert resultado["status"] == "success"
    assert resultado["siniestro"]["estado"] == "EN_EVALUACION"
    assert "descripcion" not in resultado["siniestro"]


@pytest.mark.parametrize("valor", ["SIN-1", "POL-00000001", "sin00000001", ""])
def test_consultar_siniestro_formato_invalido(valor):
    assert consultar_estado_siniestro(valor)["status"] == "error"


def test_consultar_siniestro_inexistente():
    assert consultar_estado_siniestro("SIN-99999999")["status"] == "error"


def test_factory_por_defecto_es_memoria():
    from agente_polizas.repositories.memory_repo import InMemoryPolizaRepository

    assert isinstance(factory.get_repository(), InMemoryPolizaRepository)
