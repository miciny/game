import time
from common.common_utils import screen_shot
from common.gui_utils import *

width, height = auto.size()
pic_region = (0, 0, width, height)


def single_run():
    input_page = get_pic_position("input_1", 'deal_smoke/pic', pic_region)
    if not input_page:
        return 1
    click_screen(input_page, delay_sec=1)

    auto_input('6901028' + '315005')

    time.sleep(1)

    auto_key("enter")

    time.sleep(1)

    get_pay_page = get_pic_position("get_pay", 'deal_smoke/pic', pic_region)
    if not get_pay_page:
        return 2
    click_screen(get_pay_page, delay_sec=1)

    cash_page = get_pic_position("cash", 'deal_smoke/pic', pic_region)
    if not cash_page:
        return 3
    click_screen(cash_page, delay_sec=1)

    cash_confirm_page = get_pic_position("cash_confirm", 'deal_smoke/pic', pic_region)
    if not cash_confirm_page:
        return 4
    click_screen(cash_confirm_page, delay_sec=1)

    time.sleep(1)
    input_page = get_pic_position("input_1", 'deal_smoke/pic', pic_region)
    if not input_page:
        return 5

    return 0


def get_pay_info():
    pay_info_page = get_pic_position("pay_info", 'deal_smoke/pic', pic_region)
    if not pay_info_page:
        return 6
    click_screen(pay_info_page, delay_sec=1)

    pic_path = screen_shot()

    pay_info_back_page = get_pic_position("pay_info_back", 'deal_smoke/pic', pic_region)
    if not pay_info_back_page:
        return 7
    click_screen(pay_info_back_page, delay_sec=1)

    time.sleep(1)
    input_page = get_pic_position("input_1", 'deal_smoke/pic', pic_region)
    if not input_page:
        return 8

    return pic_path
