param (
    [Parameter(Mandatory=$true)]
    [string]$ZipFileName,

    [string[]]$Exclude,

    [Parameter(Mandatory=$true)]
    [string[]]$Directories,

    [Parameter(Mandatory=$true)]
    [string]$MountPath,

    [int]$Versions = 5,

    [int]$CompressionLevel = 5
)

function Write-LogMessage($Message) {
    Write-Host $Message
    Add-Content -Path "BackupTo-Mount.log" -Value "$(Get-Date) $Message"
}

$date = Get-Date -Format "yyyyMMddHHmmss"
$zipFile = "${ZipFileName}_${date}.zip"
if (Test-Path $zipFile) {
    Write-LogMessage "Removing existing zip file: ${zipFile}."
    Remove-Item -Force $zipFile
} else {
    Write-LogMessage "Zip file: ${zipFile} does not exist."
}

foreach ($dir in $Directories) {
    Write-LogMessage "Backing up directory: ${dir}."
}

if ($Exclude) {
    $excludeOptions = $Exclude | ForEach-Object { "-xr!`"$_`"" }
    $excludeOptions = $excludeOptions -join " "
    Write-LogMessage "Parsed exclude options: $excludeOptions."
} else {
    $excludeOptions = ""
}

$directoryList = $Directories -join ' '
Write-LogMessage "Compressing to file: $zipFile."
Invoke-Expression "7z a -mx=$CompressionLevel '$zipFile' $excludeOptions $directoryList" | Out-Null

Write-LogMessage "Moving zip file to $MountPath."
Move-Item -Force $zipFile "$MountPath"

$files = Get-ChildItem -Path $MountPath -Filter "${ZipFileName}_*.zip" | Sort-Object LastWriteTime
$filesCount = $files.Count

if (($Versions -gt 0) -and ($filesCount -gt $Versions)) {
    Write-LogMessage "Deleting last $($filesCount - $Versions) versions."
    $filesToRemove = $files | Select-Object -First ($filesCount - $Versions)
    foreach ($file in $filesToRemove) {
        Write-LogMessage "Removing old backup: $($file.FullName)."
        Remove-Item -Force $file.FullName
    }
}
