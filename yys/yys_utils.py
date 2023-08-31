import pyautogui as auto
from common.common_utils import print_wait
from common.gui_utils import *
from config import screen_width, screen_height
from yys import runtime_setting
import random



# 检测图片，返回中心点 或 None
def get_pic_pos(pic_name, center=True):
    if runtime_setting.current_screen == 1:
        pic_region = (runtime_setting.det_one_x, runtime_setting.det_one_y, screen_width, screen_height)
    elif runtime_setting.current_screen == 2:
        pic_region = (runtime_setting.det_two_x, runtime_setting.det_two_y, screen_width, screen_height)
    else:
        width, height = auto.size()
        pic_region = (0, 0, width, height)
    return get_pic_position(pic_name, 'yys_image', pic_region, center=center)


# 检测图片, 有一个存在就返回，返回中心点 或 None
def get_pic_list_pos(pic_name_list, center=True, dir_name='yys_image'):
    for pic_name in pic_name_list:
        if runtime_setting.current_screen == 1:
            pic_region = (runtime_setting.det_one_x, runtime_setting.det_one_y, screen_width, screen_height)
        elif runtime_setting.current_screen == 2:
            pic_region = (runtime_setting.det_two_x, runtime_setting.det_two_y, screen_width, screen_height)
        else:
            width, height = auto.size()
            pic_region = (0, 0, width, height)
        res = get_pic_position(pic_name, dir_name, pic_region, center=center)
        if res:
            return res
    return None

# 自动寻找两个窗口的左上标识
def find_windows():
    window_1_pos = get_pic_list_pos(["window_1", "window_11"], center=False)
    window_2_pos = get_pic_list_pos(["window_2", "window_22"], center=False)

    if window_1_pos is None and window_2_pos is None:
        print("请不要遮挡左上角logo")
        return 0
    if window_1_pos is None and window_2_pos is not None:
        print("没有找到第一个游戏窗口")
        runtime_setting.det_one_x = window_2_pos[0] - 5
        runtime_setting.det_one_y = window_2_pos[1] - 5
        return 1
    if window_1_pos is not None and window_2_pos is None:
        print("没有找到第二个游戏窗口")
        runtime_setting.det_one_x = window_1_pos[0] - 5
        runtime_setting.det_one_y = window_1_pos[1] - 5
        return 1
    if window_1_pos is not None and window_2_pos is not None:
        runtime_setting.det_one_x = window_1_pos[0] - 5
        runtime_setting.det_one_y = window_1_pos[1] - 5
        runtime_setting.det_two_x = window_2_pos[0] - 5
        runtime_setting.det_two_y = window_2_pos[1] - 5
        if runtime_setting.det_two_y < runtime_setting.det_one_y:
            print("位置切换，位置高的为第一个窗口")
            runtime_setting.det_one_x, runtime_setting.det_two_x = runtime_setting.det_two_x, runtime_setting.det_one_x
            runtime_setting.det_one_y, runtime_setting.det_two_y = runtime_setting.det_two_y, runtime_setting.det_one_y
        return 2


# 返回当前游戏窗口的位置
def get_screen_pos():
    if runtime_setting.current_screen == 1:
        click_x = runtime_setting.det_one_x + 80
        click_y = runtime_setting.det_one_y + 10
    else:
        click_x = runtime_setting.det_two_x + 80
        click_y = runtime_setting.det_two_y + 10
    return [click_x, click_y]


# 点击切换游戏屏幕
def switch_screen_click(to_screen):
    if to_screen == 1:
        runtime_setting.current_screen = 1
        click_pos = get_screen_pos()
    else:
        runtime_setting.current_screen = 2
        click_pos = get_screen_pos()
    click_screen(click_pos, "切换到第 " + str(runtime_setting.current_screen) + " 个窗口！位置：", delay_sec=1)


# 检测是否出现了接收按钮 确认按钮，一般在结束后容易出现意外
def check_other_btn():
    click_screen(get_pic_pos("confirm"), "点击确认")
    click_screen(get_pic_pos("confirm_1"), "点击确认")
    click_screen(get_pic_pos("confirm_2"), "点击确认")
    click_screen(get_pic_pos("accept"), "点击确认")


# 应该是可以通用的 返回是否结束，结束图片有两个，一个刚结束，一个结束了出现了奖励，底色不一样
def check_finish():
    res_pos = get_pic_list_pos(["finish_check_1", "finish_check_2", "finish_yl"])
    return res_pos is not None


# 返回是否在准备战斗页的坐标，组队的话，只有一种图片group，个人的话，都用挑战检测single
def check_back_main():
    pic_name = "group"
    if runtime_setting.fight_type == 1 or runtime_setting.fight_type == 5:
        pic_name = "single"
    the_pos = get_pic_pos(pic_name)
    return [the_pos.x + random.randint(-10, 10), the_pos.y + random.randint(-5, 10)] if the_pos else None


# 结束时的点击，检测不到结束图片，就结束
def final_click(index_check=True):
    if index_check:
        print("随机点击最多30次屏幕，为了返回首页")
        for _ in range(30):
            click_screen(fight_click_pos(1), "点击屏幕！位置：", random.randint(5, 8) / 8)
            if not check_finish():
                break
    else:
        print("随机点击最多5次屏幕，由于是首次，不检测图片")
        for _ in range(5):
            click_screen(fight_click_pos(1), "点击屏幕！位置：", random.randint(5, 8) / 8)


# 1战斗结束点击屏幕的位置, 2战斗中点击屏幕的位置，[3, 4, 5, 6]觉醒切换位置时点击屏幕的位置
def fight_click_pos(pos_type=1):
    if pos_type == 2:
        click_x = screen_width * 0.5 + random.randint(-int(0.1 * screen_width), int(0.1 * screen_width))
        click_y = screen_height * 0.5 + random.randint(-int(0.17 * screen_height), int(0.17 * screen_width))
    elif pos_type in [3, 4, 5, 6]:
        click_x = screen_width * 0.05769
        click_y = screen_height * 0.29455 + (screen_height * 0.17) * (pos_type - 3)
    else:
        click_x = screen_width * 0.83333 + random.randint(10, 150)
        click_y = screen_height * 0.6596 + random.randint(-90, 70)
    if runtime_setting.current_screen == 1:
        return [click_x + runtime_setting.det_one_x, click_y + runtime_setting.det_one_y]
    else:
        return [click_x + runtime_setting.det_two_x, click_y + runtime_setting.det_two_y]


# 主线任务的点击点
def ghost_main_mission_pos(main_check=False):
    if not main_check:
        for i in range(1, 7):
            res_pos = get_pic_pos("mission_" + str(i))
            if res_pos:
                return res_pos
        else:
            return None
    else:
        return get_pic_pos("main_plus")


# 百鬼的一些位置，1开始，2选择三个鬼王随机，3鬼王选择后的开始，4选择鬼王后，确保已选中，检测下，5结束检测图
# 6如果在百鬼结束页，点击空白的位置，7豆的位置，把它拖到10个豆
# 其他是砸豆的位置随机
def ghost_hit_pos(pos_type=1):
    if pos_type == 1:
        return get_pic_pos("ghost_add")
    elif pos_type == 2:
        index = random.randint(-1, 1)
        click_x = screen_width / 2 + screen_width * 0.30873 * index
        click_y = screen_height * 0.677
    elif pos_type == 3:
        return get_pic_pos("ghost_begin")
    elif pos_type == 4:
        return get_pic_pos("ghost_selected")
    elif pos_type == 5:
        return get_pic_pos("ghost_finish")
    elif pos_type == 6:
        click_x = screen_width / 5
        click_y = 80
    elif pos_type == 7:
        return get_pic_pos("ghost_bean_no")
    elif pos_type == 8:
        return get_pic_pos("frozen")
    else:
        wight = int(screen_width * 0.45)
        index = random.randint(-wight, wight)
        click_x = screen_width / 2 + index
        click_y = screen_height * 0.594
    if runtime_setting.current_screen == 1:
        return [click_x + runtime_setting.det_one_x, click_y + runtime_setting.det_one_y]
    else:
        return [click_x + runtime_setting.det_two_x, click_y + runtime_setting.det_two_y]


# 检测主页面，失败了就重试三次，每次重新点击第一个屏幕和第二个屏幕
def check_main_false():
    for i in range(3):
        print("检测" + str(runtime_setting.current_screen) + "屏幕是否到主页！第", i + 1, "次")
        main_check = check_back_main()
        if not main_check:
            print("没有回到主页")
            check_other_btn()
            print_wait(3, "等待")
            final_click()
            if runtime_setting.fight_type == 3:
                switch_screen_click(to_screen=2)
                check_other_btn()
                final_click()
                switch_screen_click(to_screen=1)
        else:
            print("回到主页")
            return main_check
    return None


# 检测主页面，主要用在点击开始后，实际没开始的情况
def check_main_true_operation(start_pos):
    click_screen(start_pos, "点击开始战斗！位置：")
    print_wait(3, "等待检测是否真的开始")
    click_screen(get_pic_pos('prepare_fight'), '点击准备')
    for i in range(3):
        print("检测是否真的开始！第", i, "次")
        start_pos = check_back_main()
        if not start_pos:
            print("没有在主页，继续")
            return True
        else:
            print("还在主页，检查是否有其他按钮遮挡，然后重新点击开始按钮")
            check_other_btn()
            if runtime_setting.fight_type == 3:
                switch_screen_click(to_screen=2)
                check_other_btn()
                switch_screen_click(to_screen=1)
            click_screen(start_pos, "点击开始战斗！位置：")
            print_wait(3, "等待")
    return False


# 检测是否结束，失败了就重试，重试次数是 fight_sec / 2， 每次睡三秒
def check_finish_false_operation():
    print_wait(1, "等待检测是否结束")
    count = int(runtime_setting.fight_sec / 2)
    for i in range(count):
        print("检测是否结束：", i, "/", count)
        finish_check = check_finish()
        if not finish_check:
            if runtime_setting.fight_type == 1:
                start_pos = check_back_main()
                if not start_pos:
                    print("未结束")
                else:
                    print("已在主页")
                    return True
            print_wait(3, "等待检测是否结束：")
        else:
            print("已结束")
            return True
    print("似乎一直未结束！继续操作，看是否到开始页面")
    return False


# 切换窗口 - 检测结束
def switch_and_finish(to_screen, finish_check=True, index_check=True):
    switch_screen_click(to_screen)
    # 检查是否结束了
    if finish_check:
        check_finish_false_operation()
    final_click(index_check)