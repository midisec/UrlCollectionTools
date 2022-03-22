from module.Engine.bing.bing import BingEngine
from module.Engine.bing.bingInternational import BingInternationalEngine

import threading


def work1(keyword_list):
    bing = BingEngine(keyword_list)
    bing.run()


def work2(keyword_list):
    bing = BingInternationalEngine(keyword_list)
    bing.run()


if __name__ == '__main__':
    test_list = ['cms', '后台']
    threads = []
    threads.append(threading.Thread(target=work1,args=(test_list,)))
    threads.append(threading.Thread(target=work2,args=(test_list,)))
    for t in threads:
        t.start()
