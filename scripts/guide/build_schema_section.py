"""Generate the guide's Schemas section from the UMF table specs.

Run by documentor (publish.site.sections) from the repository root with DOCUMENTOR_SECTION_OUT set to
the section's directory under the Hugo content root. Writes the table reference and the schema-browser
page there, and builds the upstream UMF schema browser into the site's static files.

    uv run --no-project --with pyyaml python scripts/guide/build_schema_section.py
"""
import os
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "docs/helix/02-design/umf/tables"
OUT = Path(os.environ["DOCUMENTOR_SECTION_OUT"]).resolve()
STATIC = OUT.parent.parent / "static" / "schema-browser"


def load() -> list[dict]:
    return [yaml.safe_load(p.read_text(encoding="utf-8")) for p in sorted(TABLES.glob("*.yaml"))]


def column_type(c: dict) -> str:
    t = c["data_type"]
    if c.get("precision"):
        return f"{t}({c['precision']},{c.get('scale', 0)})"
    return f"{t}({c['length']})" if c.get("length") else t


def rules(c: dict) -> str:
    out = []
    for v in c.get("validations") or []:
        kw = v.get("kwargs") or {}
        if "value_set" in kw:
            out.append("one of " + ", ".join(f"`{x}`" for x in kw["value_set"]))
        elif "min_value" in kw or "max_value" in kw:
            lo, hi = kw.get("min_value"), kw.get("max_value")
            out.append(f"{lo if lo is not None else '...'} to {hi if hi is not None else '...'}")
    return "; ".join(out)


def esc(text: str) -> str:
    return str(text).replace("|", "\\|")


def front(title: str, weight: int, extra: str = "") -> str:
    return f"---\ntitle: {title}\nweight: {weight}\n{extra}---\n\n"


def er_diagram(tables: list[dict]) -> str:
    lines = ["erDiagram"]
    by = {t["table_name"]: t for t in tables}
    for t in tables:
        cols = {c["name"]: c for c in t["columns"]}
        for fk in (t.get("relationships") or {}).get("foreign_keys") or []:
            nullable = cols[fk["column"]].get("nullable")
            one_to_one = fk["column"] in t.get("primary_key", []) and len(t["primary_key"]) == 1
            left = "||" if not nullable else "|o"
            right = "o|" if one_to_one else "o{"
            lines.append(f'    {fk["references_table"]} {left}--{right} {t["table_name"]} : "{fk["column"]}"')
    assert all(r in by for t in tables for r in [fk["references_table"] for fk in (t.get("relationships") or {}).get("foreign_keys") or []])
    return "\n".join(lines)


def reference(tables: list[dict]) -> str:
    body = [front("Table reference", 1),
            "Every table, column, key, and relationship in Tempo's database, generated from the "
            "[UMF table specs](https://github.com/DocumentDrivenDX/tempo/tree/main/docs/helix/02-design/umf/tables). "
            "Rules that live only in the database (the period-close trigger, the audit-log permissions, the `local_date` "
            "consistency check) are described in the data design and ADR-005, ADR-006, and ADR-007.\n",
            "## Relationships\n\n```mermaid\n" + er_diagram(tables) + "\n```\n",
            "## Tables\n"]
    body.append("| Table | Purpose |\n|---|---|\n" + "\n".join(
        f"| [`{t['table_name']}`](#{t['table_name'].replace('_', '-')}) | {esc(t['description'])} |" for t in tables) + "\n")
    for t in tables:
        name = t["table_name"]
        body.append(f"### {name}\n\n{t['description']}\n")
        body.append("| Column | Type | Null | Key | Rules | Description |\n|---|---|---|---|---|---|")
        for c in t["columns"]:
            key = (c.get("key_type") or "").replace("foreign_one_to_many", "foreign").replace("foreign_one_to_one", "foreign (1:1)")
            body.append(f"| `{c['name']}` | {column_type(c)} | {'yes' if c.get('nullable') else 'no'} | {key} | {esc(rules(c))} | {esc(c['description'])} |")
        body.append("")
        body.append("**Primary key:** " + ", ".join(f"`{k}`" for k in t["primary_key"]))
        if t.get("unique_constraints"):
            body.append("\n**Unique:** " + "; ".join("(" + ", ".join(f"`{k}`" for k in u) + ")" for u in t["unique_constraints"]))
        fks = (t.get("relationships") or {}).get("foreign_keys") or []
        if fks:
            body.append("\n**Foreign keys:** " + "; ".join(f"`{f['column']}` → `{f['references_table']}.{f['references_column']}`" for f in fks))
        body.append(f"\n[Source spec](https://github.com/DocumentDrivenDX/tempo/blob/main/docs/helix/02-design/umf/tables/{name}.yaml)\n")
    return "\n".join(body)


def browser_page() -> str:
    return (front("Schema browser", 2)
            + "The upstream [UMF](https://github.com/DocumentDrivenDX/umf) schema browser, loaded with Tempo's nine table specs. "
              "Search fields, follow foreign keys, and download the original YAML. "
              "[Open it full screen](../../schema-browser/assets/index.html).\n\n"
              '<iframe src="../../schema-browser/assets/index.html" title="Tempo schema browser" '
              'style="width:100%;height:80vh;border:1px solid #8884;border-radius:6px" loading="lazy"></iframe>\n')


def ensure_nav(site: Path) -> None:
    """Put the Schemas and Record sections in the navbar and on the home page.

    documentor's Hextra scaffold writes the menu and the home cards before project sections exist and
    only lists a section under params.sections, so these two would be reachable only by URL. This adds
    them idempotently; drop it when documentor links sections into the menu itself.
    """
    config_file = site / "hugo.yaml"
    config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
    menu = config["menu"]["main"]
    present = {m["name"] for m in menu}
    extras = [("Schemas", "/schemas/", 3), ("Record", "/record/", 4)]
    for name, ref, weight in extras:
        if name not in present and (site / "content" / ref.strip("/")).is_dir():
            menu.append({"name": name, "pageRef": ref, "weight": weight})
    for m in menu:
        if m["name"] == "How this guide was made":
            m["weight"] = 5
    menu.sort(key=lambda m: m["weight"])
    config_file.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")
    home = site / "content" / "_index.md"
    text = home.read_text(encoding="utf-8")
    cards = {"schemas/": ("Schemas", "The database tables, keys, and relationships, with an interactive schema browser."),
             "record/": ("Record", "The vision, requirements, and design documents, as written.")}
    add = "".join(f'  {{{{< card link="{link}" title="{t}" subtitle="{sub}" >}}}}\n'
                  for link, (t, sub) in cards.items() if f'link="{link}"' not in text)
    if add:
        home.write_text(text.replace("{{< /cards >}}", add + "{{< /cards >}}", 1), encoding="utf-8")


def main() -> int:
    tables = load()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "_index.md").write_text(
        front("Schemas", 5, "sidebar:\n  open: true\n")
        + "The detailed database schema for Tempo.\n\n"
          "- [Table reference](reference/): every table, column, key, and relationship, with an entity diagram.\n"
          "- [Schema browser](browser/): the interactive UMF schema browser.\n", encoding="utf-8")
    (OUT / "reference.md").write_text(reference(tables), encoding="utf-8")
    (OUT / "browser.md").write_text(browser_page(), encoding="utf-8")
    ensure_nav(OUT.parent.parent)
    subprocess.run(["node", str(ROOT / "docs/helix/02-design/umf/build-browser.mjs"), str(STATIC)], check=True, cwd=ROOT)
    print(f"schemas section: {len(tables)} tables -> {OUT}; browser -> {STATIC}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
