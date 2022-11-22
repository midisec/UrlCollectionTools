from module.Engine.bing.bing import BingEngine
from module.Engine.bing.bingInternational import BingInternationalEngine

import threading


def work1(keyword_list):
    bing = BingEngine(keyword_list)
    # bing.run()
    bing.asy_run()


def work2(keyword_list):
    bing = BingInternationalEngine(keyword_list)
    # bing.run()
    bing.asy_run()


if __name__ == '__main__':
    with open('keywords.txt', 'r', encoding='utf-8') as f:
        keyword_list = f.readlines()
    threads = []
    threads.append(threading.Thread(target=work1,args=(keyword_list,)))
    threads.append(threading.Thread(target=work2,args=(keyword_list,)))
    for t in threads:
        t.start()
