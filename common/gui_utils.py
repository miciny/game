import random
import pyautogui as auto
from common.common_utils import print_wait
from config import self_path, confidence_setting
import os
import pyperclip as clip


width, height = auto.size()
pic_region_full = (0, 0, width, height)


# 点击屏幕， delay_sec 点击完成后等待时常
def click_screen(click_pos, des="", delay_sec=None):
    if click_pos:
        print(des, click_pos)
        x = click_pos[0]
        y = click_pos[1]
        # 如果带了长宽，就随机
        if len(click_pos) == 4:
            w = int(click_pos[2] / 2) - 5
            h = int(click_pos[3] / 2) - 5
            x += random.randint(-w, w)
            y += random.randint(-h, h)

        print(des + '。点击具体位置：', x, y)
        auto.click(x=x, y=y, clicks=1, interval=1.0, button="left")
        if delay_sec:
            print_wait(delay_sec)


# 检测图片，返回【x, y, width, height】 或 None
def get_pic_position(pic_name, dir_name, pic_region=pic_region_full, center=True, without_tail=True):
    pic_path = os.path.join(self_path, dir_name, pic_name + (".png" if without_tail else ''))
    res = auto.locateOnScreen(pic_path, region=pic_region, confidence=confidence_setting, grayscale=True)
    if res is not None and center:
        res_center = auto.center(res)
        res = res_center + res[-2:]
    print(f'屏幕，检测图片: {pic_path}, 结果： {res}')
    return res


def auto_input(input_str, delay=0.5):
    auto.typewrite(input_str, delay)


def auto_key(key_str):
    auto.keyDown(key_str)


def screen_shot(pic_name, regine=pic_region_full):
    pic_path = os.path.join(self_path, "Logs", pic_name + ".png")
    auto.screenshot(pic_path, region=regine)
    return pic_path


def move_to(x, y, duration=0.2):
    auto.moveTo(x, y, duration=duration)


def drag_to(x, y, duration=1):
    auto.dragTo(x, y, duration=duration)

def paste_to(o_str):
    clip.copy(str(o_str))
    auto.hotkey("ctrl", "v")
