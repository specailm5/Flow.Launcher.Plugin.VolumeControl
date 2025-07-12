#!/bin/bash

# Build script for Flow Launcher Rust Volume Control Plugin
# This script builds the Rust executable and copies it to the correct location

echo "Building Rust Volume Control Plugin..."


if [ ! -d "rust_source" ]; then
    echo "Error: rust_source directory not found. Make sure you're in the plugin root directory."
    exit 1
fi


cd rust_source

echo "Compiling Rust executable..."
cargo build --release


if [ $? -eq 0 ]; then
    echo "Build successful!"
    
   
    if [ -f "target/release/vol_control.exe" ]; then
        cp target/release/vol_control.exe ../vol_control.exe
        echo "Copied vol_control.exe to plugin directory."
        echo "Plugin is ready to use!"
    else
        echo "Error: vol_control.exe not found in target/release/"
        exit 1
    fi
else
    echo "Build failed!"
    exit 1
fi

cd ..
