import random
import time

import easyocr

from common.wechat_services import send_wechat_notice
from deal_smoke.smoke_script import single_run, get_pay_info


def run():
    flag = True
    flag_index = 0
    flag_info_index = 0
    while flag:
        try:
            flag_index = single_run()
            flag = True if flag_index == 0 else False
        except Exception as e:
            print(e)
        finally:
            if flag:
                flag_info_index = get_pay_info()
                if flag_info_index not in (6, 7, 8):
                    reader = easyocr.Reader(['ch_sim', 'en'])
                    pay_info = reader.readtext(flag_info_index)
                    send_wechat_notice("刷单成功了", pay_info)
                    gap_min = random.randint(8, 15)
                    time.sleep(gap_min * 60)
                    continue
            send_wechat_notice("刷单报错了", f"请检查: {flag_index}, {flag_info_index}")


if __name__ == '__main__':
    # run()
    flag_info_index = 'D:\Project\game\Logs\smoke_pay_info.png'
    reader = easyocr.Reader(['ch_sim', 'en'])
    pay_info = reader.readtext(flag_info_index)
    print(pay_info)
