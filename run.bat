@echo off
REM -------------------------------
REM Start FastAPI using uv environment
REM -------------------------------

REM Run FastAPI app
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause