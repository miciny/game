import time
import easyocr
from common.wechat_services import send_wechat_notice, send_image
from common.common_utils import api_request
from common.gui_utils import *


# pay_type = 1 现金支付， 2 微信支付
def single_run(smoke_id, item_name, run_count, pay_type=1):
    if not smoke_id:
        raise Exception("没有找到可刷的商品")

    # 检查输入框，是不是在首页，在首页就点击
    input_page = get_pic_position("input_1", 'deal_smoke/pic')
    if not input_page:
        raise Exception("不在首页")
    click_screen(input_page, delay_sec=1)

    # 如果是微信 剩余库存大于2，则刷两个
    for _ in range(run_count):
        # 输入编码
        auto_input(smoke_id)
        time.sleep(1)
        # 按回车，进到收银
        auto_key("enter")
        time.sleep(1)

    # 点击收银
    get_pay_page = get_pic_position("get_pay", 'deal_smoke/pic')
    if not get_pay_page:
        raise Exception("收银按钮没找到")
    click_screen(get_pay_page, delay_sec=1)

    # 现金
    if pay_type == 1:
        # 选择现金
        cash_page = get_pic_position("cash", 'deal_smoke/pic')
        if not cash_page:
            raise Exception("没找到现金选择按钮")
        click_screen(cash_page, delay_sec=1)

        # 收款确认
        cash_confirm_page = get_pic_position("cash_confirm", 'deal_smoke/pic')
        if not cash_confirm_page:
            raise Exception("现金支付，没找到收款确认")
        click_screen(cash_confirm_page, delay_sec=1)
        time.sleep(1)

        # 检查输入框，是不是在首页
        input_page = get_pic_position("input_1", 'deal_smoke/pic')
        if not input_page:
            raise Exception("现金收款完成，但不在首页")
        return True

    # 微信
    else:
        pay_no = ""
        for i in range(50 * 60):
            # 检查输入框，是不是在首页,在首页，说明有人支付了
            input_page = get_pic_position("input_1", 'deal_smoke/pic')
            if input_page:
                return True

            # 没在首页，则请求支付码，有支付码了，就走后面的自动填写流程
            pay_no = get_pay_no()
            if pay_no:
                break
                
            # 如果一直没人理，3分钟发消息
            if int(i % 60) == 0 and int(i / 60) % 3 == 0:
                send_wechat_notice("支付提醒", f"{item_name} 请求支付中！\n请手动完成微信支付, 支付后返回到首页", user_name='ZhangGongZhu|LengYueHanShuang')
            time.sleep(1)

        if not pay_no:
            return False

        send_wechat_notice("支付提醒", f"{item_name} 自动微信支付中，请勿手动操作", user_name='ZhangGongZhu|LengYueHanShuang')
        auto_input(pay_no)
        time.sleep(1)

        # 收款确认
        cash_confirm_page = get_pic_position("cash_confirm", 'deal_smoke/pic')
        if not cash_confirm_page:
            raise Exception("微信支付，没找到收款确认")
        click_screen(cash_confirm_page, delay_sec=1)
        time.sleep(5)
        
        not_found = 0
        for i in range(30):
            # 有个收款查询，需要点击，不成功的情况下，会一直有这个按钮
            pay_check_page = get_pic_position("pay_check", 'deal_smoke/pic')
            if pay_check_page:
                click_screen(pay_check_page, delay_sec=1)
                not_found = 0
            else:
                # 如果没有查询按钮，检查是不是在首页，在首页说明成功了
                input_page = get_pic_position("input_1", 'deal_smoke/pic')
                if input_page:
                    return True
        
                # 也不在首页，那就试四次
                not_found += 1
                if not_found > 2:
                    return False
            time.sleep(5)


def get_pay_info():
    # 点击收款信息按钮
    pay_info_page = get_pic_position("pay_info", 'deal_smoke/pic')
    if not pay_info_page:
        raise Exception("没找到收款信息按钮")
    click_screen(pay_info_page, delay_sec=1)

    # 微信 支付宝 现金收款的信息
    pic_path_1 = ""
    cash_pay_info_page = get_pic_position("cash_pay_info", 'deal_smoke/pic', center=False)
    if cash_pay_info_page:
        cash_pay_info_page = (cash_pay_info_page[0],
                              cash_pay_info_page[1],
                              cash_pay_info_page[2] + 380,
                              cash_pay_info_page[3],)
        pic_path_1 = screen_shot('cash_pay_info', regine=cash_pay_info_page)

    pic_path_2 = ""
    wx_pay_info_page = get_pic_position("wx_pay_info", 'deal_smoke/pic', center=False)
    if wx_pay_info_page:
        wx_pay_info_page = (wx_pay_info_page[0],
                            wx_pay_info_page[1],
                            wx_pay_info_page[2] + 380,
                            wx_pay_info_page[3],)
        pic_path_2 = screen_shot('wx_pay_info', regine=wx_pay_info_page)

    pic_path_3 = ""
    ali_pay_info_page = get_pic_position("ali_pay_info", 'deal_smoke/pic', center=False)
    if ali_pay_info_page:
        ali_pay_info_page = (ali_pay_info_page[0],
                             ali_pay_info_page[1],
                             ali_pay_info_page[2] + 380,
                             ali_pay_info_page[3],)
        pic_path_3 = screen_shot('ali_pay_info', regine=ali_pay_info_page)

    # 总的收款图
    pay_total_page = get_pic_position("pay_total", 'deal_smoke/pic')
    if pay_total_page:
        pay_total_page = (pay_total_page[0] - 480,
                          pay_total_page[1] - 24,
                          pay_total_page[2] + 370 * 2,
                          pay_total_page[3] + 650,)
        screen_shot('pay_total_info', regine=pay_total_page)

    # 点击返回
    pay_info_back_page = get_pic_position("pay_info_back", 'deal_smoke/pic')
    if not pay_info_back_page:
        raise Exception("没找到收款信息的返回按钮")
    click_screen(pay_info_back_page, delay_sec=1)
    time.sleep(1)

    # 检查输入框，是不是在首页
    input_page = get_pic_position("input_1", 'deal_smoke/pic')
    if not input_page:
        raise Exception("获取收款信息完成，但没返回到首页")

    return pic_path_1, pic_path_2, pic_path_3


def get_pay_information():
    pay_info_str = ""
    # 获取支付信息
    flag_info_index = get_pay_info()
    cash_all = 0
    online_all = 0
    rate = 0
    for pic in flag_info_index:
        if pic:
            reader = easyocr.Reader(['ch_sim', 'en'])
            reader_info = reader.readtext(pic)
            if len(reader_info) > 0:
                pay_name = reader_info[0][1]
                pay_num = reader_info[-1][1].split(".")[0]
                if pay_name == "现金" and pay_num.isdigit():
                    cash_all += float(reader_info[-1][1])
                if pay_name != "现金" and pay_num.isdigit():
                    online_all += float(reader_info[-1][1])
            for item in reader_info:
                pay_info_str += item[1] + " "
            pay_info_str += "\n"
    if cash_all + online_all > 0:
        rate = round(online_all / (cash_all + online_all), 2)
        pay_info_str += f"主扫比例:{rate * 100}%\n"
    else:
        pay_info_str += f"主扫比例: 计算失败 {cash_all}, {online_all}\n"
    send_pay_info_image()
    return pay_info_str, rate


def send_pay_info_image(user_name="ZhangGongZhu|LengYueHanShuang", pic_path="D:\Project\game\Logs\pay_total_info.png"):
    send_image(user_name, pic_path)


def get_this_time_info():
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': '1'
    }
    ref, resp = api_request(url, data=para_data)
    if ref:
        return resp
    raise Exception("获取刷单信息失败")


# 2成功更新商品  4根据当前的主扫比例，给出下次的支付类型
def set_this_time_stock(item_id, get_type="2", run_count=1):
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': get_type,
        'run_count': int(run_count),
        'id': item_id
    }
    ref, resp = api_request(url, data=para_data)
    if ref:
        return resp
    return None


# 3获取支付码
def get_pay_no(get_type="3"):
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': get_type
    }
    pay_no = "0"
    ref, resp = api_request(url, data=para_data)
    if ref and 'data' in resp:
        pay_no = resp['data']
    return str(pay_no) if pay_no and len(str(pay_no)) == 18 and str(pay_no).isdigit() else None


def screen_shot_error():
    return screen_shot('smoke_error_run')


if __name__ == '__main__':
    send_pay_info_image("MaoCaiYuan")
