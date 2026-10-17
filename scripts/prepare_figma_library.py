#!/usr/bin/env python3
"""Prepare deterministic, self-contained Figma library builders from local sources.

This command does not connect to Figma. The generated JavaScript is an async
Figma Plugin API body for use_figma. It imports the real SVGs, retains editable
nodes and uses the variable/style IDs recorded in docs/figma-library.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PAGE_COMPONENTS = "03 — Componentes"
PAGE_SIGNATURES = "02 — Assinaturas"
ICON_NAMES = ("arrow-right", "build", "check", "close", "direction", "focus", "learn", "observe")
LAYOUT_DEFAULTS = {
    "components": {"reviewX": 120, "reviewY": 120, "masterX": 2920, "masterY": 120},
    "signatures": {"reviewX": 120, "reviewY": 120, "masterX": 2400, "masterY": 120},
}
SIGNATURE_CATALOG = [
    ("assets/logo/ab-primary.svg", "AB/Logo/Primary", "Principal", "Monograma e órbita em duas cores. Largura mínima de 96 px.", "paper", None),
    ("assets/logo/ab-reverse.svg", "AB/Logo/Reverse", "Principal reversa", "Monograma branco e órbita azul sobre fundo escuro. Largura mínima de 96 px.", "ink", None),
    ("assets/logo/ab-black.svg", "AB/Logo/Mono Ink", "Uma cor / tinta", "Assinatura integral em uma cor para reprodução monocromática. Largura mínima de 96 px.", "paper", None),
    ("assets/logo/ab-white.svg", "AB/Logo/Mono White", "Uma cor / branca", "Assinatura integral branca para fundos escuros e impressão em negativo. Largura mínima de 96 px.", "blue", None),
    ("assets/logo/ab-compact.svg", "AB/Logo/Compact", "Compacta", "Compensações ópticas para larguras entre 64 e 95 px. Fundo claro.", "paper", None),
    ("assets/logo/ab-compact-reverse.svg", "AB/Logo/Compact Reverse", "Compacta reversa", "Compensações ópticas para larguras entre 64 e 95 px. Fundo escuro.", "ink", None),
    ("assets/logo/ab-alexandre-belo.svg", "AB/Logo/Alexandre Belo", "Assinatura nominal", "Monograma e nome em contornos Sora. Usar na identificação inicial da marca.", "paper", None),
    ("assets/logo/ab-alexandre-belo-reverse.svg", "AB/Logo/Alexandre Belo Reverse", "Nominal reversa", "Monograma e nome em contornos Sora para fundos escuros.", "ink", None),
    ("assets/logo/ab-edia.svg", "AB/Logo/ED&IA", "Extensão ED&IA", "Assinatura nominal com identificador literal ED&IA. Aplicar quando esse contexto for necessário.", "paper", None),
    ("assets/logo/ab-edia-reverse.svg", "AB/Logo/ED&IA Reverse", "ED&IA reversa", "Assinatura nominal com identificador ED&IA para fundos escuros.", "ink", None),
    ("assets/icons/ab-micro.svg", "AB/Micro/Blue Field", "A· / campo azul", "Assinatura abreviada contextual de 16 a 63 px; não substitui AB na primeira apresentação.", "paper", 96),
    ("assets/icons/ab-micro-transparent.svg", "AB/Micro/Transparent", "A· / transparente", "A em tinta e foco azul sobre fundo claro. Uso contextual mínimo de 16 × 16 px.", "paper", 96),
    ("assets/icons/ab-micro-reverse.svg", "AB/Micro/Reverse", "A· / reversa", "A branco e foco azul sobre fundo escuro. Uso contextual mínimo de 16 × 16 px.", "ink", 96),
    ("assets/icons/ab-micro-mono.svg", "AB/Micro/Mono Ink", "A· / uma cor", "A e foco em uma cor, com fundo transparente. Uso contextual mínimo de 16 × 16 px.", "paper", 96),
    ("assets/graphics/trajectory.svg", "AB/Graphic/Trajectory", "Trajetória", "Elemento de apoio extraído da órbita do símbolo. Não substitui a assinatura.", "paper", None),
    ("assets/graphics/focus-point.svg", "AB/Graphic/Focus Point", "Ponto de foco", "Elemento circular de apoio. Manter circularidade e hierarquia; não substitui a assinatura.", "paper", 160),
]


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name}: a raiz JSON precisa ser um objeto.")
    return value


def absolute_from(root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False) as handle:
            temp_path = Path(handle.name)
            handle.write(text)
        os.replace(temp_path, path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


def text_id(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"ID ausente ou inválido: {field}.")
    return value


def validate_foundations(library: dict, brand: dict) -> dict:
    text_id(library.get("fileKey"), "fileKey")
    foundation = library.get("foundations")
    if not isinstance(foundation, dict):
        raise ValueError("O mapa foundations não existe.")
    expected_modes = {"AB / Primitives": {"Value"}, "AB / Color": {"Light", "Dark"}, "AB / Geometry": {"Value"}}
    collections = foundation.get("collections", {})
    if set(collections) != set(expected_modes):
        raise ValueError("São necessárias as coleções AB / Primitives, AB / Color e AB / Geometry.")
    for name, modes in expected_modes.items():
        item = collections[name]
        text_id(item.get("id"), name)
        if set(item.get("modes", {})) != modes:
            raise ValueError(f"Modos divergentes em {name}.")
        for mode, identifier in item["modes"].items():
            text_id(identifier, name + "/" + mode)
    expected_variables = {"AB / Primitives/" + name for name in brand["palette"]}
    expected_variables |= {"AB / Color/" + name for name in brand["semantic"]}
    expected_variables |= {f"AB / Geometry/{category}/{name}" for category, values in brand["dimensions"].items() for name in values}
    variables = foundation.get("variables", {})
    if set(variables) != expected_variables:
        missing = sorted(expected_variables - set(variables))
        extra = sorted(set(variables) - expected_variables)
        raise ValueError(f"Variáveis incompatíveis com tokens/brand.json. Ausentes={missing}; extras={extra}.")
    styles = foundation.get("styles", {})
    expected_styles = {item["name"] for item in brand["typography"]["styles"]}
    if set(styles) != expected_styles:
        raise ValueError("Os estilos de texto não correspondem aos tokens da marca.")
    for mapping_name, mapping in (("variables", variables), ("styles", styles)):
        for name, identifier in mapping.items():
            text_id(identifier, mapping_name + "/" + name)
        if len(set(mapping.values())) != len(mapping):
            raise ValueError(f"IDs duplicados em foundations.{mapping_name}.")
    for name in (PAGE_COMPONENTS, PAGE_SIGNATURES):
        text_id(foundation.get("pages", {}).get(name), name)
    return {key: foundation[key] for key in ("collections", "variables", "styles", "pages")}


def parse_figma_result(path: Path) -> dict:
    result = read_json(path)
    if result.get("isError") or result.get("error"):
        raise ValueError(f"{path.name} contém um erro, não um resultado de importação.")
    if "content" in result:
        candidates = []
        for block in result["content"]:
            if block.get("type") == "text":
                try:
                    parsed = json.loads(block.get("text", ""))
                except json.JSONDecodeError:
                    continue
                if isinstance(parsed, dict):
                    candidates.append(parsed)
        if len(candidates) != 1:
            raise ValueError(f"{path.name}: esperado um único objeto JSON retornado por use_figma.")
        result = candidates[0]
    return result


def concise_signatures(result: dict) -> dict:
    expected = {item[0] for item in SIGNATURE_CATALOG}
    signatures = result.get("signatures", {})
    if set(signatures) != expected:
        raise ValueError("O resultado de assinaturas precisa conter os 16 caminhos canônicos.")
    keep = {"componentId", "width", "height", "viewBox", "name", "sourceSha256", "background", "usage"}
    concise = {}
    for path, entry in signatures.items():
        text_id(entry.get("componentId"), path)
        for dimension in ("width", "height"):
            number = entry.get(dimension)
            if not isinstance(number, (int, float)) or not math.isfinite(number) or number <= 0:
                raise ValueError(f"Dimensão inválida: {path}/{dimension}.")
        concise[path] = {key: value for key, value in entry.items() if key in keep}
        concise[path]["assetHasIntrinsicBackground"] = path == "assets/icons/ab-micro.svg"
    return concise


def update_counts(library: dict) -> None:
    families = library.get("components", {}).get("components", {})
    variant_count = sum(len(families.get(name, {}).get("variants", [])) for name in ("Button", "Input", "Badge"))
    card_count = int(bool(families.get("Card")))
    icon_count = len(families.get("Icons", {}))
    foundation = library["foundations"]
    library["counts"] = {
        "collections": len(foundation["collections"]),
        "variables": len(foundation["variables"]),
        "textStyles": len(foundation["styles"]),
        "componentSets": sum(bool(families.get(name)) for name in ("Button", "Input", "Badge")),
        "componentMasters": variant_count + card_count + icon_count,
        "signatureMasters": len(library.get("signatures", {})),
    }


def apply_records(library: dict, args: argparse.Namespace, root: Path) -> bool:
    changed = any((args.record_foundations, args.record_components, args.record_signatures))
    if args.file_key and not args.record_foundations:
        raise ValueError("--file-key deve acompanhar --record-foundations para não reutilizar IDs de outro arquivo.")
    if args.record_foundations:
        if not args.file_key:
            raise ValueError("--record-foundations exige --file-key com a chave do arquivo que gerou os IDs.")
        result = parse_figma_result(absolute_from(root, args.record_foundations))
        library.clear()
        library["fileKey"] = args.file_key
        library["foundations"] = {key: result[key] for key in ("collections", "variables", "styles", "pages")}
        library["components"] = {"components": {}, "propertyKeys": {}}
        library["signatures"] = {}
        library["reviews"] = {}
    for kind, filename in (("components", args.record_components), ("signatures", args.record_signatures)):
        if not filename:
            continue
        result = parse_figma_result(absolute_from(root, filename))
        if result.get("validationPassed") is False:
            raise ValueError(f"O resultado {kind} informa que a validação falhou.")
        if result.get("fileKey", library["fileKey"]) != library["fileKey"]:
            raise ValueError(f"O resultado {kind} pertence a outro arquivo Figma.")
        page_id = text_id(result.get("pageId"), kind + "/pageId")
        if kind == "components":
            families = result.get("components", {})
            if set(families) != {"Button", "Input", "Badge", "Card", "Icons"}:
                raise ValueError("Resultado incompleto de componentes.")
            for name, count in (("Button", 12), ("Input", 4), ("Badge", 4)):
                if len(families[name].get("variants", [])) != count:
                    raise ValueError(f"Quantidade divergente de variantes em {name}.")
            if set(families["Icons"]) != set(ICON_NAMES):
                raise ValueError("Os oito ícones esperados não estão no resultado.")
            library[kind] = {"components": families, "propertyKeys": result["propertyKeys"]}
            library["foundations"]["pages"][PAGE_COMPONENTS] = page_id
            review = result["review"]
            library.setdefault("reviews", {})[kind] = {"pageId": page_id, "nodeId": review["id"], "width": review["width"], "height": review["height"]}
        else:
            library[kind] = concise_signatures(result)
            library["foundations"]["pages"][PAGE_SIGNATURES] = page_id
            library.setdefault("reviews", {})[kind] = {"pageId": page_id, "nodeId": result["reviewFrameId"], "width": result["reviewWidth"], "height": result["reviewHeight"]}
    if changed:
        library["schemaVersion"] = 1
        update_counts(library)
    return changed


def read_svg(path: Path) -> tuple[str, list[float]]:
    raw = path.read_bytes()
    source = raw.decode("utf-8")
    if re.search(r"<!\s*(DOCTYPE|ENTITY)\b", source, re.IGNORECASE):
        raise ValueError(f"Declaração XML externa proibida: {path.name}.")
    xml = ET.fromstring(source)
    if xml.tag != "{http://www.w3.org/2000/svg}svg":
        raise ValueError(f"Raiz SVG inválida: {path.name}.")
    if xml.get("width") is not None or xml.get("height") is not None:
        raise ValueError(f"O SVG canônico deve usar viewBox sem width/height fixos: {path.name}.")
    view = [float(value) for value in xml.get("viewBox", "").replace(",", " ").split()]
    if len(view) != 4 or not all(math.isfinite(value) for value in view) or view[:2] != [0, 0] or min(view[2:]) <= 0:
        raise ValueError(f"viewBox inválido ou com origem diferente de 0 0: {path.name}.")
    allowed = {"svg", "g", "path", "rect", "circle", "ellipse", "line", "polygon", "polyline", "title", "desc"}
    for node in xml.iter():
        if node.tag.rsplit("}", 1)[-1] not in allowed:
            raise ValueError(f"Elemento não estático ou não suportado em {path.name}: {node.tag}.")
        for key, value in node.attrib.items():
            name = key.rsplit("}", 1)[-1].lower()
            if name.startswith("on") or name in {"href", "style"} or "url(" in value.lower():
                raise ValueError(f"Atributo ou referência não suportada em {path.name}: {key}.")
    return source, view


def load_assets(root: Path) -> tuple[dict, list, list]:
    icons = {}
    for name in ICON_NAMES:
        source, view = read_svg(root / "assets/icons/ui" / (name + ".svg"))
        if view != [0, 0, 24, 24]:
            raise ValueError(f"O ícone {name} precisa de viewBox 0 0 24 24.")
        icons[name] = source
    path_dictionary: list[str] = []
    lookup: dict[str, int] = {}

    def intern(match: re.Match) -> str:
        path = match.group(1)
        if path not in lookup:
            lookup[path] = len(path_dictionary)
            path_dictionary.append(path)
        return ' d="@' + str(lookup[path]) + '@"'

    signatures = []
    for path, name, title, usage, background, display_width in SIGNATURE_CATALOG:
        source, view = read_svg(root / path)
        template = re.sub(r' d="([^"]+)"', intern, source)
        restored = re.sub(r' d="@(\d+)@"', lambda match: ' d="' + path_dictionary[int(match.group(1))] + '"', template)
        if restored.encode("utf-8") != source.encode("utf-8"):
            raise ValueError(f"A deduplicação de paths não preservou os bytes de {path}.")
        signatures.append({"path": path, "name": name, "title": title, "usage": usage, "background": background, "displayWidth": display_width, "width": view[2], "height": view[3], "viewBox": " ".join(f"{value:g}" for value in view), "sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(), "svg": template})
    return icons, signatures, path_dictionary


def read_layout(root: Path, filename: str | None) -> dict:
    layout = {name: dict(values) for name, values in LAYOUT_DEFAULTS.items()}
    if filename:
        overrides = read_json(absolute_from(root, filename))
        if set(overrides) - set(layout):
            raise ValueError("Layout aceita somente components e signatures.")
        for name, values in overrides.items():
            if not isinstance(values, dict) or set(values) - set(layout[name]):
                raise ValueError(f"Campos de layout desconhecidos em {name}.")
            for key, value in values.items():
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                    raise ValueError(f"Coordenada inválida: {name}.{key}.")
                layout[name][key] = value
    return layout


def js_constant(name: str, value: object) -> str:
    return "const " + name + "=" + json.dumps(value, ensure_ascii=False, separators=(",", ":")) + ";\n"


def compact_template(source: str) -> str:
    """Remove only insignificant line indentation and whole-line comments.

    Templates with potentially multiline literals or block comments are left
    intact. This is intentionally not a general JavaScript minifier.
    """
    if "`" in source or "\\\n" in source or "/*" in source:
        return source
    lines = [line.lstrip() for line in source.splitlines()]
    return "\n".join(line for line in lines if line and not line.startswith("//")) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--library", default="docs/figma-library.json")
    parser.add_argument("--output-dir", default="build")
    parser.add_argument("--components-page-id")
    parser.add_argument("--signatures-page-id")
    parser.add_argument("--layout-config")
    parser.add_argument("--record-foundations")
    parser.add_argument("--file-key")
    parser.add_argument("--record-components")
    parser.add_argument("--record-signatures")
    parser.add_argument("--check", action="store_true", help="Compare generated bytes with existing build files without writing.")
    parser.add_argument("--max-script-chars", type=int, default=50000, help="Fail before writing scripts above the use_figma code-length limit.")
    args = parser.parse_args()
    root = args.root.resolve()
    library_path = absolute_from(root, args.library)
    library = read_json(library_path)
    brand = read_json(root / "tokens/brand.json")
    if args.check and any((args.record_foundations, args.record_components, args.record_signatures)):
        raise ValueError("--check não pode ser combinado com gravação de resultados.")
    changed = apply_records(library, args, root)
    foundation = validate_foundations(library, brand)
    icons, signatures, dictionary = load_assets(root)
    layout = read_layout(root, args.layout_config)
    output = absolute_from(root, args.output_dir)
    brand_runtime = {"typography": {"family": brand["typography"]["family"]}}
    common = js_constant("FOUNDATION", foundation) + js_constant("BRAND", brand_runtime)
    builders = {}
    for kind, page_name, override in (("components", PAGE_COMPONENTS, args.components_page_id), ("signatures", PAGE_SIGNATURES, args.signatures_page_id)):
        page_id = override or foundation["pages"][page_name]
        text_id(page_id, kind + "/pageId")
        config = {"fileKey": library["fileKey"], "pageId": page_id, "layout": layout[kind]}
        source = "// Generated by scripts/prepare_figma_library.py; edit the source templates.\n" + js_constant("CONFIG", config) + common
        if kind == "components":
            source += js_constant("ICON_SOURCE", icons)
        else:
            source += js_constant("SOURCE_PATHS", dictionary) + js_constant("SOURCES", signatures)
        template = (root / "scripts" / ("figma_" + kind + ".js")).read_text(encoding="utf-8")
        source += compact_template(template)
        size = len(source)
        if size > args.max_script_chars:
            raise ValueError(f"figma-{kind}.js: {size} caracteres excedem o limite de {args.max_script_chars}; divida a importação antes de enviar ao conector.")
        builders[output / ("figma-" + kind + ".js")] = source
    if args.check:
        divergent = [path.name for path, source in builders.items() if not path.exists() or path.read_bytes() != source.encode("utf-8")]
        if divergent:
            raise ValueError("Builders ausentes ou desatualizados: " + ", ".join(divergent))
    else:
        for path, source in builders.items():
            atomic_text(path, source)
        if changed:
            atomic_text(library_path, json.dumps(library, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"mode": "check" if args.check else "generate", "fileKey": library["fileKey"], "libraryUpdated": changed, "builders": [{"path": os.path.relpath(path, root), "characters": len(source), "bytes": len(source.encode("utf-8")), "sha256": hashlib.sha256(source.encode("utf-8")).hexdigest()} for path, source in builders.items()], "assets": {"icons": len(icons), "signatures": len(signatures), "uniquePaths": len(dictionary)}}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        print("Erro: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
