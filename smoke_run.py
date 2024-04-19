import time
from common.common_utils import print_wait, shutdown_pc
from common.wechat_services import send_wechat_notice
from deal_smoke.smoke_script import single_run, get_this_time_info, set_this_time_stock, \
    send_pay_info_image, screen_shot_error, get_pay_information, stock_run


# 刷库存
def run_stock():
    smoke_map_res = get_this_time_info(get_type="5")
    smoke_map = smoke_map_res['data']
    for key, value in smoke_map.items():
        try:
            stock_run(key)
        except Exception as e:
            send_wechat_notice("库存获取错误", value["name"] + f"{e}", user_name='')


def run():
    flag = True
    next_type = ""
    while flag:
        try:
            # 从接口获取刷单信息
            smoke_map = get_this_time_info()
            item_id = smoke_map['data']['id']
            item_stock = smoke_map['data']['stock']
            item_name = smoke_map['data']['name']
            pay_type = smoke_map['data']['pay_type']
            run_count = smoke_map['data']['run_count']
            next_gap = int(smoke_map['data']['next_gap'])
            if "run_flag" in smoke_map['data'].keys() and smoke_map['data']['run_flag'] == 0:
                flag = False
                continue
            
            # 刷单
            pay_type = 2 if pay_type == 2 else 1
            pay_flag, ctx = single_run(item_id, item_name, run_count, pay_type)
            pay_info_str = f"{item_name} 剩余：{int(item_stock) - run_count} \n"

            # 更新库存 都默认成功，比如微信，最后必须手动成功
            all_info_no = ctx['all_info_no'] if "all_info_no" in ctx.keys() else None
            set_this_time_stock(item_id, run_count=run_count, smoke_stock_temp=all_info_no)

            # 现金支付的
            if pay_type == 1:
                # 获取支付信息
                info_str, rate, cash_all, online_all = get_pay_information()
                pay_info_str += info_str
                next_type = set_this_time_stock(rate, get_type="4", cash_all=cash_all, online_all=online_all)
                title = "现金刷单成功"
            # 微信收款的提醒
            else:
                if pay_flag:
                    time.sleep(3)
                    title = "微信刷单成功"
                    info_str, rate, cash_all, online_all = get_pay_information()
                    pay_info_str += info_str
                    next_type = set_this_time_stock(rate, get_type="4", cash_all=cash_all, online_all=online_all)
                else:
                    title = "微信支付失败"
                    pay_info_str += '微信收款失败，请手动查看和收款，收款后返回到首页\n'

            pay_info_str += f'下次刷单为{next_type}, {next_gap}分钟后\n停止刷单请回复【停止刷单】'
            send_wechat_notice(title, pay_info_str, user_name='')
            print_wait(next_gap * 60, "刷单成功等待：")

        except Exception as e:
            error_pic = screen_shot_error()
            time_gap = 2
            send_wechat_notice("刷单报错了", f"请检查: {e} \n将在{time_gap}分钟后重试", user_name='')
            send_pay_info_image(user_name="MaoCaiYuan", pic_path=error_pic)
            print_wait(time_gap * 60, "刷单成功等待：")
    
    delay_time = 300
    send_wechat_notice("关机执行中", str(delay_time) + "秒倒计时关机！", user_name='')
    shutdown_pc(delay_time)


if __name__ == '__main__':
    run()
    # run_stock()

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
