# Frontend Setup Script for Windows PowerShell
# This script initializes the React + Vite frontend with TailwindCSS

Write-Host "Setting up React + Vite Frontend..." -ForegroundColor Green

# Navigate to project root
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

# Create frontend with Vite
Write-Host "`nCreating Vite React project..." -ForegroundColor Yellow
npm create vite@latest frontend -- --template react

# Navigate to frontend directory
Set-Location frontend

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
npm install

# Install additional packages
Write-Host "`nInstalling additional packages..." -ForegroundColor Yellow
npm install react-router-dom axios recharts
npm install -D tailwindcss postcss autoprefixer
npm install lucide-react

# Initialize TailwindCSS
Write-Host "`nInitializing TailwindCSS..." -ForegroundColor Yellow
npx tailwindcss init -p

Write-Host "`n✅ Frontend setup complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Update tailwind.config.js with content paths" -ForegroundColor White
Write-Host "2. Add Tailwind directives to src/index.css" -ForegroundColor White
Write-Host "3. Create components and pages" -ForegroundColor White
Write-Host "4. Run 'npm run dev' to start development server" -ForegroundColor White
