from yys.CommonFuncs import shutdown_pc
from yys.Utils import get_pic_list_pos, click_screen
from yys.WechatServices import send_wechat_notice


def ghost_thing():
    while True:
        the_list = ["loss_choose_shuangxue", "goin", "blank_1", "blank_2", "blank_3", "fight_1", "fight_boss",
                    "go_on_1", "go_on_2", "boss_1"]
        res_pos = get_pic_list_pos(the_list)
        if res_pos:
            click_screen(res_pos)

        res_pos = get_pic_list_pos(["finish_check"])
        if res_pos:
            res_pos = get_pic_list_pos(["back_to"])
            click_screen(res_pos)

            res_pos = get_pic_list_pos(["finish"])
            click_screen(res_pos)


def ghost_thing_little():
    i = 0
    flag = 1
    run_flag = True
    while run_flag:
        the_list = ["loss_choose_jiuguan", "goin",
                    "forward", "fight_boss", "go_next",
                    "finish_check_1",
                    "go_on_1", "go_on_2", "boss_1", "leave",
                    "next_lvl_1", "fight_2", "fight_22", "fight_3", "fight_4",
                    "blank_33", "blank_44", "blank_55", "blank_66"]
        res_pos = get_pic_list_pos(the_list)
        if res_pos:
            flag = 1
            click_screen(res_pos)
            i += 1
            print(i)

        flag += 1
        if flag > 100:
            run_flag = False
            send_wechat_notice("error", "出错了!")


if __name__ == '__main__':
    # ghost_thing()
    ghost_thing_little()
    shutdown_pc()
