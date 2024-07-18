# This script requires the following PS modules:
#   1) 'Sharepoint Online Management Shell'
#   2) Microsoft.Online.SharePoint.PowerShell
# 1) This can be installed using this link: https://www.microsoft.com/en-us/download/details.aspx?id=35588
# 2) This can be installed with the PS command: `Install-Module -Name SharePointPnPPowerShellOnline -AllowClobber -Force`

param (
    [Parameter(Position=0,mandatory=$true)]
    [string]$SiteAdminUrl,
    [Parameter(Position=1,mandatory=$true)]
    [string]$Username,
    [Parameter(Position=2,mandatory=$true)]
    [string]$Password
)

$credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $Username, $(ConvertTo-SecureString $Password -AsPlainText -Force)
Connect-SPOService -Url $SiteAdminUrl -Cred $credential

$allSites = Get-SPOSite -Limit All
$teamsSites = $allSites | Where-Object { $_.IsTeamsConnected -eq $True } | Select-Object -ExpandProperty Url
$teamsConnectedSites = $allSites | Where-Object { $_. IsTeamsChannelConnected -eq $True } | Select-Object -ExpandProperty Url

$fileName = "TeamsSites_$(New-Guid).txt"
$allTeamsSites = ($teamsSites + $teamsConnectedSites) | Sort-Object -Unique
Set-Content -Path $fileName -Value $allTeamsSites

Write-Output $fileName
