import json

from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)


def create_plan(task: str) -> dict:
    """Generate a structured execution plan for a user task."""

    prompt = f"""
You are an AI workflow planner.

Analyze the user's task and create an execution plan.

Available tools:
1. analyze_csv - Analyze a CSV file.
2. generate_report - Generate a report from analysis results.

Return ONLY valid JSON in this format:

{{
    "task": "original user task",
    "steps": [
        "analyze_csv",
        "generate_report"
    ]
}}

Rules:
- Use only available tools.
- If the task asks for CSV analysis, include analyze_csv.
- If the task asks for a report, include generate_report.
- Do not include markdown formatting.
- Do not include explanations outside JSON.

User task:
{task}
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)
    except (json.JSONDecodeError, TypeError):
        return {
            "task": task,
            "steps": ["analyze_csv", "generate_report"],
        }