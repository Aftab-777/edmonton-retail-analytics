"""Build a native PBIP/PBIR report from the committed retail snapshot.

Uses only Python's standard library. Open the generated PBIP in Power BI
Desktop, refresh its embedded snapshot, and verify the native rendering.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "powerbi" / "project"
REPORT = PROJECT / "Retail.Report"
MODEL = PROJECT / "Retail.SemanticModel"
SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/"
FACT = "retail_sales_monthly"
BLUE = "#1D5DB5"
ORANGE = "#E57939"
INK = "#172B4D"
MUTED = "#536581"
WIDTH, HEIGHT = 1280, 720


def write(path: Path, content: str | dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, dict):
        content = json.dumps(content, ensure_ascii=False, indent=2) + "\n"
    path.write_text(content, encoding="utf-8")


def identifier(label: str) -> str:
    return hashlib.sha256(label.encode()).hexdigest()[:20]


def literal(value: str | bool | int | float) -> dict:
    if isinstance(value, bool):
        text = str(value).lower()
    elif isinstance(value, str):
        text = "'" + value.replace("'", "''") + "'"
    else:
        text = f"{value}D"
    return {"expr": {"Literal": {"Value": text}}}


def color(value: str) -> dict:
    return {"solid": {"color": literal(value)}}


def object_properties(properties: dict, selector: dict | None = None) -> list:
    result = {"properties": properties}
    if selector:
        result["selector"] = selector
    return [result]


def field(kind: str, table: str, name: str, source: bool = False) -> dict:
    return {kind: {"Expression": {"SourceRef": {"Source" if source else "Entity": table}}, "Property": name}}


def projection(kind: str, table: str, name: str, display: str | None = None) -> dict:
    result = {"field": field(kind, table, name), "queryRef": f"{table}.{name}", "nativeQueryRef": name}
    if display:
        result["displayName"] = display
    if kind == "Column":
        result["active"] = True
    return result


def query(**roles: list) -> dict:
    return {"queryState": {role: {"projections": ps} for role, ps in roles.items()}}


def sort_by(query_definition: dict, expression: dict, direction: str = "Ascending") -> None:
    query_definition["sortDefinition"] = {"sort": [{"field": expression, "direction": direction}], "isDefaultSort": False}


def filter_definition(table: str, column: str, values: list[str], date: bool = False) -> dict:
    literals = [f"datetime'{v}T00:00:00'" if date else "'" + v.replace("'", "''") + "'" for v in values]
    return {
        "Version": 2,
        "From": [{"Name": "s", "Entity": table, "Type": 0}],
        "Where": [{"Condition": {"In": {
            "Expressions": [field("Column", "s", column, source=True)],
            "Values": [[{"Literal": {"Value": value}}] for value in literals],
        }}}],
    }


def container(title: str = "", alt: str = "", background: bool = True) -> dict:
    return {
        "title": object_properties({"show": literal(bool(title)), "text": literal(title), "fontSize": literal(13), "fontFamily": literal("Segoe UI"), "fontColor": color(INK), "alignment": literal("left"), "titleWrap": literal(True)}),
        "background": object_properties({"show": literal(background), "color": color("#FFFFFF"), "transparency": literal(0)}),
        "border": object_properties({"show": literal(background), "color": color("#E1E7F0"), "radius": literal(8)}),
        "padding": object_properties({key: literal(12) for key in ("top", "bottom", "left", "right")}),
        "general": object_properties({"altText": literal(alt or title)}),
    }


def add_visual(page: str, label: str, typ: str, x: int, y: int, w: int, h: int, order: int, q: dict | None = None, objects: dict | None = None, framing: dict | None = None, filters: dict | None = None) -> str:
    name = identifier(page + "/" + label)
    visual = {"visualType": typ, "visualContainerObjects": framing or container()}
    if q is not None:
        visual["query"] = q
    if objects:
        visual["objects"] = objects
    item = {"$schema": SCHEMA + "item/report/definition/visualContainer/2.4.0/schema.json", "name": name,
            "position": {"x": x, "y": y, "z": order, "width": w, "height": h, "tabOrder": order}, "visual": visual}
    if filters:
        item["filterConfig"] = filters
    write(REPORT / "definition" / "pages" / page / "visuals" / name / "visual.json", item)
    return name


def text(page: str, label: str, value: str, x: int, y: int, w: int, h: int, order: int, size: int = 12, shade: str = MUTED) -> str:
    framing = container(value, value, background=False)
    framing["title"][0]["properties"].update({"fontSize": literal(size), "fontColor": color(shade)})
    framing["border"][0]["properties"]["show"] = literal(False)
    framing["padding"] = object_properties({key: literal(0) for key in ("top", "bottom", "left", "right")})
    return add_visual(page, label, "textbox", x, y, w, h, order,
                      objects={"general": object_properties({"paragraphs": [{"textRuns": [{"value": ""}]}]})}, framing=framing)


def geography_filter(label: str, geographies: list[str]) -> dict:
    return {"filters": [{"name": identifier(label), "field": field("Column", FACT, "geography"),
                          "type": "Categorical", "howCreated": "User", "filter": filter_definition(FACT, "geography", geographies)}]}


def build_model(csv_bytes: bytes) -> None:
    write(MODEL / "definition.pbism", {"$schema": SCHEMA + "item/semanticModel/definitionProperties/1.0.0/schema.json", "version": "4.0", "settings": {"qnaEnabled": False}})
    write(MODEL / "definition" / "database.tmdl", "database EdmontonRetailPulse\n\tcompatibilityLevel: 1601\n\tcompatibilityMode: powerBI\n")
    write(MODEL / "definition" / "model.tmdl", "model Model\n\tculture: en-CA\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tsourceQueryCulture: en-CA\n\tdiscourageImplicitMeasures\n\nannotation __PBI_TimeIntelligenceEnabled = 0\nannotation PBI_QueryOrder = [\"retail_sales_monthly\",\"Report Month\"]\n\nref table retail_sales_monthly\nref table 'Report Month'\n")
    helper = (ROOT / "powerbi" / "retail-measures.tmdl").read_text(encoding="utf-8")
    measures = helper.split("ref table retail_sales_monthly", 1)[1]
    measures = "\n".join(line[1:] if line.startswith("\t") else line for line in measures.splitlines()).strip("\n")
    extra = """

\t/// Sales for the selected report month; preserves the geography on the chart axis.
\tmeasure 'Selected Month Sales CAD' =
\t\t\tVAR TargetMonth = COALESCE ( SELECTEDVALUE ( 'Report Month'[month] ), CALCULATE ( MAX ( retail_sales_monthly[month] ), REMOVEFILTERS ( retail_sales_monthly ) ) )
\t\t\tRETURN
\t\t\t    CALCULATE ( SUM ( retail_sales_monthly[sales_cad_thousands] ) * 1000, retail_sales_monthly[month] = TargetMonth )
\t\tformatString: "#,0"
"""
    columns = """

\tcolumn month
\t\tdataType: dateTime
\t\tformatString: "mmm yyyy"
\t\tsummarizeBy: none
\t\tsourceColumn: month
\t\tannotation UnderlyingDateTimeDataType = Date

\tcolumn geography
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: geography

\tcolumn sales_cad_thousands
\t\tdataType: int64
\t\tformatString: "#,0"
\t\tsummarizeBy: none
\t\tsourceColumn: sales_cad_thousands

\tcolumn quality_status
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: quality_status
"""
    encoded = base64.b64encode(csv_bytes).decode("ascii")
    partition = f"""

\tpartition retail_sales_monthly = m
\t\tmode: import
\t\tsource =
\t\t\tlet
\t\t\t    Source = Csv.Document(Binary.FromText("{encoded}", BinaryEncoding.Base64), [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    Dates = Table.TransformColumns(Headers, {{{{"month", each Date.FromText(_ & "-01", [Format="yyyy-MM-dd", Culture="en-CA"]), type date}}}}),
\t\t\t    Types = Table.TransformColumnTypes(Dates, {{{{"geography", type text}}, {{"sales_cad_thousands", Int64.Type}}, {{"quality_status", type text}}}})
\t\t\tin
\t\t\t    Types
"""
    write(MODEL / "definition" / "tables" / "retail_sales_monthly.tmdl", "table retail_sales_monthly\n\n" + measures + extra + columns + partition)
    write(MODEL / "definition" / "tables" / "Report Month.tmdl", """/// Disconnected month selector. No relationship to the fact table.
table 'Report Month'

\tcolumn month
\t\tdataType: dateTime
\t\tformatString: "mmm yyyy"
\t\tsummarizeBy: none
\t\tsourceColumn: [month]
\t\tannotation UnderlyingDateTimeDataType = Date

\tpartition 'Report Month' = calculated
\t\tmode: import
\t\tsource = DISTINCT ( retail_sales_monthly[month] )
""")


def build_report(latest_month: str) -> None:
    overview, quality = identifier("retail-overview"), identifier("source-quality")
    write(PROJECT / "Edmonton-Retail-Pulse.pbip", {"$schema": SCHEMA + "pbip/pbipProperties/1.0.0/schema.json", "version": "1.0", "artifacts": [{"report": {"path": "Retail.Report"}}], "settings": {"enableAutoRecovery": True}})
    write(REPORT / "definition.pbir", {"$schema": SCHEMA + "item/report/definitionProperties/2.0.0/schema.json", "version": "4.0", "datasetReference": {"byPath": {"path": "../Retail.SemanticModel"}}})
    write(REPORT / "definition" / "version.json", {"$schema": SCHEMA + "item/report/definition/versionMetadata/1.0.0/schema.json", "version": "2.0.0"})
    theme_version = {"visual": "2.4.0", "page": "2.0.0", "report": "3.0.0"}
    write(REPORT / "definition" / "report.json", {
        "$schema": SCHEMA + "item/report/definition/report/3.0.0/schema.json",
        "themeCollection": {
            "baseTheme": {"name": "CY24SU02", "reportVersionAtImport": theme_version, "type": "SharedResources"},
            "customTheme": {"name": "retail-theme.json", "reportVersionAtImport": theme_version, "type": "RegisteredResources"},
        },
        "resourcePackages": [
            {"name": "SharedResources", "type": "SharedResources", "items": [{"name": "CY24SU02", "path": "BaseThemes/CY24SU02.json", "type": "BaseTheme"}]},
            {"name": "RegisteredResources", "type": "RegisteredResources", "items": [{"name": "retail-theme.json", "path": "retail-theme.json", "type": "CustomTheme"}]},
        ],
        "settings": {"useStylableVisualContainerHeader": True, "defaultFilterActionIsDataFilter": True, "allowChangeFilterTypes": True, "useEnhancedTooltips": True},
    })
    theme = json.loads((ROOT / "powerbi" / "retail-theme.json").read_text())
    theme["dataColors"] = [ORANGE, BLUE, "#3F9C88", "#7987A0", "#9A6BC5"]
    write(REPORT / "StaticResources" / "RegisteredResources" / "retail-theme.json", theme)
    write(REPORT / "definition" / "pages" / "pages.json", {"$schema": SCHEMA + "item/report/definition/pagesMetadata/1.0.0/schema.json", "pageOrder": [overview, quality], "activePageName": overview})
    for page, title in [(overview, "Retail overview"), (quality, "Source data & notes")]:
        write(REPORT / "definition" / "pages" / page / "page.json", {"$schema": SCHEMA + "item/report/definition/page/2.0.0/schema.json", "name": page, "displayName": title, "displayOption": "FitToPage", "height": HEIGHT, "width": WIDTH,
            "objects": {"background": object_properties({"color": color("#F6F8FC"), "transparency": literal(0)})}})

    text(overview, "heading", "Edmonton Retail Pulse", 24, 14, 950, 48, 1000, 26, INK)
    text(overview, "subtitle", "Monthly retail activity | Edmonton, Calgary and Alberta | Unadjusted sales", 24, 66, 940, 35, 2000, 12)
    slicer_q = query(Values=[projection("Column", "Report Month", "month", "Report month")])
    sort_by(slicer_q, field("Column", "Report Month", "month"), "Descending")
    add_visual(overview, "report-month", "slicer", 1000, 16, 256, 88, 3000, slicer_q, {
        "data": object_properties({"mode": literal("Dropdown")}),
        "selection": object_properties({"singleSelect": literal(True), "strictSingleSelect": literal(True), "selectAllCheckboxEnabled": literal(False)}),
        "header": object_properties({"show": literal(False)}),
        "items": object_properties({"textSize": literal(12), "fontColor": color(INK)}),
        "general": object_properties({"filter": {"filter": filter_definition("Report Month", "month", [latest_month + "-01"], date=True)}}),
    }, container("Report month", "Select one month. Cards and sales comparison update; the growth chart retains the full history."))

    cards = [
        ("Edmonton Sales CAD", "Edmonton sales · CAD", BLUE, 1000000000, 3),
        ("Edmonton YoY %", "Edmonton growth · YoY", BLUE, 1, 2),
        ("Edmonton Share of Alberta %", "Edmonton share of Alberta", BLUE, 1, 2),
        ("Calgary Sales CAD", "Calgary sales · CAD", ORANGE, 1000000000, 3),
        ("Calgary YoY %", "Calgary growth · YoY", ORANGE, 1, 2),
    ]
    for i, (name, label, shade, units, precision) in enumerate(cards):
        add_visual(overview, name, "cardVisual", 24 + i * 248, 124, 240, 132, 4000 + i * 1000,
            query(Data=[projection("Measure", FACT, name, label)]), {
                "value": object_properties({"fontSize": literal(28), "fontColor": color(shade), "bold": literal(True), "horizontalAlignment": literal("left"), "labelDisplayUnits": literal(units), "labelPrecision": literal(precision)}, {"id": "default"}),
                "label": object_properties({"show": literal(False)}, {"id": "default"}),
                "layout": object_properties({"alignment": literal("top")}),
                "fillCustom": object_properties({"show": literal(False)}),
            }, container(label, label + ". Value is for the selected report month."))

    trend_q = query(Category=[projection("Column", FACT, "month", "Month")], Y=[projection("Measure", FACT, "Trend YoY %", "Year-over-year growth")], Series=[projection("Column", FACT, "geography", "City")])
    sort_by(trend_q, field("Column", FACT, "month"))
    trend = add_visual(overview, "city-growth-trend", "lineChart", 24, 280, 764, 316, 9000, trend_q, {
        "categoryAxis": object_properties({"axisType": literal("Scalar"), "showAxisTitle": literal(False), "fontSize": literal(10)}),
        "valueAxis": object_properties({"showAxisTitle": literal(False), "fontSize": literal(10), "labelDisplayUnits": literal(1), "labelPrecision": literal(0)}),
        "legend": object_properties({"show": literal(True), "position": literal("Top"), "showTitle": literal(False), "fontSize": literal(11)}),
        "lineStyles": object_properties({"strokeWidth": literal(3)}),
    }, container("Retail sales growth · same month a year earlier", "Edmonton and Calgary year-over-year growth, January 2024 to July 2026. 2023 is blank because 2022 data is not included."), geography_filter("trend-city-filter", ["Edmonton, Alberta", "Calgary, Alberta"]))

    comparison_q = query(Category=[projection("Column", FACT, "geography", "Geography")], Y=[projection("Measure", FACT, "Selected Month Sales CAD", "Sales CAD")])
    sort_by(comparison_q, field("Measure", FACT, "Selected Month Sales CAD"), "Descending")
    comparison = add_visual(overview, "selected-month-comparison", "clusteredBarChart", 804, 280, 452, 316, 10000, comparison_q, {
        "categoryAxis": object_properties({"showAxisTitle": literal(False), "fontSize": literal(10)}),
        "valueAxis": object_properties({"showAxisTitle": literal(False), "fontSize": literal(10), "labelDisplayUnits": literal(1000000000), "labelPrecision": literal(1), "start": literal(0)}),
        "labels": object_properties({"show": literal(True), "fontSize": literal(11), "labelDisplayUnits": literal(1000000000), "labelPrecision": literal(3)}),
        "dataPoint": object_properties({"defaultColor": color(BLUE)}),
    }, container("Selected month sales · CAD billions", "Edmonton, Calgary and the Alberta provincial total. Alberta includes both cities; these values must not be added."), geography_filter("comparison-geography-filter", ["Alberta", "Edmonton, Alberta", "Calgary, Alberta"]))

    text(overview, "comparison-note", "Alberta includes both cities. The province and city figures are not additive.", 804, 608, 452, 46, 11000, 10)
    text(overview, "source-note", "Source: Statistics Canada table 20-10-0056-01 | Jan 2023–Jul 2026 | Snapshot accessed Sep 27, 2026. Unadjusted monthly sales can be revised. The month selector changes the cards and comparison; the trend shows the full history.", 24, 610, 764, 83, 12000, 11)
    text(overview, "share-note", "Edmonton's share is a geographic share of Alberta retail sales, not a company's market share.", 804, 660, 452, 44, 13000, 10)
    page_path = REPORT / "definition" / "pages" / overview / "page.json"
    page_obj = json.loads(page_path.read_text())
    page_obj["visualInteractions"] = [{"source": source, "target": target, "type": "NoFilter"} for source, target in [(comparison, trend), (trend, comparison)]]
    write(page_path, page_obj)

    text(quality, "heading", "Source data & calculation notes", 24, 14, 1232, 52, 1000, 24, INK)
    text(quality, "subtitle", "All 172 source observations | Four geographies | January 2023–July 2026", 24, 72, 1232, 38, 2000, 12)
    quality_q = query(Values=[projection("Column", FACT, "month", "Month"), projection("Column", FACT, "geography", "Geography"), projection("Measure", FACT, "Retail Sales CAD", "Sales CAD"), projection("Column", FACT, "quality_status", "Source quality status")])
    sort_by(quality_q, field("Column", FACT, "month"), "Descending")
    add_visual(quality, "source-table", "tableEx", 24, 132, 790, 548, 3000, quality_q, {
        "columnHeaders": object_properties({"fontSize": literal(12), "fontColor": color(INK), "backColor": color("#EAF0F8"), "wordWrap": literal(True)}),
        "values": object_properties({"fontSize": literal(11), "fontColor": color(INK)}),
        "grid": object_properties({"rowPadding": literal(6), "gridVertical": literal(False)}),
        "total": object_properties({"totals": literal(False)}),
    }, container("Monthly source records", "Full snapshot, not limited by the overview month selector. No total is shown because national, provincial and city records overlap."))
    notes = [
        ("question", "Business question", "How is Edmonton retail activity changing, and how does it compare with Calgary and Alberta?"),
        ("units", "Units and calculations", "Source sales are in thousands of CAD. Multiply by 1,000 for CAD. YoY growth = (current month − same month last year) ÷ same month last year."),
        ("share", "Geographic share", "Edmonton sales ÷ Alberta sales. Alberta includes Edmonton and Calgary. Do not sum overlapping geography totals."),
        ("limits", "Interpretation limits", "Unadjusted sales reflect seasonality and can be revised. Growth for 2023 is blank because no 2022 comparison is in this snapshot. Source quality codes are retained as provided."),
        ("source", "Source and licence", "Statistics Canada table 20-10-0056-01, released Sep 24, 2026; accessed Sep 27, 2026. Statistics Canada Open Licence. Independent portfolio analysis."),
    ]
    for i, (key, title, body) in enumerate(notes):
        y = 132 + 110 * i
        text(quality, key + "-title", title, 844, y, 412, 32, 4000 + 2000 * i, 14, INK)
        text(quality, key + "-body", body, 844, y + 35, 412, 75, 5000 + 2000 * i, 11)


def main() -> None:
    csv_bytes = (ROOT / "data" / "retail_sales_monthly.csv").read_bytes()
    rows = list(csv.DictReader(io.StringIO(csv_bytes.decode("utf-8-sig"))))
    assert len(rows) == 172, "Unexpected snapshot: review data and documentation before rebuilding."
    latest_month = max(row["month"] for row in rows)
    assert latest_month == "2026-07", "Review the report's snapshot labels before using newer data."
    build_model(csv_bytes)
    build_report(latest_month)
    write(PROJECT / ".gitignore", "**/.pbi/\n")
    count = len(list(REPORT.rglob("visual.json")))
    print(f"Created native project: {PROJECT / 'Edmonton-Retail-Pulse.pbip'}")
    print(f"{len(rows)} embedded rows; 2 report pages; {count} visuals. Power BI Desktop validation remains required.")


if __name__ == "__main__":
    main()
