# -*- coding: utf-8 -*-

import requests
import re
import chardet
import pymysql

class DB:
    def __init__(self, host="localhost", port=3306, db="", user="", passwd="", charset="gbk"):
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        self.cursor = self.conn.cursor(cursor = pymysql.cursors.DictCursor)
        
    def __enter__(self):
        return self.cursor
        
    def __exit__(self, exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        
def write_txt(file_name, txt):
    with open(file_name, "w") as wd:
        wd.write(txt)

def geturl():

    for page in range(0,0):    
#        url = "http://www./list_34_{}.html".format(str(page))
#        url = "http:///list_373_{}.html".format(str(page))
        url = "http://www./shandong/list_378_{}.html".format(str(page))
        html = requests.get(url)
        try:
            content = html.text.encode('ISO-8859-1').decode('gbk')
        except Exception as e:
            print(e)
#            content = html.text.encode('ISO-8859-1').decode('gb2312')
#            chardet.detect(txt)["encoding"]
#        print(content)
        write_txt("text.txt", content)
#        #获取url  #<a href="/.html">2014年山东高考满分作文范文800字 窗外</a>
        pattern2 = re.compile('<li><h3><a href=(.*?)</a></h3> ',re.S)
        items = re.findall(pattern2,content)
#        print(items)
        for i,text in enumerate(items):
            url_text = r"http://.cn" + text.split(">")[0].strip(r'"')
            name_text = text.split(">")[1]
            remark = name_text.split(" ")[0]
            new_name = name_text.strip(remark)
            if not new_name.strip(" "):
                new_name = remark
            
            print("The {1} url of the {0} page".format(page,i))
            with DB(db="test", user="root", passwd="********") as cursor:  #查重之后在判断是否加入
                sql = "insert into text_url(url,text_name,remark) values('{}','{}','{}')".format(url_text, new_name, remark)
#                print(sql)
                cursor.execute(sql)

def geturl_zuowen():
    """http:///index.shtml内的爬取所有url"""
    num = 0
    for page in range(2,86):
        url = "http:///manfen/index_{}.shtml".format(str(page))
#        url = "http:///manfen/index.shtml"
        html = requests.get(url)
        content = html.text.encode('ISO-8859-1').decode('gbk')
        pattern2 = re.compile('<div class="artbox_l_t">(.*?)</div>',re.S)
        items = re.findall(pattern2,content)
        
        for j in items:
             pattern = re.compile('<a href="(.*?)target="_blank">',re.S)
             item = re.findall(pattern,j)[0]
#             print(item, "\n")
             url = item.split('shtml')[0] + "shtml"
             all_inf = item.split('title="')[1][:-2]
             print(all_inf)
             if ":" in all_inf or "：" in all_inf:
                 all_inf = all_inf.replace("：", ":")
                 remark = all_inf.split(":")[0]
                 text_name = all_inf.split(":")[1]
             else:
                 remark, text_name = "", all_inf
             print(num, "#", page)
             with DB(db="test", user="root", passwd="********") as cursor:  #查重之后在判断是否加入
                num += 1
                sql = "insert into zw2(url,text_name,remark,all_inf) values('{}','{}','{}', '{}')".format(url, text_name, remark, all_inf)
                cursor.execute(sql)

def get_txt(url):
    pass

#geturl_zuowen()


with DB(db="test", user="root", passwd="********") as cursor:
    sql = "select * from zw2"
    isnum = cursor.execute(sql)
#    print(isnum)
    for sql_ in cursor.fetchall():
#        print(sql_["url"])  #dict
        url = sql_["url"]
        html = requests.get(url)
        content = html.text.encode('ISO-8859-1').decode('gbk')
        pattern = re.compile('<div class="con_main wx_dbclick">(.*?)</div>',re.S)
        
#        <div class="con_main wx_dbclick">
#        <div class="con_content">
        text = re.findall(pattern,content)[0]
        with open("page.txt", "w") as wd:
            wd.write(content)
        break
print("end")
