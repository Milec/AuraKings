@echo off
setlocal enabledelayedexpansion
REM ============================================================================
REM  Aura Kings - Crusader Kings III mod installer (Windows)
REM
REM  Double-click this file. It registers the mod with the CK3 launcher by
REM  writing a small descriptor into your Paradox "mod" folder that points back
REM  to wherever this repo lives. Nothing is copied, so "git pull" here updates
REM  the mod in place.
REM ============================================================================

echo.
echo   Aura Kings - CK3 mod installer
echo   ==============================
echo.

REM --- Repo location = the folder this script sits in --------------------------
set "REPO=%~dp0"
if "%REPO:~-1%"=="\" set "REPO=%REPO:~0,-1%"

REM --- Find the real Documents folder (handles OneDrive redirection) -----------
set "DOCS="
for /f "usebackq delims=" %%D in (`powershell -NoProfile -Command "[Environment]::GetFolderPath('MyDocuments')" 2^>nul`) do set "DOCS=%%D"
if not defined DOCS set "DOCS=%USERPROFILE%\Documents"

set "CK3DIR=%DOCS%\Paradox Interactive\Crusader Kings III"
set "MODDIR=%CK3DIR%\mod"

if not exist "%CK3DIR%" (
    echo   ERROR: Could not find your CK3 user folder at:
    echo     "%CK3DIR%"
    echo   Run Crusader Kings III at least once, then try again.
    echo.
    pause
    exit /b 1
)

if not exist "%MODDIR%" mkdir "%MODDIR%"

REM --- CK3 descriptors use forward slashes ------------------------------------
set "FWDPATH=%REPO:\=/%"

REM --- Write the launcher descriptor ------------------------------------------
set "DESC=%MODDIR%\AuraKings.mod"
> "%DESC%" echo version="0.1.0"
>> "%DESC%" echo name="Aura Kings"
>> "%DESC%" echo supported_version="1.19.*"
>> "%DESC%" echo path="%FWDPATH%"

echo   Installed!
echo     Mod source : %REPO%
echo     Descriptor : %DESC%
echo.
echo   Next: open the CK3 launcher, go to Mods, add "Aura Kings" to a
echo   playset, enable it, and play.
echo.
echo   (If the launcher warns about the game version, edit supported_version
echo    in descriptor.mod and AuraKings.mod to match your CK3 version.)
echo.
pause
endlocal
