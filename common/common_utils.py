import time
import os
import sys
import requests
import json


def api_request(url, method="post", headers=None, data=None):
    print(f"request url: {method} {url}; data: {data}; headers: {headers}")
    timeout_sec = 60
    try:
        if method.lower() == "get":
            result_res = requests.request(method=method, url=url, headers=headers, timeout=timeout_sec)
        else:
            result_res = requests.request(method=method, url=url, json=data, headers=headers, timeout=timeout_sec)
        # 打印返回
        print(f"{url} result_res: {result_res.text}")
        res_j = json.loads(result_res.text)
        return True, res_j
    except Exception as e:
        print(e)
        return False, str(e)
    

def upload_file(url, file_path):
    try:
        with open(file_path, 'rb') as file:
            res = requests.post(url, files={'file': file})
            j_data = res.json()
            print('upload_file', j_data)
            if j_data['code'] == 0:
                return True, j_data['data']
    except Exception as e:
        print(e)
        return False, str(e)


# 平均值
def get_average(data_list):
    if len(data_list) == 0:
        return 0
    else:
        sum_all = 0
        for item in data_list:
            sum_all += item
        return sum_all / len(data_list)


# 时间格式化显示
def time_format(time_dlt):
    if time_dlt < 60:
        return str(round(time_dlt, 2)) + "s"
    elif time_dlt < 3600:
        time_dlt_m = int(time_dlt / 60)
        time_dlt_s = int(time_dlt % 60)
        return str(time_dlt_m) + "m " + str(time_dlt_s) + "s"
    else:
        time_dlt_h = int(time_dlt / 3600)
        time_dlt_m = int(time_dlt / 60 - 60 * time_dlt_h)
        time_dlt_s = int(time_dlt % 60)
        return str(time_dlt_h) + "h " + str(time_dlt_m) + "m " + str(time_dlt_s) + "s"


# 打印等待
def print_wait(time_sec, des=None):
    if des is None:
        time.sleep(time_sec)
    else:
        time_sec = int(time_sec)
        for i in range(time_sec):
            time.sleep(1)
            des_out = '\r%s: %s' % (des, str(i + 1) + "/" + str(time_sec))
            sys.stdout.write(des_out)
            sys.stdout.flush()
        print("")


# 关机
def shutdown_pc(delay_time=99):
    print_wait(delay_time, "自动关机倒计时：")
    os.system("shutdown /s")
