"""
Shared HTML rendering for the interactive feature catalogue.

Used by the Sphinx docs site and (optionally) the Quarto table builder so the
searchable / filterable feature table stays a single source of truth.
"""

from __future__ import annotations

import re
from typing import Optional

import pandas as pd

from melody_features.feature_metadata import build_table, count_features

_IMPL_BADGE_CLASSES: dict[str, str] = {
    "FANTASTIC": "impl-fantastic",
    "jSymbolic": "impl-jsymbolic",
    "IDyOM": "impl-idyom",
    "MIDI Toolbox": "impl-midi-toolbox",
    "MUST": "impl-must",
    "SIMILE": "impl-simile",
    "Melsim": "impl-melsim",
    "Novel": "impl-novel",
    "Partitura": "impl-partitura",
}


def format_implementations_html(implementations: str) -> str:
    """Render implementation sources as compact badges."""
    if not implementations:
        return ""
    tokens = [t.strip() for t in implementations.split(",") if t.strip()]
    badges = []
    for token in tokens:
        css_class = _IMPL_BADGE_CLASSES.get(token, "impl-default")
        badges.append(f'<span class="impl-badge {css_class}">{token}</span>')
    return '<span class="impl-badges">' + " ".join(badges) + "</span>"


def format_type_badge_html(type_label: str) -> str:
    """Render Descriptor / Sequence as a colored pill."""
    if not type_label:
        return ""
    css_class = "type-descriptor" if type_label == "Descriptor" else "type-sequence"
    return f'<span class="type-badge {css_class}">{type_label}</span>'


def format_references_html(references: str) -> str:
    """Render citation strings as inline text or a compact list."""
    if not references:
        return ""
    parts = [p.strip() for p in references.split(" | ") if p.strip()]
    if len(parts) == 1:
        return f'<span class="citation-inline">{parts[0]}</span>'
    items = "".join(f"<li>{part}</li>" for part in parts)
    return f'<ul class="citation-list">{items}</ul>'


def format_notes_html(notes: str) -> str:
    """Improve readability of notes: code tokens, implementation names, emphasis."""
    if not notes:
        return ""

    text = notes

    def _code_token(match: re.Match[str]) -> str:
        return f"<code>{match.group(1)}</code>"

    text = re.sub(
        r"\bThis is called\s+([a-z][a-z0-9_]*)\s+in\s+([^.;]+)",
        r'This is called <code>\1</code> in <span class="impl-ref">\2</span>',
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r'\bThis feature is named\s+"([^"]+)"\s+in\s+([^.;]+)',
        r'This feature is named <strong>\1</strong> in <span class="impl-ref">\2</span>',
        text,
    )
    text = re.sub(
        r'\bnamed\s+"([^"]+)"\s+in\s+([^.;]+)',
        r'named <strong>\1</strong> in <span class="impl-ref">\2</span>',
        text,
    )
    text = re.sub(r"`([^`]+)`", _code_token, text)
    text = re.sub(
        r"\b([a-z][a-z0-9]*(?:_[a-z0-9]+)+)\b",
        _code_token,
        text,
    )
    return f'<span class="feature-notes">{text}</span>'


def format_description_html(description: str) -> str:
    """Wrap description text for consistent table typography."""
    if not description:
        return ""
    text = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", description)
    return f'<span class="feature-description">{text}</span>'


def format_name_html(name: str, source_url: str) -> str:
    """Render the feature name as a link to its source definition, if known."""
    if source_url:
        return (
            f'<a class="feature-name-link" href="{source_url}" target="_blank" '
            f'rel="noopener noreferrer">{name}</a>'
        )
    return f'<span class="feature-name-text">{name}</span>'


def format_table_display_html(df: pd.DataFrame) -> pd.DataFrame:
    """Apply HTML formatting to columns shown in the feature table."""
    display = df.copy()
    name_col = "Name" if "Name" in display.columns else "name"
    if name_col in display.columns and "source_url" in display.columns:
        display[name_col] = display.apply(
            lambda r: format_name_html(r[name_col], r.get("source_url", "")), axis=1
        )
    if "Pre-existing Implementations" in display.columns:
        display["Pre-existing Implementations"] = display["Pre-existing Implementations"].map(
            lambda v: format_implementations_html(v if isinstance(v, str) else "")
        )
    if "Type" in display.columns:
        display["Type"] = display["Type"].map(
            lambda v: format_type_badge_html(v if isinstance(v, str) else "")
        )
    if "Notes" in display.columns:
        display["Notes"] = display["Notes"].map(
            lambda v: format_notes_html(v if isinstance(v, str) else "")
        )
    if "Further References" in display.columns:
        display["Further References"] = display["Further References"].map(
            lambda v: format_references_html(v if isinstance(v, str) else "")
        )
    if "Description" in display.columns:
        display["Description"] = display["Description"].map(
            lambda v: format_description_html(v if isinstance(v, str) else "")
        )
    return display


def _normalize_implementation_token(token: str) -> str:
    token_low = token.lower()
    if token_low == "fantastic":
        return "FANTASTIC"
    if token_low == "jsymbolic":
        return "jSymbolic"
    if token_low in {"midi toolbox", "midi_toolbox"}:
        return "MIDI Toolbox"
    if token_low == "simile":
        return "SIMILE"
    if token_low == "idyom":
        return "IDyOM"
    if token_low == "must":
        return "MUST"
    return token


def _option_html(values: list[str]) -> str:
    return "\n".join(f'        <option value="{v}">{v}</option>' for v in values)


def _add_data_attributes(table_html: str, df_renamed: pd.DataFrame) -> str:
    lines = table_html.split("\n")
    result_lines = []
    data_row_index = 0
    for line in lines:
        if "<tr>" in line and "thead" not in line:
            if data_row_index < len(df_renamed):
                row = df_renamed.iloc[data_row_index]
                category = row.get("category", "")
                impls = row.get("Pre-existing Implementations", "") or ""
                ftype = row.get("Type", "") or ""
                domain = row.get("domain", "") or ""
                line = line.replace(
                    "<tr>",
                    (
                        f'<tr data-category="{category}" data-impl="{impls}" '
                        f'data-type="{ftype}" data-domain="{domain}">'
                    ),
                )
                data_row_index += 1
        result_lines.append(line)
    return "\n".join(result_lines)


_FEATURE_TABLE_CSS = """
.feature-catalogue .filter-container {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}
.feature-catalogue .search-input {
    flex: 1;
    min-width: 200px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}
.feature-catalogue .category-filter {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
    background-color: white;
    min-width: 150px;
}
.feature-catalogue .feature-counter {
    padding: 10px 15px;
    font-size: 16px;
    font-weight: 600;
    color: #495057;
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    white-space: nowrap;
    align-self: center;
}
.feature-catalogue .table-container {
    width: 100%;
    max-width: none;
    overflow-x: auto;
}
.feature-catalogue table.features-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: auto;
}
.feature-catalogue table.features-table td,
.feature-catalogue table.features-table th {
    word-wrap: break-word;
    word-break: normal;
    vertical-align: top;
    padding: 12px 15px;
    border: 1px solid #dee2e6;
}
.feature-catalogue table.features-table th {
    background-color: #f8f9fa;
    font-weight: bold;
    text-align: left;
    cursor: pointer;
    user-select: none;
    position: relative;
}
.feature-catalogue table.features-table th:hover {
    background-color: #eef1f4;
}
.feature-catalogue table.features-table th.sortable::after {
    content: ' ↕';
    opacity: 0.5;
}
.feature-catalogue table.features-table th.sortable.asc::after {
    content: ' ↑';
    opacity: 1;
}
.feature-catalogue table.features-table th.sortable.desc::after {
    content: ' ↓';
    opacity: 1;
}
.feature-catalogue #features-table td:first-child {
    min-width: 220px;
    width: 22%;
}
.feature-catalogue a.feature-name-link {
    color: #0d6efd;
    font-weight: 600;
    text-decoration: none;
}
.feature-catalogue a.feature-name-link:hover {
    text-decoration: underline;
}
.feature-catalogue .feature-name-text {
    font-weight: 600;
}
.feature-catalogue .impl-badges { display: flex; flex-wrap: wrap; gap: 0.35rem; }
.feature-catalogue .impl-badge {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    line-height: 1.3;
    white-space: nowrap;
    border: 1px solid transparent;
}
.feature-catalogue .impl-fantastic { background: #e8f4ea; color: #1b5e20; border-color: #c8e6c9; }
.feature-catalogue .impl-jsymbolic { background: #e3f2fd; color: #0d47a1; border-color: #bbdefb; }
.feature-catalogue .impl-idyom { background: #f3e5f5; color: #4a148c; border-color: #e1bee7; }
.feature-catalogue .impl-midi-toolbox { background: #fff3e0; color: #e65100; border-color: #ffe0b2; }
.feature-catalogue .impl-must { background: #e0f2f1; color: #004d40; border-color: #b2dfdb; }
.feature-catalogue .impl-simile { background: #fce4ec; color: #880e4f; border-color: #f8bbd0; }
.feature-catalogue .impl-melsim { background: #ede7f6; color: #4527a0; border-color: #d1c4e9; }
.feature-catalogue .impl-novel { background: #eceff1; color: #37474f; border-color: #cfd8dc; }
.feature-catalogue .impl-partitura { background: #e8eaf6; color: #1a237e; border-color: #c5cae9; }
.feature-catalogue .impl-default { background: #f1f3f5; color: #495057; border-color: #dee2e6; }
.feature-catalogue .type-badge {
    display: inline-block;
    padding: 0.2rem 0.55rem;
    border-radius: 0.35rem;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.feature-catalogue .type-descriptor { background: #eef2ff; color: #3730a3; }
.feature-catalogue .type-sequence { background: #ecfdf5; color: #065f46; }
.feature-catalogue .feature-description { color: #212529; line-height: 1.45; }
.feature-catalogue .feature-notes {
    display: block;
    color: #495057;
    font-size: 0.92rem;
    line-height: 1.45;
}
.feature-catalogue .feature-description code,
.feature-catalogue .feature-notes code {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.85em;
    padding: 0.1rem 0.35rem;
    border-radius: 0.25rem;
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    color: #c7254e;
    word-break: break-word;
}
.feature-catalogue .feature-notes .impl-ref { font-weight: 600; color: #343a40; }
.feature-catalogue .citation-inline {
    display: inline;
    font-size: 0.9rem;
    color: #495057;
    line-height: 1.35;
}
.feature-catalogue .citation-list {
    margin: 0;
    padding-left: 1.1rem;
    font-size: 0.88rem;
    color: #6c757d;
    line-height: 1.4;
}
.feature-catalogue .citation-list li { margin-bottom: 0.2rem; }
.feature-catalogue #features-table th:nth-child(2),
.feature-catalogue #features-table td:nth-child(2) { min-width: 11rem; }
.feature-catalogue #features-table th:nth-child(3),
.feature-catalogue #features-table td:nth-child(3) { min-width: 9.5rem; }
.feature-catalogue #features-table th:nth-child(4),
.feature-catalogue #features-table td:nth-child(4) { min-width: 16rem; }
.feature-catalogue #features-table th:nth-child(6),
.feature-catalogue #features-table td:nth-child(6) { min-width: 18rem; }
"""

_FEATURE_TABLE_JS = """
(function() {
    function initFeatureCatalogue() {
        const table = document.getElementById('features-table');
        if (!table) return;
        const root = table.closest('.feature-catalogue') || document;
        const searchInput = root.querySelector('#searchInput');
        const categoryFilter = root.querySelector('#categoryFilter');
        const implementationFilter = root.querySelector('#implementationFilter');
        const typeFilter = root.querySelector('#typeFilter');
        const domainFilter = root.querySelector('#domainFilter');
        const featureCounter = root.querySelector('#featureCounter');
        const tbody = table.querySelector('tbody');
        if (!tbody || !searchInput) return;
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const headers = table.querySelectorAll('th');

        headers.forEach((header, index) => {
            header.classList.add('sortable');
            header.addEventListener('click', () => sortTable(index));
        });

        function filterRows() {
            const searchTerm = searchInput.value.toLowerCase();
            const selectedCategory = categoryFilter ? categoryFilter.value : '';
            const selectedImplementation = implementationFilter ? implementationFilter.value : '';
            const selectedType = typeFilter ? typeFilter.value : '';
            const selectedDomain = domainFilter ? domainFilter.value : '';

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                const category = row.getAttribute('data-category') || '';
                const impl = row.getAttribute('data-impl') || '';
                const ftype = row.getAttribute('data-type') || '';
                const domain = row.getAttribute('data-domain') || '';

                const matchesSearch = text.includes(searchTerm);
                const matchesCategory = !selectedCategory || category.split(',').map(s => s.trim()).includes(selectedCategory);
                const matchesImplementation = !selectedImplementation || impl.split(',').map(s => s.trim()).includes(selectedImplementation);
                const matchesType = !selectedType || ftype === selectedType;

                let matchesDomain = true;
                if (selectedDomain) {
                    if (selectedDomain === 'Pitch') {
                        matchesDomain = domain === 'pitch' || domain === 'pitch,rhythm';
                    } else if (selectedDomain === 'Rhythm') {
                        matchesDomain = domain === 'rhythm' || domain === 'pitch,rhythm';
                    } else if (selectedDomain === 'Pitch & Rhythm') {
                        matchesDomain = domain === 'both';
                    } else {
                        matchesDomain = domain === selectedDomain.toLowerCase();
                    }
                }

                row.style.display = (matchesSearch && matchesCategory && matchesImplementation && matchesType && matchesDomain) ? '' : 'none';
            });

            if (featureCounter) {
                const visibleCount = rows.filter(row => row.style.display !== 'none').length;
                const totalCount = rows.length;
                if (visibleCount === totalCount) {
                    featureCounter.textContent = `${totalCount} feature${totalCount !== 1 ? 's' : ''}`;
                } else {
                    featureCounter.textContent = `${visibleCount} of ${totalCount} feature${totalCount !== 1 ? 's' : ''}`;
                }
            }
        }

        let sortColumn = -1;
        let sortDirection = 'asc';

        function sortTable(columnIndex) {
            const isAsc = sortColumn === columnIndex && sortDirection === 'asc';
            sortDirection = isAsc ? 'desc' : 'asc';
            sortColumn = columnIndex;

            headers.forEach((header, index) => {
                header.classList.remove('asc', 'desc');
                if (index === columnIndex) {
                    header.classList.add(sortDirection);
                }
            });

            const sortedRows = rows.slice().sort((a, b) => {
                const aText = a.cells[columnIndex].textContent.trim();
                const bText = b.cells[columnIndex].textContent.trim();
                const aNum = parseFloat(aText);
                const bNum = parseFloat(bText);
                if (!isNaN(aNum) && !isNaN(bNum)) {
                    return sortDirection === 'asc' ? aNum - bNum : bNum - aNum;
                }
                return sortDirection === 'asc'
                    ? aText.localeCompare(bText)
                    : bText.localeCompare(aText);
            });
            sortedRows.forEach(row => tbody.appendChild(row));
        }

        searchInput.addEventListener('input', filterRows);
        if (categoryFilter) categoryFilter.addEventListener('change', filterRows);
        if (implementationFilter) implementationFilter.addEventListener('change', filterRows);
        if (typeFilter) typeFilter.addEventListener('change', filterRows);
        if (domainFilter) domainFilter.addEventListener('change', filterRows);
        filterRows();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initFeatureCatalogue);
    } else {
        initFeatureCatalogue();
    }
})();
"""


def build_interactive_catalogue_html(df: Optional[pd.DataFrame] = None) -> str:
    """Return a self-contained interactive HTML fragment for the feature table."""
    if df is None:
        df = build_table()

    feature_count = len(df)
    df_renamed = df.rename(
        columns={
            "name": "Name",
            "implementations": "Pre-existing Implementations",
            "references": "Further References",
            "description": "Description",
            "type_label": "Type",
            "notes": "Notes",
        }
    )

    df_display = df_renamed.drop(
        columns=[
            "category",
            "domain",
            "sort_name",
            "python_name",
            "feature_types",
            "has_corpus_stats_param",
        ],
        errors="ignore",
    )
    df_display = format_table_display_html(df_display)
    df_display = df_display.drop(columns=["source_url"], errors="ignore")

    table_html = df_display.to_html(
        classes="features-table table table-striped table-hover",
        table_id="features-table",
        escape=False,
        index=False,
    )
    table_html = _add_data_attributes(table_html, df_renamed)

    all_categories = set()
    for cat_str in df["category"].fillna(""):
        for cat in [c.strip() for c in str(cat_str).split(",") if c.strip()]:
            all_categories.add(cat)
    category_options = _option_html(sorted(all_categories))
    domain_options = _option_html(["Pitch", "Rhythm", "Pitch & Rhythm"])

    impl_tokens = set()
    for value in df["implementations"].fillna(""):
        for token in [t.strip() for t in str(value).split(",") if t.strip()]:
            impl_tokens.add(_normalize_implementation_token(token))
    implementation_options = _option_html(sorted(impl_tokens))
    type_options = _option_html(sorted(df["type_label"].dropna().unique()))

    return f"""
<div class="feature-catalogue">
<style>
{_FEATURE_TABLE_CSS}
</style>
<p>This table provides a comprehensive overview of all <strong>{feature_count}</strong> melody features available in this package.</p>
<div class="filter-container">
    <input type="text" class="search-input" id="searchInput" placeholder="Search features...">
    <select class="category-filter" id="domainFilter">
        <option value="">All Domains</option>
{domain_options}
    </select>
    <select class="category-filter" id="categoryFilter">
        <option value="">All Categories</option>
{category_options}
    </select>
    <select class="category-filter" id="implementationFilter">
        <option value="">All Implementations</option>
{implementation_options}
    </select>
    <select class="category-filter" id="typeFilter">
        <option value="">All Types</option>
{type_options}
    </select>
    <span class="feature-counter" id="featureCounter">0 features</span>
</div>
<div class="table-container">
{table_html}
</div>
<script>
{_FEATURE_TABLE_JS}
</script>
</div>
""".strip()


__all__ = [
    "build_interactive_catalogue_html",
    "build_table",
    "count_features",
    "format_table_display_html",
    "format_implementations_html",
    "format_type_badge_html",
    "format_references_html",
    "format_notes_html",
    "format_description_html",
    "format_name_html",
]
