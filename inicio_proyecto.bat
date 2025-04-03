@echo off
cd "C:\Users\beatr\Desktop\TFG INFORMATICA\Web Microbiota\backend"

set PYTHONPATH=%CD%

docker-compose up -d

:: Lanza Uvicorn en una ventana nueva
start cmd /k python -m uvicorn myapp.main:app --reload

cd "..\frontend"
npm run host

pause
