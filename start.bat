@echo off
REM ------------------------------------------------
REM Start FastAPI app with uv environment and Alembic
REM ------------------------------------------------

REM Step 1: Apply Alembic migrations
echo Running database migrations...
uv run alembic upgrade head

IF %ERRORLEVEL% NEQ 0 (
    echo Migration failed! Exiting.
    pause
    exit /b %ERRORLEVEL%
)

REM Step 2: Start FastAPI server
echo Starting FastAPI server...
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause