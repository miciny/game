import re
import time
import easyocr
from common.wechat_services import send_image
from common.gui_utils import *


def check_have(pic_name):
    return smoke_pic_operation(pic_name, raise_error=False, click_flag=False)


# 判断需不需要从连接开始
def connect_check():
    return check_have("connect_3")


# 判断是不是锁了
def locked_check():
    return check_have("locked")


# 判断是不是首页
def main_page_check():
    return check_have("input_1")


# 判断是不是在支付了
def online_pay_check():
    return check_have("online_pay_not_input") or check_have("online_pay_not_input_1")


# 判断是不是非商品 或 新商品
def not_or_new_product_check():
    return check_have("not_product") or check_have("new_product") or check_have("error_product")


# 判断是不是負數了
def negative_product_check():
    return check_have("negative_product")


# 如果锁了，解锁
def locked_and_enter():
    if locked_check():
        click_screen([500, 500])
        auto_key("enter")
        print_wait(5, des="等待解锁完成")


def clear_all():
    smoke_pic_operation(["confirm"], raise_error=False)
    time.sleep(3)
    smoke_pic_operation("clear_all", raise_error=False)
    time.sleep(3)
    smoke_pic_operation("clear_confirm", raise_error=False)


# 不在首页，异常处理
def not_main_page_deal():
    times = 5
    index = 0
    while ((not_or_new_product_check() or negative_product_check()) or (not main_page_check())) and index < times:
        index += 1
        if not_or_new_product_check():
            smoke_pic_operation(["confirm"], raise_error=False)
            continue
        if negative_product_check():
            clear_all()
            continue
        for i in range(20):
            time.sleep(0.1)
            auto_key("backspace")


# 点击连接 + 确认
def prepare_smoke():
    c_pos = smoke_pic_operation("connect_3", random_flag=False, error_msg="连接connect_2按钮没找到")
    if c_pos:
        c_pos = (c_pos[0] + 20, c_pos[1] + 20)
        click_screen(c_pos, delay_sec=1)
    time.sleep(10)
    # smoke_pic_operation("out_full", random_flag=False, error_msg="连接out_full按钮没找到")


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


def send_pay_info_image(user_name="MaoCaiYuan", pic_path="pay_total_info", send=True, full_path=False):
    pic_path_real = f"D:\Project\game\Logs\{pic_path}.png" if not full_path else pic_path
    send_image(user_name, pic_path_real, send=send)


def smoke_pic_operation(pic_name, raise_error=True, click_flag=True, error_msg="", random_flag=True):
    search_page = None
    if isinstance(pic_name, str):
        search_page = get_pic_position(pic_name, 'deal_smoke/pic')
    if isinstance(pic_name, list):
        for pic in pic_name:
            search_page = get_pic_position(pic, 'deal_smoke/pic')
            if search_page:
                break

    if raise_error and not search_page:
        raise Exception(error_msg)
    if click_flag and search_page:
        click_screen(search_page, delay_sec=1, random_flag=random_flag)
    return search_page


def screen_shot_error():
    return screen_shot('smoke_error_run')


if __name__ == '__main__':
    get_pay_info()
    # print(get_smoke_stock())
