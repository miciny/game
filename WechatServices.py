import requests
import urllib3
urllib3.disable_warnings()


def send_wechat_notice(title, desc):
    key = 'SCU140810T91212209da974ea43a3e07e211d41c095feacae619327'
    url = 'https://sc.ftqq.com/%s.send' % key
    para_data = {
        'text': title,
        'desp': desc
    }
    return requests.get(url, params=para_data)


if __name__ == '__main__':
    res = send_wechat_notice("ceshiss", '自己')
    print(res.text)
