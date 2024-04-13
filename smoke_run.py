import time
from common.common_utils import print_wait
from common.wechat_services import send_wechat_notice
from deal_smoke.smoke_script import single_run, get_this_time_info, set_this_time_stock, \
    send_pay_info_image, screen_shot_error, get_pay_information


def run():
    flag = True
    while flag:
        try:
            # 从接口获取刷单信息
            smoke_map = get_this_time_info()
            item_id = smoke_map['data']['id']
            item_stock = smoke_map['data']['stock']
            item_name = smoke_map['data']['name']
            pay_type = smoke_map['data']['pay_type']
            next_gap = int(smoke_map['data']['next_gap'])
            if "run_flag" in smoke_map['data'].keys() and smoke_map['data']['run_flag'] == 0:
                flag = False
                continue
            
            # 刷单
            pay_type = 2 if pay_type == 2 else 1
            pay_flag, run_count = single_run(item_id, item_name, item_stock, pay_type)
            pay_info_str = f"{item_name} 剩余：{int(item_stock) - 1} \n"

            # 更新库存 都默认成功，比如微信，最后必须手动成功
            set_this_time_stock(item_id, run_count=run_count)

            # 现金支付的
            if pay_type == 1:
                # 获取支付信息
                info_str, rate = get_pay_information()
                pay_info_str += info_str
                set_this_time_stock(rate, get_type="4")
                title = "现金刷单成功"
            # 微信收款的提醒
            else:
                if pay_flag:
                    time.sleep(3)
                    title = "微信刷单成功"
                    info_str, rate = get_pay_information()
                    pay_info_str += info_str
                    set_this_time_stock(rate, get_type="4")
                else:
                    title = "微信支付提醒"
                    pay_info_str += '微信收款失败，请手动查看和收款，收款后返回到首页\n'

            pay_info_str += f'下次刷单是{next_gap}分钟后\n停止刷单请回复【停止刷单】'
            send_wechat_notice(title, pay_info_str, user_name='ZhangGongZhu|LengYueHanShuang')
            print_wait(next_gap * 60, "刷单成功等待：")

        except Exception as e:
            error_pic = screen_shot_error()
            time_gap = 3
            send_wechat_notice("刷单报错了", f"请检查: {e} \n将在{time_gap}分钟后重试", user_name='ZhangGongZhu|LengYueHanShuang')
            send_pay_info_image(user_name="MaoCaiYuan", pic_path=error_pic)
            print_wait(time_gap * 60, "刷单成功等待：")


if __name__ == '__main__':
    run()

    # online_all = 0
    # pic_path = 'D:\Project\game\Logs\wx_pay_info.png'
    # reader = easyocr.Reader(['ch_sim', 'en'])
    # reader_info = reader.readtext(pic_path)
    # print(reader_info[0][1], reader_info[-1][1])
    # pay_name = reader_info[0][1]
    # pay_num = reader_info[-1][1].split(".")[0]
    # if pay_name != "现金" and pay_num.isdigit():
    #     online_all += float(pay_num)
    # print(online_all)
    # for item in reader_info:
    #     print(item)

    # smoke_map = get_this_time_info()
    # print(smoke_map)

    # send_wechat_notice("刷单成功了", "haha", user_name='ZhangGongZhu')
    # time.sleep(10)
    # screen_shot_error()
