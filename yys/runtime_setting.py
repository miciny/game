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

# 当前次数
current_time = 0

# 战斗类型 1个人 3组队 5两个号分开刷
fight_type = 0

# 副本类型 1普通战斗 3主线 5百鬼
fight_to = 0

# 预计战斗时长
fight_sec = 0

# 双号刷，记录每个号是否成功
two_flags = [True, True]

# 截图之后不能再调整窗口大小，两个屏幕不要挡着左上角的游戏logo
# yys窗口大小
yys_screen_width = 1000
yys_screen_height = 585

# fight_type    1单号       3组队       5两个号分开刷
# fight_to      1普通战斗    3主线       5百鬼
fight_setting_list = [
    {"fight_sec": 15, "fight_type": 3, "fight_to": 1, 'desc': '组队-魂土'},
    {"fight_sec": 20, "fight_type": 3, "fight_to": 1, 'desc': '组队-日轮'},
    {"fight_sec": 25, "fight_type": 5, "fight_to": 1, 'desc': '双号-业原'},
    {"fight_sec": 1, "fight_type": 5, "fight_to": 1, 'desc': '双号-活动'},
    {"fight_sec": 7, "fight_type": 1, "fight_to": 5, 'desc': '单刷-百鬼'},
    {"fight_sec": 7, "fight_type": 1, "fight_to": 3, 'desc': '单刷-主线'}
]
