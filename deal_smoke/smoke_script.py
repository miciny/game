import re
import time
import easyocr
from common.wechat_services import send_image
from common.gui_utils import *


# 判断是否有图片
def check_have(pic_name):
    """
    判断是否有图片
    :param pic_name: 图片名称
    :return: 是否有图片
    """
    return smoke_pic_operation(pic_name, raise_error=False, click_flag=False)


# 判断是否有图片
def check_have_by_dir(dir_name):
    """
    判断是否有图片
    :param dir_name: 目录名称
    :return: 是否有图片
    """
    return smoke_pic_operation_by_dir(dir_name, raise_error=False, click_flag=False)


# 判断需不需要从连接开始
def connect_check():
    return check_have_by_dir("connect")


# 判断是不是锁了
def locked_check():
    return check_have_by_dir("locked")


# 判断是不是首页
def main_page_check():
    return check_have_by_dir("input")


# 判断是不是在支付了
def online_pay_check():
    return check_have_by_dir("online_pay_not_input")


# 判断是不是非商品 或 新商品
def not_or_new_product_check():
    return check_have_by_dir("product_error")

# 判断是不是負數了
def negative_product_check():
    """
    判断是不是負數了
    :return:
    """
    return check_have_by_dir("negative_product")


# 如果锁了，解锁
def locked_and_enter():
    """
    如果锁了，解锁
    :return:
    """
    if locked_check():
        click_screen([500, 500])
        auto_key("enter")
        print_wait(5, des="等待解锁完成")


def clear_all():
    """
    清除所有商品
    :return:
    """
    smoke_pic_operation_by_dir("confirm", raise_error=False)
    time.sleep(3)
    smoke_pic_operation_by_dir("clear_all", raise_error=False)
    time.sleep(3)
    smoke_pic_operation_by_dir("clear_confirm", raise_error=False)


# 不在首页，异常处理
def not_main_page_deal():
    """
    不在首页，异常处理
    :return:
    """
    times = 5
    index = 0
    while ((not_or_new_product_check() or negative_product_check()) or (not main_page_check())) and index < times:
        index += 1
        if not_or_new_product_check():
            smoke_pic_operation_by_dir("confirm", raise_error=False)
            continue
        if negative_product_check():
            clear_all()
            continue
        for i in range(20):
            time.sleep(0.1)
            auto_key("backspace")
            

# 点击连接 + 确认
def prepare_smoke():
    """
    准备烟
    :return:
    """
    c_pos = smoke_pic_operation_by_dir("connect", random_flag=False, error_msg="连接connect按钮没找到")
    if c_pos:
        c_pos = (c_pos[0] + 20, c_pos[1] + 20)
        click_screen(c_pos, delay_sec=1)
    time.sleep(10)
    # smoke_pic_operation("out_full", random_flag=False, error_msg="连接out_full按钮没找到")


def get_pay_info():
    """
    获取收款信息
    :return: 收款信息
    """
    # 点击收款信息按钮
    smoke_pic_operation_by_dir("pay_info", error_msg="没找到收款信息按钮")
    time.sleep(8)

    # 现金收款的信息，本地识别
    pic_path_1 = ""
    cash_pay_info_page = smoke_pic_operation_by_dir("cash_pay_info", center=False, click_flag=False, raise_error=False)
    if cash_pay_info_page:
        cash_pay_info_page = (cash_pay_info_page[0],
                              cash_pay_info_page[1],
                              cash_pay_info_page[2] + 380,
                              cash_pay_info_page[3])
        pic_path_1 = screen_shot('cash_pay_info', regine=cash_pay_info_page)

    # 微信收款的信息，本地识别
    pic_path_2 = ""
    wx_pay_info_page = smoke_pic_operation_by_dir("wx_pay_info", center=False, click_flag=False, raise_error=False)
    if wx_pay_info_page:
        wx_pay_info_page = (wx_pay_info_page[0],
                            wx_pay_info_page[1],
                            wx_pay_info_page[2] + 380,
                            wx_pay_info_page[3])
        pic_path_2 = screen_shot('wx_pay_info', regine=wx_pay_info_page)

    # 支付宝收款的信息，本地识别
    pic_path_3 = ""
    ali_pay_info_page = smoke_pic_operation_by_dir("ali_pay_info", center=False, click_flag=False, raise_error=False)
    if ali_pay_info_page:
        ali_pay_info_page = (ali_pay_info_page[0],
                             ali_pay_info_page[1],
                             ali_pay_info_page[2] + 380,
                             ali_pay_info_page[3])
        pic_path_3 = screen_shot('ali_pay_info', regine=ali_pay_info_page)

    # 总的收款图，不识别，发送通知用
    pay_total_page = smoke_pic_operation_by_dir("pay_total", click_flag=False, raise_error=False)
    if pay_total_page:
        pay_total_page = (pay_total_page[0] - 480,
                          pay_total_page[1] - 24,
                          pay_total_page[2] + 370 * 2,
                          pay_total_page[3] + 650)
        screen_shot('pay_total_info', regine=pay_total_page)

    # 总的收款简图，发送到服务器，chatGPT识别
    pay_all_page = smoke_pic_operation_by_dir("pay_total", click_flag=False, raise_error=False)
    if pay_all_page:
        pay_all_page = (pay_all_page[0] - 350,
                        pay_all_page[1] + 225,
                        pay_all_page[2] + 350,
                        pay_all_page[3] + 200)
        screen_shot('pay_all_info', regine=pay_all_page)

    # 点击返回
    smoke_pic_operation_by_dir("pay_info_back", raise_error=False)
    time.sleep(2)

    # 检查输入框，是不是在首页
    smoke_pic_operation_by_dir("input", error_msg="获取收款信息完成，但没返回到首页", click_flag=False, raise_error=False)
    return pic_path_1, pic_path_2, pic_path_3


def get_pay_information():
    """
    获取支付信息
    :return: 支付信息
    """
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
    """
    库存检查
    :param run_count: 刷单数量
    :return:
    """
    now_info_no, all_info_no = get_smoke_stock()
    print("now_info_no, all_info_no: ", now_info_no, all_info_no)
    if all_info_no is not None:
        if all_info_no < float(run_count):
            raise Exception("剩余库存小于刷单数量了，请检查！")
    return now_info_no, all_info_no


def get_smoke_stock():
    """
    ocr 获取库存信息
    :return: 库存信息
    """
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
    """
    发送收款信息图片
    :param user_name: 用户名
    :param pic_path: 图片路径
    :param send: 是否发送
    :param full_path: 是否是完整路径
    :return:
    """
    pic_path_real = f"D:\Project\game\Logs\{pic_path}.png" if not full_path else pic_path
    send_image(user_name, pic_path_real, send=send)


def smoke_pic_operation(pic_name, raise_error=True, click_flag=True, error_msg="", random_flag=True):
    """
    检测图片，返回【x, y, width, height】 或 None
    :param pic_name: 图片名称
    :param raise_error: 是否抛出异常
    :param click_flag: 是否点击
    :param error_msg: 异常信息
    :param random_flag: 是否随机点击
    :return: 检测结果
    """
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


def smoke_pic_operation_by_dir(dir_name, raise_error=True, click_flag=True, error_msg="", random_flag=True, center=True):
    """
    检测图片，返回【x, y, width, height】 或 None
    :param dir_name: 图片目录名称, 是 'deal_smoke/pic' 下的子目录，例如 input
    :param raise_error: 是否抛出异常
    :param click_flag: 是否点击
    :param error_msg: 异常信息
    :param random_flag: 是否随机点击
    :return: 检测结果
    """

    # 找到所有图片
    pic_names = os.listdir(os.path.join(self_path, f'deal_smoke/pic/{dir_name}'))
    print(pic_names)
    pic_names = [str(pic_name).split(".")[0] for pic_name in pic_names]
    search_page = ""
    for pic_name in pic_names:
        print(pic_name)
        search_page = get_pic_position(pic_name, f'deal_smoke/pic/{dir_name}', center=center)
        if search_page:
            break

    if raise_error and not search_page:
        raise Exception(error_msg)
    if click_flag and search_page:
        click_screen(search_page, delay_sec=1, random_flag=random_flag)
    return search_page


def screen_shot_error():
    """
    截图错误信息
    :return: 截图路径
    """
    return screen_shot('smoke_error_run')


if __name__ == '__main__':
    # get_pay_info()
    # print(get_smoke_stock())
    print(smoke_pic_operation_by_dir("input"))
