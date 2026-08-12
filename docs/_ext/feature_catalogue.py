"""Sphinx extension that embeds the interactive feature catalogue."""

from __future__ import annotations

from docutils import nodes
from docutils.parsers.rst import Directive


class FeatureCatalogueDirective(Directive):
    """Insert the searchable / filterable feature catalogue HTML."""

    has_content = False

    def run(self):
        from feature_table_html import build_interactive_catalogue_html

        html = build_interactive_catalogue_html()
        return [nodes.raw("", html, format="html")]


def setup(app):
    app.add_directive("feature-catalogue", FeatureCatalogueDirective)
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
