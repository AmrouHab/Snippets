# This script will move all files from subfolders into the main root folder and remove empty directories afterward. 

$rootFolder = Get-Location  # Use the current directory as root

# Get all files from subdirectories
Get-ChildItem -Path $rootFolder -Directory | ForEach-Object {
    Get-ChildItem -Path $_.FullName -File | ForEach-Object {
        $destination = Join-Path -Path $rootFolder -ChildPath $_.Name
        
        # If a file with the same name exists, rename it
        if (Test-Path $destination) {
            $destination = Join-Path -Path $rootFolder -ChildPath ("$(Get-Random)_" + $_.Name)
        }
        
        Move-Item -Path $_.FullName -Destination $destination -Force
    }
}

# Remove empty directories
Get-ChildItem -Path $rootFolder -Directory | Where-Object { $_.GetFiles().Count -eq 0 -and $_.GetDirectories().Count -eq 0 } | Remove-Item -Force -Recurse
