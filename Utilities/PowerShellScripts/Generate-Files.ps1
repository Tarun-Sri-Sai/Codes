param (
	[Parameter(Position=0,mandatory=$true)]
	[int]$FileSizeBytes,
	
	[Parameter(Position=1,mandatory=$true)]
	[int]$Files,
	
	[Parameter(Position=2,mandatory=$true)]
	[string]$Extension
)

function Get-RandomString {
	param (
		[Parameter(Position=0,mandatory=$true)]
		$Length
	)
	
	$chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	$string = -join ((Get-Random -InputObject $chars -Count $Length))
	return $string
}

for ($i = 1; $i -le $Files; $i++) {
	$filePath = "File_$i.$Extension"
	$randomString = Get-RandomString -length $FileSizeBytes
	Set-Content -Path $filePath -Value $randomString
	if (($Files -ge 100) -and ($i % ([int]($Files / 100))) -eq 0) {
		Write-Host "Added $i files"
	}
}
