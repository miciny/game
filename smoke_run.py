import random
import time
import easyocr
from common.wechat_services import send_wechat_notice
from deal_smoke.smoke_script import single_run, get_pay_info


item_id_map = {
    0: '6901028' + '315005',
    1: "88880756517",
    2: '6901028' + '024037',
    3: '6901028' + '018616'
}


def run():
    flag = True
    flag_index = 0
    flag_info_index = 0
    while flag:
        try:
            id_index = random.randint(0, len(item_id_map) - 1)
            flag_index = single_run(item_id_map[id_index])
            flag = True if flag_index == 0 else False
        except Exception as e:
            print(e)
        finally:
            if flag:
                flag_info_index = get_pay_info()
                pay_info_str = ''
                if isinstance(flag_info_index, tuple) and len(flag_info_index) == 2:
                    for pic in flag_info_index:
                        reader = easyocr.Reader(['ch_sim', 'en'])
                        reader_info = reader.readtext(pic)
                        for item in reader_info:
                            pay_info_str += item[1] + " "
                    gap_min = random.randint(8, 15)
                    pay_info_str += f'\n下次刷单是{gap_min}分钟后'
                    send_wechat_notice("刷单成功了", pay_info_str, user_name='ZhangGongZhu')
                    time.sleep(gap_min * 60)
                    continue

            send_wechat_notice("刷单报错了", f"请检查: {flag_index}, {flag_info_index}", user_name='ZhangGongZhu')
            print("报错，开始等待")
            time.sleep(10 * 60)


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
    # reader_info = reader.readtext(pic_path)
    # for item in reader_info:
    #     print(item)
    #     pay_info_str += item[1] + " "
    # print(pay_info_str)
