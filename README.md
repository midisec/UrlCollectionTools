# [UrlCollectionTools](https://github.com/midisec/UrlCollectionTools)

**一款根据关键词进行多线程、多引擎同时并发采集url的工具，支持多个关键词，结果自动去重。**



## 支持的搜索引擎

| 搜索引擎   | 多线程 | 时间       |
| ---------- | ------ | ---------- |
| Bing国内版 | √      | 2022-11-22 |
| Bing国际版 | √      | 2022-11-22 |
|            |        |            |




## 快速上手

克隆项目

```
git clone https://github.com/midisec/UrlCollectionTools
```

python3的环境，安装依赖包。

```bash
pip3 install -r requirements.txt
```

创建mysql数据库，并将sql.sql文件导入进mysql

修改连接数据库配置文件(./db/dbserver.py)



### 数据库结构

| 数据库名 | 表名       | 字段名1                    | 字段名2            |
| -------- | ---------- | -------------------------- | ------------------ |
| url      | url_tables | id(int, primary key, auto) | url(text, len(30)) |

设置多个关键词 keywords.txt

启动

```bash
python3 main_tools.py
```




## 效果预览

2H2G4M的机器，十个小时约8w条url



## 更新消息

2022-03-22


* 重写项目结构
* 支持bing国内、国际搜索引擎
* 新增多线程，可同时对多个搜索引擎采集

2022-11-22

* bing搜索引擎支持关键词的多线程采集，提升性能
