Connect-SPOService -Url https://yourtenant-admin.sharepoint.com

$uniqueUsers = @{}
$siteCollections = Get-SPOSite

foreach ($site in $siteCollections) {
    Write-Host "Processing site collection:" $site.Url
        $users = Get-SPOUser -Site $site.Url
        foreach ($user in $users) {
        $uniqueUsers[$user.LoginName] = $true
    }
}

Write-Host "Unique Users:"
foreach ($user in $uniqueUsers.Keys) {
    Write-Host $user
}
