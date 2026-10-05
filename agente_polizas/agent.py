import logging

from google.adk.agents import Agent

from .config import settings
from .guardrails import after_model_callback, before_model_callback
from .prompts import INSTRUCCION_SISTEMA
from .tools import consultar_estado_siniestro, consultar_poliza, listar_coberturas

logging.basicConfig(level=settings.log_level)

root_agent = Agent(
    name="agente_polizas",
    model=settings.model,
    description="Asistente de Consulta de Pólizas: estado de pólizas, coberturas y siniestros.",
    instruction=INSTRUCCION_SISTEMA,
    tools=[consultar_poliza, listar_coberturas, consultar_estado_siniestro],
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
