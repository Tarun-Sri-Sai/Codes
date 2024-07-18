param (
    [string]$filename
)

Get-Content $filename | Sort-Object | Out-File $filename
