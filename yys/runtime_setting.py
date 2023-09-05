# 切换到第一个窗口，点击的位置
screen_pos_one = (0, 0)
# 第一个窗口扫描的开始点
screen_scan_one = (0, 0)
# 切换到第二个窗口，点击的位置
screen_pos_two = (0, 0)
# 第二个窗口扫描的开始点
screen_scan_two = (0, 0)

# 第二个窗口，离原点的位置
det_two_x = 0
det_two_y = 0

# 当前屏幕
current_screen = 0

# 战斗类型 1个人 3组队 5两个号分开刷
fight_type = 0

# 副本类型 1魂土 2业原火 3日轮 4觉醒 7主线 9百鬼
fight_to = 0

# 预计战斗时长
fight_sec = 0

# 截图之后不能再调整窗口大小，两个屏幕不要挡着左上角的游戏logo
# yys窗口大小
yys_screen_width = 1000
yys_screen_height = 585

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
