# MineGuard AI 🛡️⛏️

> **"Predict the risk. Trace the impact. Plan the migration."**
>
> *Intelligent Post-Quantum Cybersecurity Platform for Safety-Critical Mining Infrastructure.*

---

## 🌟 Executive Summary

Mining operations rely on industrial operational technology (OT) with lifespans of 20–30 years.
Adversaries are executing **Harvest Now, Decrypt Later (HNDL)** attacks against SCADA telemetry,
ventilation control, gas monitoring, and hoist motors. 

**MineGuard AI** eliminates quantum vulnerabilities before Cryptographically-Relevant Quantum Computers (CRQCs) arrive (~2029) by:
1. **Scanning** code and configurations for Shor-vulnerable cryptography (`RSA`, `ECDSA`, `MD5`).
2. **Scoring** asset criticality and blast radiuses using deterministic severity metrics.
3. **Simulating** cascading physical failures via Breadth-First Search (BFS) graph propagation.
4. **Planning** a 3-phase, budget-feasible migration roadmap aligned with **NIST PQC Standards (FIPS 203 ML-KEM, FIPS 204 ML-DSA, FIPS 205 SLH-DSA)**.

---

## 📁 Project Architecture

```
MineGuard-AI/
├── start_mineguard.bat        # Interactive 1-click Windows launcher
├── requirements.txt           # Unified dependency specification
├── README.md                  # This document
│
├── presentation/              # Presentation Deck & Downloads
│   ├── MineGuard_Presentation.pdf    # 16:9 Landscape PDF (Widescreen, Ready to present)
│   ├── MineGuard_Presentation.pptx   # Microsoft PowerPoint deck
│   ├── MineGuard_Pitch_Deck.html     # Interactive browser presentation (1-click print to PDF)
│   └── generate_presentation.py     # Python generator script
│
├── web_dashboard/             # Standalone Zero-Dependency Web App
│   ├── app.py                 # Pure Python HTTP server & REST API (port 8080)
│   ├── engine.py              # Quantum risk & BFS cascade engine
│   ├── engine.js / engine-real.js  # Client-side graph simulator
│   ├── index.html             # Main dashboard hub
│   └── page1.html - page6.html# Scanner, Cascade, Risk, Graph, CBOM, and RAG pages
│
├── minimal/                   # Minimal 4-Feature Production Edition
│   ├── frontend/
│   │   ├── page1.html         # Feature 1: Scanner UI
│   │   ├── page2.html         # Feature 2: Cascade Simulator UI
│   │   ├── page3.html         # Features 3 & 4: Risk Scorer & Migration Roadmap UI
│   │   └── api.js             # API client with offline in-browser failover
│   └── backend/
│       ├── main.py            # FastAPI REST API (Endpoints: /scan, /cascade, /score, /plan)
│       ├── scanner.py         # Feature 1: Cryptographic regex scanner
│       ├── cascade.py         # Feature 2: BFS cascade simulation
│       ├── scorer.py          # Feature 3: Risk ranking algorithm
│       ├── planner.py         # Feature 4: Budgeted migration roadmap
│       └── test_minimal.py    # 10/10 automated pytest suite
│
└── enterprise/                # Enterprise Modular AI Platform (Phases A-F)
    └── backend/
        ├── requirements.txt
        ├── requirements-scanner.txt
        ├── app/
        │   ├── main.py        # Enterprise FastAPI gateway
        │   ├── engines/       # Real scanner, CBOM ingestion, ML training & SHAP explainability
        │   ├── rag/           # Vector embeddings, FAISS knowledge base & LLM guardrails
        │   ├── ilp/           # PuLP Integer Linear Programming migration optimizer
        │   └── api/           # Granular REST routers
        └── tests/             # 101/101 automated test suite
```

---

## 🚀 Quickstart Guide

### 1. Interactive 1-Click Launcher (Windows)
Double-click `start_mineguard.bat` to launch the menu, which lets you:
- Launch the **Web Dashboard** (runs locally on `http://localhost:8080`).
- Start the **Minimal FastAPI Backend** (port 8000).
- Start the **Enterprise Backend** (port 8000).
- Run the **Automated Test Suite**.
- Open the **Presentation PDF** or **PowerPoint Deck**.

### 2. Run the Web Dashboard Directly
```bash
cd web_dashboard
python app.py --port 8080
```
Open [http://localhost:8080](http://localhost:8080) in your browser.

### 3. Run the Minimal 4-Feature Backend
```bash
cd minimal/backend
pip install -r ../../requirements.txt
python -m uvicorn main:app --reload --port 8000
```
Open `minimal/frontend/page1.html` directly in your browser. It includes automatic offline failover so it works even if the server is stopped!

---

## 🧪 Automated Testing

To run the automated unit test suite:
```bash
cd minimal/backend
pytest test_minimal.py -v
```
**Results:** `10 passed in 0.40s (100% passing)`

---

## 📊 Presentations & Pitch Decks

All presentation files are located in the `presentation/` directory:
- **`MineGuard_Presentation.pdf`**: Widescreen 16:9 PDF formatted with clear headings, dark theme, and an architecture flowchart on Slide 3.
- **`MineGuard_Presentation.pptx`**: Native Microsoft PowerPoint presentation.
- **`MineGuard_Pitch_Deck.html`**: Clean browser-based deck with keyboard arrows navigation and a **Print to PDF** button.

---

## 🔒 NIST Post-Quantum Cryptography Alignment

| Vulnerable Algorithm | Threat Mechanism | NIST PQC Replacement Standard | Status |
| :--- | :--- | :--- | :--- |
| **RSA-2048 / RSA-4096** | Broken by Shor's Algorithm | **ML-KEM-768 / ML-KEM-1024 (FIPS 203)** | Standardized Aug 2024 |
| **ECDSA / ECDH** | Broken by Shor's Algorithm | **ML-DSA-65 / ML-DSA-87 (FIPS 204)** | Standardized Aug 2024 |
| **MD5 / SHA-1** | Pre-image collision / Grover | **SLH-DSA (FIPS 205) / SHA-3** | Standardized Aug 2024 |

---

## 🏆 Business & Safety Impact

- **Downtime Avoided:** \$150,000 / hour (Tier-1 mine shutdown cost).
- **Migration Cost:** \$210,000 over 14 weeks for all 5 safety-critical systems.
- **ROI:** The entire quantum migration costs less than **two hours** of unplanned downtime.
