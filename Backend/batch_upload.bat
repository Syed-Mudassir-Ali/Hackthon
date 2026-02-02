@echo off
REM Batch upload script for 1400+ images
REM Usage: batch_upload.bat <image_directory> [chunk_size] [confidence]
REM Example: batch_upload.bat uploads/testing 100 0.25

setlocal enabledelayedexpansion

if "%1"=="" (
    echo.
    echo Usage: batch_upload.bat ^<image_directory^> [chunk_size] [confidence]
    echo Example: batch_upload.bat uploads/testing 100 0.25
    echo.
    echo This script uploads images in chunks to avoid request size limits.
    echo Default chunk size: 100 images per request
    echo.
    set /p image_dir="Enter path to images directory: "
) else (
    set "image_dir=%1"
)

if "!image_dir!"=="" (
    echo Error: No directory specified
    exit /b 1
)

set chunk_size=100
if not "%2"=="" set chunk_size=%2

set confidence=0.25
if not "%3"=="" set confidence=%3

echo.
echo Starting batch upload...
echo Image directory: !image_dir!
echo Chunk size: !chunk_size! images
echo Confidence threshold: !confidence!
echo.

python batch_upload.py "!image_dir!" !chunk_size! !confidence!

pause
