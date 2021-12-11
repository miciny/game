from yys.Utils import get_pic_list_pos, click_screen


def ghost_thing():
    while True:
        the_list = ["loss_choose_shuangxue", "goin", "blank_1", "blank_2", "fight_1", "fight_boss",
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


if __name__ == '__main__':
    ghost_thing()
