@echo off
title MineGuard AI - Minimal Backend
echo Starting Minimal FastAPI Backend on http://localhost:8000 ...
cd minimal\backend
python -m uvicorn main:app --reload --port 8000
pause
