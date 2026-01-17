@echo off
REM COIN:OPERATED JRPG - One-Click Windows Installer
REM Fully automated setup for Windows

title COIN:OPERATED - Installation Wizard
color 0D

echo.
echo ================================================================
echo.
echo              COIN:OPERATED JRPG
echo.
echo           Automated Installation Wizard
echo.
echo ================================================================
echo.
echo This installer will:
echo   - Check system requirements
echo   - Install dependencies automatically
echo   - Create desktop shortcut
echo   - Set up quick launch
echo.
echo Press any key to begin installation, or Ctrl+C to cancel
pause > nul

REM Check Python
echo.
echo [INFO] Checking Python installation...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python found

REM Check pip
echo.
echo [INFO] Checking pip installation...
python -m pip --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not installed!
    echo.
    echo Installing pip...
    python -m ensurepip --default-pip
)

echo [OK] pip is ready

REM Install dependencies
echo.
echo [INFO] Installing Python dependencies (this may take a minute)...
echo.

python -m pip install --upgrade pip > nul 2>&1
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies!
    echo.
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo [OK] Dependencies installed successfully

REM Verify pygame
echo.
echo [INFO] Verifying pygame installation...
python -c "import pygame" 2> nul
if %errorlevel% neq 0 (
    echo [WARNING] Pygame import failed, retrying...
    python -m pip install --force-reinstall pygame
)

python -c "import pygame"
if %errorlevel% neq 0 (
    echo [ERROR] Could not install pygame
    pause
    exit /b 1
)

echo [OK] Pygame is working

REM Verify Pillow
echo.
echo [INFO] Verifying Pillow installation...
python -c "from PIL import Image" 2> nul
if %errorlevel% neq 0 (
    echo [ERROR] Pillow installation failed
    pause
    exit /b 1
)

echo [OK] Pillow is working

REM Create launch script
echo.
echo [INFO] Creating quick launch script...

echo @echo off > play.bat
echo cd /d "%%~dp0" >> play.bat
echo python coin_operated.py >> play.bat

echo [OK] Quick launch script created (play.bat)

REM Create desktop shortcut
echo.
set /p CREATE_SHORTCUT="Would you like a desktop shortcut? (y/n): "

if /i "%CREATE_SHORTCUT%"=="y" (
    echo [INFO] Creating desktop shortcut...
    
    REM Use PowerShell to create shortcut
    powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\COIN-OPERATED.lnk'); $Shortcut.TargetPath = '%CD%\play.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.IconLocation = '%CD%\assets\icon.ico'; $Shortcut.Description = 'COIN:OPERATED JRPG - 16-bit Retro RPG'; $Shortcut.Save()"
    
    if %errorlevel% equ 0 (
        echo [OK] Desktop shortcut created
    ) else (
        echo [WARNING] Could not create desktop shortcut automatically
        echo You can manually create a shortcut to play.bat
    )
)

REM Success
echo.
echo ================================================================
echo.
echo              Installation Complete!
echo.
echo ================================================================
echo.
echo You can now launch COIN:OPERATED by:
echo.
echo   1. Double-clicking the Desktop Shortcut (if created)
echo   2. Double-clicking play.bat in this folder
echo   3. Running: python coin_operated.py
echo.
echo What to expect:
echo   - Beautiful splash screen with golden Coin logo
echo   - 16-bit retro JRPG graphics
echo   - Play as Coin - a mystical being made of enchanted coins
echo   - Pure GUI experience (no console window)
echo.
echo ================================================================
echo.

set /p LAUNCH_NOW="Would you like to launch the game now? (y/n): "

if /i "%LAUNCH_NOW%"=="y" (
    echo.
    echo [INFO] Launching COIN:OPERATED...
    timeout /t 1 > nul
    start "" python coin_operated.py
    echo.
    echo [OK] Game launched! Enjoy your journey from coin to goddess!
)

echo.
echo ================================================================
echo   From coin to goddess, from tool to deity
echo   A Universe Beyond the Universe
echo ================================================================
echo.
pause
