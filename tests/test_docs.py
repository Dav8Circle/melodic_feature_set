"""Smoke tests so documentation stays aligned with the package surface."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import pytest

import melody_features as mf
import melody_features.features as features_module
from melody_features.feature_metadata import get_feature_metadata
from melody_features.feature_registry import discover_atomic_features, list_available_features

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"

REQUIRED_GUIDE_PAGES = (
    "index.rst",
    "installation.rst",
    "quickstart.rst",
    "usage.rst",
    "feature_catalogue.rst",
    "corpora.rst",
    "idyom.rst",
    "melsim.rst",
    "contour.rst",
    "contributing.rst",
    "license.rst",
    "api/index.rst",
    "api/melsim.rst",
    "api/melody_features.rst",
    "api/contour.rst",
    "api/idyom.rst",
    "api/tokenizer.rst",
)

FEATURE_DEFINITION_MODULES = sorted(
    p.stem
    for p in (REPO_ROOT / "src" / "melody_features" / "feature_definitions").glob("*.py")
    if p.stem != "__init__"
)

HAS_SPHINX = importlib.util.find_spec("sphinx") is not None


def test_required_guide_pages_exist():
    missing = [name for name in REQUIRED_GUIDE_PAGES if not (DOCS_DIR / name).is_file()]
    assert not missing, f"Missing docs pages: {missing}"


def test_feature_definition_modules_have_api_pages():
    missing = [
        name
        for name in FEATURE_DEFINITION_MODULES
        if not (DOCS_DIR / "api" / "feature_definitions" / f"{name}.rst").is_file()
    ]
    assert not missing, f"Feature modules without API RST pages: {missing}"


def test_index_toctree_entries_resolve():
    index = (DOCS_DIR / "index.rst").read_text(encoding="utf-8")
    # Entries under the two toctree blocks (relative docnames without .rst)
    entries = re.findall(r"(?m)^\s{3}([a-z0-9_./]+)\s*$", index)
    assert "quickstart" in entries
    assert "api/index" in entries
    missing = [
        entry
        for entry in entries
        if not (DOCS_DIR / f"{entry}.rst").is_file() and not (DOCS_DIR / entry / "index.rst").is_file()
    ]
    assert not missing, f"index.rst toctree points at missing docs: {missing}"


def test_catalogue_metadata_covers_discovered_features():
    """Every discovered feature should have catalogue metadata (family-prefixed)."""
    discovered = list_available_features()
    meta_names = set(get_feature_metadata()["feature_name"])
    meta_suffixes = {name.split(".", 1)[-1] for name in meta_names}

    missing = []
    for name in discovered:
        suffix = name.split(".", 1)[-1]
        # Contour / class descriptors are snake_cased in metadata
        # (e.g. StepContour.global_variation -> step_contour_global_variation).
        snake = re.sub(r"(?<!^)(?=[A-Z])", "_", name).replace(".", "_").lower()
        if name in meta_names or suffix in meta_suffixes or snake in meta_suffixes:
            continue
        if any(meta.endswith("_" + suffix) or meta.endswith(suffix) for meta in meta_suffixes):
            continue
        missing.append(name)

    assert not missing, f"Discovered features missing from catalogue metadata: {missing}"


def test_public_features_have_decorator_metadata_and_docstrings():
    incomplete = []
    for entry in discover_atomic_features(features_module):
        if "." in entry.name:
            continue  # class descriptors; metadata comes from the class
        func = getattr(features_module, entry.name, None)
        if func is None:
            incomplete.append((entry.name, "not imported on features module"))
            continue
        sources = getattr(func, "_feature_sources", None) or (
            [func._feature_source] if getattr(func, "_feature_source", None) else []
        )
        types = getattr(func, "_feature_types", None) or []
        domain = getattr(func, "_feature_domain", None)
        doc = (func.__doc__ or "").strip()
        problems = []
        if not sources:
            problems.append("missing source decorator")
        if not types:
            problems.append("missing type decorator")
        if not domain:
            problems.append("missing domain decorator")
        if not doc:
            problems.append("missing docstring")
        if problems:
            incomplete.append((entry.name, ", ".join(problems)))

    assert not incomplete, "Features incomplete for docs discovery:\n" + "\n".join(
        f"  {name}: {reason}" for name, reason in incomplete
    )


def test_docs_brand_symbols_remain_importable():
    for name in (
        "get_all_features",
        "list_available_features",
        "get_feature_metadata",
        "to_long_format",
        "Config",
        "FantasticConfig",
        "IDyOMConfig",
        "get_corpus_path",
        "get_corpus_files",
        "list_available_corpora",
        "pitch_range",
    ):
        assert hasattr(mf, name), f"melody_features.{name} missing (docs examples use mf.{name})"


def test_interactive_catalogue_html_builds():
    sys.path.insert(0, str(DOCS_DIR))
    from feature_table_html import build_interactive_catalogue_html, count_features

    html = build_interactive_catalogue_html()
    n_features = count_features()
    assert "feature-catalogue" in html
    assert n_features > 200
    assert str(n_features) in html


@pytest.mark.skipif(not HAS_SPHINX, reason="sphinx not installed (pip install -r docs/requirements.txt)")
def test_sphinx_docs_build(tmp_path):
    from sphinx.cmd.build import build_main

    out_dir = tmp_path / "dirhtml"
    status = build_main(["-b", "dirhtml", "-q", str(DOCS_DIR), str(out_dir)])
    assert status == 0, "sphinx-build failed"
    assert (out_dir / "index.html").is_file()
    assert (out_dir / "feature_catalogue" / "index.html").is_file()
    assert (out_dir / "usage" / "index.html").is_file()
    assert (out_dir / "api" / "melsim" / "index.html").is_file()
