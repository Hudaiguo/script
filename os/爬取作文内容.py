# -*- coding: utf-8 -*-

import os
import time
import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# selenium启动Chrome配置参数
chrome_options = Options()
chrome_options.add_argument('--headless')  #Headless Chrome 是 Chrome 浏览器的无界面形态
chrome_options.add_argument('--disable-gpu') #加上这个属性来规避bug
chrome_options.add_argument('blink-settings=imagesEnabled=false') # 不加载图片, 提升速度


conn = pymysql.connect(host="localhost", port=3306, db="test", user="root", passwd="********", charset="gbk")
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
sql = "select * from zw2"
cursor.execute(sql)
for sql_ in cursor.fetchall():
    url = sql_["url"]
    id = sql_["id"]
    download_status = sql_["download_status"]
    print("id:{}, url:{}, status:{}".format(id, url, download_status))

    if download_status != "1":
        try:
            # 创建浏览器对象
            browser = webdriver.Chrome(chrome_options=chrome_options)
            browser.get(url)
            txt = browser.find_elements_by_class_name("con_content")
            txt_title = browser.find_elements_by_class_name("h_title")
            for i in txt_title:
                zuowen_title = i.text
                print(zuowen_title)
            zuowen_txt = ""
            for i in txt:
                zuowen_txt += i.text+"\n"
            with open(os.path.join("zuowen_txt", str(id)+"_"+zuowen_title+".txt"), "w+") as wd:
                wd.write(zuowen_txt)
            sql = 'update zw2 set download_status="1",txt="{}" where id={}'.format(zuowen_txt, id)
            cursor.execute(sql)
            conn.commit()
            # time.sleep(1)
            browser.close()
            browser.quit()
        except Exception:
            sql = 'update zw2 set download_status="0" where id={}'.format(id)
            cursor.execute(sql)
            conn.commit()

cursor.close()
conn.close()
print("end")