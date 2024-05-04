# Get status
$statusLines = git status --short | foreach-object { $_.trim() }
if ($statusLines.length -eq 0) {
    write-host "ERROR`tNothing to commit"
    exit 1
}

# Extract file names
$fileNames = [system.collections.generic.hashset[string]]::new()
$statusLines | foreach-object {
    # Extract file paths
    $lineParts = $_ -split ' '
    $remainingWords = $lineParts[1..($lineParts.count - 1)]

    # Remove quotes
    $joinedWords = $remainingWords -join ' '
    $joinedWords = $joinedWords -replace '"', ''

    # Remove leading directory path
    $fileName = $joinedWords -replace '.*/', ''
    if ($fileName.length -gt 0) {
        $fileNames.add($fileName) | out-null
    } else {
        $fileNames.add($joinedWords) | out-null
    }
}

# Prepare commit message with the changed file names
$joinedFileNames = $fileNames -join ','
$charLimit = 72
$trimmedFileNames = if ($joinedFileNames.length -gt $charLimit) {
    $joinedFileNames.substring(0, $charLimit - 3) + '...'
} else {
    $joinedFileNames
}
write-host "INFO`tCommit message: $trimmedFileNames"

# Stage all files
git add .
write-host "INFO`tgit add executed"

# Commit the changes
git commit -m $trimmedFileNames
write-host "INFO`tgit commit executed"
