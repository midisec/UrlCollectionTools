# collect-url-tools-base-keywords

一款根据关键词批量采集url的小脚本，支持多个关键词批量采集。



### Tools详情
基于python3的小脚本，自带去重功能，目前仅支持bing国际引擎采集，由于搜索引擎的不稳定性后续会根据情况更新或新增其他引擎！
目前没有实现多线程，等待后续改进！

### 使用条件

python3+mysql

> $ pip install request

下载lxml
地址：http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml

#
> $ python -m pip install 对应本地路径./lxml-3.7.1-cp35-cp35m-win_amd64.whl


#### 获取工具

> $ git clone https://github.com/Digeya/collect-url-tools-base-keywords-.git


### 提示
将/db/dbserver.py中的信息修改为自己的数据库

作者数据库结构为：
  数据库名： url
  数据库表名：url_tables
  字段：id、url
  (id为主键 int 类型 url 为longtext类型)


### 效果预览


![采集](https://github.com/Digeya/collect-url-tools-base-keywords-/blob/main/2.png)
![结果](https://github.com/Digeya/collect-url-tools-base-keywords-/blob/main/1.png)

#### 后续
欢迎交流学习，有问题直接issue
互相学习。

目前该项目是六个月之前了，这个暑假会想办法更新一下。
  
