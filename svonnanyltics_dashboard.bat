@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Check if Miniconda is installed
where conda >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Miniconda not found, installing...
    :: Download and install Miniconda - change the URL to the specific version you need
    powershell -Command "Invoke-WebRequest -Uri https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -OutFile %TEMP%\Miniconda3.exe"
    :: Install Miniconda silently
    %TEMP%\Miniconda3.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\Miniconda3
    SET "PATH=%UserProfile%\Miniconda3;%UserProfile%\Miniconda3\Scripts;%UserProfile%\Miniconda3\Library\bin;%PATH%"
    echo Miniconda installed.
) ELSE (
    echo Miniconda already installed.
)

:: Check if the environment is already created
conda env list | findstr /C:"myenv" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Creating conda environment 'myenv'...
    conda create --name myenv python=3.x --yes
    echo Environment 'myenv' created.
) ELSE (
    echo Conda environment 'myenv' already exists.
)

:: Activate the environment
CALL conda activate myenv

:: Install requirements if not already installed
conda list -n myenv | findstr /C:"dash" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installing requirements from requirements.txt...
    conda install --name myenv --file requirements.txt
    echo Requirements installed.
) ELSE (
    echo Requirements already installed.
)

:: Ask user for custom path or use default
echo Enter the path for FM24 export or press Enter to use the default path:
set "DEFAULTPATH=%USERPROFILE%\Documents\Sports Interactive\Football Manager 2024\exported_html"
set /p CUSTOMPATH="Path (default: %DEFAULTPATH%): "
IF "!CUSTOMPATH!"=="" SET CUSTOMPATH=%DEFAULTPATH%
echo Selected path: !CUSTOMPATH!

:: Create the directory if it doesn't exist
IF NOT EXIST "!CUSTOMPATH!" (
    mkdir "!CUSTOMPATH!"
    echo Directory created: !CUSTOMPATH!
) ELSE (
    echo Directory already exists: !CUSTOMPATH!
)

:: Update configurations.py with the selected path
powershell -Command "$content = Get-Content configurations.py; $content -replace 'F:\\\\Games\\\\FM24 Files\\\\exported_html', '!CUSTOMPATH!' | Set-Content configurations.py"
echo Updated configurations.py with the selected path.

:: Run the Dash app
echo Starting Dash application...
python dash_app.py

ENDLOCAL
