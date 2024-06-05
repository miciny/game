
from common.common_utils import shutdown_pc


if __name__ == '__main__':
    f_ready = input("关机时间(min): ")
    f_ready = int(f_ready)
    delay_time = 60 * f_ready
    shutdown_pc(delay_time)
