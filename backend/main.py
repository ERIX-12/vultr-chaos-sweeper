import os
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sandbox_runner import (
    HardenedSandboxRunner,
    run_csv_analyst,
    run_prove_it_code_reviewer,
    run_chart_anything,
    run_file_fixer,
    run_self_healing_runner,
)

app = FastAPI(
    title="Vultr Chaos Sweeper — Autonomous Site QA & Sandboxed Code Suite",
    description="Blast Radius Zero Browser QA & Pattern A Code Execution on Vultr Cloud Compute & Serverless Inference",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VULTR_INFERENCE_BASE_URL = os.getenv("VULTR_INFERENCE_BASE_URL", "https://api.vultrinference.com/v1")
sandbox_runner = HardenedSandboxRunner()

class SweepRequest(BaseModel):
    target_url: str
    chaos_mode: bool = False
    memory_limit_mb: int = 512
    cpu_quota: float = 0.5
    timeout_seconds: int = 25

class CsvAnalystRequest(BaseModel):
    csv_text: str
    question: str

class ProveItReviewRequest(BaseModel):
    code_snippet: str
    test_snippet: str

class ChartAnythingRequest(BaseModel):
    prompt: str
    chart_type: str = "bar"

class FileFixerRequest(BaseModel):
    raw_content: str
    file_format: str = "csv"

class SelfHealingRequest(BaseModel):
    initial_code: str
    max_retries: int = 3

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "author": "Tusiime Eriya (MMU)",
        "orchestrator": "Vultr Cloud Compute Control Plane",
        "inference_endpoint": VULTR_INFERENCE_BASE_URL,
        "sandbox_isolation": "Docker Ephemeral + Zero-Secret Hygiene",
    }

@app.post("/api/sweep")
async def run_qa_and_chaos_sweep(req: SweepRequest):
    run_id = f"sweep-{uuid.uuid4().hex[:8]}"
    telemetry = await sandbox_runner.run_isolated_browser_sweep(
        run_id=run_id,
        target_url=req.target_url,
        chaos_mode=req.chaos_mode,
        memory_limit_mb=req.memory_limit_mb,
        cpu_quota=req.cpu_quota,
        timeout_seconds=req.timeout_seconds,
    )
    return {"run_id": run_id, "target_url": req.target_url, "sandbox_telemetry": telemetry}

@app.post("/api/pattern-a/csv-analyst")
async def api_csv_analyst(req: CsvAnalystRequest):
    return run_csv_analyst(req.csv_text, req.question)

@app.post("/api/pattern-a/prove-it-reviewer")
async def api_prove_it_reviewer(req: ProveItReviewRequest):
    return run_prove_it_code_reviewer(req.code_snippet, req.test_snippet)

@app.post("/api/pattern-a/chart-anything")
async def api_chart_anything(req: ChartAnythingRequest):
    return run_chart_anything(req.prompt, req.chart_type)

@app.post("/api/pattern-a/file-fixer")
async def api_file_fixer(req: FileFixerRequest):
    return run_file_fixer(req.raw_content, req.file_format)

@app.post("/api/pattern-a/self-healing-runner")
async def api_self_async def api_self_healing_runner(req: SelfHealingRequest):
  heal    return run_self_healing_runner(req.initial_code, req.max_retries)ing_runner(req: SelfHealingRequest):
    return run_self_healing_runner(req.initial_code, req.max_retries)
