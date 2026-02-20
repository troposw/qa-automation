@echo off
setlocal

echo Setup starting...

REM Check for Python interpreter
set "PYTHON_CMD="
python --version >nul 2>&1 && set "PYTHON_CMD=python"
if not defined PYTHON_CMD (
    python3 --version >nul 2>&1 && set "PYTHON_CMD=python3"
)

if not defined PYTHON_CMD (
    set "err_msg=Python could not be found."
    goto error_exit
)

REM Create virtual environment
if not exist venv (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv venv || (
        set "err_msg=Failed to create virtual environment."
        goto error_exit
    )
) else (
    echo Virtual environment already exists.
)

REM Install Python dependencies
echo Installing Python dependencies...
call venv\Scripts\python -m pip install -r requirements.txt --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    set "err_msg=Python dependencies installation failed."
    goto error_exit
)

REM Create .env file if it doesn't exist
if not exist .env (
    if exist .env.example (
        echo Creating .env configuration...
        copy .env.example .env >nul 2>&1
    )
)

REM Install Node.js dependencies
where npm >nul 2>nul
if %errorlevel% equ 0 (
    echo Installing Node.js dependencies...
    call npm ci --silent --no-audit --no-fund >nul 2>&1
    if %errorlevel% neq 0 (
        set "err_msg=Node.js dependencies installation failed."
        goto error_exit
    )
) else (
    echo Warning: npm not found. Node.js dependencies were not installed.
)

echo.
echo Setup complete.
echo.
pause
exit /b 0

:error_exit
echo Error: %err_msg%
pause
exit /b 1
