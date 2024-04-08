import random
import time
import easyocr
from common.common_utils import print_wait
from common.wechat_services import send_wechat_notice
from deal_smoke.smoke_script import single_run, get_pay_info, get_this_time_info, set_this_time_stock


def run():
    flag = True
    gap_min_range = (5, 18)
    while flag:
        try:
            # 从接口获取刷单信息
            smoke_map = get_this_time_info()
            item_id = smoke_map['data']['id']
            item_stock = smoke_map['data']['stock']
            item_name = smoke_map['data']['name']
            pay_type = smoke_map['data']['pay_type']
            if "run_flag" in smoke_map['data'].keys() and smoke_map['data']['run_flag'] == 0:
                flag = False
                continue
            
            # 刷单
            pay_type = 2 if pay_type == 2 else 1
            single_run(item_id, pay_type)  

            # 更新库存
            set_this_time_stock(item_id)  

            # 获取支付信息
            flag_info_index = get_pay_info()
            pay_info_str = f"{item_name} 库存：{item_stock} \n"
            for pic in flag_info_index:
                if pic:
                    reader = easyocr.Reader(['ch_sim', 'en'])
                    reader_info = reader.readtext(pic)
                    for item in reader_info:
                        pay_info_str += item[1] + " "
                    pay_info_str += "\n"
            
            # 下次时间
            gap_min = random.randint(gap_min_range[0], gap_min_range[1])
            pay_info_str += f'\n下次刷单是{gap_min}分钟后\n停止刷单请回复【停止刷单】'
            send_wechat_notice("刷单成功了", pay_info_str, user_name='ZhangGongZhu|LengYueHanShuang')
            print_wait(gap_min * 60, "刷单成功等待：")
        except Exception as e:
            send_wechat_notice("刷单报错了", f"请检查: {e}", user_name='MaoCaiYuan')
            print_wait(5 * 60, "刷单成功等待：")
            


if __name__ == '__main__':
    run()

    # pic_path = 'D:\Project\game\Logs\wx_pay_info.png'
    # reader = easyocr.Reader(['ch_sim', 'en'])
    # reader_info = reader.readtext(pic_path, low_text=0.0001)
    # for item in reader_info:
    #     print(item)

    # smoke_map = get_this_time_info()
    # print(smoke_map)

    # send_wechat_notice("刷单成功了", "haha", user_name='ZhangGongZhu')
