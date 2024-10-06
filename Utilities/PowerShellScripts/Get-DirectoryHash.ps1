param (
    [Parameter(Mandatory = $true, Position = 0)]
    [String]$Directory
)

$fileCount = 0
$md5 = [System.Security.Cryptography.MD5]::Create()

function Update-Hash {
    param (
        [byte[]]$Data
    )
    $md5.TransformBlock($Data, 0, $Data.Length, $Data, 0) | Out-Null
}

function Add-FileHash {
    param (
        [string]$FilePath,
        [string]$BaseDirectory
    )
    $relativePath = $FilePath.Substring($BaseDirectory.Length).TrimStart("\\")
    $relativeBytes = [System.Text.Encoding]::UTF8.GetBytes($relativePath)
    
    $fileStream = [System.IO.File]::OpenRead($FilePath)
    $fileHash = $md5.ComputeHash($fileStream)
    $fileStream.Close()
    
    $colonBytes = [System.Text.Encoding]::UTF8.GetBytes(":")
    $semiColonBytes = [System.Text.Encoding]::UTF8.GetBytes(";")

    Update-Hash -Data $relativeBytes
    Update-Hash -Data $colonBytes
    Update-Hash -Data $fileHash
    Update-Hash -Data $semiColonBytes
}

if (-Not (Test-Path -PathType Container $Directory)) {
    Write-Error "$Directory is not a valid directory"
    exit 1
}

try {
    $files = Get-ChildItem -Recurse -File $Directory | Sort-Object -Property FullName
    foreach ($file in $files) {
        Add-FileHash -FilePath $file.FullName -BaseDirectory $Directory

        $fileCount = $fileCount + 1
        if (($fileCount % 1000) -eq 0) {
            Write-Host "$fileCount files hashed"
        }
    }
}
catch {
    Write-Error "Error while calculating directory hash: $($_.Exception.Message)"
    exit 1
}

$md5.TransformFinalBlock([byte[]]@(), 0, 0)
$finalHash = [BitConverter]::ToString($md5.Hash).Replace("-", "")
Write-Output $finalHash
