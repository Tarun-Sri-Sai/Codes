function Test-AzureApp {
    param (
        [Parameter(Position = 0, mandatory = $true)]
        [string]$ClientId,
        [Parameter(Position = 1, mandatory = $true)]
        [string]$DirectoryId
    )
    
    $ClientSecretSecure = Read-Host -Prompt "Client Secret" -AsSecureString
    $clientSecret = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($ClientSecretSecure))
    
    $body = @{
        client_id     = $ClientId
        client_secret = $clientSecret
        scope         = "https://graph.microsoft.com/.default"
        grant_type    = "client_credentials"
    }
    
    $tokenEndpoint = "https://login.microsoftonline.com/$DirectoryId/oauth2/v2.0/token"
    $response = Invoke-RestMethod -Uri $tokenEndpoint -Method Post -Body $body
    
    if ($response.access_token) {
        Write-Host -ForegroundColor Green "Correct client ID and secret for the tenant."
    }
    else {
        Write-Host -ForegroundColor Red "Incorrect client ID and secret for the tenant."
    }
}
