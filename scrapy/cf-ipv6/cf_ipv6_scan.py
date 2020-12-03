import threading
import requests

# multithread
def multi_check_ip(start, end):
    print(threading.current_thread().name, 'start!')
    for i in range(start, end):
        hex_num = str(hex(i)).split('x')[-1]
        ip = base_ip + hex_num + '::'
        url = f'http://[{ip}]/cdn-cgi/trace'
        try:
            r = requests.get(url, timeout=1)
            solo = r.text.split()[6].split('=')[-1]
            lock.acquire()
            valid_ip.write(ip + ' ' + solo + '\n')
            lock.release()
            print(ip, solo)
        except Exception as e:
            print(url, e)


if __name__ == '__main__':
    base_ip = '2606:4700:'
    valid_ip = open('cf_valid_ipv6.txt', 'a+')
    thread_list = []
    lock = threading.Lock()
    thread_num = 64
    task_num = int(65536 / thread_num)
    for i in range(thread_num):
        start = i * task_num
        end = (i + 1) * task_num
        t = threading.Thread(target=multi_check_ip, args=(start, end))
        thread_list.append(t)

    last_start = thread_num * task_num
    last_task = threading.Thread(target=multi_check_ip, args=(last_start, 65536))
    thread_list.append(last_task)

    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

    valid_ip_num = len(valid_ip.readlines())
    valid_ip.close()
    print(f'本次扫描结束，共扫到{valid_ip_num}个有效ip')
