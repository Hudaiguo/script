# -*- coding: utf-8 -*-
import  pymysql


class DB:
    def __init__(self, host="localhost", port=3306, db="", user="", passwd="", charset="gbk"):
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":

    with DB(db="test", user="root", passwd="********") as cursor: 
        sql = "insert into zw2(url,text_name,remark,all_inf) values('{}','{}','{}', '{}')".format(url, text_name, remark, all_inf)
        cursor.execute(sql)
		
    with DB(db="test", user="root", passwd="********") as cursor:
        sql = 'update zw2 set download_status="1",txt="{}" where id={}'.format(zuowen_txt, id)
        cursor.execute(sql)