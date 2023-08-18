param (
    [string]$command
)

$iterations = 10
$totalTime = 0

for ($i = 1; $i -le $iterations; $i++) {
    $start = Get-Date
    Invoke-Expression $command
    $end = Get-Date
    $elapsedTime = ($end - $start).TotalMilliseconds
    $totalTime += $elapsedTime
}

$averageTime = $totalTime / $iterations

$filePath = Join-Path $PSScriptRoot "results.txt"
Add-Content -Path $filePath -Value ("Command: " + $command)
Add-Content -Path $filePath -Value ("Average Time: " + $averageTime.ToString() + " ms")
Add-Content -Path $filePath -Value ""

Write-Host "Results appended to $filePath"
