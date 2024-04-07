import random
import time
import easyocr

from common.common_utils import print_wait
from common.wechat_services import send_wechat_notice
from deal_smoke.smoke_script import single_run, get_pay_info, get_this_time_info, set_this_time_stock

item_id_map = {
    "6901028315005": 20,
    "6901028053822": 50,
    "6901028071772": 9,
    "6901028072540": 20,
    "6901028072557": 10,
    "6901028072601": 20,
    "6901028072618": 10
}


def run():
    flag = True
    flag_index = 0
    flag_info_index = 0
    item_name = ""
    item_id = ""
    err_msg = ""
    item_stock = 0
    gap_min_range = (5, 18)
    all_times = random.randint(30, 40)
    while flag and all_times > 0:
        try:
            smoke_map = get_this_time_info()
            item_id = smoke_map['data']['id']
            item_stock = smoke_map['data']['stock']
            item_name = smoke_map['data']['name']
            if not item_id:
                flag = False
                raise Exception("没有找到可刷的商品")

            flag_index = single_run(item_id)  # 刷单
            flag = True if flag_index == 0 else False
        except Exception as e:
            err_msg = str(e)
        finally:
            if flag:
                set_this_time_stock(item_id)  # 更新库存
                # 获取支付信息
                flag_info_index = get_pay_info()
                pay_info_str = f"{item_name} 库存：{item_stock} \n"
                flag = isinstance(flag_info_index, tuple) and len(flag_info_index) == 2
                if flag:
                    for pic in flag_info_index:
                        if pic:
                            reader = easyocr.Reader(['ch_sim', 'en'])
                            reader_info = reader.readtext(pic)
                            for item in reader_info:
                                pay_info_str += item[1] + " "
                            pay_info_str += "\n"
                    gap_min = random.randint(gap_min_range[0], gap_min_range[1])
                    pay_info_str += f'\n下次刷单是{gap_min}分钟后\n'
                    all_times -= 1
                    pay_info_str += f"今日剩余刷单次数：{all_times}"
                    send_wechat_notice("刷单成功了", pay_info_str, user_name='ZhangGongZhu|LengYueHanShuang')
                    print_wait(gap_min * 60, "刷单成功等待：")
                    continue

            send_wechat_notice("刷单报错了",
                               f"请检查: {flag_index}, {flag_info_index}, {err_msg}",
                               user_name='ZhangGongZhu')


if __name__ == '__main__':
    run()
    # pay_info_str = ''
    # flag_info_index = get_pay_info()
    # if isinstance(flag_info_index, tuple) and len(flag_info_index) == 2:
    #     for pic in flag_info_index:
    #         print(pic)
    #         reader = easyocr.Reader(['ch_sim', 'en'])
    #         reader_info = reader.readtext(pic)
    #         for item in reader_info:
    #             pay_info_str += item[1] + " "
    #     send_wechat_notice("刷单成功了", pay_info_str)

    # pic_path = 'D:\Project\game\Logs\wx_pay_info.png'
    # reader = easyocr.Reader(['ch_sim', 'en'])
    # reader_info = reader.readtext(pic_path, low_text=0.0001)
    # for item in reader_info:
    #     print(item)

    # smoke_map = get_this_time_info()
    # print(smoke_map)

    # send_wechat_notice("刷单成功了", "haha", user_name='ZhangGongZhu')
