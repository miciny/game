import time
import os
import sys
from Email import send_mail
from Config import rec_list, self_path
import pyautogui as auto
from WechatServices import send_wechat_notice


def get_average(data_list):
    if len(data_list) == 0:
        return 0
    else:
        sum_all = 0
        for item in data_list:
            sum_all += item
        return sum_all / len(data_list)


def time_format(time_dlt):
    if time_dlt < 60:
        return str(round(time_dlt, 2)) + "s"
    elif time_dlt < 3600:
        time_dlt_m = int(time_dlt / 60)
        time_dlt_s = int(time_dlt % 60)
        return str(time_dlt_m) + "m " + str(time_dlt_s) + "s"
    else:
        time_dlt_h = int(time_dlt / 3600)
        time_dlt_m = int(time_dlt / 60 - 60 * time_dlt_h)
        time_dlt_s = int(time_dlt % 60)
        return str(time_dlt_h) + "h " + str(time_dlt_m) + "m " + str(time_dlt_s) + "s"


# 打印等待
def print_wait(time_sec, des=None):
    if des is None:
        time.sleep(time_sec)
    else:
        time_sec = int(time_sec)
        for i in range(time_sec):
            time.sleep(1)
            des_out = '\r%s: %s' % (des, str(i + 1) + "/" + str(time_sec))
            sys.stdout.write(des_out)
            sys.stdout.flush()
        print("")


# 关机
def shutdown_pc(delay_time=60):
    mcy_send_mail(str(delay_time) + "秒准备关机！", 4)
    print_wait(delay_time, "自动关机倒计时：")
    os.system("shutdown /s")


# 1成功 2失败 3过程中 4通知
def mcy_send_mail(content_str, status=1):
    if status == 2:
        pic_path = os.path.join(self_path, "YysImage\\error.png")
        title = "错误"
    elif status == 3:
        pic_path = os.path.join(self_path, "YysImage\\progress.png")
        title = "过程中"
    elif status == 1:
        pic_path = os.path.join(self_path, "YysImage\\done.png")
        title = "成功"
    else:
        pic_path = os.path.join(self_path, "YysImage\\notice.png")
        title = "通知"
    auto.screenshot(pic_path)
    try:
        send_wechat_notice(title, content_str)
        send_mail(title, content_str, rec_list, [pic_path])
    except Exception as e:
        print(e)


# 点击屏幕， delay_sec 点击完成后等待时常
def click_screen(click_pos, des=None, delay_sec=None):
    print(des, click_pos)
    auto.click(x=click_pos[0], y=click_pos[1], clicks=1, interval=1.0, button="left")
    if delay_sec is not None:
        print_wait(delay_sec)
