# from task.hotel.spiderWeiye import SpiderWyn88
from task.hotel.spiderWC import SpiderWyn88
if __name__ == '__main__':
    spider = SpiderWyn88(worknum=6, queuetype='P', worktype='COROUTINE')
    spider.fetchDatas('wap', 'http://wap.wyn88.com/Hotel/Index')
    spider.statistic()
