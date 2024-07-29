# Get status
$statusLines = git status --short | ForEach-Object { $_.Trim() }
if ($statusLines.Length -eq 0) {
    Write-Host "ERROR`tNothing to commit"
    exit 1
}

# Extract file names
$fileNames = [System.Collections.Generic.HashSet[string]]::new()
$statusLines | ForEach-Object {
    # Extract file paths
    $lineParts = $_ -split ' '
    $remainingWords = $lineParts[1..($lineParts.Count - 1)]

    # Remove quotes
    $joinedWords = $remainingWords -join ' '
    $joinedWords = $joinedWords -replace '"', ''

    # Remove leading directory path
    $fileName = $joinedWords -replace '.*/', ''
    if ($fileName.Length -gt 0) {
        $fileNames.Add($fileName) | Out-Null
    } else {
        $fileNames.Add($joinedWords) | Out-Null
    }
}

# Prepare commit message with the changed file names
$joinedFileNames = $fileNames -join ','
$charLimit = 260
$trimmedFileNames = if ($joinedFileNames.Length -gt $charLimit) {
    $joinedFileNames.Substring(0, $charLimit - 3) + '...'
} else {
    $joinedFileNames
}
Write-Host "INFO`tCommit message: $trimmedFileNames"

# Stage all files
git add -A
Write-Host "INFO`tgit add executed"

# Commit the changes
git commit -m $trimmedFileNames
Write-Host "INFO`tgit commit executed"
