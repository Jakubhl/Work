# Set the root folder to start changing creation dates from
$RootFolder = "D:\JHV\Kamery\mazani_test4"

# Set the new creation date in the desired format
$newCreationDate = Get-Date "2023-09-20 10:00:00"

# Recursively loop through all files in the root folder and its subfolders
Get-ChildItem -Path $RootFolder -File -Recurse | ForEach-Object {
    # Set the file's creation date to the new value
    $_.CreationTime = $newCreationDate
    Write-Host "Changed creation date for $($_.FullName)"
}