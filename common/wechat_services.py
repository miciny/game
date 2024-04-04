import requests
import urllib3
urllib3.disable_warnings()


def send_wechat_notice(title, desc, user_name='MaoCaiYuan'):
    url = 'https://www.xlovem.club/v1/notice/wechat'
    para_data = {
        'title': title,
        'desc': desc,
        'user_name': user_name
    }
    return requests.post(url, json=para_data)


if __name__ == '__main__':
    res = send_wechat_notice("wo", '自己\n换行', user_name='ZhangGongZhu')
    print(res.text)
