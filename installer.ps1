$packages = @(
    "sqlite3",
    "pyinstaller"
)

# Loop through the list of packages and install each one
foreach ($package in $packages) {
    Write-Host "Installing $package..."
    try {
        pip install $package
        Write-Host "$package installed successfully." -ForegroundColor Green
    } catch {
        Write-Host "Failed to install $package : $_" -ForegroundColor Red
    }
}

# Set the path to your Python script
$pythonScript = "final.py"

# Set the path to your icon file
$iconFile = "application_icon.ico"

# Set the output file name
$outputFile = "final.exe"

# Create the application
pyinstaller --onefile $pythonScript --icon=$iconFile

Write-Host "Application created: $outputFile"
New-Item -Path "C:\Student Grading Application" -ItemType Directory
Copy-Item -Path "dist\final.exe" -Destination "C:\Student Grading Application" -Force
Copy-Item -Path "final.py" -Destination "C:\Student Grading Application" -Force
Copy-Item -Path "dist\final.exe" -Destination "C:\Student Grading Application" -Force