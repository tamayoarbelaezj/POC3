# Asistente de Consulta de Pólizas

Agente en Google ADK que responde consultas sobre estado de pólizas, coberturas de productos y estado de siniestros.

## Requisitos

- Python 3.11+
- Credenciales de GCP (`gcloud auth application-default login`) si se usa Vertex AI / Firestore

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
```

## Ejecución

```bash
adk web                      # UI de desarrollo
uvicorn main:app --port 8080 # API
```

## Tests

```bash
pytest
ruff check .
```

## Variables de entorno

`GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, `GOOGLE_GENAI_USE_VERTEXAI`, `MODEL`, `FIRESTORE_COLLECTION`, `REPOSITORY_BACKEND` (`memory` | `firestore`), `LOG_LEVEL`
