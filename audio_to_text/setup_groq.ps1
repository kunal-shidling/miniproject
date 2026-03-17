# Setup Script for Groq API Integration

Write-Host "=" -NoNewline
Write-Host ("=" * 69)
Write-Host "GROQ API SETUP FOR AUDIO SUMMARIZATION"
Write-Host "=" -NoNewline
Write-Host ("=" * 69)

Write-Host ""
Write-Host "This script will help you set up the Groq API for text summarization."
Write-Host ""

# Check if API key is already set
$existingKey = [System.Environment]::GetEnvironmentVariable('GROQ_API_KEY', 'User')

if ($existingKey) {
    Write-Host "✓ GROQ_API_KEY is already set!" -ForegroundColor Green
    Write-Host "  Current key: $($existingKey.Substring(0, 10))..." -ForegroundColor Gray
    Write-Host ""
    $update = Read-Host "Do you want to update it? (y/n)"
    if ($update -ne 'y') {
        Write-Host ""
        Write-Host "Setup complete! You're ready to use summarization." -ForegroundColor Green
        exit
    }
}

# Get API key
Write-Host ""
Write-Host "Step 1: Get your Groq API Key" -ForegroundColor Cyan
Write-Host "  1. Visit: https://console.groq.com/keys"
Write-Host "  2. Sign up or log in"
Write-Host "  3. Click 'Create API Key'"
Write-Host "  4. Copy your API key"
Write-Host ""

$apiKey = Read-Host "Paste your Groq API key here"

if ([string]::IsNullOrWhiteSpace($apiKey)) {
    Write-Host ""
    Write-Host "Error: No API key provided. Setup cancelled." -ForegroundColor Red
    exit
}

# Set environment variable permanently
Write-Host ""
Write-Host "Step 2: Setting up environment variable..." -ForegroundColor Cyan

try {
    [System.Environment]::SetEnvironmentVariable('GROQ_API_KEY', $apiKey, 'User')
    $env:GROQ_API_KEY = $apiKey
    
    Write-Host "✓ GROQ_API_KEY has been set!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Step 3: Install required packages" -ForegroundColor Cyan
    
    $install = Read-Host "Do you want to install/update the groq package? (y/n)"
    if ($install -eq 'y') {
        Write-Host "Installing groq package..." -ForegroundColor Yellow
        pip install groq --upgrade
    }
    
    Write-Host ""
    Write-Host "=" -NoNewline
    Write-Host ("=" * 69)
    Write-Host "SETUP COMPLETE! ✨" -ForegroundColor Green
    Write-Host "=" -NoNewline
    Write-Host ("=" * 69)
    Write-Host ""
    Write-Host "You can now use summarization features!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Quick Examples:" -ForegroundColor Cyan
    Write-Host "  python cli_transcribe.py meeting.mp3 --summarize"
    Write-Host "  python cli_transcribe.py talk.wav --summarize --structured-summary"
    Write-Host "  python example_with_summary.py audio.mp3"
    Write-Host ""
    Write-Host "Note: You may need to restart your terminal for changes to take effect." -ForegroundColor Yellow
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "Error: Failed to set environment variable." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Set it manually for this session:" -ForegroundColor Yellow
    Write-Host "  `$env:GROQ_API_KEY = '$apiKey'"
    Write-Host ""
}
