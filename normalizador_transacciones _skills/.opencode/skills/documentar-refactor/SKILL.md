---
name: documentar-refactor
description: "Genera la documentación técnica del proyecto refactorizado: README principal, sección de descripción de cada skill, changelog de decisiones humanas vs IA, y arquitectura modular. Usar cuando se termine una refactorización o cuando el usuario pida 'genera el README', 'documenta el proyecto' o 'explica las skills'."
---

# Documentar Refactor

## QUÉ HACE

Produce la documentación técnica completa del proyecto refactorizado: README con arquitectura, listado y descripción de skills, ejemplos de uso, changelog de decisiones humanas vs IA, y guía de ejecución. Su salida es el entregable de documentación de la actividad.

## CUÁNDO USARLA

- Al terminar una refactorización significativa del proyecto.
- Cuando el usuario pida "genera el README", "documenta las skills" o "escribe el changelog".
- Antes de hacer commit final de una entrega.
- Frases típicas: *"documenta esto"*, *"arma el README"*, *"explica qué cambió"*.

## PASOS QUE DEBE SEGUIR

1. **Leer** la estructura actual del proyecto y los módulos refactorizados.
2. **Listar todas las skills** disponibles en `.opencode/skills/` leyendo cada `SKILL.md`.
3. **Redactar el README** con estas secciones obligatorias:
   - Título y descripción del proyecto.
   - Objetivo de la refactorización.
   - Arquitectura modular (antes vs después).
   - Listado de skills: nombre, qué hace, cuándo se usa.
   - Cómo ejecutar el proyecto.
   - Cómo se integran las skills con OpenCode.
   - Changelog de decisiones humanas vs IA.
   - Créditos.
4. **Generar la tabla de decisiones** con dos columnas: *"Sugerido por IA"* y *"Decisión humana"*.
5. **Incluir ejemplos reales** de invocación de cada skill.
6. **Escribir en español**, tono técnico pero claro, sin relleno.

## FORMATO DE SALIDA ESPERADO

Documento Markdown con:

- **Secciones obligatorias** (todas las del paso 3).
- **Tablas** para arquitectura, skills y decisiones.
- **Bloques de código** para ejemplos de uso.
- **Longitud**: entre 1 y 3 páginas equivalentes.
- **Tono**: técnico, directo, sin adjetivos vacíos.

## EJEMPLO DE ENTRADA Y SALIDA

**Entrada:** proyecto `normalizador_transacciones` con 5 skills en `.opencode/skills/`.

**Salida (extracto del README generado):**

```markdown
# Normalizador de Transacciones — Refactorizado con Skills

## Arquitectura modular

| Antes | Después |
|---|---|
| Lógica de normalización en 1 archivo | Skill `normalizar-transaccion` |
| Validaciones hardcodeadas | Skill `validar-reglas-negocio` |
| Detección de fuente manual | Skill `detectar-fuente-transaccion` |
| Métricas acopladas a CLI | Skill `generar-metricas` |
| README manual | Skill `documentar-refactor` |

## Skills disponibles

### 1. `normalizar-transaccion`
Normaliza una transacción cruda a formato canónico...