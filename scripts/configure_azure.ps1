param(
    [Parameter(Mandatory=$true)][string]$AccountName,
    [Parameter(Mandatory=$true)][string]$ContainerName
)
$ErrorActionPreference = 'Stop'
if ($AccountName -notmatch '^[a-z0-9]{3,24}$') { throw 'Invalid storage account name' }
if ($ContainerName -notmatch '^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$') { throw 'Invalid container name' }
dvc remote add -d -f azure "azure://$ContainerName/vineyard-lab"
if ($LASTEXITCODE -ne 0) { throw 'DVC remote creation failed' }
dvc remote modify azure account_name $AccountName
if ($LASTEXITCODE -ne 0) { throw 'DVC configuration failed' }
Write-Host 'Remote configured. Authenticate with az login using Storage Blob Data Contributor access, then run dvc push --all-commits.'
Write-Host 'Never commit a connection string or access key. Local fallback: dvc remote modify --local azure connection_string <value entered locally>.'
