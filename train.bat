@echo off
setlocal enabledelayedexpansion
REM =====================================================================
REM Wicked Zerg Challenger - Integrated Training Control Center
REM =====================================================================
REM All-in-one batch file for system check, GPU verification, and training
REM =====================================================================

cd /d "%~dp0"

:INIT
call utils.bat set_sc2path >nul 2>&1

:MENU
cls
echo ====================================================================
echo   Wicked Zerg Challenger - Training Control Center
echo ====================================================================
echo.
echo   First Time Setup (Recommended for new users):
echo   99. First Time Setup Wizard (Run system check + install deps + GPU check)
echo.
echo   System Management:
echo   1. System Check (Check files, processes, Python, GPU, SC2PATH)
echo   2. Clean Processes (Kill all SC2 and training processes)
echo   3. GPU Verification (Check CUDA availability)
echo   9. Install Dependencies (Install required Python packages)
echo   10. Clean Logs (Remove old training log files)
echo   11. Set SC2PATH Manually (Set StarCraft II installation path)
echo.
echo   Training:
echo   4. Start Training - Maximum Speed (Hidden windows, fastest)
echo   5. Start Training - Visual Mode (Single instance, visible window)
echo   6. Start Training - Parallel Visual (Multiple instances, visible)
echo   7. Start Training - Timed (Auto-stop after hours)
echo   8. Stop All Training (Kill all training processes)
echo.
echo   Real-Time Code Monitor (Game Code Inspection):
echo   13. Start Real-Time Monitor (Background code inspection during game)
echo   14. Start Training + Monitor (Auto-start both training and monitor)
echo   15. Stop Real-Time Monitor (Stop background monitor)
echo.
echo   Quick Actions:
echo   12. Quick Start (System Check + Clean + GPU Check + Start Training)
echo.
echo   0. Exit
echo.
echo ====================================================================
if defined SC2PATH (
    echo   SC2PATH: %SC2PATH%
    if exist "%SC2PATH%" (
        echo   Status: [OK] Path exists
    ) else (
        echo   Status: [WARNING] Path does not exist! Use option 11 to fix
    )
) else (
    echo   SC2PATH: NOT SET (Auto-detection will run)
    echo   Status: Use option 11 to set manually if auto-detection fails
)
echo ====================================================================
set /p choice="Select option (0-15, 99): "

if "%choice%"=="1" goto SYSTEM_CHECK
if "%choice%"=="2" goto CLEAN_PROCESSES
if "%choice%"=="3" goto GPU_CHECK
if "%choice%"=="4" goto MAX_SPEED
if "%choice%"=="5" goto VISUAL_SINGLE
if "%choice%"=="6" goto VISUAL_PARALLEL
if "%choice%"=="7" goto TIMED_TRAIN
if "%choice%"=="8" goto STOP_ALL
if "%choice%"=="9" goto INSTALL_DEPS
if "%choice%"=="10" goto CLEAN_LOGS
if "%choice%"=="11" goto SET_SC2PATH
if "%choice%"=="12" goto QUICK_START
if "%choice%"=="13" goto START_MONITOR
if "%choice%"=="14" goto TRAIN_WITH_MONITOR
if "%choice%"=="15" goto STOP_MONITOR
if "%choice%"=="99" goto FIRST_TIME_SETUP
if "%choice%"=="0" goto END
goto MENU

:SYSTEM_CHECK
cls
echo ====================================================================
echo System Check
echo ====================================================================
echo.
call :SYSTEM_CHECK_INTERNAL
echo.
pause
goto MENU

:SYSTEM_CHECK_INTERNAL
REM Internal system check function (can be called from wizard)
echo.

REM Check 1: Required Python files
echo [1/6] Checking required Python files...
set "MISSING_FILES=0"

if exist "main_integrated.py" (
    echo     [OK] main_integrated.py found
) else (
    echo     [ERROR] main_integrated.py NOT FOUND (REQUIRED)
    set /a MISSING_FILES+=1
)

if exist "parallel_train_integrated.py" (
    echo     [OK] parallel_train_integrated.py found
) else (
    echo     [WARNING] parallel_train_integrated.py NOT FOUND
    echo     [INFO] Parallel training options 6 and 7 will not work
)

if exist "check_gpu.py" (
    echo     [OK] check_gpu.py found
) else (
    echo     [WARNING] check_gpu.py NOT FOUND
    echo     [INFO] GPU check option 3 will not work
)

if exist "early_defense_manager.py" (
    echo     [OK] early_defense_manager.py found
) else (
    echo     [WARNING] early_defense_manager.py NOT FOUND
    echo     [INFO] This is OK - the bot will use a dummy manager
)

echo.

REM Check 2: SC2PATH detection
echo [2/6] Checking StarCraft II installation path...
set "SC2PATH_FOUND=0"
if defined SC2PATH (
    if exist "%SC2PATH%" (
        echo     [OK] SC2PATH environment variable set: %SC2PATH%
        set "SC2PATH_FOUND=1"
    )
)
if "!SC2PATH_FOUND!"=="0" (
    if exist "C:\Program Files (x86)\StarCraft II" (
        echo     [OK] Found SC2 at default location: C:\Program Files (x86)\StarCraft II
        set "SC2PATH_FOUND=1"
    )
)
if "!SC2PATH_FOUND!"=="0" (
    if exist "C:\Program Files\StarCraft II" (
        echo     [OK] Found SC2 at: C:\Program Files\StarCraft II
        set "SC2PATH_FOUND=1"
    )
)
if "!SC2PATH_FOUND!"=="0" (
    echo     [WARNING] StarCraft II installation not found in common locations
    echo     [INFO] Use option 11 from main menu to set SC2PATH manually
    echo     [INFO] Example: D:\Games\StarCraft II
    echo     [INFO] Common locations checked:
    echo     [INFO]   - C:\Program Files (x86)\StarCraft II
    echo     [INFO]   - C:\Program Files\StarCraft II
    echo     [INFO]   - D:\Program Files (x86)\StarCraft II
    echo     [INFO]   - D:\Games\StarCraft II
)

echo.

REM Check 3: Running SC2 processes
echo [3/6] Checking for running SC2 processes...
tasklist /FI "IMAGENAME eq SC2_x64.exe" 2>nul | find /I "SC2_x64.exe" >nul
if %ERRORLEVEL% EQU 0 (
    echo     [WARNING] SC2_x64.exe processes are running
    echo     [INFO] Select option 2 to clean up before training
) else (
    echo     [OK] No SC2 processes running
)

echo.

REM Check 4: Python installation
echo [4/6] Checking Python installation...
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    python --version
    echo     [OK] Python is available
) else (
    echo     [ERROR] Python is not found in PATH
    echo     [INFO] Please install Python 3.10+ or add it to PATH
)

echo.

REM Check 5: GPU memory (nvidia-smi if available)
echo [5/6] Checking GPU memory (if NVIDIA GPU available)...
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader 2>nul
if %ERRORLEVEL% EQU 0 (
    echo     [OK] GPU information retrieved
    echo     [WARNING] For RTX 2060 (6GB), recommend NUM_INSTANCES=1 for safety
    echo     [WARNING] Multiple instances may cause VRAM Out of Memory errors
) else (
    echo     [INFO] nvidia-smi not available - not NVIDIA GPU or not installed
    echo     [INFO] Training will use CPU mode (slower)
)

echo.

REM Check 6: Python dependencies (basic check)
echo [6/6] Checking Python dependencies...
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    python -c "import sc2" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo     [OK] burnysc2 module found
    ) else (
        echo     [WARNING] burnysc2 module not found
        echo     [INFO] Run option 9 to install dependencies
    )
    
    python -c "import torch" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo     [OK] PyTorch module found
    ) else (
        echo     [WARNING] PyTorch module not found - neural network features disabled
    )
    
    python -c "from loguru import logger" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo     [OK] loguru module found
    ) else (
        echo     [WARNING] loguru module not found - will use standard logging
    )
) else (
    echo     [SKIP] Python not available, skipping dependency check
)

echo.
echo ====================================================================
echo System Check Complete
echo ====================================================================
echo.
if !MISSING_FILES! GTR 0 (
    echo [CRITICAL] Some required files are missing!
    echo Please ensure all required files are present before training.
    echo.
)
echo Recommendations:
echo - If early_defense_manager.py is missing: Bot will use dummy manager - OK
echo - If SC2 processes are running: Select option 2 to clean up
echo - For RTX 2060 (6GB): Use option 4 or 5 (single instance) to avoid VRAM issues
echo - If dependencies are missing: Select option 9 to install
echo.
exit /b 0

:FIRST_TIME_SETUP
cls
echo ====================================================================
echo   First Time Setup Wizard
echo ====================================================================
echo.
echo   This wizard will guide you through initial setup in order:
echo   1. System Check - Verify all files and configurations
echo   2. Install Dependencies - Install required Python packages
echo   3. GPU Verification - Check CUDA availability
echo.
echo   Recommended for new users or after fresh installation.
echo.
pause

REM Step 1: System Check
cls
echo ====================================================================
echo   Step 1/3: System Check
echo ====================================================================
echo.
call :SYSTEM_CHECK_INTERNAL
echo.
echo [INFO] System check completed. Review results above.
echo.
pause

REM Step 2: Install Dependencies
cls
echo ====================================================================
echo   Step 2/3: Install Dependencies
echo ====================================================================
echo.
call :INSTALL_DEPS_INTERNAL
echo.
echo [INFO] Dependency installation completed.
echo.
pause

REM Step 3: GPU Verification
cls
echo ====================================================================
echo   Step 3/3: GPU Verification
echo ====================================================================
echo.
call :GPU_CHECK_INTERNAL
echo.
echo [INFO] GPU verification completed.
echo.
pause

REM Summary
cls
echo ====================================================================
echo   First Time Setup Complete!
echo ====================================================================
echo.
echo   Setup Summary:
echo   [OK] System check completed
echo   [OK] Dependencies installation attempted
echo   [OK] GPU verification completed
echo.
echo   Next Steps:
echo   - If SC2PATH was not found, use option 11 to set it manually
echo   - If dependencies failed to install, check Python installation
echo   - You can now start training using options 4-7
echo.
echo   Ready to start training!
echo.
pause
goto MENU

:CLEAN_PROCESSES
cls
echo ====================================================================
echo Process Cleanup
echo ====================================================================
echo.
echo This will kill all SC2 and training processes...
echo.

REM Delegate process cleanup to shared utility which handles training and SC2 processes
call utils.bat stop_all

echo.
echo [INFO] Process cleanup complete!
echo.
pause
goto MENU

:GPU_CHECK
cls
echo ====================================================================
echo GPU Detection Check (Python 3.12)
echo ====================================================================
echo.
call :GPU_CHECK_INTERNAL
echo.
pause
goto MENU

:GPU_CHECK_INTERNAL
REM Internal GPU check function (can be called from wizard)
echo.

REM Check if check_gpu.py exists
if not exist "check_gpu.py" (
    echo [ERROR] check_gpu.py not found!
    echo [INFO] Skipping GPU check - will use available mode
    exit /b 1
)

REM Try py launcher first
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python launcher found - Trying Python 3.12 via py launcher
    py -3.12 check_gpu.py
    if %ERRORLEVEL% NEQ 0 (
        echo [WARNING] 'py -3.12' failed. Trying direct Python 3.12 executable...
        if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
            "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" check_gpu.py
        ) else (
            echo [WARNING] Python 3.12 not found, using default python...
            python check_gpu.py
        )
    )
) else (
    echo [WARNING] py launcher not found, trying direct path...
    if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
        "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" check_gpu.py
    ) else (
        echo [INFO] Python 3.12 not found in default location
        echo [INFO] Trying default python...
        python check_gpu.py
    )
)

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================================================
    echo GPU check completed successfully!
    echo ====================================================================
) else (
    echo.
    echo ====================================================================
    echo GPU check failed or CUDA not available
    echo ====================================================================
    echo [INFO] Training will continue in CPU mode if GPU is not available
)

exit /b 0

:MAX_SPEED
cls
echo ====================================================================
echo Training - Maximum Speed Mode
echo ====================================================================
echo.
echo This will start training with maximum speed (hidden windows).
echo Press Ctrl+C to stop.
echo.
echo Current directory: %CD%
echo.

REM Set environment variables
set SHOW_WINDOW=false
set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
call utils.bat set_sc2path >nul 2>&1
echo [INFO] SC2PATH: %SC2PATH%

REM Use Python 3.12 explicitly if available
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py -3.12 main_integrated.py
    if %ERRORLEVEL% NEQ 0 (
        if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
            "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" main_integrated.py
        ) else (
            python main_integrated.py
        )
    )
) else (
    python main_integrated.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to start training!
    echo Please check Python installation and dependencies.
    pause
)
goto MENU

:VISUAL_SINGLE
cls
echo ====================================================================
echo Training - Visual Mode (Single Instance)
echo ====================================================================
echo.
echo This will start ONE game instance with visible window.
echo Press Ctrl+C to stop.
echo.

REM Set environment variable to show window
set SHOW_WINDOW=true
set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
REM Ensure SC2PATH is set via shared utility
call utils.bat set_sc2path >nul 2>&1
echo [INFO] SC2PATH: %SC2PATH%

REM Run main_integrated.py with visual mode
call utils.bat set_sc2path >nul 2>&1
echo [INFO] SC2PATH: %SC2PATH%

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py -3.12 main_integrated.py
    if %ERRORLEVEL% NEQ 0 (
        if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
            "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" main_integrated.py
        ) else (
            python main_integrated.py
        )
    )
) else (
    python main_integrated.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to start training!
    pause
)
goto MENU

:VISUAL_PARALLEL
cls
echo ====================================================================
echo Training - Parallel Visual Mode
echo ====================================================================
echo.
echo Current directory: %CD%
echo WARNING: Showing windows will significantly reduce training speed!
echo This is useful for debugging and visual verification.
echo.
echo Press Ctrl+C to stop all instances.
echo.

REM Check if parallel_train_integrated.py exists
if not exist "parallel_train_integrated.py" (
    echo [ERROR] parallel_train_integrated.py not found!
    echo [INFO] Use option 5 for single instance visual mode instead.
    pause
    goto MENU
)

REM Set environment variables
set SHOW_WINDOW=true
set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
REM Ensure SC2PATH is set via shared utility
call utils.bat set_sc2path >nul 2>&1
echo [INFO] SC2PATH: %SC2PATH%
REM IMPORTANT: For RTX 2060 (6GB), keep NUM_INSTANCES=1 to avoid VRAM Out of Memory errors
set NUM_INSTANCES=1
call utils.bat set_sc2path >nul 2>&1
echo [INFO] SC2PATH: %SC2PATH%
echo [WARNING] For RTX 2060 (6GB), NUM_INSTANCES=1 to avoid VRAM Out of Memory

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py -3.12 parallel_train_integrated.py
    if %ERRORLEVEL% NEQ 0 (
        if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
            "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" parallel_train_integrated.py
        ) else (
            python parallel_train_integrated.py
        )
    )
) else (
    python parallel_train_integrated.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to start parallel training.
    echo Please check if Python is installed and in PATH.
    pause
)
goto MENU

:TIMED_TRAIN
cls
echo ====================================================================
echo Training - Timed Mode (Auto-stop)
echo ====================================================================
echo.

set /p HOURS="How many hours to train? (Enter whole number only): "
if "%HOURS%"=="" (
    echo [ERROR] No hours specified. Exiting.
    pause
    goto MENU
)

REM Validate numeric input and compute seconds
set /a SECONDS=%HOURS% * 3600 >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Invalid number of hours specified. Use whole numbers only.
    pause
    goto MENU
)

REM Prepare safe timestamp for log filename
call utils.bat timestamp >nul 2>&1

echo.
echo [INFO] Training will start now and stop after %HOURS% hours.
echo [INFO] Press Ctrl+C to stop manually before timeout.
echo.

REM Set environment variables
set SHOW_WINDOW=false
set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
REM Use auto-detected SC2PATH or default
if not defined SC2PATH (
    if exist "C:\Program Files (x86)\StarCraft II" (
        set "SC2PATH=C:\Program Files (x86)\StarCraft II"
    ) else if exist "C:\Program Files\StarCraft II" (
        set "SC2PATH=C:\Program Files\StarCraft II"
    ) else (
        set "SC2PATH=C:\Program Files (x86)\StarCraft II"
        echo [WARNING] SC2PATH not found, using default path
    )
)

REM Start training in background
call utils.bat set_sc2path >nul 2>&1
echo [INFO] Use option 8 to stop training manually if needed.
echo.

REM Start training with timeout wrapper
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py -3.12 run_with_timeout.py %SECONDS% main_integrated.py
    if %ERRORLEVEL% NEQ 0 (
        if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
            "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" run_with_timeout.py %SECONDS% main_integrated.py
        ) else (
            python run_with_timeout.py %SECONDS% main_integrated.py
        )
    )
) else (
    python run_with_timeout.py %SECONDS% main_integrated.py
)

echo.
echo ====================================================================
echo [TIMEOUT] Training time elapsed. Stopping all processes...
echo ====================================================================

REM Stop all training processes
call :STOP_ALL_INTERNAL

echo.
echo [INFO] All training processes have been stopped.
echo [INFO] Check training_log_*.txt for training output.
echo.
pause
goto MENU

:STOP_ALL
cls
echo ====================================================================
echo Stop All Training Processes
echo ====================================================================
echo.
echo This will terminate all Python training processes and SC2 processes...
echo.

call :STOP_ALL_INTERNAL

echo.
echo ====================================================================
echo [COMPLETE] Training stop process finished
echo ====================================================================
echo.
pause
goto MENU

:STOP_ALL_INTERNAL
REM Delegate process termination to shared Python utility or PowerShell fallback
call utils.bat stop_all
exit /b 0

:INSTALL_DEPS
cls
echo ====================================================================
echo Install Dependencies
echo ====================================================================
echo.
echo This will install all required Python packages from requirements.txt
echo.
call :INSTALL_DEPS_INTERNAL
echo.
pause
goto MENU

:INSTALL_DEPS_INTERNAL
REM Internal install dependencies function (can be called from wizard)
echo.
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found!
    echo [INFO] Creating requirements.txt with default packages...
    echo.
    echo # StarCraft 2 Bot Dependencies > requirements.txt
    echo burnysc2^>=1.0.0 >> requirements.txt
    echo numpy^>=1.20.0 >> requirements.txt
    echo torch^>=1.9.0 >> requirements.txt
    echo loguru^>=0.7.0 >> requirements.txt
    echo sc2reader^>=1.0.0 >> requirements.txt
    echo requests^>=2.25.0 >> requirements.txt
    echo python-dotenv^>=0.19.0 >> requirements.txt
    echo [OK] Created requirements.txt
    echo.
)

echo [INFO] Installing packages from requirements.txt...
echo.
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ====================================================================
        echo [OK] Dependencies installed successfully!
        echo ====================================================================
    ) else (
        echo.
        echo ====================================================================
        echo [ERROR] Some packages failed to install
        echo ====================================================================
        echo [INFO] Please check error messages above
    )
) else (
    echo [ERROR] Python is not found in PATH
    echo [INFO] Please install Python 3.10+ or add it to PATH
)
exit /b 0

:CLEAN_LOGS
cls
echo ====================================================================
echo Clean Log Files
echo ====================================================================
echo.
echo This will remove old training log files.
echo.
set /p CONFIRM="Delete all training_log_*.txt files? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Operation cancelled.
    pause
    goto MENU
)

set "LOG_COUNT=0"
if exist training_log_*.txt (
    for %%f in (training_log_*.txt) do (
        set /a LOG_COUNT+=1
        del /F /Q "%%f" >nul 2>&1
    )
)

if !LOG_COUNT! GTR 0 (
    echo [OK] Deleted !LOG_COUNT! log file(s)
) else (
    echo [INFO] No training log files found
)

REM Also clean logs directory if it exists and has files
if exist "logs\*.log" (
    echo.
    echo [INFO] Checking logs directory...
    for %%f in (logs\*.log) do (
        set /a LOG_COUNT+=1
        del /F /Q "%%f" >nul 2>&1
    )
    if !LOG_COUNT! GTR 0 (
        echo [OK] Also cleaned logs directory
    )
)

echo.
echo [INFO] Log cleanup complete!
echo.
pause
goto MENU

:SET_SC2PATH
cls
echo ====================================================================
echo Set SC2PATH Manually
echo ====================================================================
echo.
echo Current SC2PATH: 
if defined SC2PATH (
    echo   %SC2PATH%
    if exist "%SC2PATH%" (
        echo   [OK] Path exists
    ) else (
        echo   [WARNING] Path does not exist!
    )
) else (
    echo   NOT SET
)
echo.
echo Please enter the full path to your StarCraft II installation folder.
echo Example: C:\Program Files (x86)\StarCraft II
echo Example: D:\Games\StarCraft II
echo.
set /p NEW_SC2PATH="Enter SC2PATH (or press Enter to keep current): "

if not "%NEW_SC2PATH%"=="" (
    REM Remove trailing backslash if present
    if "%NEW_SC2PATH:~-1%"=="\" set "NEW_SC2PATH=%NEW_SC2PATH:~0,-1%"
    
    REM Check if path exists
    if exist "%NEW_SC2PATH%" (
        set "SC2PATH=%NEW_SC2PATH%"
        echo.
        echo [OK] SC2PATH set to: %SC2PATH%
        echo [INFO] This setting will be active for the current session
        echo [INFO] To make it permanent, set it as a system environment variable
    ) else (
        echo.
        echo [ERROR] Path does not exist: %NEW_SC2PATH%
        echo [INFO] Please verify the path and try again
        echo [INFO] Common locations to check:
        echo [INFO]   - C:\Program Files (x86)\StarCraft II
        echo [INFO]   - C:\Program Files\StarCraft II
        echo [INFO]   - D:\Program Files (x86)\StarCraft II
        echo [INFO]   - D:\Games\StarCraft II
    )
) else (
    echo.
    echo [INFO] SC2PATH unchanged
)

echo.
pause
goto MENU

:QUICK_START
cls
echo ====================================================================
echo Quick Start - Automated Setup and Training
echo ====================================================================
echo.
echo This will automatically run:
echo 1. System Check
echo 2. Clean Processes
echo 3. GPU Verification
echo 4. Start Training (Visual Mode)
echo.
pause

REM Step 1: System Check
cls
echo ====================================================================
echo [1/4] System Check
echo ====================================================================
call :SYSTEM_CHECK_INTERNAL
echo.
pause

REM Step 2: Clean Processes
cls
echo ====================================================================
echo [2/4] Clean Processes
echo ====================================================================
echo.
call utils.bat stop_all
echo.
echo [OK] Process cleanup complete!
pause

REM Step 3: GPU Check
cls
echo ====================================================================
echo [3/4] GPU Verification
echo ====================================================================
call :GPU_CHECK_INTERNAL
echo.
pause

REM Step 4: Start Training
cls
echo ====================================================================
echo [4/4] Starting Training (Visual Mode)
echo ====================================================================
echo.
echo Quick Start setup complete! Starting training now...
echo Press Ctrl+C to stop training at any time.
echo.
pause

REM Set environment and start training
set SHOW_WINDOW=true
set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
call utils.bat set_sc2path >nul 2>&1
echo [INFO] SC2PATH: %SC2PATH%

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py -3.12 main_integrated.py
    if %ERRORLEVEL% NEQ 0 (
        if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
            "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" main_integrated.py
        ) else (
            python main_integrated.py
        )
    )
) else (
    python main_integrated.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Training failed to start!
    pause
)
goto MENU

:START_MONITOR
cls
echo ====================================================================
echo Real-Time Code Monitor - Background Mode
echo ====================================================================
echo.
echo This will start the real-time code monitor in background.
echo The monitor will scan logs every 5 seconds for errors and
echo automatically generate fixes using Gemini API.
echo.
set /p DURATION="How long to monitor (hours, default 1)? "
if "%DURATION%"=="" set DURATION=1

REM Convert hours to seconds
set /a SECONDS=%DURATION% * 3600

echo.
echo [INFO] Starting real-time monitor for %DURATION% hour(s)...
echo [INFO] Monitor will run in background - you can close this window
echo [INFO] Use option 15 to stop the monitor manually
echo.

REM Check if realtime_code_monitor.py exists
if not exist "realtime_code_monitor.py" (
    echo [ERROR] realtime_code_monitor.py not found!
    echo [INFO] Please ensure the file exists in the project directory
    pause
    goto MENU
)

REM Check GEMINI_API_KEY
if not defined GEMINI_API_KEY (
    echo [WARNING] GEMINI_API_KEY not set!
    echo [INFO] Auto-fix will be disabled (error detection only)
    echo.
    set /p CONTINUE="Continue without auto-fix? (y/n): "
    if /i not "!CONTINUE!"=="y" (
        echo Operation cancelled.
        pause
        goto MENU
    )
)

REM Start monitor in background
echo [INFO] Starting monitor in background...
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    start /b py -3.12 realtime_code_monitor.py --file wicked_zerg_bot_pro.py --duration %SECONDS% > monitor_log.txt 2>&1
) else (
    start /b python realtime_code_monitor.py --file wicked_zerg_bot_pro.py --duration %SECONDS% > monitor_log.txt 2>&1
)

echo.
echo ====================================================================
echo [OK] Real-Time Monitor Started!
echo ====================================================================
echo.
echo Monitor is running in background and will:
echo - Scan logs every 5 seconds
echo - Detect errors automatically
echo - Generate fixes via Gemini API
echo - Save fixes to self_healing_logs/
echo.
echo Log file: monitor_log.txt
echo.
pause
goto MENU

:TRAIN_WITH_MONITOR
cls
echo ====================================================================
echo Training + Real-Time Monitor (Combined Mode)
echo ====================================================================
echo.
echo This will start BOTH:
echo 1. Training (Visual Mode)
echo 2. Real-Time Code Monitor (Background)
echo.
echo The monitor will detect errors during training and
echo automatically generate fixes.
echo.
pause

REM Check if realtime_code_monitor.py exists
if not exist "realtime_code_monitor.py" (
    echo [ERROR] realtime_code_monitor.py not found!
    echo [INFO] Starting training without monitor...
    pause
    goto VISUAL_SINGLE
)

REM Check GEMINI_API_KEY
if not defined GEMINI_API_KEY (
    echo [WARNING] GEMINI_API_KEY not set!
    echo [INFO] Monitor will detect errors but cannot auto-fix
    echo.
)

REM Start monitor in background first
echo [1/2] Starting real-time monitor in background...
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    start /b py -3.12 realtime_code_monitor.py --file wicked_zerg_bot_pro.py --duration 36000 > monitor_log.txt 2>&1
) else (
    start /b python realtime_code_monitor.py --file wicked_zerg_bot_pro.py --duration 36000 > monitor_log.txt 2>&1
)
timeout /t 2 /nobreak >nul
echo [OK] Monitor started

echo.
echo [2/2] Starting training (Visual Mode)...
echo Press Ctrl+C to stop both training and monitor
echo.

REM Set environment and start training
set SHOW_WINDOW=true
set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
call utils.bat set_sc2path >nul 2>&1
echo [INFO] SC2PATH: %SC2PATH%
echo.

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py -3.12 main_integrated.py
    if %ERRORLEVEL% NEQ 0 (
        if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
            "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" main_integrated.py
        ) else (
            python main_integrated.py
        )
    )
) else (
    python main_integrated.py
)

REM When training stops, stop monitor too
echo.
echo [INFO] Training stopped. Stopping monitor...
goto STOP_MONITOR

:STOP_MONITOR
cls
echo ====================================================================
echo Stop Real-Time Monitor
echo ====================================================================
echo.
echo This will stop all running real-time monitor processes...
echo.

REM Find and kill Python processes running realtime_code_monitor.py
echo [INFO] Looking for monitor processes...
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /C:"PID"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /C:"realtime_code_monitor.py" >nul
    if !ERRORLEVEL! EQU 0 (
        echo [INFO] Stopping monitor process (PID: %%a)
        taskkill /F /PID %%a >nul 2>&1
    )
)

echo.
echo [OK] Monitor stop complete!
echo.

REM Show monitor results if available
if exist "self_healing_logs\fix_*.json" (
    echo ====================================================================
    echo [INFO] Monitor Results Available
    echo ====================================================================
    echo The monitor generated fix files in self_healing_logs/
    dir /B /O-D self_healing_logs\fix_*.json 2>nul | findstr "fix_"
    echo.
    echo Review these files to see detected errors and suggested fixes.
    echo.
)

pause
goto MENU

:END
cls
echo.
echo Thank you for using Wicked Zerg Challenger Training Control Center!
echo.
exit /b 0
