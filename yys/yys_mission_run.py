from yys.yys_utils import ghost_main_mission_pos
from common.gui_utils import click_screen


# 新号做主线任务
def main_mission():
    for i in range(100):
        pic_pos = ghost_main_mission_pos()
        if pic_pos:
            click_screen(pic_pos, "点击屏幕", 1)
        else:
            print_wait(1, "等待点击")
            main_pic_pos = ghost_main_mission_pos(True)
            if main_pic_pos:
                print("已回到首页，停止")
                return False
            click_screen(fight_click_pos(2), "没有可点击的，随机点", 1)
    return True