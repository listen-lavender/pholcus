#!/usr/bin/python
# coding=utf-8

HCT = {"如家":"001",
    "和颐":"001",
    "云上四季":"001",
    "汉庭":"002",
    "漫心":"002",
    "禧玥":"002",
    "海友":"027",
    "全季":"028",
    "星程":"029",
    "锦江之星":"003",
    "锦江都城":"003",
    "金广快捷":"021",
    "百时快捷":"013",
    "7天优品":"020",
    "7天阳光":"020",
    "稻家酒店":"020",
    "喆·啡":"020",
    "麗枫":"020",
    "ZMAX潮漫":"020",
    "铂涛菲诺":"020",
    # "7天":"020",
    "速8":"005",
    "桔子":"006",
    "宜必思":"007",
    "格林豪泰":"008",
    "格林联盟":"008",
    "青皮树":"008",
    "格林东方":"008",
    "莫泰":"015",
    "布丁":"010",
    "Zhotels智尚":"010",
    "99旅馆":"011",
    "城市之家":"014",
    "古井君莱":"014",
    "禧龙快捷":"054",
    "南苑E家":"055",
    "清沐酒店":"057",
    "驿家365":"058",
    "城市客栈":"061",
    "今天连锁":"062",
    "欣燕都":"063",
    "山水时尚":"064",
    "富驿时尚":"068",
    "云端快捷":"900",
    "城市便捷":"016",
    "精通酒店":"017",
    "易佰":"018",
    "锐思特":"019",
    "A家连锁":"069",
    "爱尊客":"070",
    "八方快捷":"071",
    "春天时尚":"073",
    "方圆快捷":"074",
    "肯定":"075",
    "浦江之星":"076",
    "艳阳天":"077",
    "中州快捷":"079",
    "银座佳驿":"023",
    "吉泰":"024",
    "维也纳":"025",
    "都市118":"026",
    "格子微":"300",
    "e家连锁":"300",
    "其他品牌":"300",
    "尚客优":"032",
}

def formatDatestr(build_time, decorate_time):
    """
        格式化开业事件，装修时间
        @param build_time: 开业时间
        @param decorate_time: 装修时间
        @return build_time: 返回格式化的开业时间
        @return decorate_time: 返回格式化的装修时间
    """
    build_time = build_time or ''
    build_time = build_time.split('-')
    decorate_time = decorate_time or ''
    decorate_time = decorate_time.split('-')
    build_time = build_time[0] + '-' + build_time[1].rjust(2, '0') if build_time and len(build_time) > 1 else ''
    if decorate_time and decorate_time[0] < '2003':
        decorate_time = ''
    else:
        decorate_time = decorate_time[0] + '-' + decorate_time[1].rjust(2, '0') if decorate_time and len(decorate_time) > 1 else ''
    return build_time, decorate_time

def ensureHotelclass(isclear, hotel_name, hotel_prefix, hotel_type):
    """
        确定酒店名称，酒店前缀，酒店type
        @param isclear: 是否清洗成功
        @param hotel_name: 名称
        @param hotel_prefix: 前缀
        @param hotel_type: type
        @return isclear: 清洗状态
        @return hotel_name: 返回规范化的名称
        @return hotel_prefix: 返回规范化的前缀
        @return hotel_type: 返回规范化的type
    """
    hotel_name = hotel_name or ''
    nameRE = re.compile('(\(|（)((原[^)]*)|(郊区)|(内宾)|(外宾)|(中宾))(\)|）)')
    hotel_name = nameRE.sub('', hotel_name)
    hotel_name = hotel_name.replace('（', '').replace('）', '').replace('(', '').replace(')', '')
    for key, val in HCT.items():
        if hotel_name.startswith(key):
            hotel_name = hotel_name.replace(key + '快捷酒店', '')
            hotel_name = hotel_name.replace(key + '连锁酒店', '')
            hotel_name = hotel_name.replace(key + '酒店', '')
            hotel_name = hotel_name.replace(key + '快捷', '')
            hotel_name = hotel_name.replace(key + '连锁', '')
            hotel_name = hotel_name.replace(key, '')
            hotel_prefix = key or hotel_prefix
            hotel_type = val or hotel_type
            break
        elif '和颐' in hotel_name:
            hotel_prefix = '和颐'
            hotel_type = '001'
            hotel_name = hotel_name.replace('和颐酒店', '店')
            break
        elif '漫心' in hotel_name:
            hotel_prefix = '漫心'
            hotel_type = '002'
            hotel_name = hotel_name.replace('漫心丽江度假酒店', '')
            hotel_name = hotel_name.strip()
            if hotel_name == '':
                hotel_name = '漫心丽江度假酒店'
            else:
                hotel_name = hotel_name + '店'
            break
        elif '禧玥' in hotel_name:
            hotel_prefix = '禧玥'
            hotel_type = '002'
            hotel_name = hotel_name.replace('禧玥酒店', '店')
            break
        elif '锦江都城' in hotel_name:
            hotel_prefix = '锦江都城'
            hotel_type = '003'
            hotel_name = hotel_name.replace('锦江都城', '')
            break
        elif '白玉兰酒店' in hotel_name:
            hotel_prefix = '白玉兰酒店'
            hotel_type = '003'
            hotel_name = hotel_name.replace('白玉兰酒店', '').replace('白玉兰', '')
            break
        elif '稻家酒店' in hotel_name:
            hotel_prefix = '稻家酒店'
            hotel_type = '020'
            hotel_name = hotel_name.replace('稻家酒店', '')
            break
        elif '铂涛菲诺' in hotel_name:
            hotel_prefix = '铂涛菲诺'
            hotel_type = '020'
            hotel_name = hotel_name.replace('铂涛菲诺酒店', '').replace('铂涛菲诺管理', '').replace('铂涛菲诺', '')
            break
        elif '7天阳光' in hotel_name:
            hotel_prefix = '7天阳光'
            hotel_type = '020'
            hotel_name = hotel_name.replace('7天阳光酒店', '').replace('标准装修', '').replace('7天阳光', '')
            break
        elif '7天优品' in hotel_name:
            hotel_prefix = '7天优品'
            hotel_type = '020'
            hotel_name = hotel_name.replace('7天优品酒店', '').replace('标准装修', '').replace('7天优品', '')
            break
        elif '喆啡' in hotel_name:
            hotel_prefix = '喆啡'
            hotel_type = '020'
            hotel_name = hotel_name.replace('喆啡酒店', '店')
            break
        elif '麗枫酒店·' in hotel_name:
            hotel_prefix = '麗枫酒店'
            hotel_type = '020'
            hotel_name = hotel_name.replace('麗枫酒店·', '')
            break
        elif '潮漫酒店' in hotel_name:
            hotel_prefix = '潮漫酒店'
            hotel_type = '020'
            hotel_name = hotel_name.replace('潮漫酒店', '店')
            break
        elif hotel_name.startswith('7天'):
            hotel_name = hotel_name.replace('7天' + '快捷酒店', '')
            hotel_name = hotel_name.replace('7天' + '连锁酒店', '')
            hotel_name = hotel_name.replace('7天' + '酒店', '')
            hotel_name = hotel_name.replace('7天' + '快捷', '')
            hotel_name = hotel_name.replace('7天' + '连锁', '')
            hotel_name = hotel_name.replace('7天', '')
            hotel_prefix = '7天'
            hotel_type = '020'
            break
        elif '古井君莱' in hotel_name:
            hotel_prefix = '君莱'
            hotel_type = '014'
            hotel_name = hotel_name.replace('古井君莱酒店', '店')
            break
        elif 'Zhotels' in hotel_name or '智尚酒店' in hotel_name:
            hotel_prefix = '智尚'
            hotel_type = '010'
            hotel_name = hotel_name.replace('智尚酒店', '').replace('Zhotels', '')
            break
        elif '格林联盟' in hotel_name:
            hotel_prefix = '格林联盟'
            hotel_type = '008'
            hotel_name = hotel_name.replace('格林联盟酒店', '').replace('格林联盟', '')
            break
        elif '格林东方' in hotel_name:
            hotel_prefix = '格林东方'
            hotel_type = '008'
            hotel_name = hotel_name.replace('格林东方酒店', '').replace('格林东方', '')
            break
        elif hotel_name.startswith('青皮树'):
            hotel_prefix = '青皮树'
            hotel_type = '008'
            hotel_name = hotel_name.replace('青皮树酒店', '').replace('青皮树', '')
            break
    else:
        if hotel_prefix in HCT:
            hotel_type = hotel_type or val
        else:
            hotel_prefix = ''
            hotel_type = '300'
    if '太原' in hotel_name:
        pass
    else:
        hotel_name = hotel_name.split('原')[0].replace('-', '').replace('(按照7天酒店标准装修)', '').replace('连锁酒店', '店').replace('快捷酒店', '店').split('省')[-1]
    # hotel_name = specifyName(hotel_name)
    return isclear and True, hotel_name, hotel_prefix, hotel_type
