param (
    [Parameter(Position=0,mandatory=$true)]
    [string]$SiteAdminUrl,
    [Parameter(Position=1,mandatory=$true)]
    [string]$Username
)

$password = Read-Host -Prompt "Password" -AsSecureString
$credentialObject = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $Username,$password
Connect-SPOService -Url $SiteAdminUrl -Credential $credentialObject


$allSiteCollections = Get-SPOSite -Limit ALL

$outputFile = "site_collections.txt"
Write-Output $allSiteCollections.Url | Sort-Object | Out-File $outputFile
Write-Host "Writing $($(${allSiteCollections}.Url).Count) site collections to $outputFile"

Disconnect-SPOService
