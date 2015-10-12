1. 数据源 result

数据源请求 url = 'http://www.homeinns.com/hotel'
数据源请求 method = get
数据源请求 format = html

提取项 citys1
    提取源 result
    提取方式 findall
    提取路径 //ul[@class='ml_order_link']//a
提取项 city
    提取源 citys
    提取方式 find
    提取路径 .
    提取内容 {'ATTR':'href'}
    传递 yes
    存储 no

2. 数据源 result

数据源请求 url = 'http://www.homeinns.com/beijing/p1'
数据源请求 method = get
数据源请求 format = html

翻页数据 next_page
    提取源 result
    提取方式 find
    提取路径 .//div[@class='page_next']//a
    提取内容 {'ATTR':'href'}

提取项 hotels
    提取源 result
    提取方式 findall
    提取路径 .//div[@class='list_intro_name_tj']//a
提取项 hotel
    提取源 hotels
    提取方式 find
    提取路径 .
    提取内容 {'ATTR':'href'}
    传递 yes
    存储 no


3. 数据源 result

数据源请求 url = 'http://www.homeinns.com/hotel/AJ1023'
数据源请求 method = get
数据源请求 format = html

数据源 rpq

数据源请求 url = url
数据源请求 method = parturl
数据源请求 format = url

提取项 hotel_id
    提取源 rpq
    提取方式 find
    提取路径 [0][-1]
    提取内容 
    传递 no
    存储 yes

提取项 hotel_name
    提取源 result
    提取方式 find
    提取路径 .//div[@class='hotelname']
    提取内容 TEXT
    传递 no
    存储 yes

提取项 hotel_type
    默认值 001

提取项 lat
    提取源 result
    提取方式 find
    提取路径 .//input[@id='zuobiao_y']
    提取内容 {'ATTR':'value'}
    传递 no
    存储 yes

提取项 lnt
    提取源 result
    提取方式 find
    提取路径 .//input[@id='zuobiao_x']
    提取内容 {'ATTR':'value'}
    传递 no
    存储 yes

提取项 address
    提取源 result
    提取方式 find
    提取路径 .//a[@pop='addressTip']
    提取内容 TEXT
    传递 no
    存储 yes

提取项 logo
    提取源 result
    提取方式 find
    提取路径 .//div[@class='pic1 ']//div
    提取内容 TEXT
    传递 no
    存储 yes

提取项 tel
    提取源 result
    提取方式 find
    提取路径 .//div[@class='tel']
    提取内容 {'ATTR':'_src'}
    传递 no
    存储 yes

提取项 status
    默认值 1

提取项 tid
    默认值 self.tid

提取项 create_time
    默认值 datetime.now()


grab_dataextract