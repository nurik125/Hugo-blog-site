param (
    [string]$FirstValue,
    [string]$SecondValue
)

$Confirm_git = Read-Host "Are you sure? (y/n)".ToLower()
if (($Confirm_git -ieq "y") -or ($Confirm_git -ieq "yes")){
    # Variables
    # Correct paths depending on your system
    $sourcePATH = "D:\Vaults\Regular(Main)\Blog\posts"
    $temp_dir = "D:\Vaults\Regular(Main)\Blog\temp"

    # Relative path
    $destinationPATH = "content\posts"

    $robocopyOptions = @("/mir", "/z", "/r:3", "/w:5", "/XD", '"attachments"')

    if (Get-Command 'python' -ErrorAction SilentlyContinue) {
        $pythonCommand = 'python'
    } elseif (Get-Command 'python3' -ErrorAction SilentlyContinue) {
        $pythonCommand = 'python3'
    } elseif (Get-Command 'py' -ErrorAction SilentlyContinue) {
        $pythonCommand = 'py'
    } else {
        Write-Error "Python is not installed or not in PATH."
        exit 1
    }
    #Creating temporary dir for content editing and not touching the original source
    mkdir ($temp_dir) -ErrorAction SilentlyContinue

    # Copying posts into temp file
    robocopy $sourcePATH $temp_dir $robocopyOptions > $null

    # Executing python file for images
    & $pythonCommand .\scripts\images.py

    # Mirroring the posts from temp to hugo content
    robocopy $temp_dir $destinationPATH $robocopyOptions > $null

    # #Removing the temp dir
    Remove-Item $temp_dir -Recurse -Force

    # Building hugo site
    hugo

    # pushing changes commit to git repo
    git add .

    $answer = Read-Host "Type the commit message: "

    git commit -m $answer

    git push origin main
}

