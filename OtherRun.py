import time
from yys.Utils import get_pic_list_pos, click_screen


def for_the_money():
    run_flag = True
    while run_flag:
        res_pos = get_pic_list_pos(["failed"], dir_name="OtherPics")
        if res_pos:
            res_pos = get_pic_list_pos(["cancel"], dir_name="OtherPics")
            click_screen(res_pos)

            res_pos = get_pic_list_pos(["goon"], dir_name="OtherPics")
            click_screen(res_pos)

            time.sleep(0.5)


if __name__ == '__main__':
    for_the_money()
