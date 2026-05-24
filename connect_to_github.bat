@echo off
REM Batch script to connect local repo to GitHub
REM Remote repo: https://github.com/HARIKANCHANI/market-bot.git

echo ======================================================================
echo   CONNECTING LOCAL REPO TO GITHUB
echo   Remote: https://github.com/HARIKANCHANI/market-bot.git
echo ======================================================================
echo.

REM Step 1: Initialize Git if needed
echo Step 1: Initializing Git (if needed)...
if not exist .git (
    git init
    echo   [OK] Git initialized
) else (
    echo   [OK] Git already initialized
)
echo.

REM Step 2: Remove old remote if exists
echo Step 2: Checking for existing remote...
git remote remove origin 2>nul
echo   [OK] Ready for new remote
echo.

REM Step 3: Add GitHub remote
echo Step 3: Adding GitHub remote...
git remote add origin https://github.com/HARIKANCHANI/market-bot.git
echo   [OK] Remote added
echo.

REM Step 4: Verify remote
echo Step 4: Verifying remote configuration...
git remote -v
echo.

REM Step 5: Stage all files
echo Step 5: Staging files...
git add .
echo   [OK] Files staged
echo.

REM Step 6: Create commit
echo Step 6: Creating commit...
git commit -m "Initial commit: Market Bot - Indian Stock Intelligence Suite"
echo   [OK] Commit created
echo.

REM Step 7: Set branch to main
echo Step 7: Setting branch to main...
git branch -M main
echo   [OK] Branch set to main
echo.

echo ======================================================================
echo   SUCCESS! Repository connected to GitHub
echo ======================================================================
echo.
echo Next step: Push to GitHub
echo.
echo Run this command:
echo   git push -u origin main
echo.
echo You will need:
echo   Username: HARIKANCHANI
echo   Password: Your GitHub Personal Access Token
echo.
echo Get token at: https://github.com/settings/tokens
echo.
echo ======================================================================
pause
