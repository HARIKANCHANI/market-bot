# Documentation Reorganization Script
# This script moves all documentation files to their proper locations

Write-Host "🧹 Starting Documentation Reorganization..." -ForegroundColor Cyan
Write-Host ""

# Create directory structure
$dirs = @(
    "docs/getting-started",
    "docs/guides/bot-usage",
    "docs/guides/features",
    "docs/guides/testing",
    "docs/architecture/diagrams",
    "docs/technical",
    "docs/optimization",
    "docs/deployment",
    "docs/maintenance",
    "docs/reports/audits",
    "docs/reports/test-runs",
    "docs/reports/verification",
    "docs/reference"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✅ Created: $dir" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "📁 Moving files to proper locations..." -ForegroundColor Cyan
Write-Host ""

# Define file movements (source -> destination)
$movements = @{
    # Optimization docs
    "OPTIMIZATION_COMPLETE_SUMMARY.md" = "docs/optimization/OPTIMIZATION_COMPLETE_SUMMARY.md"
    "OPTIMIZATION_IMPLEMENTATION_STATUS.md" = "docs/optimization/OPTIMIZATION_IMPLEMENTATION_STATUS.md"
    "PARALLEL_PROCESSING_OPTIMIZATION.md" = "docs/optimization/PARALLEL_PROCESSING.md"
    "AI_BOTS_COMPLETE_OPTIMIZATION_SUMMARY.md" = "docs/optimization/AI_BOTS_OPTIMIZATION_SUMMARY.md"
    "AI_BOTS_OPTIMIZATION_PLAN.md" = "docs/optimization/AI_BOTS_OPTIMIZATION_PLAN.md"
    
    # Deployment docs
    "CREDENTIALS_MIGRATION_COMPLETE.md" = "docs/deployment/CREDENTIALS_MIGRATION_COMPLETE.md"
    "CREDENTIALS_MIGRATION_GUIDE.md" = "docs/deployment/CREDENTIALS_MIGRATION_GUIDE.md"
    "GITHUB_ACTIONS_CACHE_OPTIMIZATION.md" = "docs/deployment/GITHUB_ACTIONS_CACHE_OPTIMIZATION.md"
    "GITHUB_ACTIONS_GUIDE.md" = "docs/deployment/GITHUB_ACTIONS_GUIDE.md"
    "GITHUB_PUSH_QUICK_GUIDE.md" = "docs/deployment/GITHUB_PUSH_QUICK_GUIDE.md"
    "GITHUB_WORKFLOWS_COMPLETE.md" = "docs/deployment/GITHUB_WORKFLOWS_COMPLETE.md"
    "HOW_TO_PUSH_TO_GITHUB.md" = "docs/deployment/HOW_TO_PUSH_TO_GITHUB.md"
    "PUSH_TO_GITHUB_NOW.md" = "docs/deployment/PUSH_TO_GITHUB_NOW.md"
    
    # Maintenance docs
    "DEPENDENCY_AUDIT_COMPLETE.md" = "docs/maintenance/DEPENDENCY_AUDIT_COMPLETE.md"
    "DEPENDENCY_AUDIT_REPORT.md" = "docs/maintenance/DEPENDENCY_AUDIT_REPORT.md"
    "DEPENDENCY_VERSION_ANALYSIS.md" = "docs/maintenance/DEPENDENCY_VERSION_ANALYSIS.md"
    "LINK_AUDIT_COMPLETE.md" = "docs/maintenance/LINK_AUDIT_COMPLETE.md"
    
    # Bot guides
    "INCREMENTAL_BOTS_COMPLETE.md" = "docs/guides/bot-usage/INCREMENTAL_BOTS_COMPLETE.md"
    "INCREMENTAL_BOTS_FIX_ANALYST_RATINGS.md" = "docs/guides/bot-usage/INCREMENTAL_BOTS_FIX_ANALYST_RATINGS.md"
    "INCREMENTAL_BOTS_GUIDE.md" = "docs/guides/bot-usage/INCREMENTAL_BOTS_GUIDE.md"
    "FULL_BOTS_FIX_ANALYST_RATINGS.md" = "docs/guides/bot-usage/FULL_BOTS_FIX_ANALYST_RATINGS.md"
    "README_EXCEL_VERSION.md" = "docs/guides/bot-usage/EXCEL_BOT_GUIDE.md"
    "EMOJI_SUPPORT_GUIDE.md" = "docs/guides/features/EMOJI_SUPPORT_GUIDE.md"
    
    # Feature guides
    "PRODUCTION_TICKER_MAPPING_SYSTEM.md" = "docs/guides/features/TICKER_MAPPING_SYSTEM.md"
    "PRODUCTION_TICKER_SYSTEM.md" = "docs/guides/features/TICKER_SYSTEM.md"
    "SECTOR_MAPPING_REFERENCE.md" = "docs/reference/SECTOR_MAPPING_REFERENCE.md"
    "SECTOR_MAPPING_QUICK_REFERENCE.md" = "docs/reference/SECTOR_MAPPING_QUICK_REFERENCE.md"
    "SECTOR_VALIDATION_FIX.md" = "docs/guides/features/SECTOR_VALIDATION.md"
    "TICKER_MAPPING_QUICK_REFERENCE.md" = "docs/reference/TICKER_MAPPING_QUICK_REFERENCE.md"
    "TREND_LOGIC_WITH_VOLUME.md" = "docs/guides/features/TREND_LOGIC.md"
    "ULTRA_SAFE_SYSTEM_COMPLETE.md" = "docs/guides/features/ULTRA_SAFE_SYSTEM.md"
    
    # Testing
    "TEST_SINGLE_STOCK_GUIDE.md" = "docs/guides/testing/TEST_SINGLE_STOCK_GUIDE.md"
    
    # Architecture
    "ARCHITECTURE_DIAGRAMS_MERMAID.md" = "docs/architecture/ARCHITECTURE_DIAGRAMS_MERMAID.md"
    
    # Reference
    "QUICK_REFERENCE.md" = "docs/reference/QUICK_REFERENCE.md"
    "QUICK_START_GUIDE.md" = "docs/getting-started/QUICK_START.md"
    
    # Technical docs
    "COMPLETE_PYTHON_FILES_DOCUMENTATION.md" = "docs/technical/CODE_DOCUMENTATION.md"
    
    # Reports
    "COMPLETE_AUDIT_SUMMARY.md" = "docs/reports/audits/COMPLETE_AUDIT_SUMMARY.md"
    "STOCK_LIST_CLEANUP_REPORT.md" = "docs/reports/audits/STOCK_LIST_CLEANUP_REPORT.md"
    
    # Documentation meta
    "NEW_DOCUMENTATION_COMPLETE.md" = "docs/reports/NEW_DOCUMENTATION_COMPLETE.md"
    
    # Diagram generation
    "GENERATE_IMAGES_README.md" = "docs/architecture/GENERATE_IMAGES_README.md"
    "HOW_TO_GENERATE_DIAGRAM_IMAGES.md" = "docs/architecture/HOW_TO_GENERATE_DIAGRAM_IMAGES.md"
}

# Move files
$movedCount = 0
$skippedCount = 0

foreach ($source in $movements.Keys) {
    if (Test-Path $source) {
        $dest = $movements[$source]
        Move-Item -Path $source -Destination $dest -Force
        Write-Host "  ✅ Moved: $source -> $dest" -ForegroundColor Green
        $movedCount++
    } else {
        Write-Host "  ⚠️  Not found: $source" -ForegroundColor Yellow
        $skippedCount++
    }
}

Write-Host ""
Write-Host "✅ Reorganization complete!" -ForegroundColor Green
Write-Host "  📦 Files moved: $movedCount" -ForegroundColor Cyan
Write-Host "  ⚠️  Files skipped: $skippedCount" -ForegroundColor Yellow
