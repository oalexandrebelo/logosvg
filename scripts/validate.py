#!/usr/bin/env python3
"""Validate the AB identity distribution using only the Python standard library.

Run from any working directory. --write-manifest updates the deterministic
manifest only after the content checks pass; ordinary validation never writes.
This checks static asset hygiene and integrity, not optical quality or rendering.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import sys
import xml.etree.ElementTree as ET


SVG_NS = "http://www.w3.org/2000/svg"
MANIFEST = "asset-manifest.json"
SOURCE_COMMIT = "a162752f7c5a8237352b3eac228d52e50484eddf"
SOURCE_TREE = "66146b1560a25a766c4e4703d76c383031bc81ad"
LEGACY = {
    "apple-touch-icon.svg": (2068, "d4fc34d39bf8de884762da16fc9985663c6b1f44"),
    "faviconw.svg": (2048, "5c99d73e1a3e013035b83a23065bc867a067f846"),
    "favivonb.svg": (2048, "70061d942d685e96ee334651e843ec38718ba513"),
    "logo.svg": (17700, "cc27d6df30923f253c052c3fbabbd71e8ac3b3d9"),
    "logo_dark.svg": (17698, "7919984c512bcfc7b438dfb73e44fb62e9eea6ab"),
    "logoazul.svg": (1918, "e536e3e9e5e2bf4e6005ce5624298292f8172d8a"),
    "logob.svg": (1918, "5ca834d8bb82eddc66d944eaed02cbba3b487a58"),
    "logoblack.svg": (1919, "e769f3db159f3619711b4b6b5e3a7047f4191359"),
}
DISTRIBUTION_DIRS = (
    "assets", "tokens", "brandbook", "archive", "docs", "examples", "scripts", ".github",
)
ROOT_DOCUMENTS = (
    "README.md", "CHANGELOG.md", "LICENSE.md", "requirements-build.txt", ".gitignore",
)
IGNORED_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".cache", ".DS_Store"}
REQUIRED_FILES = (
    *ROOT_DOCUMENTS,
    "assets/logo/ab-primary.svg",
    "assets/logo/ab-reverse.svg",
    "assets/logo/ab-black.svg",
    "assets/logo/ab-white.svg",
    "assets/logo/ab-compact.svg",
    "assets/logo/ab-compact-reverse.svg",
    "tokens/brand.json",
    "tokens/brand.css",
    "tokens/brand.tokens.json",
    "brandbook/AB-Brandbook.pdf",
    "brandbook/index.html",
    "brandbook/brandbook.md",
    "docs/migration.md",
    "docs/repository.md",
    "archive/2025/source-manifest.json",
    ".github/workflows/validate.yml",
)
MIME_TYPES = {
    ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif",
    ".ico": "image/vnd.microsoft.icon", ".pdf": "application/pdf",
    ".html": "text/html", ".css": "text/css", ".json": "application/json",
    ".md": "text/markdown", ".txt": "text/plain", ".py": "text/x-python",
    ".js": "text/javascript", ".mjs": "text/javascript", ".ts": "text/typescript",
    ".tsx": "text/tsx", ".yml": "text/yaml", ".yaml": "text/yaml",
    ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf",
    ".otf": "font/otf", ".zip": "application/zip",
}
VECTOR_TAGS = {
    "svg", "g", "defs", "symbol", "path", "circle", "ellipse", "line", "rect",
    "polygon", "polyline", "use", "title", "desc", "style", "linearGradient",
    "radialGradient", "stop", "clipPath", "mask", "pattern",
}
DRAWABLE_TAGS = {"path", "circle", "ellipse", "line", "rect", "polygon", "polyline", "use"}
ID_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.:\-]*\Z")
URL_RE = re.compile(r"url\s*\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)


def local_name(name: str) -> str:
    return name.rsplit("}", 1)[-1]


def media_type(path: str) -> str:
    if PurePosixPath(path).name == ".gitignore":
        return "text/plain"
    return MIME_TYPES.get(PurePosixPath(path).suffix.lower(), "application/octet-stream")


def read_json(path: Path):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)


def distribution_files(root: Path, errors: list[str]) -> list[str]:
    files: set[str] = set()
    for directory in DISTRIBUTION_DIRS:
        start = root / directory
        if not start.exists():
            continue
        if start.is_symlink() or not start.is_dir():
            errors.append(f"{directory}: distribution directory must be a real directory")
            continue
        for current, dirnames, filenames in os.walk(start, followlinks=False):
            kept = []
            for name in sorted(dirnames):
                entry = Path(current) / name
                if name in IGNORED_NAMES:
                    continue
                if entry.is_symlink():
                    errors.append(f"{entry.relative_to(root)}: symlink directory is not allowed")
                else:
                    kept.append(name)
            dirnames[:] = kept
            for name in sorted(filenames):
                if name in IGNORED_NAMES or name.endswith((".pyc", ".pyo")):
                    continue
                entry = Path(current) / name
                relative = entry.relative_to(root).as_posix()
                if entry.is_symlink() or not entry.is_file():
                    errors.append(f"{relative}: distribution entry must be a regular file")
                else:
                    files.add(relative)
    for name in (*ROOT_DOCUMENTS, *LEGACY):
        entry = root / name
        if entry.is_symlink():
            errors.append(f"{name}: symlink file is not allowed")
        elif entry.is_file():
            files.add(name)
    return sorted(files)


def validate_required(root: Path, errors: list[str]) -> None:
    for name in REQUIRED_FILES:
        entry = root / name
        if not entry.is_file() or entry.is_symlink():
            errors.append(f"{name}: required regular file is missing")
        elif entry.stat().st_size == 0:
            errors.append(f"{name}: required file is empty")
    for pattern in ("assets/icons/ab-micro*.svg", "brandbook/pages/*.svg"):
        if not any(p.is_file() and not p.is_symlink() for p in root.glob(pattern)):
            errors.append(f"{pattern}: at least one matching SVG is required")


def validate_svg(path: Path, label: str, errors: list[str]) -> None:
    def fail(message: str) -> None:
        errors.append(f"{label}: {message}")

    try:
        data = path.read_bytes()
        source = data.decode("utf-8")
        if re.search(r"<!\s*(?:DOCTYPE|ENTITY)|<\?xml-stylesheet", source, re.IGNORECASE):
            fail("DOCTYPE, ENTITY and external stylesheet processing instructions are prohibited")
            return
        svg = ET.fromstring(data)
    except (OSError, UnicodeError, ET.ParseError) as exc:
        fail(f"invalid UTF-8 SVG/XML: {exc}")
        return
    if svg.tag != f"{{{SVG_NS}}}svg":
        fail("root element must be svg in the SVG namespace")
        return
    try:
        viewbox = [float(x) for x in re.split(r"[\s,]+", svg.get("viewBox", "").strip())]
        if len(viewbox) != 4 or not all(math.isfinite(x) for x in viewbox):
            raise ValueError
        if viewbox[2] <= 0 or viewbox[3] <= 0:
            raise ValueError
    except ValueError:
        fail("viewBox must contain four finite numbers and positive width/height")

    ids: dict[str, ET.Element] = {}
    references: list[str] = []
    drawable_count = 0
    identified_geometry = False
    for element in svg.iter():
        tag = local_name(element.tag)
        if not element.tag.startswith(f"{{{SVG_NS}}}") or tag not in VECTOR_TAGS:
            fail(f"unsupported element <{tag}>; canonical assets permit static vector geometry only")
        if tag in DRAWABLE_TAGS:
            drawable_count += 1
        node_id = element.get("id")
        if node_id is not None:
            if not ID_RE.fullmatch(node_id):
                fail(f"invalid id: {node_id!r}")
            if node_id in ids:
                fail(f"duplicate id within this SVG: {node_id}")
            ids[node_id] = element
            if tag in DRAWABLE_TAGS or tag == "g":
                identified_geometry = True
        if tag == "path" and not element.get("d", "").strip():
            fail("path has an empty d attribute")
        for attribute, value in element.attrib.items():
            name = local_name(attribute).lower()
            if name.startswith("on"):
                fail(f"event handler attribute is prohibited: {name}")
            if name == "base":
                fail("xml:base or base URL attributes are prohibited")
            if name in {"href", "src"}:
                target = value.strip()
                if not target.startswith("#") or len(target) == 1:
                    fail(f"external or embedded reference is prohibited: {name}")
                else:
                    references.append(target[1:])
            if name in {"aria-labelledby", "aria-describedby"}:
                references.extend(value.split())
            inspect_css(value, references, fail)
        if tag == "style":
            inspect_css("".join(element.itertext()), references, fail)

    titles = [child for child in svg if local_name(child.tag) == "title"]
    if len(titles) != 1 or not "".join(titles[0].itertext()).strip():
        fail("one nonempty direct title element is required")
    elif not titles[0].get("id"):
        fail("title needs an id for its accessible label")
    elif titles[0].get("id") not in svg.get("aria-labelledby", "").split():
        fail("root aria-labelledby must reference the title id")
    if svg.get("role") != "img":
        fail('root role="img" is required')
    if not identified_geometry:
        fail("at least one vector shape or group needs a semantic id")
    if drawable_count == 0:
        fail("no vector geometry found")
    for reference in references:
        if reference not in ids:
            fail(f"unresolved local reference: #{reference}")


def inspect_css(value: str, references: list[str], fail) -> None:
    if re.search(r"@\s*(?:import|font-face)\b|expression\s*\(|javascript\s*:", value, re.IGNORECASE):
        fail("external CSS/font loading or executable CSS is prohibited")
    if "\\" in value:
        fail("escaped CSS is prohibited in canonical assets")
    for match in URL_RE.finditer(value):
        target = match.group(2).strip()
        if not target.startswith("#") or len(target) == 1:
            fail("url() must reference a local SVG id")
        else:
            references.append(target[1:])


def validate_legacy(root: Path, errors: list[str]) -> None:
    for name, (expected_size, expected_blob) in LEGACY.items():
        for relative in (name, f"archive/2025/{name}"):
            entry = root / relative
            if not entry.is_file() or entry.is_symlink():
                errors.append(f"{relative}: original legacy SVG is missing")
                continue
            data = entry.read_bytes()
            blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
            if len(data) != expected_size or blob != expected_blob:
                errors.append(f"{relative}: bytes differ from the verified 2025 GitHub source")
    try:
        source = read_json(root / "archive/2025/source-manifest.json")
        if source.get("repository") != "oalexandrebelo/logosvg":
            errors.append("archive/2025/source-manifest.json: unexpected source repository")
        if source.get("head_sha") != SOURCE_COMMIT or source.get("tree_sha") != SOURCE_TREE:
            errors.append("archive/2025/source-manifest.json: source commit/tree does not match the archive")
        actual = {entry["path"]: (entry["size"], entry["sha"]) for entry in source["files"]}
        if actual != LEGACY or len(source["files"]) != len(LEGACY):
            errors.append("archive/2025/source-manifest.json: source file list is inconsistent")
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append(f"archive/2025/source-manifest.json: invalid provenance: {exc}")


def make_manifest(root: Path, files: list[str]) -> dict:
    entries = []
    for name in files:
        data = (root / name).read_bytes()
        entries.append({"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                        "media_type": media_type(name)})
    return {"schema_version": 1, "hash_algorithm": "sha256", "assets": entries}


def validate_manifest(root: Path, files: list[str], errors: list[str]) -> None:
    try:
        if (root / MANIFEST).is_symlink():
            raise ValueError("manifest may not be a symlink")
        manifest = read_json(root / MANIFEST)
        if not isinstance(manifest, dict) or set(manifest) != {"schema_version", "hash_algorithm", "assets"}:
            raise ValueError("expected schema_version, hash_algorithm and assets")
        if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
            raise ValueError("unsupported schema_version")
        if manifest["hash_algorithm"] != "sha256" or not isinstance(manifest["assets"], list):
            raise ValueError("hash_algorithm must be sha256 and assets must be a list")
        names = []
        expected = {entry["path"]: entry for entry in make_manifest(root, files)["assets"]}
        for entry in manifest["assets"]:
            if not isinstance(entry, dict) or set(entry) != {"path", "bytes", "sha256", "media_type"}:
                raise ValueError("every asset needs path, bytes, sha256 and media_type")
            name = entry["path"]
            if not isinstance(name, str) or name.startswith("/") or "\\" in name:
                raise ValueError("asset path must be a relative POSIX path")
            if name != PurePosixPath(name).as_posix() or any(part in {".", ".."} for part in name.split("/")):
                raise ValueError(f"noncanonical asset path: {name}")
            if type(entry["bytes"]) is not int or entry["bytes"] < 0:
                raise ValueError(f"invalid byte count: {name}")
            if not isinstance(entry["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]):
                raise ValueError(f"invalid SHA256: {name}")
            names.append(name)
            if name not in expected:
                errors.append(f"{MANIFEST}: listed asset does not belong to the distribution: {name}")
            elif entry != expected[name]:
                errors.append(f"{MANIFEST}: content, byte count or media type mismatch: {name}")
        if names != sorted(set(names)):
            errors.append(f"{MANIFEST}: asset paths must be sorted and unique")
        for name in sorted(set(files) - set(names)):
            errors.append(f"{MANIFEST}: missing distribution file: {name}")
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        errors.append(f"{MANIFEST}: invalid or missing manifest: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="repository root; defaults to the parent of scripts/")
    parser.add_argument("--write-manifest", action="store_true",
                        help="regenerate the deterministic manifest after content checks pass")
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    files = distribution_files(root, errors)
    validate_required(root, errors)
    canonical = [name for name in files if name.endswith(".svg") and
                 name.startswith(("assets/logo/", "assets/icons/"))]
    for name in canonical:
        validate_svg(root / name, name, errors)
    validate_legacy(root, errors)
    for name in files:
        if name.startswith("tokens/") and name.endswith(".json"):
            try:
                read_json(root / name)
            except (OSError, UnicodeError, ValueError) as exc:
                errors.append(f"{name}: invalid JSON: {exc}")
    if args.write_manifest and not errors:
        destination = root / MANIFEST
        if destination.is_symlink():
            errors.append(f"{MANIFEST}: refusing to overwrite a symlink")
        else:
            destination.write_text(json.dumps(make_manifest(root, files), ensure_ascii=False, indent=2)
                                   + "\n", encoding="utf-8")
            print(f"WROTE {MANIFEST}: {len(files)} assets")
    validate_manifest(root, files, errors)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    print(f"PASS: {len(files)} distribution files; {len(canonical)} canonical SVGs; "
          f"{len(LEGACY)} original SVGs preserved in both locations; SHA256 manifest verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
