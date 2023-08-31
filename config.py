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

# yys的设置：
# YysImage的截图，截图之后不能再调整窗口大小，两个屏幕不要挡着左上角的游戏logo
# 窗口大小
screen_width = 1000
screen_height = 585
confidence_setting = 0.8

# fight_type    1个人 3组队 5两个号分开刷
# fight_to      1魂土 2业原火 3日轮 4觉醒 7主线 9百鬼
fight_1 = {"times": 120, "fight_sec": 15, "fight_type": 3, "fight_to": 1, "fight_list": []}  # 组队-魂土
fight_2 = {"times": 50, "fight_sec": 30, "fight_type": 3, "fight_to": 3, "fight_list": []}  # 组队-日轮
fight_3 = {"times": 120, "fight_sec": 60, "fight_type": 5, "fight_to": 2, "fight_list": []}  # 两个号分開单刷业原火
fight_4 = {"times": 120, "fight_sec": 60, "fight_type": 1, "fight_to": 2, "fight_list": []}  # 单刷-业原火
fight_5 = {"times": 120, "fight_sec": 7, "fight_type": 1, "fight_to": 9, "fight_list": []}  # 单砸百鬼
fight_6 = {"times": 120, "fight_sec": 7, "fight_type": 1, "fight_to": 7, "fight_list": []}  # 新号做主线任务
fight_7 = {"times": 60, "fight_sec": 7, "fight_type": 3, "fight_to": 4, "fight_list": []}  # 组队-觉醒
fight_8 = {"times": 40, "fight_sec": 7, "fight_type": 1, "fight_to": 4, "fight_list": [1, 2, 3, 4]}  # 单刷-觉醒，随机打四个

# 其他的设置：
