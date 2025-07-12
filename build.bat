@echo off
REM Build script for Flow Launcher Rust Volume Control Plugin
REM This script builds the Rust executable and copies it to the correct location

echo Building Rust Volume Control Plugin...

REM Check if we're in the right directory
if not exist "rust_source" (
    echo Error: rust_source directory not found. Make sure you're in the plugin root directory.
    pause
    exit /b 1
)

REM Navigate to rust source directory
cd rust_source

echo Compiling Rust executable...
cargo build --release

REM Check if build was successful
if %ERRORLEVEL% equ 0 (
    echo Build successful!
    
    REM Copy the executable to the plugin root
    if exist "target\release\vol_control.exe" (
        copy "target\release\vol_control.exe" "..\vol_control.exe"
        echo Copied vol_control.exe to plugin directory.
        echo Plugin is ready to use!
    ) else (
        echo Error: vol_control.exe not found in target\release\
        pause
        exit /b 1
    )
) else (
    echo Build failed!
    pause
    exit /b 1
)

cd ..
pause
