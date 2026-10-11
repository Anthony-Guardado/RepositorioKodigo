"""
Generador automático del README a partir de las skills del proyecto.

Skill asociada: documentar-refactor
Lee los SKILL.md de .opencode/skills/ y compone un README técnico
que documenta la refactorización, las skills y las decisiones humanas vs IA.

Mejoras aplicadas:
- Las skills se ordenan por flujo lógico de uso (no alfabético).
- Cada bloque "Cuándo se usa" respeta el salto de línea correcto.
- Incluye sección de casos borde y nota de generación automática.
"""

import re
from datetime import datetime
from pathlib import Path

from src.config import REFACTOR_README_PATH, SKILLS_DIR


# Orden lógico de las skills según el flujo del pipeline.
SKILL_ORDER = (
    "detectar-fuente-transaccion",
    "normalizar-transaccion",
    "validar-reglas-negocio",
    "generar-metricas",
    "documentar-refactor",
)


# ---------------------------------------------------------------------------
# Parser minimalista de frontmatter YAML
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_frontmatter(text: str) -> dict:
    """Extrae name y description del frontmatter de un SKILL.md."""
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}
    meta = {}
    for linea in match.group(1).splitlines():
        if ":" in linea:
            k, _, v = linea.partition(":")
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def _extract_section(text: str, header: str) -> str:
    """Extrae el contenido de una sección '## HEADER' hasta el siguiente '##'."""
    pattern = rf"##\s+{re.escape(header)}\s*\n(.*?)(?=\n##\s|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


# ---------------------------------------------------------------------------
# Lectura de skills
# ---------------------------------------------------------------------------

def load_skills(skills_dir: str = SKILLS_DIR) -> list[dict]:
    """
    Devuelve la lista de skills con su metadata y secciones.
    El orden sigue SKILL_ORDER (flujo del pipeline), no alfabético.
    """
    base = Path(skills_dir)
    if not base.is_dir():
        return []

    encontradas = {}
    for skill_md in base.glob("*/SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        meta = _parse_frontmatter(text)
        name = meta.get("name", skill_md.parent.name)
        encontradas[name] = {
            "name": name,
            "description": meta.get("description", ""),
            "que_hace": _extract_section(text, "QUÉ HACE"),
            "cuando_usarla": _extract_section(text, "CUÁNDO USARLA"),
        }

    # Ordenar según SKILL_ORDER, dejando al final las que no estén en la lista
    ordenadas = [encontradas[n] for n in SKILL_ORDER if n in encontradas]
    extras = [v for k, v in encontradas.items() if k not in SKILL_ORDER]
    return ordenadas + extras


# ---------------------------------------------------------------------------
# Render de secciones
# ---------------------------------------------------------------------------

_ARCH_TABLE = (
    "| Antes | Después |\n"
    "|---|---|\n"
    "| Lógica de normalización en `normalizer.py` | Skill `normalizar-transaccion` + orquestador delgado |\n"
    "| Validación hardcodeada dentro del normalizador | Skill `validar-reglas-negocio` en `validators.py` |\n"
    "| Fuente asumida explícita en el JSON | Skill `detectar-fuente-transaccion` en `source_detector.py` |\n"
    "| Métricas acopladas a la CLI | Skill `generar-metricas` con contrato fijo |\n"
    "| README escrito a mano | Skill `documentar-refactor` + `refactor_docs.py` |\n"
)

_CASOS_BORDE_TABLE = (
    "| Caso | Comportamiento |\n"
    "|------|---------------|\n"
    "| Monto con separador de miles (`\"1,250.50 USD\"`) | Se limpia y convierte a `1250.50` |\n"
    "| Moneda en español (`\"pesos\"`, `\"dólares\"`) | Alias → ISO (`MXN`, `USD`) |\n"
    "| Estado en español (`\"completado\"`, `\"fallido\"`) | Mapeo a valor canónico |\n"
    "| Fecha Unix timestamp (int) | Se convierte a `datetime` UTC |\n"
    "| Fecha inválida (`32/13/2025`) | Se marca como error, no rompe |\n"
    "| Monto cero o negativo | Se rechaza |\n"
    "| Fuente desconocida | Se marca inválida con error explícito |\n"
    "| JSON malformado | Error controlado, no rompe el programa |\n"
)


def _render_skills_section(skills: list[dict]) -> str:
    if not skills:
        return "_No se encontraron skills en `.opencode/skills/`._\n"

    bloques = []
    for i, s in enumerate(skills, 1):
        bloques.append(
            "### {n}. `{name}`\n\n"
            "**Qué hace:** {que_hace}\n\n"
            "**Cuándo se usa:**\n\n{cuando}\n".format(
                n=i,
                name=s["name"],
                que_hace=s["que_hace"] or s["description"] or "—",
                cuando=s["cuando_usarla"] or "—",
            )
        )
    return "\n".join(bloques)


def _render_metrics_block(metrics_summary: dict | None) -> str:
    if not metrics_summary:
        return ""
    return (
        "## 📊 Última ejecución\n\n"
        "- Total procesadas: **{total}**\n"
        "- Válidas: **{validas}**\n"
        "- Inválidas: **{invalidas}**\n\n"
        "---\n\n".format(
            total=metrics_summary["total"],
            validas=metrics_summary["validas"],
            invalidas=metrics_summary["invalidas"],
        )
    )


# ---------------------------------------------------------------------------
# Composición del README
# ---------------------------------------------------------------------------

def build_readme(metrics_summary: dict | None = None) -> str:
    """Compone el README completo como string."""
    skills = load_skills()
    fecha = datetime.now().strftime("%Y-%m-%d")

    plantilla = (
        "# Normalizador de Transacciones — Refactorizado con Skills\n\n"
        "> Este README fue generado automáticamente por la skill "
        "`documentar-refactor` y revisado manualmente por el autor.\n\n"
        "**Autor:** Anthony Guardado\n"
        "**Fecha de refactor:** {fecha}\n"
        "**Python:** 3.12.10\n"
        "**Dependencias:** ninguna (solo librería estándar)\n\n"
        "---\n\n"
        "## 🎯 Objetivo de la refactorización\n\n"
        "Convertir un proyecto monolítico de normalización de transacciones en un\n"
        "sistema modular donde cada responsabilidad está encapsulada en una **skill\n"
        "propia** ejecutable por un agente de OpenCode.\n\n"
        "---\n\n"
        "## 🏗️ Arquitectura modular\n\n"
        "{arch_table}\n"
        "---\n\n"
        "## 🧩 Skills disponibles\n\n"
        "Las skills se listan en el orden del flujo lógico del pipeline:\n"
        "detectar → normalizar → validar → agregar → documentar.\n\n"
        "{skills_section}\n"
        "---\n\n"
        "## 🚀 Cómo ejecutar\n\n"
        "```bash\n"
        "python main.py                                   # dataset por defecto\n"
        "python main.py pruebas/transacciones_ok.json     # dataset limpio\n"
        "python main.py pruebas/transacciones_mixtas.json # dataset con errores\n"
        "```\n\n"
        "Desde el menú de la CLI:\n\n"
        "- Opción 7 → exportar dataset normalizado a JSON.\n"
        "- Opción 8 → **regenerar este README** desde las skills.\n\n"
        "---\n\n"
        "{metrics_block}"
        "## 🤖 Integración con OpenCode\n\n"
        "Este proyecto está diseñado para ser operado por un agente de OpenCode que\n"
        "carga las skills automáticamente desde `.opencode/skills/`.\n\n"
        "### Configuración de permisos (`.opencode/opencode.json`)\n\n"
        "```json\n"
        "{{\n"
        "  \"$schema\": \"https://opencode.ai/config.json\",\n"
        "  \"permission\": {{\n"
        "    \"skill\": {{\n"
        "      \"normalizar-transaccion\": \"allow\",\n"
        "      \"validar-reglas-negocio\": \"allow\",\n"
        "      \"detectar-fuente-transaccion\": \"allow\",\n"
        "      \"generar-metricas\": \"allow\",\n"
        "      \"documentar-refactor\": \"allow\",\n"
        "      \"*\": \"ask\"\n"
        "    }},\n"
        "    \"bash\": {{\n"
        "      \"python main.py*\": \"allow\",\n"
        "      \"python -m pytest*\": \"allow\",\n"
        "      \"*\": \"ask\"\n"
        "    }}\n"
        "  }}\n"
        "}}\n"
        "```\n\n"
        "### Cómo OpenCode descubre las skills\n\n"
        "OpenCode lee el frontmatter YAML de cada `SKILL.md` (campos `name` y\n"
        "`description`) y construye un catálogo. Cuando el prompt del usuario coincide\n"
        "semánticamente con la descripción de una skill, el agente la carga y ejecuta\n"
        "los pasos definidos en el `SKILL.md`.\n\n"
        "### Evidencia de invocación automática\n\n"
        "Se ejecutaron 5 pruebas, una por skill, desde el chat de OpenCode en la raíz\n"
        "del proyecto. En cada caso, el agente reconoció la skill correspondiente sin\n"
        "que el usuario la nombrara explícitamente:\n\n"
        "| Prompt del usuario | Skill activada | Resultado |\n"
        "|---|---|---|\n"
        "| *\"Normaliza esta transacción: {...}\"* | `normalizar-transaccion` | `amount=250.5`, `currency=MXN`, `status=completed` |\n"
        "| *\"Valida esta transacción y dime si es válida\"* | `validar-reglas-negocio` | `is_valid=False`, 5 errores detectados |\n"
        "| *\"¿De qué fuente viene esta transacción?\"* | `detectar-fuente-transaccion` | `exchange_crypto` (score 5/5) |\n"
        "| *\"Ejecuta el proyecto y dame el resumen\"* | `generar-metricas` | JSON con totales, conteos y sumas por moneda |\n"
        "| *\"Genera el README del proyecto\"* | `documentar-refactor` | `README.md` de 5.5 KB generado |\n\n"
        "### Ejemplo de autocorrección del agente\n\n"
        "Durante la prueba de `generar-metricas`, el agente ejecutó inicialmente\n"
        "`load_transactions('data/transacciones.json')` pasando un `str`. El código\n"
        "esperaba un `Path` y lanzó `AttributeError`. El agente leyó `loaders.py`,\n"
        "detectó el tipo esperado y reintentó con `Path(...)` exitosamente. Este\n"
        "comportamiento demuestra que el agente no ejecuta a ciegas: lee el código,\n"
        "entiende el contrato y se corrige.\n\n"
        "---\n\n"
        "## 🔍 Casos borde manejados\n\n"
        "{casos_borde_table}\n"
        "---\n\n"
        "## 🧠 Decisiones humanas vs IA\n\n"
        "| Cambio | Sugerido por IA | Decisión humana |\n"
        "|---|---|---|\n"
        "| Separar validación en `validators.py` | Sí | Sí — el estudiante fijó las 5 reglas |\n"
        "| Extraer detección de fuente a módulo propio | Sí | Sí — se agregó umbral mínimo de confianza |\n"
        "| `normalizer.py` como orquestador delgado | Sí | Sí — se definió el orden de delegación |\n"
        "| Generar README desde las skills | Sí | Sí — se revisó y ajustó la estructura |\n"
        "| Orden de validaciones en `validate()` | No | Decisión del estudiante |\n\n"
        "---\n\n"
        "## 👤 Créditos\n\n"
        "Desarrollado por **ANTHONY GUARDADO** como parte de la actividad\n"
        "\"Refactorización y Personalización de un Sistema Agéntico mediante Skills Propias\".\n"
    )

    return plantilla.format(
        fecha=fecha,
        arch_table=_ARCH_TABLE,
        skills_section=_render_skills_section(skills),
        metrics_block=_render_metrics_block(metrics_summary),
        casos_borde_table=_CASOS_BORDE_TABLE,
    )


def write_readme(output_path: str = REFACTOR_README_PATH,
                 metrics_summary: dict | None = None) -> Path:
    """Genera el README y lo escribe en disco. Devuelve la ruta final."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_readme(metrics_summary), encoding="utf-8")
    return path