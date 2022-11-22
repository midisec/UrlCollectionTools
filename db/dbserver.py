import pymysql
import threading

class MySQLCommand(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306  # 端口号
        self.user = 'root'  # 用户名
        self.password = "*"  # 密码
        self.db = "url"  # 库
        self.table = "url_tables"  # 表
        self.lock = threading.Lock()

    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.password, db=self.db, charset='utf8')
            self.cursor = self.conn.cursor()

        except:
            print('connect mysql error.')

# 插入数据，插入之前先查询是否存在，如果存在就不再插入
    def insertData(self, url):
        table = "url_tables"  # 要操作的表格

        sqlExit = "SELECT url FROM url_tables  WHERE url = '%s'" % (url)
        self.lock.acquire()
        print(sqlExit)
        res = self.cursor.execute(sqlExit)
        self.lock.release()
        if res:  # res为查询到的数据条数如果大于0就代表数据已经存在
            print("数据已存在", res)
            return 0
        # 数据不存在才执行下面的插入操作
        try:
            sql = "INSERT INTO url_tables (url) VALUES ('%s')" % (url)
            # print(sql)
            # INSERT INTO url_tables VALUES ('test');
            #拼装后的sql如下
            # INSERT INTO home_list (img_path, url, id, title) VALUES ("https://img.huxiucdn.com.jpg"," https://www.huxiu.com90.html"," 12"," ")
            try:
                self.lock.acquire()
                result = self.cursor.execute(sql)
                insert_id = self.conn.insert_id()  # 插入成功后返回的id
                self.conn.commit()
                self.lock.release()
                # 判断是否执行成功
                if result:
                    print("插入成功", insert_id)
                    return insert_id + 1
            except pymysql.Error as e:
                # 发生错误时回滚
                self.conn.rollback()
                # 主键唯一，无法插入
                if "key 'PRIMARY'" in e.args[1]:
                    print("数据已存在，未插入数据")
                else:
                    print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

# if __name__ == '__main__':
#     mysql = MySQLCommand()
#     mysql.connectMysql()
#     mysql.insertData("test2")
