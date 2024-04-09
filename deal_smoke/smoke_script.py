import time
import requests
from common.wechat_services import send_wechat_notice
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
            raise Exception("现金支付，没找到收款确认")
        click_screen(cash_confirm_page, delay_sec=1)
        time.sleep(1)

        # 检查输入框，是不是在首页
        input_page = get_pic_position("input_1", 'deal_smoke/pic', pic_region)
        if not input_page:
            raise Exception("现金收款完成，但不在首页")
        return True

    # 微信
    else:
        # pay_no = ""
        for i in range(15 * 60):
            # 检查输入框，是不是在首页,在首页，说明有人支付了
            input_page = get_pic_position("input_1", 'deal_smoke/pic', pic_region)
            if input_page:
                return True

            # 没在首页，则请求支付码，有支付码了，就走后面的自动填写流程
            # res = get_pay_no()
            # if res and res['code'] == 0:
            #     pay_no = res['data']
            #     if pay_no and str(pay_no) == 18:
            #         break
                
            # 如果一直没人理，发消息
            if int(i / 60) > 0 and int(i % 60) == 0 and int(i / 60) % 3 == 0:
                send_wechat_notice("支付提醒", "请手动完成微信支付", user_name='ZhangGongZhu|LengYueHanShuang')
            time.sleep(1)
        return False

        # if not pay_no:
        #     send_wechat_notice("支付提醒", "请手动完成微信支付", user_name='ZhangGongZhu|LengYueHanShuang')
        #     return False

        # auto_input(pay_no)
        # time.sleep(1)

        # 收款确认
        # cash_confirm_page = get_pic_position("cash_confirm", 'deal_smoke/pic', pic_region)
        # if not cash_confirm_page:
        #     raise Exception("微信支付，没找到收款确认")
        # click_screen(cash_confirm_page, delay_sec=1)
        # time.sleep(5)
        #
        # not_found = 0
        # for i in range(30):
        #     # 有个收款查询，需要点击，不成功的情况下，会一直有这个按钮
        #     pay_check_page = get_pic_position("pay_check", 'deal_smoke/pic', pic_region)
        #     if pay_check_page:
        #         click_screen(pay_check_page, delay_sec=1)
        #         not_found = 0
        #     else:
        #         # 如果没有查询按钮，检查是不是在首页，在首页说明成功了
        #         input_page = get_pic_position("input_1", 'deal_smoke/pic', pic_region)
        #         if input_page:
        #             return True
        #
        #         # 也不在首页，那就试四次
        #         not_found += 1
        #         if not_found > 2:
        #             return False
        #     time.sleep(5)


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

    # 总的收款图
    pay_total_page = get_pic_position("pay_total", 'deal_smoke/pic', pic_region)
    if pay_total_page:
        pay_total_page = (pay_total_page[0] - 480,
                          pay_total_page[1] - 24,
                          pay_total_page[2] + 370 * 2,
                          pay_total_page[3] + 650,)
        screen_shot(pay_total_page, 'pay_total_info')

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


def send_pay_info_image(user_name):
    pic_path = "D:\Project\game\Logs\pay_total_info.png"
    if os.path.exists(pic_path):
        server_pic_path = wx_upload_pic(pic_path)
        print("server_pic_path", server_pic_path)
        if server_pic_path:
            set_this_time_stock(server_pic_path, get_type="5", user_name=user_name)


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


# 2成功更新商品 5上传的支付图片发送给用户 item_id是服务器图片地址
def set_this_time_stock(item_id, get_type="2", user_name=""):
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': get_type,
        'user_name': user_name,
        'id': item_id
    }
    res = requests.post(url, json=para_data)
    print(res)
    if res.status_code == 200:
        return res.json()
    return None


# 3获取支付码 4获取token
def get_pay_no(get_type="3"):
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': get_type
    }
    res = requests.post(url, json=para_data)
    print(res.text)
    if res.status_code == 200:
        return res.json()
    return None


def wx_upload_pic(pic_path):
    try:
        url = "https://www.xlovem.club/v1/file/upload"
        with open(pic_path, 'rb') as file:
            res = requests.post(url, files={'file': file})
            j_data = res.json()
            print('wx_upload_pic', j_data)
            if j_data['code'] == 0:
                return j_data['data']
        return None
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    send_pay_info_image("MaoCaiYuan")