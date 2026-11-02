import { useState, type ChangeEvent, type FormEvent } from 'react';
import {
  Activity,
  BarChart3,
  Bot,
  Download,
  FileSpreadsheet,
  Play,
  Upload,
} from 'lucide-react';
import './App.css';

const API_URL = 'http://127.0.0.1:8003';

type SalesInsights = {
  total_revenue: number;
  total_units_sold: number;
  top_product: string | null;
  revenue_by_product: Record<string, number>;
  revenue_by_category: Record<string, number>;
};

type WorkflowResult = {
  task: string;
  filename: string;
  status: string;
  plan?: {
    task: string;
    steps: string[];
  };
  analysis?: {
    filename: string;
    rows: number;
    columns: string[];
    sales_insights?: SalesInsights;
  };
  report?: {
    report_file: string;
    status: string;
  };
};

function App() {
  const [filename, setFilename] = useState('sales.csv');
  const [task, setTask] = useState(
    'Analyze sales performance and generate a report'
  );
  const [result, setResult] = useState<WorkflowResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const handleUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    if (!file) return;

    setUploading(true);
    setError('');
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('CSV upload failed');
      }

      const data: { filename: string } = await response.json();
      setFilename(data.filename);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Unable to upload file'
      );
    } finally {
      setUploading(false);
    }
  };

  const handleRun = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!task.trim() || !filename) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/workflow`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          task,
          filename,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || 'Workflow execution failed');
      }

      const data: WorkflowResult = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Unable to execute workflow'
      );
    } finally {
      setLoading(false);
    }
  };

  const insights = result?.analysis?.sales_insights;

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <Bot size={28} />
          <div>
            <strong>AgentFlow AI</strong>
            <span>Workflow Automation</span>
          </div>
        </div>

        <div className="sidebar-section">
          <p>WORKSPACE</p>

          <div className="nav-item active">
            <Activity size={18} />
            Dashboard
          </div>

          <div className="nav-item">
            <FileSpreadsheet size={18} />
            Data Analysis
          </div>

          <div className="nav-item">
            <BarChart3 size={18} />
            Reports
          </div>
        </div>

        <div className="sidebar-footer">
          <span className="status-dot" />
          Local AI · Ollama
        </div>
      </aside>

      <main className="main">
        <header className="header">
          <div>
            <p className="eyebrow">AI WORKSPACE</p>
            <h1>Workflow Dashboard</h1>
            <p className="subtitle">
              Automate data analysis and reporting with local AI agents.
            </p>
          </div>

          <div className="header-badge">
            <span className="status-dot" />
            Local AI
          </div>
        </header>

        <div className="content-grid">
          <section className="card">
            <div className="card-heading">
              <Upload size={20} />
              <h2>Upload Dataset</h2>
            </div>

            <p className="card-description">
              Upload a CSV file or use the existing sample dataset.
            </p>

            <label className="upload-area">
              <FileSpreadsheet size={34} />
              <strong>
                {uploading ? 'Uploading...' : 'Choose CSV File'}
              </strong>
              <span>CSV files only · Maximum 10 MB</span>

              <input
                type="file"
                accept=".csv"
                onChange={handleUpload}
                disabled={uploading || loading}
                hidden
              />
            </label>

            <div className="selected-file">
              <FileSpreadsheet size={17} />
              <span>{filename}</span>
            </div>
          </section>

          <section className="card">
            <div className="card-heading">
              <Bot size={20} />
              <h2>AI Workflow</h2>
            </div>

            <p className="card-description">
              Describe what you want the AI agent to do.
            </p>

            <form onSubmit={handleRun}>
              <textarea
                value={task}
                onChange={(event) => setTask(event.target.value)}
                placeholder="Describe your workflow..."
                rows={5}
              />

              <button
                className="primary-button"
                type="submit"
                disabled={loading || uploading || !task.trim()}
              >
                <Play size={17} />
                {loading ? 'Executing Workflow...' : 'Run AI Workflow'}
              </button>
            </form>
          </section>
        </div>

        {error && <div className="error-message">{error}</div>}

        {result && (
          <>
            <section className="card result-card">
              <div className="card-heading">
                <Activity size={20} />
                <h2>Workflow Execution</h2>

                <span className="success-badge">
                  {result.status}
                </span>
              </div>

              <div className="workflow-steps">
                {result.plan?.steps.map((step, index) => (
                  <div className="workflow-step" key={`${step}-${index}`}>
                    <span className="step-number">{index + 1}</span>
                    <span>{step.replaceAll('_', ' ')}</span>
                  </div>
                ))}
              </div>
            </section>

            {insights && (
              <>
                <div className="metrics-grid">
                  <div className="metric-card">
                    <span>Total Revenue</span>
                    <strong>
                      {insights.total_revenue.toLocaleString('en-IN')}
                    </strong>
                  </div>

                  <div className="metric-card">
                    <span>Units Sold</span>
                    <strong>{insights.total_units_sold}</strong>
                  </div>

                  <div className="metric-card">
                    <span>Top Product</span>
                    <strong>{insights.top_product || 'N/A'}</strong>
                  </div>

                  <div className="metric-card">
                    <span>Products Analyzed</span>
                    <strong>
                      {Object.keys(insights.revenue_by_product).length}
                    </strong>
                  </div>
                </div>

                <section className="card">
                  <div className="card-heading">
                    <BarChart3 size={20} />
                    <h2>Revenue by Category</h2>
                  </div>

                  <div className="category-list">
                    {Object.entries(insights.revenue_by_category).map(
                      ([category, revenue]) => {
                        const percentage =
                          insights.total_revenue > 0
                            ? (revenue / insights.total_revenue) * 100
                            : 0;

                        return (
                          <div className="category-row" key={category}>
                            <div className="category-label">
                              <span>{category}</span>
                              <strong>
                                {revenue.toLocaleString('en-IN')}
                              </strong>
                            </div>

                            <div className="progress-track">
                              <div
                                className="progress-fill"
                                style={{
                                  width: `${Math.max(
                                    0,
                                    Math.min(100, percentage)
                                  )}%`,
                                }}
                              />
                            </div>
                          </div>
                        );
                      }
                    )}
                  </div>
                </section>
              </>
            )}

            {result.report?.report_file && (
              <section className="card report-card">
                <div>
                  <div className="card-heading">
                    <Download size={20} />
                    <h2>Generated Report</h2>
                  </div>

                  <p className="card-description">
                    {result.report.report_file}
                  </p>
                </div>

                <a
                  className="download-button"
                  href={`${API_URL}/reports/${encodeURIComponent(
                    result.report.report_file
                  )}`}
                  download
                >
                  <Download size={17} />
                  Download Report
                </a>
              </section>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;