from typing import TypedDict, Any

from langgraph.graph import StateGraph, END

from app.agent import create_plan
from app.tools import analyze_csv, generate_report


class WorkflowState(TypedDict, total=False):
    task: str
    filename: str
    plan: dict
    analysis: dict
    report: dict
    status: str
    error: str


def planner_node(state: WorkflowState) -> dict:
    plan = create_plan(state["task"])

    allowed_steps = {"analyze_csv", "generate_report"}

    steps = plan.get("steps", [])

    if not isinstance(steps, list):
        steps = []

    steps = [step for step in steps if step in allowed_steps]

    if "generate_report" in steps and "analyze_csv" not in steps:
        steps.insert(0, "analyze_csv")

    return {
        "plan": {
            "task": state["task"],
            "steps": steps,
        }
    }


def analysis_node(state: WorkflowState) -> dict:
    if "analyze_csv" not in state["plan"]["steps"]:
        return {
            "status": "skipped"
        }

    analysis = analyze_csv(state["filename"])

    if "error" in analysis:
        return {
            "analysis": analysis,
            "status": "failed",
            "error": analysis["error"],
        }

    return {
        "analysis": analysis,
        "status": "analyzed",
    }


def report_node(state: WorkflowState) -> dict:
    if state.get("status") == "failed":
        return {}

    if "generate_report" not in state["plan"]["steps"]:
        return {
            "status": "completed"
        }

    report = generate_report(state["analysis"])

    return {
        "report": report,
        "status": report.get("status", "failed"),
    }


builder = StateGraph(WorkflowState)

builder.add_node("planner", planner_node)
builder.add_node("analysis", analysis_node)
builder.add_node("report", report_node)

builder.set_entry_point("planner")

builder.add_edge("planner", "analysis")
builder.add_edge("analysis", "report")
builder.add_edge("report", END)

workflow = builder.compile()