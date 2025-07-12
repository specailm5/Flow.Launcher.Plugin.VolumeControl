@echo off
REM Install Flow Launcher Volume Control Plugin - Simplified Version
REM This script copies the plugin to Flow Launcher's plugins directory and restarts Flow Launcher

echo ========================================
echo Flow Launcher Volume Control Plugin
echo Installation Script (Simplified)
echo ========================================
echo.

REM Install pyflowlauncher dependency
echo Installing pyflowlauncher dependency...
pip install pyflowlauncher[all]
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install pyflowlauncher dependency
    pause
    exit /b 1
)
echo pyflowlauncher installed successfully!
echo.

REM Set plugin name
set "PLUGIN_NAME=Flow.Launcher.Plugin.VolumeControl"

REM Set hardcoded paths for most common installation
set "FL_PATH=%LOCALAPPDATA%\FlowLauncher"
set "PLUGINS_DIR=%LOCALAPPDATA%\FlowLauncher\app-1.20.1\Plugins"

echo Using Flow Launcher path: %FL_PATH%
echo Using Plugins directory: %PLUGINS_DIR%
echo.

REM Check if plugins directory exists
if not exist "%PLUGINS_DIR%" (
    echo Error: Plugins directory not found at %PLUGINS_DIR%
    echo.
    echo Please manually enter your Flow Launcher plugins directory:
    echo Example: C:\Users\%USERNAME%\AppData\Local\FlowLauncher\app-1.20.1\Plugins
    set /p "PLUGINS_DIR=Plugins directory path: "
    
    if not exist "%PLUGINS_DIR%" (
        echo Error: The specified plugins directory does not exist.
        pause
        exit /b 1
    )
)

REM Stop Flow Launcher if running
echo Stopping Flow Launcher...
taskkill /f /im "Flow.Launcher.exe" >nul 2>&1
taskkill /f /im "FlowLauncher.exe" >nul 2>&1
timeout /t 2 >nul

REM Create plugin directory
set "PLUGIN_DIR=%PLUGINS_DIR%\%PLUGIN_NAME%"
if exist "%PLUGIN_DIR%" (
    echo Removing existing plugin installation...
    rmdir /s /q "%PLUGIN_DIR%"
)

echo Creating plugin directory...
mkdir "%PLUGIN_DIR%"
mkdir "%PLUGIN_DIR%\Images"

REM Copy essential plugin files
echo Copying plugin files...
copy "vol_control.exe" "%PLUGIN_DIR%\" >nul
copy "main.py" "%PLUGIN_DIR%\" >nul
copy "plugin.json" "%PLUGIN_DIR%\" >nul


REM Copy icon if it exists
if exist "Images\icon.png" (
    copy "Images\icon.png" "%PLUGIN_DIR%\Images\" >nul
    echo Icon copied successfully.
) else (
    copy "Images\icon_placeholder.txt" "%PLUGIN_DIR%\Images\" >nul
    echo No icon found - placeholder copied.
)

echo.
echo ========================================
echo Plugin installed successfully!
echo Location: %PLUGIN_DIR%
echo ========================================
echo.

REM Try to start Flow Launcher
echo Starting Flow Launcher...
set "FL_EXE=%FL_PATH%\app-1.20.1\Flow.Launcher.exe"

if exist "%FL_EXE%" (
    start "" "%FL_EXE%"
    echo Flow Launcher started!
    echo.
    echo Plugin is ready to use!
    echo Type 'vol' in Flow Launcher to test the volume control.
) else (
    echo Could not find Flow Launcher executable at %FL_EXE%
    echo Please start Flow Launcher manually.
)

echo.
echo Installation complete!
pause
