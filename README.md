# vultr-chaos-sweeper
Vultr Chaos Sweeper # Vultr Chaos Sweeper — Autonomous Site QA & Blast Radius Zero Sandbox

**Author:** Tusiime Eriya (Final-Year BSc Computer Science Student, Mountains of the Moon University — MMU)  
**Hackathon:** Vultr × lablab.ai Agent Rush Hackathon (November 3–8, 2026)  
**Challenge Track:** Challenge 01 — Blast Radius Zero (Combines Pattern B: Sandboxed Browser Use + Pattern A: Sandboxed Code Execution Suite)

---

## ⚡ How We Used Vultr (Official Hackathon Documentation)

### 1. Vultr Services & Infrastructure Used (100% CPU VM + Serverless Inference — Zero GPU Dependency)
- **Vultr Cloud Compute (Central Control & Orchestration Plane):** Hosts our FastAPI backend orchestrator (`backend/main.py`) and web application (deployable via **Coolify on Vultr** and backed by **Supabase on Vultr**). Complies strictly with the event rule that Vultr GPUs are not used.
- **Vultr Serverless Inference (`https://api.vultrinference.com/v1`):** Powers all agent LLM calls via its OpenAI-compatible API:
  - **Vision QA Verification:** Inspects screenshots returned from headless Chromium containers to flag UI layout overlaps (`41% CTA overlap` on `#checkout-btn`).
  - **Code & Patch Synthesis:** Generates Playwright regression tests, CSS/JS unified patches, and `pandas`/`matplotlib` scripts.
  - **Self-Healing Retry Loop:** Reads runtime `stderr` tracebacks (`KeyError`, `ZeroDivisionError`) and patches broken Python scripts across up to 3 attempts until `Exit Code 0`.
- **Vultr Object Storage (S3-Compatible):** Stores verifiable screenshot trails and before/after file diffs.

### 2. Blast Radius Zero Containment Architecture (The 4 Pillars)
1. **Process Isolation:** Executes every browser session and Python code snippet inside an ephemeral Docker/gVisor container under unprivileged UID `10001:10001`, `--read-only` root filesystem, `--cap-drop=ALL`, and `--security-opt=no-new-privileges:true`.
2. **Secret Hygiene:** `VULTR_INFERENCE_API_KEY` and S3 credentials remain strictly in the host orchestrator process on Vultr Cloud Compute; zero secrets are mounted inside worker containers.
3. **Resource Limits:** Enforces hard cgroup caps of `--memory=512m`, `--memory-swap=512m`, `--cpus=0.5`, `--pids-limit=64`, and a 25-second wall-clock timeout.
4. **Lifecycle Discipline:** Runs every container with `--rm` plus an explicit `docker rm -f <container_id>` teardown inside a `finally:` block.

### 3. Implemented Execution Patterns (Pattern B + Pattern A)
- **Pattern B (Sandboxed Browser Use):** Launches headless Chromium in a sealed container, blocks hidden DOM prompt injections (`rm -rf /`), aborts unauthorized cookie exfiltration, absorbs a 512 MB memory bomb (`Exit Code 137`), and enforces a **Human-in-the-Loop Approval Gate** before applying self-healing patches.
- **Pattern A (Sandboxed Code Execution Suite — All 5 Workflows):**
  1. **CSV Analyst (`/api/pattern-a/csv-analyst`):** Upload a spreadsheet + ask in plain English -> executed chart PNG + Python code + summary stats.
  2. **Prove-It Code Reviewer (`/api/pattern-a/prove-it-reviewer`):** Run PR snippets and unit tests in the sandbox -> pass/fail report (`Exit 0`) and hostile command interception (`Exit 126`).
  3. **Chart Anything (`/api/pattern-a/chart-anything`):** Natural language prompt in -> executed Matplotlib PNG image + code out.
  4. **File Fixer (`/api/pattern-a/file-fixer`):** Messy CSV or JSON in -> deduplicated, normalized file out + executed `difflib` before/after diff.
  5. **Self-Healing Runner (`/api/pattern-a/self-healing-runner`):** Run broken Python code -> read traceback -> patch via Vultr Serverless Inference -> retry loop visible on screen until `Exit Code 0`.

---

## Quickstart Deployment on Vultr Cloud Compute

```bash
# 1. Build the hardened Playwright sandbox image
cd sandbox
docker build -f Dockerfile.sandbox -t vultr-qa-sandbox:latest .
cd ..

# 2. Configure your Vultr Serverless Inference API key
cp .env.example .env

# 3. Start the orchestrator and demo target
docker compose up --build -d
```
