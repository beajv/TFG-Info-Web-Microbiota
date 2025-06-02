@echo off
cd "C:\Users\beatr\Desktop\TFG INFORMATICA\Web Microbiota\backend"

set PYTHONPATH=%CD%
set LOCAL_MODE=true

:: Ejecutar Uvicorn con LOCAL_MODE activado
start cmd /k "set LOCAL_MODE=true && python -m uvicorn myapp.main:app --reload"

cd "..\frontend"
npm run host

pause
