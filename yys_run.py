# -*- coding: UTF-8 -*-
import sys
import time
from yys import runtime_setting
from yys.yys_mission_run import main_mission
from yys.yys_ghost_run import ghost_hit
from yys.yys_fight_run import one_fight, two_fight
from common.wechat_services import mcy_send_notice
from common.common_utils import get_average, time_format, shutdown_pc
from yys.yys_utils import find_windows


class McyYysScript:
    def __init__(self, count=1, fight_sec=7, fight_type=1, fight_to=1):
        runtime_setting.fight_type = fight_type
        runtime_setting.fight_to = fight_to
        runtime_setting.fight_sec = fight_sec
        self.count = count          # 战斗总轮数
        self.content_str = ""       # 日志记录
        self.windows_no = find_windows()        # 窗口总数 == 0 说明有问题

    def fight_begin(self):
        # 主线
        if runtime_setting.fight_to == 3:    
            return main_mission()
        
        # 百鬼
        elif runtime_setting.fight_to == 5:
            return ghost_hit() == ""

        # 个人或组队
        elif runtime_setting.fight_type == 1 or runtime_setting.fight_type == 3:
            return one_fight()
            
        # 双号单刷
        elif runtime_setting.fight_type == 5:
            return two_fight()
        
        return False

    # 开始刷
    def gan_begin(self):
        
        time_list = []
        result_flag = False

        for i in range(self.count):
            result_flag = False
            start_time = time.time()
            runtime_setting.current_time = i + 1
            self.content_str = "===第" + str(runtime_setting.current_time) + "次, 共" + str(self.count) + "次==="
            print(self.content_str)

            # 开始战斗
            if not self.fight_begin():
                break
            
            end_time = time.time()

            # 邮件部分
            time_list.append(end_time - start_time)
            avg_time = get_average(time_list)
            # 主线不发消息
            if runtime_setting.fight_to != 3 and ((i + 1) % 10) == 0 and (i + 1) != self.count:
                time_str = "\n已耗时：" + time_format(end_time - all_start_time)
                time_str += "\n平均单次耗时：" + time_format(avg_time)
                time_str += "\n预计结束时间：" + time_format(avg_time * (self.count - i - 1))
                mcy_send_notice(self.content_str + time_str, 3)

            print("===单次耗时：", time_format(end_time - start_time), "平均耗时：", time_format(avg_time))
            result_flag = True

        print("=====结束=====")
        return result_flag

    # 主入口
    def gan_init(self):
        if self.windows_no == 0:
            raise RuntimeError("未检测到游戏窗口")

        if self.windows_no == 1 and runtime_setting.fight_type in [3, 5]:
            raise RuntimeError("只检测到一个游戏窗口")

        # 战斗开始入口
        return self.gan_begin()           


if __name__ == '__main__':
    f_ready = -1
    fight_list = runtime_setting.fight_setting_list
    input_list = []
    input_str = ''
    for index, v in enumerate(fight_list):
        input_list.append(str(index))
        input_str += f'{index}: {v["desc"]}-{v["fight_sec"]}s\n'
    input_str += "请选择: "

    while f_ready not in input_list:
        f_ready = input(input_str)

    fight = runtime_setting.fight_setting_list[int(f_ready)]
    f_type = fight["fight_type"]
    f_to = fight["fight_to"]
    f_sec = fight["fight_sec"]

    change_times = 1
    change_times_temp = input(f"战斗次数(默认{change_times}次): ")
    f_times = int(change_times_temp) if change_times_temp != '' and change_times_temp.isdigit() else change_times

    f_sec_temp = input(f"战斗时间(默认{f_sec}s): ")
    f_sec = int(f_sec_temp) if f_sec_temp != '' and f_sec_temp.isdigit() else f_sec

    shutdown_flag = input("1-不关机(默认) 2-关机: ")

    try:
        all_start_time = time.time()
        yys_handler = McyYysScript(count=f_times, fight_sec=f_sec, fight_type=f_type, fight_to=f_to)
        res = yys_handler.gan_init()
        all_end_time = time.time()
        if res:
            mcy_send_notice("成功刷完" + str(f_times) + "次，耗时：" + time_format(all_end_time - all_start_time), 1)

    except KeyboardInterrupt:
        print("键盘打断，退出")
        sys.exit(0)
    except Exception as e:
        print("发生错误：", e)
        mcy_send_notice("出错了：" + str(e), 2)
    finally:
        if shutdown_flag == "2":
            delay_time = 600
            mcy_send_notice(str(delay_time) + "秒倒计时关机！", 4)
            shutdown_pc(delay_time)
