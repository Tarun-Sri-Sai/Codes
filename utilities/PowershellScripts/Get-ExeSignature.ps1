param (
    [parameter(Mandatory=$true, Position=0)]
    [string]$folderPath
)

Get-ChildItem -Path $folderPath -Filter *.exe | ForEach-Object {
    $filePath = $_.FullName
    $certificateStatus = (Get-AuthenticodeSignature $filePath).Status
    $outputString = "{0,-75}Status: {1}" -f $_, $certificateStatus
    Write-Host $outputString
}
