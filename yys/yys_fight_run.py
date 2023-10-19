from yys import runtime_setting


# 切换窗口 - 点击开始 - 开始的检测
def switch_and_begin(to_screen):
    switch_screen_click(to_screen)
    # 检查是否到首页了
    start_pos = check_main_false()
    if not start_pos:
        mcy_send_notice(f"第{runtime_setting.current_time}次，第" + str(runtime_setting.current_screen) + "个游戏似乎出错了，没有回到主页！", 2)
        return False
    not_main_check = check_main_true_operation(start_pos)
    if not not_main_check:
        mcy_send_notice( f"第{runtime_setting.current_time}次，第" + str(runtime_setting.current_screen) + "个游戏似乎出错了，没有真的开始！", 2)
        return False
    return True

# 两个分开单刷
def two_fight():
    if runtime_setting.two_flags[0]:
        runtime_setting.two_flags[0] = switch_and_begin(1)  # 第一个屏幕
    if runtime_setting.two_flags[1]:
        runtime_setting.two_flags[1] = switch_and_begin(2)  # 第二个屏幕
    print_wait(runtime_setting.fight_sec, "等待战斗结束：")

    if runtime_setting.two_flags[0]:
        switch_and_finish(1)  # 第一个屏幕
    if runtime_setting.two_flags[1]:
        switch_and_finish(2)  # 第二个屏幕
    return runtime_setting.two_flags[0] or runtime_setting.two_flags[1]

# 单刷或组队
def one_fight():
    begin_flag = switch_and_begin(1)
    if not begin_flag:
        return False
    print_wait(runtime_setting.fight_sec, "等待战斗结束：")

    # 检查是否结束了
    switch_and_finish(1)
    if runtime_setting.fight_type == 3:
        switch_and_finish(2, finish_check=False)
    return True
