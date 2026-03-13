# Meeting Pipeline Setup Script for Windows
# Run this script to set up the integrated meeting pipeline

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 78) -ForegroundColor Cyan
Write-Host "  MEETING PIPELINE - AUTOMATED SETUP" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 78) -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   Python not found! Please install Python 3.8+" -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Install Python packages
Write-Host "`n[2/5] Installing Python dependencies..." -ForegroundColor Cyan
Write-Host "   This may take several minutes..." -ForegroundColor Yellow

try {
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    Write-Host "   Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "   Failed to install dependencies" -ForegroundColor Red
    Write-Host "   Try manually: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Check for .env file
Write-Host "`n[3/5] Checking environment configuration..." -ForegroundColor Cyan
if (Test-Path ".env") {
    Write-Host "   .env file found" -ForegroundColor Green
    
    # Check if GROQ_API_KEY is set
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "GROQ_API_KEY\s*=\s*\w+") {
        Write-Host "   GROQ_API_KEY is configured" -ForegroundColor Green
    } else {
        Write-Host "   GROQ_API_KEY not found in .env" -ForegroundColor Yellow
        Write-Host "   Please add: GROQ_API_KEY=your_key_here" -ForegroundColor Yellow
    }
} else {
    Write-Host "   .env file not found" -ForegroundColor Yellow
    Write-Host "   Creating .env template..." -ForegroundColor Yellow
    
    $envTemplate = @"
# Groq API Configuration
# Get your free API key from: https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here

# Optional: Uncomment and configure if needed
# MONGODB_URI=mongodb://localhost:27017/
# MONGODB_DATABASE=meeting_assistant
"@
    
    Set-Content -Path ".env" -Value $envTemplate
    Write-Host "   .env template created. Please edit it with your API key." -ForegroundColor Yellow
}

# Create data directories
Write-Host "`n[4/5] Creating data directories..." -ForegroundColor Cyan
$directories = @(
    "meeting_data",
    "meeting_data\images",
    "meeting_data\audio",
    "meeting_data\transcripts"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "   Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "   Exists: $dir" -ForegroundColor Gray
    }
}

# Run system test
Write-Host "`n[5/5] Running system test..." -ForegroundColor Cyan
Write-Host ""

try {
    python test_system.py
} catch {
    Write-Host "   Test script failed to run" -ForegroundColor Red
}

# Final instructions
Write-Host "`n" + ("=" * 80) -ForegroundColor Cyan
Write-Host "  SETUP COMPLETE" -ForegroundColor Green
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Ensure MongoDB is running (local or Atlas)" -ForegroundColor White
Write-Host "  2. Edit .env file with your Groq API key" -ForegroundColor White
Write-Host "  3. Update opencv/config.py with MongoDB connection string" -ForegroundColor White
Write-Host "  4. Run the pipeline: python run_pipeline.py" -ForegroundColor White
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  - Quick Start: QUICKSTART.md" -ForegroundColor White
Write-Host "  - Full Docs: README.md" -ForegroundColor White
Write-Host ""
Write-Host ("=" * 80) -ForegroundColor Cyan

# Offer to open documentation
$response = Read-Host "`nWould you like to open the Quick Start guide? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    if (Test-Path "QUICKSTART.md") {
        Start-Process "QUICKSTART.md"
    }
}

Write-Host "`nSetup script completed!" -ForegroundColor Green
