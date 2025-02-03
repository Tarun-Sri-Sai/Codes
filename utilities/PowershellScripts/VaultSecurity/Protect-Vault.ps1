param (
    [String]$Vault = "Vault",
    [String]$PasswordFile = "password.txt"
)

function Get-PasswordFromFile {
    if (-Not (Test-Path -Type Leaf $PasswordFile)) {
        Write-Host "$PasswordFile password file does not exist"
        return $null
    }

    if ((Get-Item $PasswordFile).Length -gt 0) {
        return (Get-Content -Path $PasswordFile | ConvertTo-SecureString)
    }

    Write-Host "Password file is empty"
    return $null
}

function Read-PasswordFromInput {
    $password = Read-Host "Enter a password" -AsSecureString
    $confirmPassword = Read-Host "Confirm your password" -AsSecureString

    $passwordText = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))
    $confirmPasswordText = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($confirmPassword))

    $result = $passwordText -eq $confirmPasswordText
    $exitWithFailure = $false
    if (-Not $result) {
        Write-Error "Passwords don't match. Try again"
        $exitWithFailure = $true
    }

    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($confirmPassword))

    if ($exitWithFailure) {
        Exit 1
    }

    if ($result) { return $password }
    return $null
}

function Protect-Vault {
    param (
        [Parameter(Mandatory=$true, Position=0)]
        [SecureString]$Password
    )

    $outputArchive = "$Vault.zip"
    if (Test-Path -Path $outputArchive) {
        Write-Host "Removing existing $outputArchive"
        Remove-Item -Force $outputArchive
    }

    $plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password))
    Invoke-Expression "7z a `"-p$plainPassword`" `"$outputArchive`" `"$Vault`""
    $exitWithFailure = $false
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Encryption failed: $LASTEXITCODE"
        $exitWithFailure = $true
    }
    
    if ($exitWithFailure) {
        Exit 1
    }

    Write-Host "$Vault has been encrypted to $outputArchive"
}

if (-Not (Test-Path -Type Container $Vault)) {
    Write-Error "$Vault directory does not exist"
    Exit 1
}

$securePassword = Get-PasswordFromFile
if ($null -eq $securePassword) {
    $securePassword = Read-PasswordFromInput
}

Protect-Vault -Password $securePassword

Write-Host "Removing unencrypted $Vault directory"
Remove-Item -Recurse -Force $Vault
