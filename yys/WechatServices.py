import requests
import urllib3
urllib3.disable_warnings()


def send_wechat_notice(title, desc):
    url = 'https://www.xlovem.club/v1/sendNotice'
    para_data = {
        'title': title,
        'desc': desc
    }
    return requests.post(url, json=para_data)


if __name__ == '__main__':
    res = send_wechat_notice("wo", '自己')
    print(res.text)
