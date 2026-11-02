import json
import time
import urllib.request
from pathlib import Path

API_URL = "http://127.0.0.1:8003"

TEST_CASES = [
    {
        "name": "Sales analysis and report",
        "task": "Analyze sales.csv and generate a report",
        "filename": "sales.csv",
        "expected_revenue": 1340000,
    },
    {
        "name": "Sales performance analysis",
        "task": "Analyze sales performance and generate a report",
        "filename": "sales.csv",
        "expected_revenue": 1340000,
    },
]


def run_test(test):
    start = time.time()

    payload = json.dumps({
        "task": test["task"],
        "filename": test["filename"],
    }).encode("utf-8")

    request = urllib.request.Request(
        f"{API_URL}/workflow",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        insights = result.get("analysis", {}).get("sales_insights", {})

        passed = (
            result.get("status") == "completed"
            and insights.get("total_revenue") == test["expected_revenue"]
        )

        return {
            "test": test["name"],
            "passed": passed,
            "status": result.get("status"),
            "response_time": round(time.time() - start, 2),
        }

    except Exception as exc:
        return {
            "test": test["name"],
            "passed": False,
            "error": str(exc),
        }


def main():
    results = [run_test(test) for test in TEST_CASES]

    passed = sum(result["passed"] for result in results)

    summary = {
        "total_tests": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_rate": round(passed / len(results) * 100, 2),
        "results": results,
    }

    output = Path(__file__).parent / "evaluation_results.json"

    output.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()