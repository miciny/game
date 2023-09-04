import pyautogui as auto
from common.common_utils import print_wait
from config import self_path, confidence_setting
import os


# 点击屏幕， delay_sec 点击完成后等待时常
def click_screen(click_pos, des=None, delay_sec=None):
    if click_pos:
        print(des, click_pos)
        auto.click(x=click_pos[0], y=click_pos[1], clicks=1, interval=1.0, button="left")
        if delay_sec:
            print_wait(delay_sec)


# 检测图片，返回中心点 或 None
def get_pic_position(pic_name, dir_name, pic_region, center=True):
    pic_path = os.path.join(self_path, dir_name + "\\" + pic_name + ".png")
    res = auto.locateOnScreen(pic_path, region=pic_region, confidence=confidence_setting, grayscale=True)
    if res is not None and center:
        res_center = auto.center(res)
        res = res_center + res[-2:]
    print(f'屏幕，检测图片: {pic_path}, 结果： {res}')
    return res