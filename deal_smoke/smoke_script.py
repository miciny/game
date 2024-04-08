import time
import requests
from common.common_utils import screen_shot
from common.gui_utils import *

width, height = auto.size()
pic_region = (0, 0, width, height)


# pay_type = 1 现金支付， 2 微信支付
def single_run(smoke_id, pay_type=1):
    if not smoke_id:
        raise Exception("没有找到可刷的商品")

    # 检查输入框，是不是在首页，在首页就点击
    input_page = get_pic_position("input_1", 'deal_smoke/pic', pic_region)
    if not input_page:
        raise Exception("不在首页")
    click_screen(input_page, delay_sec=1)

    # 输入编码
    auto_input(smoke_id)
    time.sleep(1)

    # 按回车，进到收银
    auto_key("enter")
    time.sleep(1)

    # 点击收银
    get_pay_page = get_pic_position("get_pay", 'deal_smoke/pic', pic_region)
    if not get_pay_page:
        raise Exception("收银按钮没找到")
    click_screen(get_pay_page, delay_sec=1)

    # 现金
    if pay_type == 1:
        # 选择现金
        cash_page = get_pic_position("cash", 'deal_smoke/pic', pic_region)
        if not cash_page:
            raise Exception("没找到现金选择按钮")
        click_screen(cash_page, delay_sec=1)

        # 收款确认
        cash_confirm_page = get_pic_position("cash_confirm", 'deal_smoke/pic', pic_region)
        if not cash_confirm_page:
            raise Exception("没找到现金确认")
        click_screen(cash_confirm_page, delay_sec=1)
        time.sleep(1)

        # 检查输入框，是不是在首页
        input_page = get_pic_position("input_1", 'deal_smoke/pic', pic_region)
        if not input_page:
            raise Exception("现金收款完成，但不在首页")
    
    # 微信
    else:
        pay_no = ""
        for i in range(300):
            res = get_pay_no()
            if res and res['code'] == 0:
                pay_no = res['data']
                if pay_no and str(pay_no) == 18:
                    break
            time.sleep(1)

        if not pay_no:
            raise Exception("没找到微信收款码")

        auto_input(pay_no)
        time.sleep(1)

        # 收款确认
        cash_confirm_page = get_pic_position("cash_confirm", 'deal_smoke/pic', pic_region)
        if not cash_confirm_page:
            raise Exception("没找到现金确认")
        click_screen(cash_confirm_page, delay_sec=1)
        time.sleep(5)

        not_found = 0
        for i in range(30):
            pay_check_page = get_pic_position("pay_check", 'deal_smoke/pic', pic_region)
            if pay_check_page:
                click_screen(pay_check_page, delay_sec=1)
                not_found = 0
            else:
                # 检查输入框，是不是在首页
                input_page = get_pic_position("input_1", 'deal_smoke/pic', pic_region)
                if not input_page:
                    not_found += 1
                if not_found > 2:
                    raise Exception("微信收款可能出现问题")
            time.sleep(5)


def get_pay_info():
    # 点击收款信息按钮
    pay_info_page = get_pic_position("pay_info", 'deal_smoke/pic', pic_region)
    if not pay_info_page:
        raise Exception("没找到收款信息按钮")
    click_screen(pay_info_page, delay_sec=1)

    # 微信 支付宝 现金收款的信息
    pic_path_1 = ""
    cash_pay_info_page = get_pic_position("cash_pay_info", 'deal_smoke/pic', pic_region, center=False)
    if cash_pay_info_page:
        cash_pay_info_page = (cash_pay_info_page[0],
                              cash_pay_info_page[1],
                              cash_pay_info_page[2] + 380,
                              cash_pay_info_page[3],)
        pic_path_1 = screen_shot(cash_pay_info_page, 'cash_pay_info')

    pic_path_2 = ""
    wx_pay_info_page = get_pic_position("wx_pay_info", 'deal_smoke/pic', pic_region, center=False)
    if wx_pay_info_page:
        wx_pay_info_page = (wx_pay_info_page[0],
                            wx_pay_info_page[1],
                            wx_pay_info_page[2] + 380,
                            wx_pay_info_page[3],)
        pic_path_2 = screen_shot(wx_pay_info_page, 'wx_pay_info')

    # 点击返回
    pay_info_back_page = get_pic_position("pay_info_back", 'deal_smoke/pic', pic_region)
    if not pay_info_back_page:
        raise Exception("没找到收款信息的返回按钮")
    click_screen(pay_info_back_page, delay_sec=1)
    time.sleep(1)

    # 检查输入框，是不是在首页
    input_page = get_pic_position("input_1", 'deal_smoke/pic', pic_region)
    if not input_page:
        raise Exception("获取收款信息完成，但没返回首页")

    return pic_path_1, pic_path_2


def get_this_time_info():
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': '1'
    }
    res = requests.post(url, json=para_data)
    print(res)
    if res.status_code == 200:
        return res.json()
    raise Exception("获取刷单信息失败")


def set_this_time_stock(item_id):
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': '2',
        'id': item_id
    }
    res = requests.post(url, json=para_data)
    print(res)
    if res.status_code == 200:
        return res.json()
    return None


def get_pay_no():
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': '3'
    }
    res = requests.post(url, json=para_data)
    print(res)
    if res.status_code == 200:
        return res.json()
    return None


if __name__ == '__main__':
    ret = get_this_time_info()
    print(ret)
