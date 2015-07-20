from task.hotel.spiderWeiye import SpiderWyn88
if __name__ == '__main__':
    print 'start'
    spider = SpiderWyn88(worknum=6, queuetype='P', worktype='GEVENT')
    spider.fetchDatas('wap', 'http://wap.wyn88.com/Hotel/Index')
    spider.statistic()
    # spider.extractFlow()
    # spider.fire('http://www.homeinns.com/')
    print 'end'