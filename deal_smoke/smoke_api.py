from common.common_utils import api_request


# 1获取这次刷单信息 5获取所有刷单map
def get_this_time_info(get_type="1"):
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': get_type
    }
    ref, resp = api_request(url, data=para_data)
    if ref:
        return resp
    raise Exception("获取刷单信息失败")


# 2成功更新商品  4根据当前的主扫比例，给出下次的支付类型
def set_this_time_stock(item_id, get_type="2", run_count=1, smoke_stock_temp=None, cash_all=0, online_all=0):
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': get_type,
        'run_count': int(run_count),
        'smoke_stock_temp': smoke_stock_temp,
        'cash_all': cash_all,
        'online_all': online_all,
        'id': item_id
    }
    ref, resp = api_request(url, data=para_data)
    if ref and "data" in resp:
        return resp['data']
    return None


# 3获取支付码
def get_pay_no(get_type="3"):
    url = 'https://www.xlovem.club/v1/smoke/run'
    para_data = {
        'type': get_type
    }
    pay_no = "0"
    ref, resp = api_request(url, data=para_data)
    if ref and 'data' in resp:
        pay_no = resp['data']
    return str(pay_no) if pay_no and len(str(pay_no)) == 18 and str(pay_no).isdigit() else None
