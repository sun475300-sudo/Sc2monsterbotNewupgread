@echo off
REM ============================================================================
REM   HYPER-FAST CODE INSPECTOR
REM   Ultra-fast code quality checks using Ruff (Rust-based)
REM   
REM   Performance: 10-100x faster than traditional tools
REM   Capability: 1 million+ lines per second
REM ============================================================================

setlocal enabledelayedexpansion

REM Colors (Windows 10+)
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "CYAN=[96m"
set "RESET=[0m"

:MENU
cls
echo.
echo %CYAN%============================================================================%RESET%
echo %CYAN%   HYPER-FAST CODE INSPECTOR%RESET%
echo %CYAN%   Rust-powered ^| Sub-second ^| 1M+ lines/second%RESET%
echo %CYAN%============================================================================%RESET%
echo.
echo   %GREEN%[1]%RESET% Full Project Scan           (all Python files)
echo   %GREEN%[2]%RESET% Incremental Scan            (modified files only - ultra-fast)
echo   %GREEN%[3]%RESET% Scan + Auto-Fix             (fix issues automatically)
echo   %GREEN%[4]%RESET% Format Code                 (Ruff formatter)
echo   %GREEN%[5]%RESET% Performance Profile         (show detailed stats)
echo   %GREEN%[6]%RESET% Install/Update Tools        (install Ruff + pre-commit)
echo   %GREEN%[7]%RESET% Setup Pre-commit Hooks      (automatic checks on commit)
echo.
echo   %YELLOW%[8]%RESET% Run Manual Ruff Check       (direct Ruff command)
echo   %YELLOW%[9]%RESET% Check Ruff Status           (version and installation)
echo.
echo   %RED%[0]%RESET% Exit
echo.
set /p choice="%CYAN%Select option:%RESET% "

if "%choice%"=="1" goto FULL_SCAN
if "%choice%"=="2" goto INCREMENTAL_SCAN
if "%choice%"=="3" goto SCAN_FIX
if "%choice%"=="4" goto FORMAT_CODE
if "%choice%"=="5" goto PERFORMANCE_PROFILE
if "%choice%"=="6" goto INSTALL_TOOLS
if "%choice%"=="7" goto SETUP_PRECOMMIT
if "%choice%"=="8" goto MANUAL_RUFF
if "%choice%"=="9" goto CHECK_STATUS
if "%choice%"=="0" goto END

echo %RED%Invalid option. Please try again.%RESET%
timeout /t 2 >nul
goto MENU

REM ============================================================================
REM   FULL PROJECT SCAN
REM ============================================================================
:FULL_SCAN
echo.
echo %CYAN%[SCAN] Running full project scan...%RESET%
echo.
python fast_code_inspector.py --profile
echo.
pause
goto MENU

REM ============================================================================
REM   INCREMENTAL SCAN (Only modified files)
REM ============================================================================
:INCREMENTAL_SCAN
echo.
echo %CYAN%[SCAN] Running incremental scan (modified files only)...%RESET%
echo.
python fast_code_inspector.py --fast --profile
echo.
pause
goto MENU

REM ============================================================================
REM   SCAN + AUTO-FIX
REM ============================================================================
:SCAN_FIX
echo.
echo %CYAN%[SCAN+FIX] Running scan with automatic fixes...%RESET%
echo.
python fast_code_inspector.py --fix --profile
echo.
pause
goto MENU

REM ============================================================================
REM   FORMAT CODE
REM ============================================================================
:FORMAT_CODE
echo.
echo %CYAN%[FORMAT] Running Ruff formatter...%RESET%
echo.
python fast_code_inspector.py --format
echo.
pause
goto MENU

REM ============================================================================
REM   PERFORMANCE PROFILE
REM ============================================================================
:PERFORMANCE_PROFILE
echo.
echo %CYAN%[PROFILE] Running with detailed performance statistics...%RESET%
echo.
python fast_code_inspector.py --profile --json
echo.
pause
goto MENU

REM ============================================================================
REM   INSTALL/UPDATE TOOLS
REM ============================================================================
:INSTALL_TOOLS
echo.
echo %CYAN%[INSTALL] Installing/updating hyper-fast code inspection tools...%RESET%
echo.
echo Installing Ruff (ultra-fast linter)...
pip install --upgrade ruff
echo.
echo Installing pre-commit (git hooks)...
pip install --upgrade pre-commit
echo.
echo %GREEN%[SUCCESS] Tools installed successfully!%RESET%
echo.
pause
goto MENU

REM ============================================================================
REM   SETUP PRE-COMMIT HOOKS
REM ============================================================================
:SETUP_PRECOMMIT
echo.
echo %CYAN%[PRE-COMMIT] Setting up git hooks for automatic checks...%RESET%
echo.

REM Check if git repository
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR] Not a git repository!%RESET%
    echo Initialize git first: git init
    pause
    goto MENU
)

REM Install pre-commit
echo Installing pre-commit...
pip install pre-commit
echo.

REM Install hooks
echo Installing git hooks...
pre-commit install
echo.

REM Run test
echo Testing hooks (this may take a moment)...
pre-commit run --all-files
echo.

echo %GREEN%[SUCCESS] Pre-commit hooks installed!%RESET%
echo.
echo Now every git commit will automatically:
echo   - Run Ruff linter (ultra-fast)
echo   - Format code automatically
echo   - Check for common issues
echo.
pause
goto MENU

REM ============================================================================
REM   MANUAL RUFF CHECK
REM ============================================================================
:MANUAL_RUFF
echo.
echo %CYAN%[RUFF] Running direct Ruff command...%RESET%
echo.
set /p ruff_args="Enter Ruff arguments (or press Enter for default check): "
if "%ruff_args%"=="" (
    ruff check .
) else (
    ruff check %ruff_args%
)
echo.
pause
goto MENU

REM ============================================================================
REM   CHECK STATUS
REM ============================================================================
:CHECK_STATUS
echo.
echo %CYAN%============================================================================%RESET%
echo %CYAN%   TOOL STATUS CHECK%RESET%
echo %CYAN%============================================================================%RESET%
echo.

REM Check Ruff
echo Checking Ruff installation...
ruff --version 2>nul
if errorlevel 1 (
    echo %RED%[NOT INSTALLED] Ruff%RESET%
    echo Install with: pip install ruff
) else (
    echo %GREEN%[INSTALLED]%RESET%
)
echo.

REM Check pre-commit
echo Checking pre-commit installation...
pre-commit --version 2>nul
if errorlevel 1 (
    echo %RED%[NOT INSTALLED] pre-commit%RESET%
    echo Install with: pip install pre-commit
) else (
    echo %GREEN%[INSTALLED]%RESET%
)
echo.

REM Check Python
echo Checking Python version...
python --version
echo.

REM Check git hooks
echo Checking git pre-commit hooks...
if exist ".git\hooks\pre-commit" (
    echo %GREEN%[INSTALLED] Git hooks are active%RESET%
) else (
    echo %YELLOW%[NOT INSTALLED] Git hooks not set up%RESET%
    echo Run option [7] to install
)
echo.

REM Check configuration files
echo Checking configuration files...
if exist "pyproject.toml" (
    echo %GREEN%[FOUND]%RESET% pyproject.toml
) else (
    echo %YELLOW%[MISSING]%RESET% pyproject.toml
)

if exist ".pre-commit-config.yaml" (
    echo %GREEN%[FOUND]%RESET% .pre-commit-config.yaml
) else (
    echo %YELLOW%[MISSING]%RESET% .pre-commit-config.yaml
)

if exist "fast_code_inspector.py" (
    echo %GREEN%[FOUND]%RESET% fast_code_inspector.py
) else (
    echo %YELLOW%[MISSING]%RESET% fast_code_inspector.py
)
echo.

echo %CYAN%============================================================================%RESET%
pause
goto MENU

REM ============================================================================
REM   EXIT
REM ============================================================================
:END
echo.
echo %GREEN%Thank you for using Hyper-Fast Code Inspector!%RESET%
echo.
timeout /t 2 >nul
exit /b 0
