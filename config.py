import os
self_path = os.path.dirname(os.path.realpath(__file__))

# pip3 install pyautogui -i http://mirrors.aliyun.com/pypi/simple  --trusted-host mirrors.aliyun.com
# pip3 install opencv-python -i http://mirrors.aliyun.com/pypi/simple  --trusted-host mirrors.aliyun.com
# pip3 install opencv-contrib-python -i http://mirrors.aliyun.com/pypi/simple  --trusted-host mirrors.aliyun.com
# pip3 install smtplib -i http://mirrors.aliyun.com/pypi/simple  --trusted-host mirrors.aliyun.com

# bat
# 文件，需要管理员方式打开：
# @echo off
# >nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
# if '%errorlevel%' NEQ '0' (
# goto UACPrompt
# ) else ( goto gotAdmin )
# :UACPrompt
# echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
# echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
# "%temp%\getadmin.vbs"
# exit /B
# :gotAdmin
# if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
# python C:\Users\miciny\Desktop\OtherRun.py

confidence_setting = 0.8
