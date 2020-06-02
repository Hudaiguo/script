# -*- coding: utf-8 -*-
"""
@Time:   2020/6/2 16:34
@Author: Hudaiguo
@python version: 3.5.2
"""


from wxpy import *
import requests
import time

bot = Bot()  # 连接微信,会出现一个登陆微信的二维码


# def get_news():  #可以通过爬虫获得天气或美文
#    '''获取金山词霸每日一句'''
#    url = 'http://open.iciba.com/dsapi'
#    r = requests.get(url)
#    content = r.json()['content']
#    note = r.json()['note']
#    return content,note
def send_news(people):

    try:
        #        contents = get_news()
        #        my_friend.send(contents[1])
        my_friend = bot.friends().search(people)[0]  # 这里是你微信好友的昵称
        my_friend.send("记")
    #        t = Timer(3600,send_news)#这里是一天发送一次，86400s = 24h
    except:
        my_friend = bot.friends().search('sixkery')[0]  # 这里是你的微信昵称
        my_friend.send(u'今天消息发送失败了')

def sleeptime(hour, min_, sec):
    return hour * 3600 + min_ * 60 + sec

if __name__ == '__main__':
    timetime = input("输入需要间隔的时间，例如：1,0,0").split(",")
    timetime = [int(i) for i in timetime]
    people = input("发送好友名称：")
    while True:
        send_news(people)
        localtime = time.asctime(time.localtime(time.time())).split(" ")[3]
        time.sleep(sleeptime(timetime[0], timetime[1], timetime[2]))
        print(localtime)