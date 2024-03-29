import time
import os
import sys
from config import self_path
import pyautogui as auto
from common.wechat_services import send_wechat_notice


# 平均值
def get_average(data_list):
    if len(data_list) == 0:
        return 0
    else:
        sum_all = 0
        for item in data_list:
            sum_all += item
        return sum_all / len(data_list)


# 时间格式化显示
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
def shutdown_pc(delay_time=99):
    mcy_send_notice(str(delay_time) + "秒倒计时关机！", 4)
    print_wait(delay_time, "自动关机倒计时：")
    os.system("shutdown /s")


# 1成功 2失败 3过程中 4通知
def mcy_send_notice(content_str, status=1):
    if status == 2:
        pic_path = os.path.join(self_path, "Logs", "error.png")
        pic_path_1 = os.path.join(self_path, "Logs", "error_1.png")
        title = "错误"
    elif status == 3:
        pic_path = os.path.join(self_path, "Logs", "progress.png")
        pic_path_1 = os.path.join(self_path, "Logs", "progress_1.png")
        title = "过程中"
    elif status == 1:
        pic_path = os.path.join(self_path, "Logs", "done.png")
        pic_path_1 = os.path.join(self_path, "Logs", "done_1.png")
        title = "成功"
    else:
        pic_path = os.path.join(self_path, "Logs", "notice.png")
        pic_path_1 = os.path.join(self_path, "Logs", "notice_1.png")
        title = "通知"
    auto.screenshot(pic_path)
    time.sleep(2)
    auto.screenshot(pic_path_1)
    try:
        send_wechat_notice(title, content_str)
    except Exception as e:
        print(e)
