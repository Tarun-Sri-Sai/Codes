param (
    [String]$Vault = "Vault"
)

function Get-PasswordFromInput {
    $password = Read-Host "Enter the master password" -AsSecureString
    return $password
}

function Unprotect-Vault {
    param (
        [Parameter(Mandatory=$true, Position=0)]
        [String]$Archive,

        [Parameter(Mandatory=$true, Position=1)]
        [SecureString]$Password
    )

    if (-Not (Test-Path -Path $Archive -PathType Leaf)) {
        Write-Error "The encrypted file $archive does not exist"
        Exit 1
    }

    $plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password))
    Invoke-Expression "7z x `"-p$plainPassword`" `"$Archive`""
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Decryption failed: $LASTEXITCODE"
        Write-Host "Removing partially created $Vault"
        Remove-Item -Recurse -Force $Vault   # Directory with empty files is created if the password is wrong
        [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password))
        Exit $LASTEXITCODE
    }

    Write-Host "The archive $Archive has been decrypted and extracted"
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password))
}

if (Test-Path -Type Container $Vault) {
    Write-Error "$Vault directory already exists. Cannot overwrite"
    Exit 1
}

$securePassword = Get-PasswordFromInput
Unprotect-Vault -Archive "$Vault.zip" -Password $securePassword
