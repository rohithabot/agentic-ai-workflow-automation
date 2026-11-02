# AgentFlow AI — Agentic Workflow Automation Platform

An end-to-end AI-powered workflow automation platform built using LangGraph, LangChain, Ollama, FastAPI, React, and SQLite.

The application uses a locally hosted LLM to plan workflows, analyze CSV datasets, generate business insights, and produce downloadable reports.

## Features

* AI-powered workflow planning using Ollama
* LangGraph workflow orchestration
* CSV dataset upload and processing
* Automated sales performance analysis
* Business insights and revenue breakdown
* Automated Markdown report generation
* Interactive React dashboard
* SQLite workflow execution history
* Automated workflow evaluation
* Fully local AI execution without paid API calls

## Technology Stack

| Component       | Technology              |
| --------------- | ----------------------- |
| Frontend        | React, TypeScript, Vite |
| Backend         | Python, FastAPI         |
| AI Framework    | LangChain, LangGraph    |
| LLM             | Ollama — Llama 3.2      |
| Data Processing | Pandas                  |
| Database        | SQLite, SQLAlchemy      |
| Evaluation      | Python                  |
| Version Control | Git, GitHub             |

## System Architecture

```text
React Dashboard
       |
       v
FastAPI REST API
       |
       v
LangGraph Workflow
       |
       v
Ollama AI Planner
       |
       v
CSV Analysis
       |
       v
Report Generation
       |
       +------> SQLite Workflow History
       |
       v
React Dashboard
```

## Project Structure

```text
agentic-ai-workflow-automation/
├── backend/
│   ├── app/
│   │   ├── agent.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── tools.py
│   │   └── workflow.py
│   └── requirements.txt
├── data/
│   └── sales.csv
├── evaluation/
│   ├── test_workflows.py
│   └── evaluation_results.json
├── frontend/
│   └── react-app/
├── reports/
├── .gitignore
└── README.md
```

## Installation

### Prerequisites

* Python 3.12
* Node.js and npm
* Ollama
* Llama 3.2 model

### 1. Install the AI model

```powershell
ollama pull llama3.2:3b
```

### 2. Start the backend

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --port 8003
```

FastAPI documentation is available at `http://127.0.0.1:8003/docs`.

### 3. Start the frontend

Open another terminal:

```powershell
cd frontend\react-app
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

## API Endpoints

| Method | Endpoint              | Description                |
| ------ | --------------------- | -------------------------- |
| GET    | `/`                   | API health check           |
| POST   | `/upload`             | Upload CSV dataset         |
| POST   | `/workflow`           | Execute AI workflow        |
| GET    | `/history`            | Retrieve execution history |
| GET    | `/reports/{filename}` | Download generated report  |

## Example Workflow

**User instruction:**

Analyze sales performance and generate a report.

**Execution:**

1. The AI planner interprets the instruction.
2. LangGraph orchestrates the predefined workflow steps.
3. Pandas analyzes the sales dataset.
4. The application calculates business metrics.
5. A Markdown report is generated.
6. Execution details are saved in SQLite.
7. The React dashboard displays the results.

### Sample Results

| Metric              | Value      |
| ------------------- | ---------- |
| Total Revenue       | ₹13,40,000 |
| Units Sold          | 170        |
| Top Product         | Mobile     |
| Products Analyzed   | 6          |
| Electronics Revenue | ₹11,80,000 |
| Accessories Revenue | ₹1,60,000  |

These results are based on the included sample dataset.

## Automated Evaluation

Run the evaluation script from the project root while FastAPI is running:

```powershell
.\backend\.venv\Scripts\python.exe evaluation\test_workflows.py
```

The evaluation checks workflow completion and expected sales revenue.

Results are saved in `evaluation/evaluation_results.json`.

## Future Enhancements

* Dynamic agent tool selection
* Human-in-the-loop approval workflows
* Workflow retry and recovery mechanisms
* Interactive execution history dashboard
* Additional enterprise data integrations
* Docker deployment

## Project Purpose

This project demonstrates practical skills in:

* Generative AI application development
* Agentic workflow orchestration
* Local LLM integration
* REST API development
* Full-stack AI applications
* Automated data analysis
* Persistent workflow history
* AI workflow testing

## License

Created as a personal learning and portfolio project.
