from common.common_utils import api_request


def get_this_time_info():
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': '1'
    }
    ref, resp = api_request(url, data=para_data)
    if ref:
        return resp
    raise Exception("获取刷单信息失败")


if __name__ == '__main__':
    get_this_time_info()
