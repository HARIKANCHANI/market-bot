# PowerShell script to connect local repo to GitHub
# Remote repo: https://github.com/HARIKANCHANI/market-bot.git

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  CONNECTING LOCAL REPO TO GITHUB" -ForegroundColor Cyan
Write-Host "  Remote: https://github.com/HARIKANCHANI/market-bot.git" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if Git is initialized
Write-Host "Step 1: Checking Git initialization..." -ForegroundColor Yellow
if (Test-Path .git) {
    Write-Host "  ✅ Git is already initialized" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Git not initialized. Initializing now..." -ForegroundColor Yellow
    git init
    Write-Host "  ✅ Git initialized successfully" -ForegroundColor Green
}
Write-Host ""

# Step 2: Check current remote
Write-Host "Step 2: Checking current remote configuration..." -ForegroundColor Yellow
$remotes = git remote -v 2>&1
if ($remotes -match "origin") {
    Write-Host "  ⚠️  Remote 'origin' already exists:" -ForegroundColor Yellow
    git remote -v
    Write-Host ""
    Write-Host "  Removing old remote..." -ForegroundColor Yellow
    git remote remove origin
    Write-Host "  ✅ Old remote removed" -ForegroundColor Green
}
Write-Host ""

# Step 3: Add new remote
Write-Host "Step 3: Adding GitHub remote..." -ForegroundColor Yellow
git remote add origin https://github.com/HARIKANCHANI/market-bot.git
Write-Host "  ✅ Remote added successfully" -ForegroundColor Green
Write-Host ""

# Step 4: Verify remote
Write-Host "Step 4: Verifying remote configuration..." -ForegroundColor Yellow
git remote -v
Write-Host ""

# Step 5: Check for uncommitted changes
Write-Host "Step 5: Checking repository status..." -ForegroundColor Yellow
$status = git status --porcelain
if ($status) {
    Write-Host "  📝 Found uncommitted changes. Staging files..." -ForegroundColor Yellow
    
    # Stage all files
    git add .
    Write-Host "  ✅ Files staged" -ForegroundColor Green
    
    # Create commit
    Write-Host "  📝 Creating commit..." -ForegroundColor Yellow
    git commit -m "Initial commit: Market Bot - Indian Stock Intelligence Suite with comprehensive documentation"
    Write-Host "  ✅ Commit created" -ForegroundColor Green
} else {
    Write-Host "  ✅ No uncommitted changes" -ForegroundColor Green
}
Write-Host ""

# Step 6: Set branch to main
Write-Host "Step 6: Setting branch to 'main'..." -ForegroundColor Yellow
git branch -M main
Write-Host "  ✅ Branch set to 'main'" -ForegroundColor Green
Write-Host ""

# Step 7: Ready to push
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  ✅ REPOSITORY CONNECTED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Remote Configuration:" -ForegroundColor Yellow
git remote -v
Write-Host ""
Write-Host "🚀 Next Step: Push to GitHub" -ForegroundColor Yellow
Write-Host "   Run this command:" -ForegroundColor White
Write-Host ""
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "   You will be prompted for:" -ForegroundColor White
Write-Host "   • Username: HARIKANCHANI" -ForegroundColor White
Write-Host "   • Password: Your GitHub Personal Access Token" -ForegroundColor White
Write-Host ""
Write-Host "💡 Don't have a token?" -ForegroundColor Yellow
Write-Host "   1. Go to: https://github.com/settings/tokens" -ForegroundColor White
Write-Host "   2. Click 'Generate new token (classic)'" -ForegroundColor White
Write-Host "   3. Select 'repo' scope" -ForegroundColor White
Write-Host "   4. Copy the token and use it as password" -ForegroundColor White
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
