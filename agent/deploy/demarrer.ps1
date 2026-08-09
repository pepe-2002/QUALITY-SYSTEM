# ARA — démarrage en une commande, sous Windows.
#
# Ouvrir PowerShell et coller :
#
#     irm https://raw.githubusercontent.com/pepe-2002/QUALITY-SYSTEM/claude/ai-autonomous-research-creative-agent-0su1cb/agent/deploy/demarrer.ps1 | iex
#
# ou, si le dépôt est déjà sur la machine :
#
#     powershell -ExecutionPolicy Bypass -File agent\deploy\demarrer.ps1
#
# Aucune bibliothèque à installer : ARA n'a aucune dépendance obligatoire.
# Pas de pip, pas d'environnement virtuel, pas de compilateur.

$ErrorActionPreference = 'Stop'

$Depot   = 'https://github.com/pepe-2002/QUALITY-SYSTEM.git'
$Branche = 'claude/ai-autonomous-research-creative-agent-0su1cb'
$Port    = if ($env:ARA_PORT) { $env:ARA_PORT } else { '8800' }

# --- 1. Python ---------------------------------------------------------------
$Python = $null
foreach ($candidat in @('python', 'python3', 'py')) {
  $trouve = Get-Command $candidat -ErrorAction SilentlyContinue
  if ($trouve) {
    & $candidat -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>$null
    if ($LASTEXITCODE -eq 0) { $Python = $candidat; break }
  }
}
if (-not $Python) {
  Write-Host ''
  Write-Host '✕ Python 3.10 ou plus récent est nécessaire.' -ForegroundColor Red
  Write-Host '  Installez-le depuis le Microsoft Store (cherchez « Python »),'
  Write-Host "  ou avec :  winget install Python.Python.3.12"
  Write-Host '  Puis relancez cette commande.'
  return
}

# --- 2. Le code --------------------------------------------------------------
$Ici = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
if (Test-Path (Join-Path $Ici '..\ara\cli.py')) {
  $Racine = (Resolve-Path (Join-Path $Ici '..')).Path
  Write-Host "→ Code trouvé sur place : $Racine"
} else {
  $Base = Join-Path $HOME 'ara'
  if (Test-Path (Join-Path $Base '.git')) {
    Write-Host '→ Mise à jour du code…'
    git -C $Base fetch --quiet origin $Branche 2>$null
    git -C $Base checkout --quiet $Branche 2>$null
    git -C $Base pull --quiet origin $Branche 2>$null
  } else {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
      Write-Host '✕ git est nécessaire :  winget install Git.Git' -ForegroundColor Red
      return
    }
    Write-Host "→ Récupération du code dans $Base…"
    git clone --quiet --branch $Branche --depth 1 $Depot $Base
  }
  $Racine = Join-Path $Base 'agent'
}
Set-Location $Racine

# --- 3. Le jeton -------------------------------------------------------------
# Sans lui, quiconque atteint l'adresse pilote l'agent. Il est conservé pour
# que le lien enregistré sur le téléphone reste valable d'une fois sur l'autre.
$DossierTravail = Join-Path $Racine 'workspace'
$FichierJeton   = Join-Path $DossierTravail '.jeton'
if ($env:ARA_TOKEN) {
  $Jeton = $env:ARA_TOKEN
} elseif (Test-Path $FichierJeton) {
  $Jeton = (Get-Content $FichierJeton -Raw).Trim()
} else {
  $Jeton = & $Python -c 'import secrets; print(secrets.token_urlsafe(24))'
  New-Item -ItemType Directory -Force -Path $DossierTravail | Out-Null
  Set-Content -Path $FichierJeton -Value $Jeton -NoNewline
}
$env:ARA_TOKEN = $Jeton
if (-not $env:ARA_HOST) { $env:ARA_HOST = '127.0.0.1' }
$env:ARA_PORT = $Port

# --- 4. Le serveur -----------------------------------------------------------
$Journal = Join-Path $env:TEMP 'ara-serveur.log'
$Serveur = Start-Process -FilePath $Python -ArgumentList '-m', 'ara.cli', '--serve' `
  -RedirectStandardOutput $Journal -RedirectStandardError "$Journal.err" `
  -NoNewWindow -PassThru

$Adresse = "http://127.0.0.1:$Port/?token=$Jeton"
$Pret = $false
foreach ($essai in 1..30) {
  Start-Sleep -Milliseconds 500
  if ($Serveur.HasExited) { break }
  try {
    Invoke-WebRequest -Uri "http://127.0.0.1:$Port/api/health?token=$Jeton" `
      -UseBasicParsing -TimeoutSec 2 | Out-Null
    $Pret = $true
    break
  } catch { }
}

if (-not $Pret) {
  Write-Host '✕ ARA n''a pas démarré. Journal :' -ForegroundColor Red
  if (Test-Path $Journal) { Get-Content $Journal -Tail 20 }
  if (Test-Path "$Journal.err") { Get-Content "$Journal.err" -Tail 20 }
  return
}

Start-Process $Adresse

Write-Host ''
Write-Host '────────────────────────────────────────────────────────────────'
Write-Host '  ARA tourne. Ouvrez :'
Write-Host ''
Write-Host "  $Adresse" -ForegroundColor Green
Write-Host ''
Write-Host '  Essayez, par exemple :'
Write-Host '    · « Crée un site vitrine pour le marché couvert de Fomboni »'
Write-Host '    · « Fais-moi un flyer pour la traversée du samedi »'
Write-Host '    · « Quels sont les tarifs des traversées ? »'
Write-Host '────────────────────────────────────────────────────────────────'
Write-Host ''
Write-Host '  · Le jeton est conservé : le lien reste le même à chaque démarrage.'
Write-Host "  · L'agent n'écoute que sur cette machine ($($env:ARA_HOST))."
Write-Host '  · Fermez cette fenêtre pour arrêter.'
Write-Host "  · Journal : $Journal"
Write-Host ''
Write-Host '  Pour y accéder depuis le téléphone : voir deploy\tunnel\README.md'
Write-Host ''

Wait-Process -Id $Serveur.Id
