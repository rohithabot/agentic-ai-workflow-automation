from pathlib import Path
from datetime import datetime, timezone

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
REPORT_DIR = PROJECT_ROOT / "reports"

DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def analyze_csv(filename: str) -> dict:
    """Analyze a CSV file and generate business insights."""

    file_path = DATA_DIR / Path(filename).name

    if not file_path.exists():
        return {"error": f"File not found: {filename}"}

    try:
        df = pd.read_csv(file_path)

        result = {
            "filename": file_path.name,
            "rows": len(df),
            "columns": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
        }

        if {"product", "category", "quantity", "revenue"}.issubset(df.columns):
            df["quantity"] = pd.to_numeric(df["quantity"], errors="raise")
            df["revenue"] = pd.to_numeric(df["revenue"], errors="raise")

            product_revenue = (
                df.groupby("product")["revenue"]
                .sum()
                .sort_values(ascending=False)
            )

            category_revenue = (
                df.groupby("category")["revenue"]
                .sum()
                .sort_values(ascending=False)
            )

            result["sales_insights"] = {
                "total_revenue": float(df["revenue"].sum()),
                "total_units_sold": int(df["quantity"].sum()),
                "top_product": (
                    str(product_revenue.index[0])
                    if not product_revenue.empty
                    else None
                ),
                "revenue_by_product": product_revenue.to_dict(),
                "revenue_by_category": category_revenue.to_dict(),
            }

        return result

    except Exception as exc:
        return {"error": str(exc)}


def generate_report(analysis: dict) -> dict:
    """Generate a Markdown report containing business insights."""

    if "error" in analysis:
        return analysis

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    report_name = f"analysis_report_{timestamp}.md"
    report_path = REPORT_DIR / report_name

    insights = analysis.get("sales_insights", {})

    report_content = f"""# AI Workflow Analysis Report

Generated: {datetime.now(timezone.utc).isoformat()}

## Dataset Information

- Filename: {analysis.get("filename")}
- Rows: {analysis.get("rows")}
- Columns: {", ".join(analysis.get("columns", []))}

## Sales Performance

- Total Revenue: {insights.get("total_revenue", "N/A")}
- Total Units Sold: {insights.get("total_units_sold", "N/A")}
- Top Product: {insights.get("top_product", "N/A")}

## Revenue by Product

{insights.get("revenue_by_product", {})}

## Revenue by Category

{insights.get("revenue_by_category", {})}

## Missing Values

{analysis.get("missing_values", {})}
"""

    report_path.write_text(report_content, encoding="utf-8")

    return {
        "report_file": report_name,
        "report_path": str(report_path),
        "status": "completed",
    }