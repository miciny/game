# -*- coding: UTF-8 -*-
from common.common_utils import *
from yys.yys_utils import *
from yys import runtime_setting


class McyYysScript:
    def __init__(self, count=1, fight_sec=7, fight_type=1, fight_to=1, fight_list=None):
        runtime_setting.fight_type = fight_type
        runtime_setting.fight_to = fight_to
        runtime_setting.fight_sec = fight_sec

        self.count = count          # 战斗总轮数
        self.current_index = 0      # 战斗第几轮
        self.content_str = ""       # 日志记录
        self.fight_list = fight_list
        self.windows_no = find_windows()        # 窗口总数 == 0 说明有问题

    # 切换窗口 - 点击开始 - 开始的检测
    def switch_and_begin(self, to_screen):
        switch_screen_click(to_screen)
        # 检查是否到首页了
        start_pos = check_main_false()
        if not start_pos:
            mcy_send_notice(self.content_str + "\n第" + str(runtime_setting.current_screen) + "个游戏似乎出错了，没有回到主页！", 2)
            return False
        not_main_check = check_main_true_operation(start_pos)
        if not not_main_check:
            mcy_send_notice(self.content_str + "\n第" + str(runtime_setting.current_screen) + "个游戏似乎出错了，没有真的开始！", 2)
            return False
        return True

    # 两个分开单刷，基本上只用在业原火yyh
    def two_fight(self, two_flags):
        if two_flags[0]:
            two_flags[0] = self.switch_and_begin(1)  # 第一个屏幕
        if two_flags[1]:
            two_flags[1] = self.switch_and_begin(2)  # 第二个屏幕
        print_wait(runtime_setting.fight_sec, "等待战斗结束：")
        if two_flags[0]:
            switch_and_finish(1)  # 第一个屏幕
        if two_flags[1]:
            switch_and_finish(2)  # 第二个屏幕
        return two_flags[0] or two_flags[1]

    # 单刷或组队
    def one_fight(self):
        begin_flag = self.switch_and_begin(1)
        if not begin_flag:
            return False
        print_wait(runtime_setting.fight_sec, "等待战斗结束：")

        # 检查是否结束了
        switch_and_finish(1)
        if runtime_setting.fight_type == 3:
            switch_and_finish(2, finish_check=False)
        return True

    # 砸百鬼, 目前只能单砸
    def ghost_hit(self):
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
                mcy_send_notice(self.content_str + "\n砸百鬼出错了：" + hit_res, 2)

    # 新号做主线任务
    def main_mission(self):
        for i in range(self.count*4):
            pic_pos = ghost_main_mission_pos()
            if pic_pos:
                click_screen(pic_pos, "点击屏幕", 1)
            else:
                print_wait(3, "等待点击")
                main_pic_pos = ghost_main_mission_pos(True)
                if main_pic_pos:
                    print("已回到首页，停止")
                    return False
                click_screen(fight_click_pos(2), "没有可点击的，随机点", 1)
        return True

    # 开始刷
    def gan_begin(self):
        two_flags = [True, True]
        time_list = []
        result_flag = False

        for i in range(self.count):
            result_flag = False
            start_time = time.time()
            self.content_str = "===第" + str(i + 1) + "次, 共" + str(self.count) + "次==="
            self.current_index = i
            print(self.content_str)

            # 百鬼
            if runtime_setting.fight_to == 9:
                if self.ghost_hit() != "":
                    break

            # 个人或组队
            elif runtime_setting.fight_type == 1 or runtime_setting.fight_type == 3:
                if not self.one_fight():
                    break
                
            # 双号单刷
            elif runtime_setting.fight_type == 5:
                if not self.two_fight(two_flags):
                    break

            end_time = time.time()

            # 邮件部分
            time_list.append(end_time - start_time)
            avg_time = get_average(time_list)
            if runtime_setting.fight_to != 7 and ((i + 1) % 10) == 0 and (i + 1) != self.count:
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

        # 单刷觉醒，四个轮着来刷, fight_list=[1, 2, 3, 4]
        if runtime_setting.fight_type == 1 and runtime_setting.fight_to == 4 and self.fight_list is not None:
            for item in self.fight_list:
                click_pos = fight_click_pos(item + 2)
                click_screen(click_pos, "切换到第" + str(item) + "个觉醒！位置：", 1)
                if not self.gan_begin():      # 其他的战斗开始入口
                    return False
            return True
        elif runtime_setting.fight_to == 7:    # 主线
            return self.main_mission()
        else:
            return self.gan_begin()           # 其他的战斗开始入口


if __name__ == '__main__':
    f_ready = -1
    f_list = []
    f_type = -1
    f_to = -1
    f_times = -1
    f_sec = -1
    while f_ready not in ["0", "1", "2", "3", "4", "5", "6", "7"]:
        f_ready = input("0: 组队-魂土-"+str(runtime_setting.fight_setting_list[0]['times'])+"次\n"
                        "1: 组队-日轮-"+str(runtime_setting.fight_setting_list[1]['times'])+"次\n"
                        "2: 双号-业原火-"+str(runtime_setting.fight_setting_list[2]['times'])+"次\n"
                        "3: 单刷-业原火-"+str(runtime_setting.fight_setting_list[3]['times'])+"次\n"
                        "4: 单刷-百鬼-"+str(runtime_setting.fight_setting_list[4]['times'])+"次\n"
                        "5: 单刷-主线-"+str(runtime_setting.fight_setting_list[5]['times'])+"次\n"
                        "6: 组队-觉醒-"+str(runtime_setting.fight_setting_list[6]['times'])+"次\n"
                        "7: 单刷-觉醒(随机)-"+str(runtime_setting.fight_setting_list[7]['times'])+"次\n"
                        "请选择: ")

    fight = runtime_setting.fight_setting_list[int(f_ready)]
    f_list = fight["fight_list"]
    f_type = fight["fight_type"]
    f_to = fight["fight_to"]
    f_times = fight["times"]
    f_sec = fight["fight_sec"]

    need_change_times = input("1-不修改次数 2-修改次数: ")
    if need_change_times == "2":
        change_times = input("请输入修改的次数: ")
        f_times = int(change_times)

    shutdown_flag = input("1-不关机 2-关机: ")

    try:
        all_start_time = time.time()
        yys_handler = McyYysScript(count=f_times, fight_sec=f_sec, fight_type=f_type, fight_to=f_to, fight_list=f_list)
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
            shutdown_pc()
