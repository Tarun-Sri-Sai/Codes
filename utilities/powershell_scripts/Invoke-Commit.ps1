# Stage all files
git add -A
Write-Host "INFO`tgit add executed"

# Get status
$statusLines = git status --short | ForEach-Object { $_.Trim() }
if ($statusLines.Length -eq 0) {
    Write-Host "ERROR`tNothing to commit"
    exit 1
}

# Extract file names with their status
$fileStatuses = @()
$statusLines | ForEach-Object {
    # Extract status and file path
    $status = $_.Substring(0, 2).Trim()
    $filePath = $_.Substring(2).Trim()

    # Remove quotes from the file path
    $filePath = $filePath -replace '"', ''

    # Remove leading directory path to get just the file name
    $fileName = $filePath -replace '^.*/', ''

    # Add status and file name to the list
    if ($fileName.Length -gt 0) {
        $fileStatuses += "$status $fileName"
    } else {
        $fileStatuses += "$status $filePath"
    }
}

# Prepare commit message with the changed file names and their statuses
$joinedFileStatuses = $fileStatuses -join ', '
$charLimit = 260
$trimmedFileStatuses = if ($joinedFileStatuses.Length -gt $charLimit) {
    $joinedFileStatuses.Substring(0, $charLimit - 3) + '...'
} else {
    $joinedFileStatuses
}
Write-Host "INFO`tCommit message: $trimmedFileStatuses"

# Commit the changes
git commit -m $trimmedFileStatuses
Write-Host "INFO`tgit commit executed"
