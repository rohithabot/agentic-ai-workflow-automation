import json
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
)
from sqlalchemy.orm import declarative_base, sessionmaker


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = PROJECT_ROOT / "workflow_history.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class WorkflowHistory(Base):
    __tablename__ = "workflow_history"

    id = Column(Integer, primary_key=True, index=True)

    task = Column(Text, nullable=False)

    filename = Column(String(255), nullable=False)

    plan = Column(Text, nullable=True)

    status = Column(String(50), nullable=False)

    report_file = Column(String(255), nullable=True)

    error = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )


def initialize_database():
    """Create database tables if they do not exist."""

    Base.metadata.create_all(bind=engine)


def save_workflow_history(result: dict) -> dict:
    """Save workflow execution details to SQLite."""

    db = SessionLocal()

    try:
        record = WorkflowHistory(
            task=result.get("task", ""),
            filename=result.get("filename", ""),
            plan=json.dumps(result.get("plan", {})),
            status=result.get("status", "unknown"),
            report_file=result.get("report", {}).get("report_file"),
            error=result.get("error"),
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "id": record.id,
            "status": "saved",
        }

    finally:
        db.close()


def get_workflow_history(limit: int = 50) -> list:
    """Retrieve previous workflow executions."""

    db = SessionLocal()

    try:
        records = (
            db.query(WorkflowHistory)
            .order_by(
                WorkflowHistory.created_at.desc(),
                WorkflowHistory.id.desc(),
            )
            .limit(limit)
            .all()
        )

        return [
            {
                "id": record.id,
                "task": record.task,
                "filename": record.filename,
                "plan": json.loads(record.plan or "{}"),
                "status": record.status,
                "report_file": record.report_file,
                "error": record.error,
                "created_at": (
                    record.created_at.isoformat()
                    if record.created_at
                    else None
                ),
            }
            for record in records
        ]

    finally:
        db.close()