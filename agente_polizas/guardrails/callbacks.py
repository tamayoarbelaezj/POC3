import logging
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from google.adk.agents.callback_context import CallbackContext
    from google.adk.models import LlmRequest, LlmResponse

logger = logging.getLogger(__name__)

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Celulares (3XX) y fijos (60X) con indicativo +57 opcional.
_TELEFONO_RE = re.compile(
    r"(?<![\w-])(?:\+?57[\s-]?)?(?:3\d{2}|60\d)[\s-]?\d{3}[\s-]?\d{4}(?!\d)"
)
# Cédulas: 6 a 10 dígitos, con o sin puntos. No toca POL-/SIN-.
_CEDULA_RE = re.compile(
    r"(?<![\w-])(?:\d{1,3}(?:\.\d{3}){1,3}|\d{6,10})(?![\d.]?\d)"
)

_INJECTION_PATTERNS = [
    r"ignor\w*\s+(?:\w+\s+){0,3}(?:instrucciones|reglas|indicaciones)",
    r"olvid\w*\s+(?:\w+\s+){0,3}(?:instrucciones|reglas|indicaciones)",
    r"ignore\s+(?:all\s+|the\s+)?(?:previous|prior|above)\s+instructions",
    r"(?:prompt|mensaje|instrucciones?)\s+(?:del\s+)?sistema",
    r"system\s+prompt",
    r"modo\s+(?:desarrollador|developer|dios)",
    r"developer\s+mode",
    r"jailbreak",
    r"act[uú]a\s+como\s+(?:si\s+fueras\s+)?(?:un|una)?\s*(?:hacker|administrador|desarrollador)",
    r"revela\w*\s+(?:tus|las)\s+instrucciones",
]
_INJECTION_RE = re.compile("|".join(_INJECTION_PATTERNS), re.IGNORECASE)

MENSAJE_BLOQUEO = (
    "Lo siento, no puedo procesar esa solicitud. Puedo ayudarte con el estado de tu póliza, "
    "las coberturas de tu producto o el estado de un siniestro."
)

_TERMINOS_PROHIBIDOS_SALIDA = re.compile(
    r"instrucciones\s+del\s+sistema|system\s+prompt", re.IGNORECASE
)


def enmascarar_pii(texto: str) -> str:
    if not texto:
        return texto
    texto = _EMAIL_RE.sub("[CORREO]", texto)
    texto = _TELEFONO_RE.sub("[TELEFONO]", texto)
    texto = _CEDULA_RE.sub("[DOCUMENTO]", texto)
    return texto


def es_prompt_injection(texto: str) -> bool:
    return bool(texto) and bool(_INJECTION_RE.search(texto))


def filtrar_salida(texto: str) -> str:
    if not texto:
        return texto
    if _TERMINOS_PROHIBIDOS_SALIDA.search(texto):
        return MENSAJE_BLOQUEO
    return enmascarar_pii(texto)


def _respuesta_texto(texto: str) -> "LlmResponse":
    from google.adk.models import LlmResponse
    from google.genai import types

    return LlmResponse(
        content=types.Content(role="model", parts=[types.Part(text=texto)])
    )


def before_model_callback(
    callback_context: "CallbackContext", llm_request: "LlmRequest"
) -> "LlmResponse | None":
    contents = llm_request.contents or []
    ultimo_usuario = next(
        (c for c in reversed(contents) if c.role == "user" and any(p.text for p in c.parts or [])),
        None,
    )

    if ultimo_usuario is not None:
        texto = " ".join(p.text for p in ultimo_usuario.parts if p.text)
        if es_prompt_injection(texto):
            logger.warning("Posible prompt injection bloqueado (agente=%s)",
                           callback_context.agent_name)
            return _respuesta_texto(MENSAJE_BLOQUEO)

    for content in contents:
        if content.role != "user":
            continue
        for part in content.parts or []:
            if part.text:
                part.text = enmascarar_pii(part.text)
    return None


def after_model_callback(
    callback_context: "CallbackContext", llm_response: "LlmResponse"
) -> "LlmResponse | None":
    if not llm_response.content or not llm_response.content.parts:
        return None

    modificado = False
    for part in llm_response.content.parts:
        if part.text:
            filtrado = filtrar_salida(part.text)
            if filtrado != part.text:
                part.text = filtrado
                modificado = True

    return llm_response if modificado else None
