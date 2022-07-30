import requests
from lxml import etree
import re, time
import urllib3
import config
from db.dbserver import MySQLCommand


class GoogleEngine(object):
    def __init__(self, keyword_list):
        urllib3.disable_warnings()
        self.mysql = MySQLCommand()
        self.mysql.connectMysql()
        self.keyword_list = [i.strip() for i in keyword_list]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.google.com.hk/',
            'Cookie': '1P_JAR=2022-07-21-12; NID=511=n9vG1tS6R54Id81eXSY6vi8RySxjrXNMT6d3QWKzSPYQ8WpNKD03kHB6TsTGtJFgqyPxRuIF2cophzRKhsBQR7TagmfP7SQZ7R2qXlGPWBQCTf47vw98IE3TGyYPKhDZ3zkkqOooILTyIZQ3nfgb44IVbKVP-qgtZMONIgwT9cTFKtUoBCLopYU0gL_WoxeW12qoZsg; AEC=AakniGNjeaGlCmmeL5BCWM58RXTz0SkSjouE0329LCwKKQOms7JUznlXIQ',
            'DNT': '1',
            'X-Forwarded-For': '8.8.8.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.proxies = config.PROXIES
        self.pattern = re.compile(
            r'^((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}((/)|())?')

        self.xpath = ["//a/div//text()"]

    @staticmethod
    def produce(keyword):
        return ["https://www.google.com.hk/search?q={}&lr=&newwindow=1&safe=images&hl=zh-CN&as_qdr=all&as_rights=%E4%B8%8D%E6%8C%89%E7%85%A7%E8%AE%B8%E5%8F%AF%E8%BF%87%E6%BB%A4&ei=ZUjZYqz7OPDL2roPy7CbeA&start={}&sa=N&biw=1536&bih=722&dpr=1.25".format(
                    keyword, i) for i in range(1, 150, 10)]

    def request(self, url):
        resp = requests.get(url, headers=self.headers, proxies=self.proxies, verify=False, timeout=5)
        print(url)
        print(resp.content.decode())
        return resp.content.decode()

    def withdraw(self, content, s1):
        html = etree.HTML(content)
        div_list = []
        for xpath in self.xpath:
            div_list += html.xpath(xpath)

        for div in div_list:
            m = self.pattern.match(div)
            try:
                s1.add(m.group())
            except Exception as e:
                print(e)
                time.sleep(2)  # waf
                pass

    def set_xpath(self):
        pass

    def insert_database(self, s1):
        for url in s1:
            self.mysql.insertData(url)

    def run(self):
        s1 = set()
        for keyword in self.keyword_list:
            s1.clear()
            for url in self.produce(keyword):
                content = self.request(url)
                self.withdraw(content, s1)
            self.insert_database(s1)


if __name__ == '__main__':
    test_list = ['cms', '后台']
    bing = GoogleEngine(test_list)
    bing.run()
