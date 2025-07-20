import time

from common.gui_utils import auto_key, auto_input, screen_shot, click_screen
from common.wechat_services import send_wechat_notice
from deal_smoke.smoke_api import get_pay_no
from deal_smoke.smoke_script import smoke_pic_operation, stock_check, locked_and_enter, not_main_page_deal, \
    main_page_check, online_pay_check


# pay_type = 1 现金支付， 2 微信支付
def single_run(smoke_id, item_name, run_count, pay_type=1):
    if not smoke_id:
        raise Exception("没有找到可刷的商品")

    # 被锁了检测
    locked_and_enter()
    # 不在首页，异常处理
    not_main_page_deal()
    # 检查输入框，是不是在首页，在首页就点击, 不然就报错
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
    smoke_pic_operation("get_pay_1", error_msg="收银按钮没找到")

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
        for i in range(60 * 60 * 3):
            # 检查输入框，是不是在首页,在首页，说明有人支付了
            if main_page_check():
                return True, ctx

            # 看是不是有人手动支付中, 没人支付，就请求准备自动支付，有人支付时就等
            if online_pay_check():
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
                if main_page_check():
                    return True, ctx

                # 也不在首页，那就试四次
                not_found += 1
                if not_found > 2:
                    return False, ctx
            time.sleep(5)
