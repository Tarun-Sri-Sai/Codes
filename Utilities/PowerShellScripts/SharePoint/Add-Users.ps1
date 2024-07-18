param (
    [Parameter(Position=0,mandatory=$true)]
    [string]$SiteUrl,
    [Parameter(Position=1,mandatory=$true)]
    [string]$AdminUrl,
    [Parameter(Position=2,mandatory=$true)]
    [string]$UserInfoFile,
    [Parameter(Position=3,mandatory=$true)]
    [string]$AppId,
    [Parameter(Position=4,mandatory=$true)]
    [string]$AppSecret
)

Connect-PnPOnline -Url $AdminUrl -ClientId $AppId -ClientSecret $AppSecret

$userInfo = Get-Content $UserInfoFile

foreach ($line in $userInfo) {
    $user = $line -split ","
    $userEmail = $user[0]
    $userPassword = $user[1]

    try {
        Add-PnPSiteCollectionAdmin -Owners $userEmail -Password $userPassword
        Write-Host "User $userEmail added as a site admin successfully." -ForegroundColor Green
    } catch {
        Write-Host "Error occurred while adding user $userEmail as a site admin: $_" -ForegroundColor Red
    }
}

Disconnect-PnPOnline
