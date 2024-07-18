$statusLines = Invoke-Expression "git status --short" | ForEach-Object { $_.Trim() }
if ($statusLines.Length -eq 0) {
    Write-Host "ERROR`tNothing to commit"
    exit 1
}

Invoke-Expression "git commit -m 'Fake commit'"
Invoke-Expression "git log -n 1"
Invoke-Expression "git reset --soft HEAD~1"
