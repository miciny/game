# -*- coding: UTF-8 -*-
import random
from CommonFuncs import *
from Config import *


class McyYysScript:
    def __init__(self, count=1, fight_sec=7, fight_type=1, fight_to=1, fight_list=None):
        self.count = count
        self.fight_sec = fight_sec
        self.fight_type = fight_type
        self.current_index = 0
        self.current_screen = 0
        self.content_str = ""
        self.fight_to = fight_to
        self.fight_list = fight_list

        # 第一个窗口，离原点的位置
        self.det_one_x = 0
        self.det_one_y = 0
        # 第二个窗口，离原点的位置
        self.det_two_x = 0
        self.det_two_y = 0
        self.init_windows()

    # 自动寻找两个窗口的点
    def init_windows(self):
        window_1_pos = self.get_pic_pos("window_1", center=False) or self.get_pic_pos("window_11", center=False)
        window_2_pos = self.get_pic_pos("window_2", center=False) or self.get_pic_pos("window_22", center=False)
        if window_1_pos is None and window_2_pos is None:
            print("请不要遮挡左上角logo")
            return
        if window_1_pos is None and window_2_pos is not None:
            print("没有找到第一个游戏窗口")
            self.det_one_x = window_2_pos[0] - 5
            self.det_one_y = window_2_pos[1] - 5
            return
        if window_1_pos is not None and window_2_pos is None:
            print("没有找到第二个游戏窗口")
            self.det_one_x = window_1_pos[0] - 5
            self.det_one_y = window_1_pos[1] - 5
            return
        if window_1_pos is not None and window_2_pos is not None:
            self.det_one_x = window_1_pos[0] - 5
            self.det_one_y = window_1_pos[1] - 5
            self.det_two_x = window_2_pos[0] - 5
            self.det_two_y = window_2_pos[1] - 5
            if self.det_two_y < self.det_one_y:
                print("位置切换，位置高的为第一个窗口")
                self.det_one_x, self.det_two_x = self.det_two_x, self.det_one_x
                self.det_one_y, self.det_two_y = self.det_two_y, self.det_one_y

    # 检测图片，返回中心点 或 None
    def get_pic_pos(self, pic_name, center=True):
        pic_path = os.path.join(self_path, "YysImage\\" + pic_name + ".png")
        print(str(self.current_screen), '屏幕，检测图片: ', pic_path)
        if self.current_screen == 1:
            pic_region = (self.det_one_x, self.det_one_y, screen_width, screen_height)
        elif self.current_screen == 2:
            pic_region = (self.det_two_x, self.det_two_y, screen_width, screen_height)
        else:
            width, height = auto.size()
            pic_region = (0, 0, width, height)
        if center:
            return auto.locateCenterOnScreen(pic_path, region=pic_region, confidence=confidence_setting, grayscale=True)
        else:
            return auto.locateOnScreen(pic_path, region=pic_region, confidence=confidence_setting, grayscale=True)

    # 检测是否出现了接收按钮 确认按钮
    def check_other_btn(self):
        res_pos = self.get_pic_pos("confirm")
        if res_pos:
            click_screen(res_pos, "点击确认")
        res_pos = self.get_pic_pos("accept")
        if res_pos:
            click_screen(res_pos, "点击确认")

    # 应该是可以通用的 返回是否结束，结束图片有两个，一个刚结束，一个结束了出现了奖励，底色不一样
    def check_finish(self):
        res_pos = self.get_pic_pos("finish_check_1") or self.get_pic_pos("finish_check_2") or self.get_pic_pos("finish_yl")
        return True if res_pos is not None else False

    # 切换两个游戏窗口的位置
    def switch_screen_by_pos(self):
        if self.current_screen == 1:
            click_x = self.det_one_x + 80
            click_y = self.det_one_y + 10
        else:
            click_x = self.det_two_x + 80
            click_y = self.det_two_y + 10
        return [click_x, click_y]

    # 点击切换游戏屏幕
    def switch_screen_click(self, to_screen):
        if to_screen == 1:
            self.current_screen = 1
            click_pos = self.switch_screen_by_pos()
        else:
            self.current_screen = 2
            click_pos = self.switch_screen_by_pos()
        click_screen(click_pos, "切换到第 " + str(self.current_screen) + " 个窗口！位置：", delay_sec=1)

    # 1战斗结束, 2战斗中，[3, 4, 5, 6]觉醒切换位置，点击屏幕的位置
    def fight_click_pos(self, pos_type=1):
        if pos_type == 2:
            click_x = screen_width * 0.5 + random.randint(-int(0.1 * screen_width), int(0.1 * screen_width))
            click_y = screen_height * 0.5 + random.randint(-int(0.17 * screen_height), int(0.17 * screen_width))
        elif pos_type in [3, 4, 5, 6]:
            click_x = screen_width * 0.05769
            click_y = screen_height * 0.29455 + (screen_height * 0.17) * (pos_type - 3)
        else:
            click_x = screen_width * 0.83333 + random.randint(10, 150)
            click_y = screen_height * 0.6596 + random.randint(-90, 70)
        if self.current_screen == 1:
            return [click_x + self.det_one_x, click_y + self.det_one_y]
        else:
            return [click_x + self.det_two_x, click_y + self.det_two_y]

    # 百鬼的一些位置，1开始，2选择三个鬼王随机，3鬼王选择后的开始，4选择鬼王后，确保已选中，检测下，5结束检测图
    # 6如果在百鬼结束页，点击空白的位置，7豆的位置，把它拖到10个豆
    # 其他是砸豆的位置随机
    def ghost_hit_pos(self, pos_type=1):
        if pos_type == 1:
            return self.get_pic_pos("ghost_add")
        elif pos_type == 2:
            index = random.randint(-1, 1)
            click_x = screen_width / 2 + screen_width * 0.30873 * index
            click_y = screen_height * 0.677
        elif pos_type == 3:
            return self.get_pic_pos("ghost_begin")
        elif pos_type == 4:
            return self.get_pic_pos("ghost_selected")
        elif pos_type == 5:
            return self.get_pic_pos("ghost_finish")
        elif pos_type == 6:
            click_x = screen_width / 5
            click_y = 80
        elif pos_type == 7:
            return self.get_pic_pos("ghost_bean_no")
        elif pos_type == 8:
            return self.get_pic_pos("frozen")
        else:
            wight = int(screen_width * 0.45)
            index = random.randint(-wight, wight)
            click_x = screen_width / 2 + index
            click_y = screen_height * 0.594
        if self.current_screen == 1:
            return [click_x + self.det_one_x, click_y + self.det_one_y]
        else:
            return [click_x + self.det_two_x, click_y + self.det_two_y]

    # 主线任务的点击点
    def ghost_main_mission_pos(self, main_check=False):
        if not main_check:
            for i in range(1, 7):
                res_pos = self.get_pic_pos("mission_" + str(i))
                if res_pos:
                    return res_pos
            else:
                return None
        else:
            return self.get_pic_pos("main_plus")

    # 关闭加成
    def close_hun_plus(self, open_flag=False, hun_flag=True):
        hun_plus_pos = self.get_pic_pos("hun_plus")
        if hun_plus_pos:
            click_screen(hun_plus_pos, "点击进入加成选择页", 1)
        if hun_flag:
            hun_plus_close_pos = self.get_pic_pos("hun_plus_close", center=False)
            if hun_plus_close_pos:
                click_pos = [hun_plus_close_pos[0] + hun_plus_close_pos[2] + 10,
                             hun_plus_close_pos[1] + hun_plus_close_pos[3] / 2]
                click_screen(click_pos, "点击关闭加成", 1)
                if open_flag:
                    click_screen(hun_plus_pos, "点击关闭页面", 1)
        else:
            awake_plus_close_pos = self.get_pic_pos("awake_plus_close", center=False)
            if awake_plus_close_pos:
                click_pos = [awake_plus_close_pos[0] + awake_plus_close_pos[2] + 10,
                             awake_plus_close_pos[1] + awake_plus_close_pos[3] / 2]
                click_screen(click_pos, "点击关闭加成", 1)
                if open_flag:
                    click_screen(hun_plus_pos, "点击关闭页面", 1)

    # 结束时的点击，检测不到结束图片，就结束
    def final_click(self, index_check=True):
        if index_check:
            print("随机点击最多30次屏幕，为了返回首页")
            for _ in range(30):
                click_pos = self.fight_click_pos(1)
                click_screen(click_pos, "点击屏幕！位置：", random.randint(5, 8) / 8)
                if not self.check_finish():
                    break
        else:
            print("随机点击最多5次屏幕，由于是首次，不检测图片")
            for _ in range(5):
                click_pos = self.fight_click_pos(1)
                click_screen(click_pos, "点击屏幕！位置：", random.randint(5, 8) / 8)

    # 战斗中的点击
    def fighting_click(self):
        if self.fight_sec < 12:
            print_wait(self.fight_sec, "时间太短，不点击屏幕：")
            return
        click_time = random.randint(1, 2)
        print("战斗中！随机点击", click_time, "次屏幕")
        for i in range(click_time):
            print("战斗中点击屏幕，第", i + 1, "次, 共", click_time, "次")
            time_wait_single = self.fight_sec / click_time / 2
            print_wait(time_wait_single, "等待点击战斗中屏幕")
            single_click_time = random.randint(1, 3)
            for j in range(single_click_time):
                click_pos = self.fight_click_pos(2)  # 只点击第一个屏幕的
                click_screen(click_pos, "点击屏幕！位置：", random.randint(5, 8) / random.randint(50, 100) / (i + 1))
            print_wait(time_wait_single, "等待")

    # 返回是否在主页，组队的话，只有一种图片，个人的话，都用挑战检测
    def check_back_main(self):
        pic_name = "group"
        if self.fight_type == 1 or self.fight_type == 5:
            pic_name = "single"
        the_pos = self.get_pic_pos(pic_name)
        return [the_pos.x + random.randint(-10, 10), the_pos.y + random.randint(-5, 10)] if the_pos else None

    # 检测主页面，失败了就重试三次，每次重新点击第一个屏幕和第二个屏幕
    def check_main_false(self):
        for i in range(3):
            print("检测" + str(self.current_screen) + "屏幕是否到主页！第", i + 1, "次")
            main_check = self.check_back_main()
            if not main_check:
                print("没有回到主页")
                self.check_other_btn()
                print_wait(3, "等待")
                self.final_click()
                if self.fight_type == 3:
                    self.switch_screen_click(to_screen=2)
                    self.check_other_btn()
                    self.final_click()
                    self.switch_screen_click(to_screen=1)
            else:
                print("回到主页")
                return main_check
        return None

    # 检测主页面，主要用在点击开始后，实际没开始的情况
    def check_main_true_operation(self, start_pos):
        click_screen(start_pos, "点击开始战斗！位置：")
        print_wait(3, "等待检测是否真的开始")
        for i in range(3):
            print("检测是否真的开始！第", i, "次")
            start_pos = self.check_back_main()
            if not start_pos:
                print("没有在主页，继续")
                return True
            else:
                print("还在主页，检查是否有其他按钮遮挡，然后重新点击开始按钮")
                self.check_other_btn()
                if self.fight_type == 3:
                    self.switch_screen_click(to_screen=2)
                    self.check_other_btn()
                    self.switch_screen_click(to_screen=1)
                click_screen(start_pos, "点击开始战斗！位置：")
                print_wait(3, "等待")
        return False

    # 检测是否结束，失败了就重试，重试次数是 fight_sec / 2， 每次睡三秒
    def check_finish_false_operation(self):
        print_wait(1, "等待检测是否结束")
        count = int(self.fight_sec / 2)
        for i in range(count):
            print("检测是否结束：", i, "/", count)
            finish_check = self.check_finish()
            if not finish_check:
                if self.fight_type == 1:
                    start_pos = self.check_back_main()
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

    # 切换窗口 - 点击开始 - 开始的检测
    def switch_and_begin(self, to_screen):
        self.switch_screen_click(to_screen)
        # 检查是否到首页了
        start_pos = self.check_main_false()
        if not start_pos:
            mcy_send_mail(self.content_str + "<br>第" + str(self.current_screen) + "个游戏似乎出错了，没有回到主页！", 2)
            return False
        not_main_check = self.check_main_true_operation(start_pos)
        if not not_main_check:
            mcy_send_mail(self.content_str + "<br>第" + str(self.current_screen) + "个游戏似乎出错了，没有真的开始！", 2)
            return False
        return True

    # 切换窗口 - 检测结束
    def switch_and_finish(self, to_screen, finish_check=True, index_check=True):
        self.switch_screen_click(to_screen)
        # 检查是否结束了
        if finish_check:
            self.check_finish_false_operation()
        self.final_click(index_check)

    # 关闭加成，灰度检测，所以可开可关
    def close_plus_operation(self, open_flag=False):
        if (self.fight_type == 1 or self.fight_type == 3) and (self.fight_to == 1 or self.fight_to == 4):
            hun_flag = True
            if self.fight_to == 4:
                hun_flag = False
            self.switch_screen_click(1)
            self.close_hun_plus(open_flag, hun_flag)
            if self.fight_type == 3:
                self.switch_screen_click(2)
                self.close_hun_plus(hun_flag=hun_flag)

    # 组队，第一次的邀请 接受
    def invite_accept_operation(self):
        self.switch_screen_click(1)
        auto_invite_select_pos = self.get_pic_pos("auto_invite_select", center=False)
        if auto_invite_select_pos:
            auto_invite_select_pos_r = [auto_invite_select_pos[0] + 5,
                                        auto_invite_select_pos[1] + auto_invite_select_pos[3] / 2]
            click_screen(auto_invite_select_pos_r, "点击选择默认邀请", delay_sec=1)

            auto_invite_btn_pos = self.get_pic_pos("auto_invite_btn")
            if auto_invite_btn_pos:
                click_screen(auto_invite_btn_pos, "点击邀请确认", delay_sec=3)

                self.switch_screen_click(2)
                auto_accept_invite_btn_pos = self.get_pic_pos("auto_accept_invite_btn")
                if auto_accept_invite_btn_pos:
                    click_screen(auto_accept_invite_btn_pos, "点击被邀请确认", delay_sec=3)
        else:
            print("没有弹出邀请弹窗")

    # 两个分开单刷，基本上只用在业原火yyh
    def two_fight(self, two_flags):
        if two_flags[0]:
            two_flags[0] = self.switch_and_begin(1)  # 第一个屏幕
        if two_flags[1]:
            two_flags[1] = self.switch_and_begin(2)  # 第二个屏幕
        print_wait(self.fight_sec, "等待检测：")
        if two_flags[0]:
            self.switch_and_finish(1)  # 第一个屏幕
        if two_flags[1]:
            self.switch_and_finish(2)  # 第二个屏幕
        return two_flags[0] or two_flags[1]

    # 单刷或组队
    def one_fight(self):
        begin_flag = self.switch_and_begin(1)
        if not begin_flag:
            return False
        self.fighting_click()

        # 检查是否结束了
        if self.current_index == 0 and self.fight_type == 3:
            self.switch_and_finish(1, index_check=False)
        else:
            self.switch_and_finish(1)
        if self.fight_type == 3:
            self.switch_and_finish(2, finish_check=False)
        return True

    # 砸百鬼, 目前只能单砸
    def ghost_hit(self):
        hit_res = ""
        try:
            self.switch_screen_click(1)
            add_pos = self.ghost_hit_pos(pos_type=1)
            if not add_pos:
                hit_res = "没有在首页"
                return hit_res
            click_screen(add_pos, "点击首页的开始", delay_sec=3)

            for i in range(3):
                select_pos = self.ghost_hit_pos(pos_type=2)
                click_screen(select_pos, "随机选择一个鬼王", delay_sec=1)

                selected_pos = self.ghost_hit_pos(pos_type=4)
                if selected_pos:
                    break
                if i == 1:
                    self.check_other_btn()
                if i == 2:
                    hit_res = "选择鬼王不成功"
                    return hit_res

            begin_pos = self.ghost_hit_pos(pos_type=3)
            if not begin_pos:
                hit_res = "没有在开始页"
                return hit_res
            click_screen(begin_pos, "点击开始", delay_sec=3)

            # 拖动将豆拖到10
            bean_pos = self.ghost_hit_pos(7)
            if bean_pos:
                auto.moveTo(bean_pos[0], bean_pos[1])
                auto.dragTo(bean_pos[0] + 230, bean_pos[1], duration=1)

            hit_times = 200
            for i in range(hit_times):
                frozen_status = self.ghost_hit_pos(8)
                if frozen_status:
                    print_wait(3, "等待冰冻3秒")
                hit_pos = self.ghost_hit_pos(10)
                click_screen(hit_pos, "砸百鬼：", 0.15)
                finish_flag = self.ghost_hit_pos(1) or self.ghost_hit_pos(5)
                if finish_flag:
                    break
                if i == hit_times - 1:
                    hit_res = "似乎出了问题，一直没砸完，或是进入不可知页面"
                    return hit_res

            print_wait(1, "等待一秒")
            for i in range(10):
                finish_flag = self.ghost_hit_pos(5)
                if finish_flag:
                    click_pos = self.ghost_hit_pos(6)
                    click_screen(click_pos, "点击结束", delay_sec=1)
                    click_screen(click_pos, "点击结束", delay_sec=1)

                begin_flag = self.ghost_hit_pos(1)
                if begin_flag:
                    return hit_res
                else:
                    self.check_other_btn()
            hit_res = "检测不到回到了首页"
            return hit_res
        finally:
            if hit_res != "":
                mcy_send_mail(self.content_str + "<br>砸百鬼出错了：" + hit_res, 2)

    # 新号做主线任务
    def main_mission(self):
        for i in range(self.count*4):
            pic_pos = self.ghost_main_mission_pos()
            if pic_pos:
                click_screen(pic_pos, "点击屏幕", 1)
            else:
                print_wait(3, "等待点击")
                main_pic_pos = self.ghost_main_mission_pos(True)
                if main_pic_pos:
                    print("已回到首页，停止")
                    return False
                click_screen(self.fight_click_pos(2), "没有可点击的，随机点", 1)
        return True

    # 判断是四个轮着刷觉醒 还是 其他的
    def gan_init(self):
        # 单刷觉醒，四个轮着来刷, fight_list=[1, 2, 3, 4]
        if self.fight_type == 1 and self.fight_to == 4 and self.fight_list is not None:
            for item in self.fight_list:
                click_pos = self.fight_click_pos(item + 2)
                click_screen(click_pos, "切换到第" + str(item) + "个觉醒！位置：", 1)
                if not self.gan_begin():
                    return False
            return True
        elif self.fight_type == 7:
            return self.main_mission()
        else:
            return self.gan_begin()

    def gan_to_path(self):
        self.switch_screen_click(to_screen=1)
        if self.fight_type == 9:
            ding_pos = self.get_pic_pos("ding")                                        # ##
            if ding_pos:
                click_screen(ding_pos, "点击进入町中！位置：", 3)
            ghost_hit_chose_pos = self.get_pic_pos("ghost_hit")
            if ghost_hit_chose_pos:
                click_screen(ghost_hit_chose_pos, "点击百鬼页！位置：", 1)
        elif self.fight_type == 1 or self.fight_type == 3 or self.fight_type == 5:
            tan_suo_pos = self.get_pic_pos("tan_suo")
            if tan_suo_pos:
                click_screen(tan_suo_pos, "点击进入探索！位置：", 3)
            if self.fight_to == 4:
                awake_choose_pos = self.get_pic_pos("awake_choose")
                if awake_choose_pos:
                    click_screen(awake_choose_pos, "点击进入觉醒材料！位置：", 2)
                fire_awake_pos = self.get_pic_pos("fire_awake")
                if fire_awake_pos:
                    click_screen(fire_awake_pos, "点击进入觉醒准备页！位置：", 2)
            else:
                hun_choose_pos = self.get_pic_pos("hun_choose")
                if hun_choose_pos:
                    click_screen(hun_choose_pos, "点击进入御魂！位置：", 2)
                if self.fight_to == 1:
                    hun_type_one_pos = self.get_pic_pos("hun_type_one")
                    if hun_type_one_pos:
                        click_screen(hun_type_one_pos, "点击进入八岐大蛇！位置：", 1)
                elif self.fight_to == 2:
                    hun_type_two_pos = self.get_pic_pos("hun_type_two")
                    if hun_type_two_pos:
                        click_screen(hun_type_two_pos, "点击进入业原火！位置：", 1)
                elif self.fight_to == 3:
                    hun_type_third_pos = self.get_pic_pos("hun_type_third")          # ##
                    if hun_type_third_pos:
                        click_screen(hun_type_third_pos, "点击进入日轮！位置：", 1)
        if self.fight_type == 5:
            self.switch_screen_click(to_screen=2)
            tan_suo_pos = self.get_pic_pos("tan_suo")
            if tan_suo_pos:
                click_screen(tan_suo_pos, "点击进入探索！位置：", 3)
            hun_choose_pos = self.get_pic_pos("hun_choose")
            if hun_choose_pos:
                click_screen(hun_choose_pos, "点击进入御魂！位置：", 1)
            hun_type_two_pos = self.get_pic_pos("hun_type_two")
            if hun_type_two_pos:
                click_screen(hun_type_two_pos, "点击进入业原火！位置：", 1)
            self.switch_screen_click(to_screen=1)

        if self.fight_type == 3:
            group_choose_pos = self.get_pic_pos("group_choose")
            if group_choose_pos:
                click_screen(group_choose_pos, "点击进入组队页！位置：", 2)
            group_create_pos = self.get_pic_pos("group_create")
            if group_create_pos:
                click_screen(group_create_pos, "点击创建队伍！位置：", 1)
            group_create_confirm_pos = self.get_pic_pos("group_create_confirm")
            if group_create_confirm_pos:
                click_screen(group_create_confirm_pos, "点击创建！位置：", 1)
            invite_to_pos = self.get_pic_pos("invite_to")
            if invite_to_pos:
                click_screen(invite_to_pos, "点击邀请！位置：", 1)
            love_xm_pos = self.get_pic_pos("xm")                                   # ##
            if love_xm_pos:
                click_screen(love_xm_pos, "点击邀请XM！位置：", 1)
            invite_confirm_pos = self.get_pic_pos("invite_confirm")
            if invite_confirm_pos:
                click_screen(invite_confirm_pos, "点击邀请确认！位置：", 1)

            self.switch_screen_click(to_screen=2)
            invite_accept_pos = self.get_pic_pos("invite_accept")
            if invite_accept_pos:
                click_screen(invite_accept_pos, "点击接受邀请！位置：", 1)
            self.switch_screen_click(to_screen=1)

    # 刷
    def gan_begin(self):
        two_flags = [True, True]
        time_list = []
        result_flag = False

        self.gan_to_path()

        # 开加成
        self.close_plus_operation(True)

        for i in range(self.count):
            result_flag = False
            start_time = time.time()
            self.content_str = "==========第" + str(i + 1) + "次, 共" + str(self.count) + "次=========="
            self.current_index = i
            print(self.content_str)

            if self.fight_type == 1 or self.fight_type == 3:
                if not self.one_fight():
                    break
            elif self.fight_type == 5:
                if not self.two_fight(two_flags):
                    break
            elif self.fight_type == 9:
                res_str = self.ghost_hit()
                if res_str != "":
                    break
            end_time = time.time()

            # 第一次的邀请 接受
            if self.fight_type == 3 and i == 0:
                self.invite_accept_operation()

            # 邮件部分
            time_list.append(end_time - start_time)
            avg_time = get_average(time_list)
            if self.fight_type != 7 and ((i + 1) % 10) == 0 and (i + 1) != self.count:
                time_str = "<br>已耗时：" + time_format(end_time - all_start_time)
                time_str += "<br>平均单次耗时：" + time_format(avg_time)
                time_str += "<br>预计结束时间：" + time_format(avg_time * (self.count - i - 1))
                mcy_send_mail(self.content_str + time_str, 3)

            print("==========单次耗时：", time_format(end_time - start_time), "平均耗时：", time_format(avg_time))
            result_flag = True

        # 关加成
        self.close_plus_operation()

        print("===========结束==========")
        return result_flag


if __name__ == '__main__':
    fight_setting_list = [fight_1, fight_2, fight_3, fight_4, fight_5, fight_6, fight_7, fight_8]
    f_ready = -1
    f_list = []
    f_type = -1
    f_to = -1
    f_times = -1
    f_sec = -1
    while f_ready not in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]:
        f_ready = input("0: 组队-魂土-"+str(fight_setting_list[0]['times'])+"次\n"
                        "1: 组队-日轮-"+str(fight_setting_list[1]['times'])+"次\n"
                        "2: 双号-业原火-"+str(fight_setting_list[2]['times'])+"次\n"
                        "3: 单刷-业原火-"+str(fight_setting_list[3]['times'])+"次\n"
                        "4: 单刷-百鬼-"+str(fight_setting_list[4]['times'])+"次\n"
                        "5: 单刷-主线-"+str(fight_setting_list[5]['times'])+"次\n"
                        "6: 组队-觉醒-"+str(fight_setting_list[6]['times'])+"次\n"
                        "7: 单刷-觉醒(随机)-"+str(fight_setting_list[7]['times'])+"次\n"
                        "8: 手动选择启动\n"
                        "请选择: ")
        if f_ready == "8":
            while f_type not in ["1", "3", "5", "7", "9"] and f_to not in ["1", "2", "3", "4"]:
                f_type = input("1个人 3组队 5两个号分开刷 7主线 9百鬼: ")
                if f_type == "1":
                    f_to = input("1魂土 2业原火 3日轮 4觉醒: ")
                    if f_to == "4":
                        f_list_str = input("请选择打哪几个？输入1、2、3、4: ")
                        for i_to in range(1, 5):
                            if str(i_to) in f_list_str:
                                f_list.append(i_to)
            f_times = input("请输入次数: ")
            f_sec = input("请输入预计时长: ")
            f_type = int(f_type)
            f_to = int(f_to)
            f_times = int(f_times)
            f_sec = int(f_sec)
        else:
            fight = fight_setting_list[int(f_ready)]
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
            mcy_send_mail("成功刷完" + str(f_times) + "次，耗时：" + time_format(all_end_time - all_start_time), 1)

    except KeyboardInterrupt:
        print("键盘打断，退出")
        sys.exit(0)
    except Exception as e:
        print("发生错误：", e)
        mcy_send_mail("出错了：" + str(e), 2)
    finally:
        if shutdown_flag == "2":
            shutdown_pc()
