param (
    [Parameter(Mandatory=$true)]
    [string]$ZipFileName,

    [string[]]$Exclude,

    [Parameter(Mandatory=$true)]
    [string[]]$Directories,

    [Parameter(Mandatory=$true)]
    [string]$OneDriveDirectory,

    [int]$Versions = 5,

    [int]$CompressionLevel = 5
)

function Log-Message($Message) {
	Write-Host $Message
	Add-Content -Path "BackupTo-OneDrive.log" -Value "$(Get-Date) $Message"
}

Log-Message "ZipFileName: $ZipFileName."
Log-Message "Exclude: $($Exclude -join ', ')."
Log-Message "Directories: $($Directories -join ', ')."
Log-Message "OneDriveDirectory: $OneDriveDirectory."
Log-Message "Versions: $Versions."
Log-Message "CompressionLevel: $CompressionLevel."

if (Test-Path $ZipFileName) {
	Log-Message "Removing existing zip file: ${ZipFileName}."
	Remove-Item -Force $ZipFileName
} else {
	Log-Message "Zip file: ${ZipFileName} does not exist."
}	

foreach ($dir in $Directories) {
	Log-Message "Backing up directory: ${dir}."
}

if ($Exclude) {
	$excludeOptions = $Exclude | ForEach-Object { "-xr!`"$_`"" }
	$excludeOptions = $excludeOptions -join " "
	Log-Message "Parsed exclude options: $excludeOptions."
} else {
	$excludeOptions = ""
}

$directoryList = $Directories -join ' '
$date = Get-Date -Format "yyyyMMddHHmmss"
$zipFile = "${ZipFileName}_${date}.zip"
Log-Message "Compressing to file: $zipFile."
Invoke-Expression "7z a -mx=$CompressionLevel '$zipFile' $excludeOptions $directoryList" | Out-Null

Log-Message "Moving zip file to $OneDriveDirectory."
Move-Item -Force $zipFile "$OneDriveDirectory"

$files = Get-ChildItem -Path $OneDriveDirectory -Filter "${ZipFileName}_*.zip" | Sort-Object LastWriteTime
$filesCount = $files.Count

if ($filesCount -gt $Versions) {
    $filesToRemove = $files | Select-Object -First ($filesCount - $Versions)
    foreach ($file in $filesToRemove) {
        Log-Message "Removing old backup: $($file.FullName)"
        Remove-Item -Force $file.FullName
    }
}
