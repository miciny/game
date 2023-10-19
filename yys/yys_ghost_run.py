from yys.yys_utils import ghost_hit_pos, check_other_btn, switch_screen_click
from common.common_utils import print_wait, mcy_send_notice
import pyautogui as auto
from common.gui_utils import click_screen
from yys import runtime_setting


# 砸百鬼, 目前只能单砸
def ghost_hit():
    hit_res = ""
    try:
        switch_screen_click(1)
        add_pos = ghost_hit_pos(pos_type=1)
        if not add_pos:
            hit_res = "没有在首页"
            return hit_res
        click_screen(add_pos, "点击首页的开始", delay_sec=3)

        for i in range(3):
            select_pos = ghost_hit_pos(pos_type=2)
            click_screen(select_pos, "随机选择一个鬼王", delay_sec=1)

            selected_pos = ghost_hit_pos(pos_type=4)
            if selected_pos:
                break
            if i == 1:
                check_other_btn()
            if i == 2:
                hit_res = "选择鬼王不成功"
                return hit_res

        begin_pos = ghost_hit_pos(pos_type=3)
        if not begin_pos:
            hit_res = "没有在开始页"
            return hit_res
        click_screen(begin_pos, "点击开始", delay_sec=3)

        # 拖动将豆拖到10
        bean_pos = ghost_hit_pos(7)
        if bean_pos:
            auto.moveTo(bean_pos[0], bean_pos[1])
            auto.dragTo(bean_pos[0] + 230, bean_pos[1], duration=1)

        hit_times = 200
        for i in range(hit_times):
            frozen_status = ghost_hit_pos(8)
            if frozen_status:
                print_wait(3, "等待冰冻3秒")
            hit_pos = ghost_hit_pos(10)
            click_screen(hit_pos, "砸百鬼：", 0.15)
            finish_flag = ghost_hit_pos(1) or ghost_hit_pos(5)
            if finish_flag:
                break
            if i == hit_times - 1:
                hit_res = "似乎出了问题，一直没砸完，或是进入不可知页面"
                return hit_res

        print_wait(1, "等待一秒")
        for i in range(10):
            finish_flag = ghost_hit_pos(5)
            if finish_flag:
                click_pos = ghost_hit_pos(6)
                click_screen(click_pos, "点击结束", delay_sec=1)
                click_screen(click_pos, "点击结束", delay_sec=1)

            begin_flag = ghost_hit_pos(1)
            if begin_flag:
                return hit_res
            else:
                check_other_btn()
        hit_res = "检测不到回到了首页"
        return hit_res
    finally:
        if hit_res != "":
            mcy_send_notice(f"第{runtime_setting.current_time}次，砸百鬼出错了：" + hit_res, 2)
