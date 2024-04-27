import re
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
    smoke_pic_operation("input_1", error_msg="不在首页")

    # 如果是微信 剩余库存大于2，则刷两个
    for _ in range(run_count):
        # 输入编码
        auto_input(smoke_id)
        # paste_to(smoke_id)
        time.sleep(1)
        # 按回车，进到收银
        auto_key("enter")
        time.sleep(1)
    ctx = dict()
    # 截图，准备后续得到库存
    smoke_no_page = smoke_pic_operation("smoke_no", click_flag=False, raise_error=False)
    if smoke_no_page:
        smoke_no_page = (smoke_no_page[0] - smoke_no_page[2] / 2,
                         smoke_no_page[1] + smoke_no_page[3] / 2,
                         smoke_no_page[2],
                         smoke_no_page[3] + smoke_no_page[3] - 12)
        screen_shot('smoke_no_info', regine=smoke_no_page)
        now_info_no, all_info_no = stock_check(run_count)
        if all_info_no:
            ctx["all_info_no"] = all_info_no

    # 点击收银
    smoke_pic_operation("get_pay", error_msg="收银按钮没找到")

    # 现金
    if pay_type == 1:
        # 选择现金
        smoke_pic_operation("cash", error_msg="没找到现金选择按钮")

        # 收款确认
        smoke_pic_operation("cash_confirm", error_msg="现金支付，没找到收款确认")
        time.sleep(1)

        # 检查输入框，是不是在首页
        smoke_pic_operation("input_1", error_msg="现金收款完成，但不在首页", click_flag=False)
        return True, ctx

    # 微信
    else:
        pay_no = ""
        send_flag = True
        for i in range(60 * 60):
            # 检查输入框，是不是在首页,在首页，说明有人支付了
            input_page = smoke_pic_operation("input_1", click_flag=False, raise_error=False)
            if input_page:
                return True, ctx

            # 看是不是有人手动支付中, 没人支付，就请求准备自动支付，有人支付时就等
            online_pay_not_input_page = smoke_pic_operation("online_pay_not_input", click_flag=False, raise_error=False)
            online_pay_not_input_page_1 = smoke_pic_operation("online_pay_not_input_1", click_flag=False, raise_error=False)
            if online_pay_not_input_page or online_pay_not_input_page_1:
                # 没在首页，则请求支付码，有支付码了，就走后面的自动填写流程
                pay_no = get_pay_no()
                if pay_no:
                    break
                
                # 如果一直没人理，3分钟发消息
                if int(i % 60) == 0 and int(i / 60) % 3 == 0:
                    # 前两次发群里的，后面的通知，在群里、微信机器人、飞书机器人都会发
                    send_wechat_notice("支付提醒", f"{item_name} 请求支付中！\n请手动完成微信支付, 支付后返回到首页", user_name='ZhangGongZhu')
            else:
                # 有个收款查询，需要点击
                smoke_pic_operation("pay_check", raise_error=False)

                if send_flag:
                    send_flag = False
                    # 仅发给需要关注的人
                    send_wechat_notice("手动支付提醒", f"{item_name} 疑似有人在手动支付，请注意！", user_name='ZhangGongZhu')
            time.sleep(1)

        if not pay_no:
            return False, ctx

        # 自动支付的话，发群里，也可能发给个人
        send_wechat_notice("支付提醒", f"{item_name} 自动微信支付中，请勿手动操作", user_name='ZhangGongZhu')
        auto_input(pay_no)
        # paste_to(pay_no)
        time.sleep(1)

        # 收款确认
        smoke_pic_operation("cash_confirm", error_msg="微信支付，没找到收款确认")
        time.sleep(5)
        
        not_found = 0
        for i in range(30):
            # 有个收款查询，需要点击，不成功的情况下，会一直有这个按钮
            pay_check_page = smoke_pic_operation("pay_check", raise_error=False, click_flag=False)
            if pay_check_page:
                click_screen(pay_check_page, delay_sec=1)
                not_found = 0
            else:
                # 如果没有查询按钮，检查是不是在首页，在首页说明成功了
                input_page = smoke_pic_operation("input_1", click_flag=False, raise_error=False)
                if input_page:
                    return True, ctx
        
                # 也不在首页，那就试四次
                not_found += 1
                if not_found > 2:
                    return False, ctx
            time.sleep(5)


# 刷库存用
def stock_run(smoke_id):
    if not smoke_id:
        raise Exception("商品id有误")

    # 检查输入框，是不是在首页，在首页就点击
    smoke_pic_operation("input_1", error_msg="不在首页")

    # 输入编码
    auto_input(smoke_id)
    # 按回车，进到收银
    auto_key("enter")

    time.sleep(1)
    flag = False
    # 截图，准备后续得到库存
    smoke_no_page = smoke_pic_operation("smoke_no", click_flag=False, raise_error=False)
    if smoke_no_page:
        smoke_no_page = (smoke_no_page[0] - smoke_no_page[2] / 2,
                         smoke_no_page[1] + smoke_no_page[3] / 2,
                         smoke_no_page[2],
                         smoke_no_page[3] + smoke_no_page[3] - 12)
        screen_shot('smoke_no_info', regine=smoke_no_page)
        print("截图成功")
        now_info_no, all_info_no = stock_check(-1)
        if all_info_no is not None:
            # 更新库存
            set_this_time_stock(smoke_id, run_count=0, smoke_stock_temp=all_info_no)
            flag = True
    
    smoke_pic_operation("clear", error_msg="没找到清除按钮")

    if not flag:
        raise Exception("未识别到库存")


def get_pay_info():
    # 点击收款信息按钮
    smoke_pic_operation("pay_info", error_msg="没找到收款信息按钮")
    time.sleep(2)

    # 现金收款的信息，本地识别
    pic_path_1 = ""
    cash_pay_info_page = get_pic_position("cash_pay_info", 'deal_smoke/pic', center=False)
    if cash_pay_info_page:
        cash_pay_info_page = (cash_pay_info_page[0],
                              cash_pay_info_page[1],
                              cash_pay_info_page[2] + 380,
                              cash_pay_info_page[3])
        pic_path_1 = screen_shot('cash_pay_info', regine=cash_pay_info_page)

    # 微信收款的信息，本地识别
    pic_path_2 = ""
    wx_pay_info_page = get_pic_position("wx_pay_info", 'deal_smoke/pic', center=False)
    if wx_pay_info_page:
        wx_pay_info_page = (wx_pay_info_page[0],
                            wx_pay_info_page[1],
                            wx_pay_info_page[2] + 380,
                            wx_pay_info_page[3])
        pic_path_2 = screen_shot('wx_pay_info', regine=wx_pay_info_page)

    # 支付宝收款的信息，本地识别
    pic_path_3 = ""
    ali_pay_info_page = get_pic_position("ali_pay_info", 'deal_smoke/pic', center=False)
    if ali_pay_info_page:
        ali_pay_info_page = (ali_pay_info_page[0],
                             ali_pay_info_page[1],
                             ali_pay_info_page[2] + 380,
                             ali_pay_info_page[3])
        pic_path_3 = screen_shot('ali_pay_info', regine=ali_pay_info_page)

    # 总的收款图，不识别，发送通知用
    pay_total_page = get_pic_position("pay_total", 'deal_smoke/pic')
    if pay_total_page:
        pay_total_page = (pay_total_page[0] - 480,
                          pay_total_page[1] - 24,
                          pay_total_page[2] + 370 * 2,
                          pay_total_page[3] + 650)
        screen_shot('pay_total_info', regine=pay_total_page)

    # 总的收款简图，发送到服务器，chatGPT识别
    pay_all_page = get_pic_position("pay_total", 'deal_smoke/pic')
    if pay_all_page:
        pay_all_page = (pay_all_page[0] - 350,
                        pay_all_page[1] + 225,
                        pay_all_page[2] + 350,
                        pay_all_page[3] + 200)
        screen_shot('pay_all_info', regine=pay_all_page)

    # 点击返回
    smoke_pic_operation("pay_info_back", raise_error=False)
    time.sleep(2)

    # 检查输入框，是不是在首页
    smoke_pic_operation("input_1", error_msg="获取收款信息完成，但没返回到首页", click_flag=False, raise_error=False)
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
        rate = round(online_all / (cash_all + online_all) * 100, 2)
        pay_info_str += f"主扫比例: {rate}%\n"
    else:
        pay_info_str += f"主扫比例: 计算失败 {cash_all}, {online_all}\n"
    send_pay_info_image()
    send_pay_info_image(pic_path="pay_all_info", send=False)
    send_pay_info_image(pic_path="smoke_no_info", send=False)
    return pay_info_str, rate, cash_all, online_all


def stock_check(run_count):
    now_info_no, all_info_no = get_smoke_stock()
    print("now_info_no, all_info_no: ", now_info_no, all_info_no)
    if all_info_no is not None:
        if all_info_no < float(run_count):
            raise Exception("剩余库存小于刷单数量了，请检查！")
    return now_info_no, all_info_no


def get_smoke_stock():
    pic = "D:\Project\game\Logs\smoke_no_info.png"
    if os.path.exists(pic):
        reader = easyocr.Reader(['ch_sim', 'en'])
        reader_info = reader.readtext(pic)
        if len(reader_info) == 2:
            now_info = reader_info[0][1]
            all_info = reader_info[1][1]
            float_re = r'\d+\.?\d*'
            try:
                now_info_nos = re.findall(float_re, now_info)
                all_info_nos = re.findall(float_re, all_info)
                if now_info_nos and len(now_info_nos) > 0 and all_info_nos and len(all_info_nos) > 0:
                    return float(now_info_nos[0]), float(all_info_nos[0])
            except Exception as e:
                print(e)
    return None, None


def send_pay_info_image(user_name="MaoCaiYuan", pic_path="pay_total_info", send=True):
    pic_path_real = f"D:\Project\game\Logs\{pic_path}.png"
    send_image(user_name, pic_path_real, send=send)


def smoke_pic_operation(pic_name, raise_error=True, click_flag=True, error_msg=""):
    search_page = get_pic_position(pic_name, 'deal_smoke/pic')
    if raise_error and not search_page:
        raise Exception(error_msg)
    if click_flag and search_page:
        click_screen(search_page, delay_sec=1)
    return search_page


# 1获取这次刷单信息 5获取所有刷单map
def get_this_time_info(get_type="1"):
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': get_type
    }
    ref, resp = api_request(url, data=para_data)
    if ref:
        return resp
    raise Exception("获取刷单信息失败")


# 2成功更新商品  4根据当前的主扫比例，给出下次的支付类型
def set_this_time_stock(item_id, get_type="2", run_count=1, smoke_stock_temp=None, cash_all=0, online_all=0):
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': get_type,
        'run_count': int(run_count),
        'smoke_stock_temp': smoke_stock_temp,
        'cash_all': cash_all,
        'online_all': online_all,
        'id': item_id
    }
    ref, resp = api_request(url, data=para_data)
    if ref and "data" in resp:
        return resp['data']
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
    get_pay_info()
    # print(get_smoke_stock())

