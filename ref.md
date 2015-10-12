数据源 result

数据源请求 url = 'http://www.homeinns.com/hotel'
数据源请求 method = get
数据源请求 format = html

数据源请求 datas
数据源请求 headers
数据源请求 cookies
数据源请求 timeout
数据源请求 additions

提取项 citys
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
