# Script PowerShell pour build automatique de Sécurité 360
# Compatible Windows PowerShell et PowerShell Core

Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "🛡️  BUILD SÉCURITÉ 360 - EXÉCUTABLE WINDOWS" -ForegroundColor Yellow
Write-Host "=" -ForegroundColor Cyan -NoNewline  
Write-Host ("=" * 59) -ForegroundColor Cyan

# Vérification de Python
Write-Host "`n📋 Vérification de Python..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python détecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    exit 1
}

# Vérification des fichiers requis
Write-Host "`n📁 Vérification des fichiers..." -ForegroundColor Blue
$requiredFiles = @("launcher.py", "app.py", "Securite360.spec", "icone.ico", "requirements.txt")

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file manquant" -ForegroundColor Red
        exit 1
    }
}

# Installation des dépendances
Write-Host "`n📦 Installation des dépendances..." -ForegroundColor Blue
Write-Host "Mise à jour de pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host "Installation de PyInstaller..." -ForegroundColor Yellow
python -m pip install pyinstaller==6.16.0

Write-Host "Installation des dépendances du projet..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

# Nettoyage des builds précédents
Write-Host "`n🧹 Nettoyage des builds précédents..." -ForegroundColor Blue
$dirsToClean = @("build", "dist", "__pycache__")

foreach ($dir in $dirsToClean) {
    if (Test-Path $dir) {
        Remove-Item -Recurse -Force $dir
        Write-Host "✅ Supprimé: $dir" -ForegroundColor Green
    }
}

# Nettoyage des caches Python
Get-ChildItem -Path . -Recurse -Name "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Recurse -Name "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue

# Build de l'exécutable
Write-Host "`n🔨 Création de l'exécutable..." -ForegroundColor Blue
Write-Host "Cela peut prendre plusieurs minutes..." -ForegroundColor Yellow

try {
    $buildProcess = Start-Process -FilePath "python" -ArgumentList "-m", "PyInstaller", "--clean", "--noconfirm", "Securite360.spec" -Wait -PassThru -NoNewWindow
    
    if ($buildProcess.ExitCode -eq 0) {
        Write-Host "✅ Build réussi !" -ForegroundColor Green
    } else {
        Write-Host "❌ Erreur lors du build (Code: $($buildProcess.ExitCode))" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Erreur lors du lancement de PyInstaller: $_" -ForegroundColor Red
    exit 1
}

# Vérification du résultat
Write-Host "`n🔍 Vérification du build..." -ForegroundColor Blue

if (Test-Path "dist\Securite360.exe") {
    $fileInfo = Get-Item "dist\Securite360.exe"
    $sizeMB = [math]::Round($fileInfo.Length / 1MB, 1)
    Write-Host "✅ Exécutable créé: dist\Securite360.exe" -ForegroundColor Green
    Write-Host "📏 Taille: $sizeMB MB" -ForegroundColor Cyan
    
    # Test rapide de l'exécutable
    Write-Host "`n🧪 Test rapide de l'exécutable..." -ForegroundColor Blue
    if ($fileInfo.Length -gt 50MB) {
        Write-Host "✅ Taille correcte pour un exécutable Streamlit" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Taille suspecte, vérifiez que tous les modules sont inclus" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Exécutable non trouvé dans dist\" -ForegroundColor Red
    exit 1
}

# Succès
Write-Host "`n🎉 BUILD TERMINÉ AVEC SUCCÈS !" -ForegroundColor Green -BackgroundColor DarkGreen
Write-Host "📁 L'exécutable se trouve dans: " -NoNewline -ForegroundColor Cyan
Write-Host "dist\Securite360.exe" -ForegroundColor Yellow

Write-Host "`n📋 Instructions d'utilisation:" -ForegroundColor Blue
Write-Host "1. Copiez dist\Securite360.exe où vous voulez" -ForegroundColor White
Write-Host "2. Double-cliquez pour lancer l'application" -ForegroundColor White  
Write-Host "3. Le splash screen apparaîtra pendant 3 secondes" -ForegroundColor White
Write-Host "4. Puis votre navigateur s'ouvrira automatiquement" -ForegroundColor White

Write-Host "`n✨ Aucune installation de Python n'est nécessaire !" -ForegroundColor Magenta

# Proposer d'ouvrir le dossier dist
Write-Host "`n📂 Voulez-vous ouvrir le dossier dist ? (O/N): " -NoNewline -ForegroundColor Yellow
$response = Read-Host

if ($response -match '^[OoYy]') {
    Start-Process explorer "dist"
}

Write-Host "`n✅ Script terminé avec succès !" -ForegroundColor Green