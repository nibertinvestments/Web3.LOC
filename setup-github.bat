@echo off
echo.
echo 🚀 Web3.LOC GitHub Pages Setup
echo =================================
echo.

REM Check if we're in the right directory
if not exist "docs\index.html" (
    echo ❌ Error: Please run this script from the Web3.LOC directory
    pause
    exit /b 1
)

echo 📋 Setup Instructions:
echo.
echo 1. CREATE GITHUB REPOSITORY:
echo    - Go to https://github.com/new
echo    - Repository name: Web3.LOC
echo    - Set to PUBLIC (required for free GitHub Pages)
echo    - Do NOT initialize with README, .gitignore, or license
echo    - Click 'Create repository'
echo.

echo 2. COPY YOUR REPOSITORY URL:
echo    - After creating, copy the HTTPS URL
echo    - It looks like: https://github.com/YOUR_USERNAME/Web3.LOC.git
echo.

echo 3. ENTER YOUR REPOSITORY URL:
set /p REPO_URL="Paste your GitHub repository URL here: "

if "%REPO_URL%"=="" (
    echo ❌ Error: Repository URL is required
    pause
    exit /b 1
)

echo.
echo 🔗 Adding remote repository...
git remote add origin "%REPO_URL%"

echo 📤 Pushing to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ SUCCESS! Code pushed to GitHub
    echo.
    echo 4. ENABLE GITHUB PAGES:
    echo    - Go to your repository on GitHub
    echo    - Click 'Settings' tab
    echo    - Scroll to 'Pages' in left sidebar
    echo    - Under 'Source' select 'GitHub Actions'
    echo    - Your site will deploy automatically!
    echo.
    echo 🌍 Your live site will be available at:
    for /f "tokens=1,2 delims=/" %%a in ("%REPO_URL%") do (
        for /f "tokens=1,2 delims=." %%c in ("%%b") do (
            echo    https://%%c.github.io/Web3.LOC/
        )
    )
    echo.
    echo 🎉 Deployment complete! Your Web3.LOC site is now live!
) else (
    echo.
    echo ❌ Error pushing to GitHub. Please check:
    echo    - Repository URL is correct
    echo    - You have push access to the repository
    echo    - Repository exists and is accessible
)

echo.
pause
