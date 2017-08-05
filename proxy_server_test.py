import urllib
from multiprocessing.pool import ThreadPool
from time import sleep

import requests

url = 'http://lol.com/'
http_proxy = "127.0.0.1:2323"
proxy_dict = {
    "http": http_proxy
}


def get(inc):
    sleep(1)
    r = requests.get(url, proxies=proxy_dict)
    if not r or r.status_code != 200:
        print('Number of request: ' + str(inc) + ' - error')
    else:
        print('Number of request: ' + str(inc) + ' - success')


if __name__ == "__main__":
    pool = ThreadPool(10)
    pool.map(get, range(0, 10000))
    pool.close()
    pool.join()
