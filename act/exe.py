# from task.hotel.spiderWeiye import SpiderWyn88
from task.hotel.spiderRujia import SpiderHomeinns

if __name__ == '__main__':
    spider = SpiderHomeinns(worknum=6, queuetype='P', worktype='COROUTINE')
    spider.fetchDatas('www', 'http://www.homeinns.com/')
    spider.statistic()
