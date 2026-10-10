@echo off
cls
echo ==============================================================
echo       MINEGUARD AI - POST-QUANTUM CYBERSECURITY PLATFORM
echo   "Predict the risk. Trace the impact. Plan the migration."
echo ==============================================================
echo.
echo  1. Launch Full Web Dashboard (Zero dependency, port 8080)
echo  2. Launch Minimal 4-Feature FastAPI Backend (port 8000)
echo  3. Launch Enterprise AI Modular Backend (port 8000)
echo  4. Run Minimal Unit Tests (10/10)
echo  5. Open Presentation PDF (16:9 Landscape)
echo  6. Open PowerPoint Pitch Deck (.pptx)
echo  7. Exit
echo.
set /p opt="Select an option [1-7]: "

if "%opt%"=="1" goto opt1
if "%opt%"=="2" goto opt2
if "%opt%"=="3" goto opt3
if "%opt%"=="4" goto opt4
if "%opt%"=="5" goto opt5
if "%opt%"=="6" goto opt6
if "%opt%"=="7" goto end

:opt1
start "" http://localhost:8080
cd web_dashboard
python app.py --port 8080
pause
goto end

:opt2
cd minimal\backend
python -m uvicorn main:app --reload --port 8000
pause
goto end

:opt3
cd enterprise\backend
python -m uvicorn app.main:app --reload --port 8000
pause
goto end

:opt4
cd minimal\backend
python -m pytest test_minimal.py -v
pause
goto end

:opt5
start "" "presentation\MineGuard_Presentation.pdf"
goto end

:opt6
start "" "presentation\MineGuard_Presentation.pptx"
goto end

:end
exit
