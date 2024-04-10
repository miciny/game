from common.gui_utils import screen_shot
from common.common_utils import api_request
import urllib3
urllib3.disable_warnings()


def send_wechat_notice(title, desc, user_name='MaoCaiYuan', bot_name='yuan_qi'):
    url = 'https://www.xlovem.club/v1/notice/wechat'
    para_data = {
        'title': title,
        'desc': desc,
        "msg_type": "text",
        'user_name': user_name,
        'bot_name': bot_name
    }
    return api_request(url, data=para_data)


def send_wechat_iamge(image_id, user_name='MaoCaiYuan', bot_name='yuan_qi'):
    url = 'https://www.xlovem.club/v1/notice/wechat'
    para_data = {
        'title': image_id,
        'desc': "",
        "msg_type": "iamge",
        'user_name': user_name,
        'bot_name': bot_name
    }
    return api_request(url, data=para_data)


def send_image(user_name, pic_path):
    if not os.path.exists(pic_path) or not user_name:
        return
    server_pic_path = wx_upload_pic(pic_path)
    print("server_pic_path", server_pic_path)
    if server_pic_path:
        set_this_time_stock(server_pic_path, get_type="5", user_name=user_name)


# yys刷的时候的通知 1成功 2失败 3过程中 4通知
def mcy_send_notice(content_str, status=1):
    if status == 2:
        pic_name = "error"
        pic_name_1 = "error_1"
        title = "错误"
    elif status == 3:
        pic_name = "progress"
        pic_name_1 = "progress_1"
        title = "过程中"
    elif status == 1:
        pic_name = "done"
        pic_name_1 = "done_1"
        title = "成功"
    else:
        pic_name = "notice"
        pic_name_1 = "notice_1"
        title = "通知"
    pic_path = screen_shot(pic_name)
    time.sleep(2)
    pic_path_1 = screen_shot(pic_name_1)

    try:
        send_wechat_notice(title, content_str)
        send_image("MaoCaiYuan", pic_path)
        send_image("MaoCaiYuan", pic_path_1)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    res = send_wechat_notice("wo", '自己\n换行', user_name='ZhangGongZhu')
    print(res.text)
