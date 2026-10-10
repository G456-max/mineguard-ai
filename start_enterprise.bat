@echo off
title MineGuard AI - Enterprise Backend
echo Starting Enterprise FastAPI Backend on http://localhost:8000 ...
cd enterprise\backend
python -m uvicorn app.main:app --reload --port 8000
pause
