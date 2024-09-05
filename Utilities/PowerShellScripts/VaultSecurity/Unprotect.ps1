param (
    [String]$Vault = "Vault"
)

function Get-PasswordFromInput {
    $password = Read-Host "Enter a password" -AsSecureString
    return $password
}

function Unprotect-Vault {
    param (
        [Parameter(Mandatory=$true, Position=0)]
        [SecureString]$Password
    )

    $archive = "$Vault.zip"
    if (-Not (Test-Path -Path $archive -PathType Leaf)) {
        Write-Error "The encrypted file $archive does not exist"
        Exit 1
    }

    $plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password))
    Invoke-Expression "7z x `"-p$plainPassword`" `"$archive`""
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Decryption failed: $LASTEXITCODE"
        Remove-Item -Recurse -Force $Vault   # Folder with empty files is created if the password is wrong
        [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password))
        Exit $LASTEXITCODE
    }

    Write-Host "The archive $archive has been decrypted and extracted"
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password))
}

$securePassword = Get-PasswordFromInput
Unprotect-Vault -Password $securePassword
