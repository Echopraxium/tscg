# Create New TSCG Poclet from Template
# Author: Echopraxium with the collaboration of Claude AI
# Date: 2026-04-18
# Usage: .\create_new_poclet.ps1 -Name "PocletName" -Domain "Physics" [-Label "Short Title"]

param(
    [Parameter(Mandatory=$true)]
    [string]$Name,
    
    [Parameter(Mandatory=$true)]
    [string]$Domain,
    
    [Parameter(Mandatory=$false)]
    [string]$Label = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Description = ""
)

# Configuration
$RepoRoot = "E:\_00_Michel\_00_Lab\_00_GitHub\tscg"
$PocletsDir = Join-Path $RepoRoot "instances\poclets"
$TemplateFile = Join-Path $RepoRoot "M0_POCLET_TEMPLATE.jsonld"
$Today = Get-Date -Format "yyyy-MM-dd"

# Validation
if (-not (Test-Path $RepoRoot)) {
    Write-Error "Repository not found at $RepoRoot"
    exit 1
}

if (-not (Test-Path $TemplateFile)) {
    Write-Error "Template file not found at $TemplateFile"
    Write-Host "Please ensure M0_POCLET_TEMPLATE.jsonld is in the repository root"
    exit 1
}

# Validate PascalCase naming
if ($Name -notmatch '^[A-Z][a-zA-Z0-9]*$') {
    Write-Warning "Poclet name should be in PascalCase (e.g., FireTriangle, FourStrokeEngine)"
    $confirm = Read-Host "Continue anyway? (y/n)"
    if ($confirm -ne 'y') {
        exit 0
    }
}

# Create poclet directory
$PocletDir = Join-Path $PocletsDir $Name
$PocletFile = Join-Path $PocletDir "M0_$Name.jsonld"

if (Test-Path $PocletDir) {
    Write-Error "Poclet directory already exists: $PocletDir"
    exit 1
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Creating New TSCG Poclet: $Name" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Create directory
Write-Host "Creating directory: $PocletDir" -ForegroundColor Yellow
New-Item -ItemType Directory -Path $PocletDir -Force | Out-Null

# Read template
Write-Host "Reading template from: $TemplateFile" -ForegroundColor Yellow
$template = Get-Content $TemplateFile -Raw -Encoding UTF8

# Set default label if not provided
if ([string]::IsNullOrEmpty($Label)) {
    $Label = "$Name - TODO: Add Short Descriptive Title"
}

# Set default description if not provided
if ([string]::IsNullOrEmpty($Description)) {
    $Description = "TODO: Add detailed description of the $Name poclet and its systemic properties. Explain what system/phenomenon is modeled and why it's a good TSCG candidate."
}

# Replace placeholders
Write-Host "Customizing template with poclet details..." -ForegroundColor Yellow

$content = $template
$content = $content -replace 'POCLET_NAME', $Name
$content = $content -replace 'Short Title', $Label
$content = $content -replace 'Detailed description of the poclet and its systemic properties\. Explain what system/phenomenon is modeled and why it''s a good TSCG candidate\.', $Description
$content = $content -replace 'DOMAIN_NAME', $Domain
$content = $content -replace '2026-04-18', $Today
$content = $content -replace 'Initial M0 poclet ontology with ASFID/REVOI bicephalous modeling', "Initial M0 poclet ontology for $Name"

# Write poclet file
Write-Host "Writing poclet file: $PocletFile" -ForegroundColor Yellow
[System.IO.File]::WriteAllText($PocletFile, $content, [System.Text.Encoding]::UTF8)

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "✓ Poclet created successfully!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "File: $PocletFile" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Open the file in your editor" -ForegroundColor White
Write-Host "  2. Complete the TODO sections:" -ForegroundColor White
Write-Host "     - Update rdfs:label if needed" -ForegroundColor Gray
Write-Host "     - Update rdfs:comment with full description" -ForegroundColor Gray
Write-Host "     - Calculate and fill ASFID scores" -ForegroundColor Gray
Write-Host "     - Calculate and fill REVOI scores" -ForegroundColor Gray
Write-Host "     - Calculate and fill m0:epistemicGap" -ForegroundColor Gray
Write-Host "     - Model m0:components" -ForegroundColor Gray
Write-Host "     - Model m0:interactions" -ForegroundColor Gray
Write-Host "  3. Validate with SHACL:" -ForegroundColor White
Write-Host "     pyshacl -s ontology\M0_Instances_Schema.shacl.ttl -df json-ld $PocletFile" -ForegroundColor Gray
Write-Host ""

# Ask if user wants to open the file
$openFile = Read-Host "Open file in default editor? (y/n)"
if ($openFile -eq 'y') {
    Start-Process $PocletFile
}

Write-Host ""
Write-Host "Happy modeling! 🚀" -ForegroundColor Cyan
