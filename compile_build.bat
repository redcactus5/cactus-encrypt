@echo off
setlocal
echo searching for builds to compile...
:: Check for the existence of Folder1
if exist "release build" (
    echo release build found!
    echo starting compilation...
    cd "release build"
    python -m nuitka --standalone --windows-icon-from-ico=cactus_encrypt_icon.ico  cactus_encrypt.py
    cd ..
) else (
    echo could not find release build.
)

:: Check for the existence of Folder2
if exist "debug build" (
    echo debug build found!
    echo starting compilation...
    cd "debug build"
    python -m nuitka --standalone --windows-icon-from-ico=cactus_encrypt_icon.ico  cactus_encrypt.py
    cd ..
) else (
    echo could not find debug build.
)

echo done!

endlocal