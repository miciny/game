import requests
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
    return requests.post(url, json=para_data)


def send_wechat_iamge(image_id, user_name='MaoCaiYuan', bot_name='yuan_qi'):
    url = 'https://www.xlovem.club/v1/notice/wechat'
    para_data = {
        'title': image_id,
        'desc': "",
        "msg_type": "iamge",
        'user_name': user_name,
        'bot_name': bot_name
    }
    return requests.post(url, json=para_data)


if __name__ == '__main__':
    res = send_wechat_notice("wo", '自己\n换行', user_name='ZhangGongZhu')
    print(res.text)
