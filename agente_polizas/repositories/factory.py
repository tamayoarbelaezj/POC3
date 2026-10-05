from functools import lru_cache

from ..config import get_settings
from .base import PolizaRepository


@lru_cache
def get_repository() -> PolizaRepository:
    settings = get_settings()
    if settings.repository_backend == "firestore":
        from .firestore_repo import FirestorePolizaRepository

        return FirestorePolizaRepository(
            project=settings.google_cloud_project,
            collection=settings.firestore_collection,
        )

    from .memory_repo import InMemoryPolizaRepository

    return InMemoryPolizaRepository()
