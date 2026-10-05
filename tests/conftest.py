import os

import pytest

os.environ.setdefault("REPOSITORY_BACKEND", "memory")


@pytest.fixture(autouse=True)
def _repo_en_memoria(monkeypatch):
    monkeypatch.setenv("REPOSITORY_BACKEND", "memory")
    from agente_polizas.config import get_settings
    from agente_polizas.repositories import factory

    get_settings.cache_clear()
    factory.get_repository.cache_clear()
    yield
    factory.get_repository.cache_clear()
