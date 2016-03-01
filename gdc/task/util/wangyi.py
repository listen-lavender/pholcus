#!/usr/bin/env python
# coding=utf8
import random, base64
from webcrawl.rsa import RSA
from Crypto.Cipher import AES

src = ["色", "流感", "这边", "弱", "嘴唇", "亲", "开心", "呲牙", "憨笑", "猫", "皱眉", "幽灵", "蛋糕", "发怒", "大哭", "兔子", "星星", "钟情", "牵手", "公鸡", "爱意", "禁止", "狗", "亲亲", "叉", "礼物", "晕", "呆", "生病", "钻石", "拜", "怒", "示爱", "汗", "小鸡", "痛苦", "撇嘴", "惶恐", "口罩", "吐舌", "心碎", "生气", "可爱", "鬼脸", "跳舞", "男孩", "奸笑", "猪", "圈", "便便", "外星", "圣诞"];
desc = {"色":"00e0b","流感":"509f6","这边":"259df","弱":"8642d","嘴唇":"bc356","亲":"62901","开心":"477df","呲牙":"22677","憨笑":"ec152","猫":"b5ff6","皱眉":"8ace6","幽灵":"15bb7","蛋糕":"b7251","发怒":"52b3a","大哭":"b17a8","兔子":"76aea","星星":"8a5aa","钟情":"76d2e","牵手":"41762","公鸡":"9ec4e","爱意":"e341f","禁止":"56135","狗":"fccf6","亲亲":"95280","叉":"104e0","礼物":"312ec","晕":"bda92","呆":"557c9","生病":"38701","钻石":"14af6","拜":"c9d05","怒":"c4f7f","示爱":"0c368","汗":"5b7a4","小鸡":"6bee2","痛苦":"55932","撇嘴":"575cc","惶恐":"e10b4","口罩":"24d81","吐舌":"3cfe4","心碎":"875d3","生气":"e8204","可爱":"7b97d","鬼脸":"def52","跳舞":"741d5","男孩":"46b8e","奸笑":"289dc","猪":"6935b","圈":"3ece0","便便":"462db","外星":"0a22b","圣诞":"8e7","流泪":"01000","强":"1","爱心":"0CoJU","女孩":"m6Qyw","惊恐":"8W8ju","大笑":"d"};

def trans(codes):
    return ''.join(desc[one] for one in codes)

USERID = trans(["流泪", "强"]) 
PASSWD = trans(src)
KEY = trans(["爱心", "女孩", "惊恐", "大笑"])

class RSA163(RSA):
    def encryptedString(self, n, t):
        p = len(t)
        l = [0] * n['chunkSize']
        for i in range(0, p):
            l[i] = ord(t[i])
        e = len(l)
        o = ""
        i = 0
        while i < e:
            c = self.bigInt(self.maxDigits)
            s = 0
            h = i
            while h < i + n['chunkSize']:
                c['digits'][s] = l[h]
                h = h + 1
                c['digits'][s] += l[h] << 8
                h = h + 1
                s = s + 1
            a = n['barrett']['powMod'](n['barrett'], c, n['e'])
            y = self.biToHex(a) if n['radix'] == 16 else self.biToString(a, n['radix'])
            o += y + " "
            i = i + n['chunkSize']
        return o[0:len(o) - 1]

    """
    function decryptedString(a, b) {
        var e, f, g, h, c = b.split(" "),
        d = "";
        for (e = 0; e < c.length; ++e) 
            for (h = 16 == a.radix ? biFromHex(c[e]) : biFromString(c[e], a.radix), g = a.barrett.powMod(h, a.d), f = 0; f <= biHighIndex(g); ++f) 
                d += String.fromCharCode(255 & g.digits[f], g.digits[f] >> 8);
        return 0 == d.charCodeAt(d.length - 1) && (d = d.substring(0, d.length - 1)), d
    }
    """


def random_lenstr(length):
    ori = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    index = 0
    sentence = ''
    while index < length:
        sentence += ori[int(random.random() * len(ori))]
        index = index + 1
    # sentence = 'wsiuDrSHrFP6eP84'
    return sentence

def pad(data):
    length = 16 - (len(data) % 16)
    return data + chr(length)*length

def encrypt_crypto(sentence, key):
    generator = AES.new(key, AES.MODE_CBC, "0102030405060708")
    return base64.b64encode(generator.encrypt(pad(sentence)))

def encrypt_rsa(sentence, userid, passwd):
    rsa = RSA163()
    ab = rsa.RSAKeyPair(userid, "", passwd)
    return rsa.encryptedString(ab, sentence)

def encrypt_163(content, userid=USERID, passwd=PASSWD, key=KEY):
    result = {}
    sentence = random_lenstr(16)
    result['encText'] = encrypt_crypto(content, key)
    result['encText'] = encrypt_crypto(result['encText'], sentence)
    result['encSecKey'] = encrypt_rsa(sentence, userid, passwd)
    return {'params':result['encText'], 'encSecKey':result['encSecKey']}

if __name__ == '__main__':
    import requests
    content = '{"a":"hao","b":"kuan"}'
    print encrypt_163(content)
    


    