# from task.hotel.spiderWeiye import SpiderWyn88
#!/usr/bin/python
# coding=utf-8
from task.hotel.spiderRujia import SpiderHomeinns
# from task.hotel.spiderHanting import SpiderHomeinns

if __name__ == '__main__':
    spider = SpiderHomeinns(worknum=6, queuetype='P', worktype='COROUTINE')
    spider.fetchDatas('www', 'http://www.homeinns.com/hotel')
    spider.statistic()
