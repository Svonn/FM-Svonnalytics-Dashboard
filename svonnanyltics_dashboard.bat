@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

echo Checking if the installation is complete...

:: Define repository root as the script's current directory
SET "REPO_ROOT=%~dp0"
echo Repository Root: "!REPO_ROOT!"

:: Check if the path contains spaces
:: This will set a flag if a space is found in the path
SET "SPACE_CHECK=!REPO_ROOT: =!"
IF NOT "!SPACE_CHECK!"=="!REPO_ROOT!" (
    echo The script cannot run in a path with spaces.
    pause
    exit /b 1
)
:: Check if Miniconda is installed in the repository
IF NOT EXIST "!REPO_ROOT!Miniconda3\Scripts\conda.exe" (
    echo Miniconda not found, installing to: "!REPO_ROOT!Miniconda3"
    :: Specify a path within the repository to download Miniconda installer
    SET "MINICONDA_INSTALLER=!REPO_ROOT!Miniconda3Installer.exe"

    :: Check if Miniconda installer already exists
    IF NOT EXIST "!MINICONDA_INSTALLER!" (
        echo Downloading Miniconda to: !MINICONDA_INSTALLER!
        :: Download Miniconda installer
        curl -Lk "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" > "!MINICONDA_INSTALLER!" || (
            echo Error downloading Miniconda installer.
            pause
            exit /b 1
        )
    ) ELSE (
        echo Miniconda installer already exists.
    )


    :: Install Miniconda
    start /wait "" "!MINICONDA_INSTALLER!" /InstallationType=JustMe /NoShortcuts=1 /AddToPath=0 /RegisterPython=0 /NoRegistry=1 /S /D=!REPO_ROOT!Miniconda3
    IF !ERRORLEVEL! NEQ 0 (
        echo Error installing Miniconda.
        pause
        exit /b !ERRORLEVEL!
    )

    echo Miniconda installation complete.
) ELSE (
    echo Miniconda already installed in the repository.
)

:: Refresh environment variables to recognize Miniconda installation
CALL "!REPO_ROOT!Miniconda3\Scripts\activate.bat"

:: Set local path to use the repository's Miniconda installation
SET "PATH=!REPO_ROOT!Miniconda3;!REPO_ROOT!Miniconda3\Scripts;!REPO_ROOT!Miniconda3\Library\bin;!PATH!"

:: Check if the environment is already created
"!REPO_ROOT!Miniconda3\Scripts\conda.exe" env list | findstr /C:"svonnalytics_env" >nul 2>&1
IF !ERRORLEVEL! NEQ 0 (
    echo Creating conda environment 'svonnalytics_env'...
    "!REPO_ROOT!Miniconda3\Scripts\conda.exe" create --name svonnalytics_env python=3.11 --yes
    IF !ERRORLEVEL! NEQ 0 (
        echo Error creating conda environment.
        pause
        exit /b !ERRORLEVEL!
    )
    echo Environment 'svonnalytics_env' created.
) ELSE (
    echo Conda environment 'svonnalytics_env' already exists.
)

:: Activate the environment
CALL "!REPO_ROOT!Miniconda3\Scripts\activate.bat" svonnalytics_env

:: Install requirements if not already installed
"!REPO_ROOT!Miniconda3\Scripts\conda.exe" list -n svonnalytics_env | findstr /C:"dash" >nul 2>&1
IF !ERRORLEVEL! NEQ 0 (
    echo Installing requirements from requirements.txt...
    "!REPO_ROOT!Miniconda3\Scripts\conda.exe" install --name svonnalytics_env -c conda-forge --file requirements.txt --yes
    IF !ERRORLEVEL! NEQ 0 (
        echo Error installing requirements.
        pause
        exit /b !ERRORLEVEL!
    )
    echo Requirements installed.
) ELSE (
    echo Requirements already installed.
)

:: Ask user for custom path or use default
echo Enter the path for FM24 export or press Enter to use the previous path:
SET "DEFAULTPATH=%USERPROFILE%\Documents\Sports Interactive\Football Manager 2024\exported_html"

:: Check if previous path file exists
IF EXIST "prev_path.txt" (
    FOR /F "delims=" %%i IN (prev_path.txt) DO SET "DEFAULTPATH=%%i"
)

set /p CUSTOMPATH="Path (default: %DEFAULTPATH%): "
IF "!CUSTOMPATH!"=="" SET CUSTOMPATH=!DEFAULTPATH!
echo Selected path: !CUSTOMPATH!

:: Save the selected path for next time
echo !CUSTOMPATH! > prev_path.txt


:: Create the directory if it doesn't exist
IF NOT EXIST "!CUSTOMPATH!" (
    mkdir "!CUSTOMPATH!"
    IF !ERRORLEVEL! NEQ 0 (
        echo Error creating directory. Please check your permissions or try again.
        pause
        exit /b !ERRORLEVEL!
    )
    echo Directory created: !CUSTOMPATH!
) ELSE (
    echo Directory already exists: !CUSTOMPATH!
)

:: Run the Dash app
echo Starting Dash application...
python dash_app.py --path "!CUSTOMPATH!"

:: Pause the script to keep the window open
pause

ENDLOCAL
