@echo off
REM Stop showing command lines in output

echo Building Docker image...
REM First attempt: normal Docker build using Dockerfile in current folder

docker build -t book_management .

REM Check if previous command failed
if %ERRORLEVEL% NEQ 0 (
    echo Docker build failed. Trying again without cache...

    REM Second attempt: build image without using cache
    REM This helps when dependency or layer issues happen
    docker build --no-cache -t book_management .

    REM Check again if build failed
    if %ERRORLEVEL% NEQ 0 (
        echo Docker build still failing.
        echo.
        echo Please check the following:
        echo 1. Docker Desktop is running
        echo 2. Internet connection is available
        echo 3. Try restarting Docker Desktop
        echo.
        echo If Docker does not work, you can run the project locally:
        echo pip install -r requirements.txt
        echo uvicorn app.main:app --reload --port 8000
        pause
        exit /b 1
    )
)

echo.
echo Docker image built successfully!
echo To run the container, use:
echo docker run -p 8000:8000 book_management
pause
