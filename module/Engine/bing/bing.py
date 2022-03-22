import requests
from lxml import etree
import re
import time
from db.dbserver import MySQLCommand

class BingEngine(object):
    def __init__(self, keyword_list):
        self.mysql = MySQLCommand()
        self.mysql.connectMysql()
        self.keyword_list = [i.strip() for i in keyword_list]
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "cookie": "DUP=Q=BWQriQwgVDG-1uxZ9j7oRQ2&T=413722706&A=2&IG=D1EAECE750FE4873AD3AA3CE155EC927; MUID=2B7AE5B0424F69112605EAD6438F6819; SNRHOP=I=&TS=; MUIDB=2B7AE5B0424F69112605EAD6438F6819; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=0725D03312B54387BBE1E7B47B892572&dmnchg=1; ENSEARCH=BENVER=1; ULC=P=51B9|1:1&H=51B9|1:1&T=51B9|1:1; _SS=SID=11605D78715C6E7826A852AB701F6F67&bIm=341; _FP=hta=on; SerpPWA=reg=1; ENSEARCHZOSTATUS=STATUS=0; KievRPSSecAuth=FABKARRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACNjbJXQoBj/BCAE9vNkU0vfQiujzKEEXXWSNsiMi0ZitKcEAb0czIJZ3vwzonozXlESTbc1YsHKxhMIgOhc92v1VIC3QzlfYO6s3WDpPOnis/ZNKDuDP%2BK8eZoUwCgm7baqh/S68jdwNZU9qCa/X0n9D5fjSZDsOlgjmcEBJnmXJOLJimYMGNldFEpd5AULy6lgqetFLBbMxVwW3cyjFiCpiMb0iA1abgcoqiGUI00wSt5L4BlYMRvh7QlT3gboUdGsFhWXvXjxX2xXNq%2B0fzUuhA6qtiivW9ygI9fvSPhJnQkmlRCXEvr28OlsfnGY%2BrjxiIFivVWLoi9eb5lSgkUTkZJlOCqZgIBzgaR/sZqeQJV8UANiGe7CAGu1YHTzP9tzU0ADiqX%2BJ; PPLState=1; ANON=A=EF96A70F0F8199A5D34957E8FFFFFFFF&E=1918&W=1; NAP=V=1.9&E=18be&C=Rr26JQgAdXit4mQy4EFHQz_lB7yg0BxQaHXYmhuwNINpWATyKDO6ag&W=1; _U=15DMfn6nsgtak4i3Lt55oPwwuogb1oCJ4FhnT4emp1uU9BlyBg2ED0hK6YoLgNoeXrYTKlXkhWqJX-QHCGDxNq1r4skT9wJdkNbqScyjpVY2Ynj0bIkWsyyGR2ZwBqzk8XjS05mBxd9ebMylwVeJ7_zA7FBDNjIWqUzlxNoJLZq76dya8GV9yyLzQTZa5Sss2; WLS=C=013892bea16ae168&N=mi; SRCHUSR=DOB=20210203&T=1612868226000&TPC=1612862553000&POEX=W; ipv6=hit=1612871830647&t=4; WLID=sPIZ6PTzUO038qUiNYGJueCscEV7vn21MXYK/gUXnagTHkKwEIZlxsYc4cgBDI/kZajIiktZPHuUMZ6vnBXHsfAYP41RgXa2aM54k488/F8=; _EDGE_S=SID=22B10F3EA4906227217B00E7A5D363F0&mkt=zh-cn; SRCHHPGUSR=BZA=0&BRW=W&BRH=S&CW=2034&CH=563&DPR=1&UTC=480&DM=0&PLTL=674&PLTA=674&PLTN=1&HV=1612868309&WTS=63748465026&SRCHLANGV2=zh-Hans"
        }
        self.pattern = re.compile(
            r'^((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}((/)|())?')

        self.xpath = ["//li[@class='b_algo']//a[@class='sb_metalink']//text()",
                      "//li[@class='b_algo']//div[@class='b_attribution']/cite//text()",
                      "//div[@class='b_caption']//div[@class='b_attribution']//cite//text()"
                      ]

    @staticmethod
    def produce(keyword):
        return ["https://cn.bing.com/search?q={}&qs=n&sp=-1&sp=-1&pq={}&sc=4-8&sk=&cvid=3C863030DEEA4A6F8CB1FB27CCAFCCE7&first={}&ubiroff=1&FORM=PERE".format(
                    keyword, keyword, i) for i in range(1, 1000, 10)]

    def request(self, url):
        resp = requests.get(url, headers=self.headers)
        print(url)
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
            # yield s1


if __name__ == '__main__':
    test_list = ['cms', '后台']
    bing = BingEngine(test_list)
    s1 = bing.run()
    for s in s1:
        print(s)