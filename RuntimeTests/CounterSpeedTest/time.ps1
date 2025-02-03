gcc counter.c -o counter_c
g++ counter.cpp -o counter_cpp

$commands = @(
    "./counter_c.exe",
    "./counter_cpp.exe",
    "java Counter.java",
    "python counter.py"
)

$iterations = 10
$totalTime = @{}

$filePath = Join-Path $PSScriptRoot "results.txt"
if (Test-Path $filePath) {
    Remove-Item -Path $filePath -Force
}

foreach ($command in $commands) {
    $commandKey = $command -replace "[^a-zA-Z]", ""  # Extracting alphanumeric characters for command name
    $totalTime[$commandKey] = 0

    for ($i = 1; $i -le $iterations; $i++) {
        $start = Get-Date
        Invoke-Expression $command
        $end = Get-Date
        $elapsedTime = ($end - $start).TotalMilliseconds
        $totalTime[$commandKey] += $elapsedTime
    }

    $averageTime = $totalTime[$commandKey] / $iterations

    $filePath = Join-Path $PSScriptRoot "results.txt"
    Add-Content -Path $filePath -Value ("Command: " + $command)
    Add-Content -Path $filePath -Value ("Average Time: " + $averageTime.ToString() + " ms")
    Add-Content -Path $filePath -Value ""
}

Write-Host "Results appended to $filePath"
