from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.workflow import workflow
from app.tools import DATA_DIR, REPORT_DIR
from app.database import (
    initialize_database,
    save_workflow_history,
    get_workflow_history,
)


app = FastAPI(
    title="Agentic AI Workflow Automation Platform",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WorkflowRequest(BaseModel):
    task: str
    filename: str


@app.on_event("startup")
def startup_event():
    initialize_database()


@app.get("/")
def home():
    return {
        "message": "Agentic AI Workflow Automation API",
        "status": "running",
    }


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    filename = Path(file.filename or "").name

    if not filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported.",
        )

    content = await file.read()

    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Maximum file size is 10 MB.",
        )

    file_path = DATA_DIR / filename
    file_path.write_bytes(content)

    return {
        "filename": filename,
        "message": "CSV uploaded successfully",
    }


@app.post("/workflow")
def run_workflow(request: WorkflowRequest):
    try:
        result = workflow.invoke({
            "task": request.task,
            "filename": request.filename,
        })

    except Exception as exc:
        result = {
            "task": request.task,
            "filename": request.filename,
            "status": "failed",
            "error": str(exc),
        }

    save_workflow_history(result)

    if result.get("status") == "failed":
        raise HTTPException(
            status_code=400,
            detail=result.get("error", "Workflow failed"),
        )

    return result


@app.get("/history")
def history(limit: int = Query(default=50, ge=1, le=100)):
    return {
        "history": get_workflow_history(limit),
    }


@app.get("/reports/{filename}")
def get_report(filename: str):
    file_path = REPORT_DIR / Path(filename).name

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    return FileResponse(
        file_path,
        filename=file_path.name,
        media_type="text/markdown",
    )