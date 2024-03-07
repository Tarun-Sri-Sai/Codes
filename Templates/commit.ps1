# Get the lines from git status --short
$statusLines = git status --short | ForEach-Object { $_.Trim() }

# Exit if nothing to commit
if ($statusLines.Length -eq 0) {
    Write-Host "ERROR`tNothing to commit"
    exit 1
}

# Process each line
$fileNames = @()

$statusLines | ForEach-Object {
    # Split the line by space
    $lineParts = $_ -split ' '

    # Remove the first word
    $remainingWords = $lineParts[1..($lineParts.Count - 1)]

    # Join the remaining words
    $joinedWords = $remainingWords -join ' '
    $joinedWords = $joinedWords -replace '"', ''

    # Remove all letters before the last forward slash
    $fileName = $joinedWords -replace '.*/', ''

    $fileNames += if ($fileName.Length -gt 0) {
        $fileName
    } else {
        $joinedWords
    }
}

# Join the filenames with ','
$joinedFileNames = $fileNames -join ','

# Trim characters with ellipses if needed
$charLimit = 60
$trimmedFileNames = if ($joinedFileNames.Length -gt $charLimit) {
    $joinedFileNames.Substring(0, $charLimit - 3) + '...'
} else {
    $joinedFileNames
}
Write-Host "INFO`tCommit message: $trimmedFileNames"

# Stage all files
git add .
Write-Host "INFO`tgit add executed"

# Commit the changes
git commit -m $trimmedFileNames
Write-Host "INFO`tgit commit executed"
