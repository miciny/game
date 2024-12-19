# 刷库存用
import time

from common.gui_utils import auto_input, auto_key, screen_shot
from deal_smoke.smoke_api import set_this_time_stock
from deal_smoke.smoke_script import smoke_pic_operation, stock_check


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
