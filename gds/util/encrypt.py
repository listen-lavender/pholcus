#!/usr/bin/env python
# coding=utf8
import random, base64
from webcrawl.rsa import RSA
from Crypto.Cipher import AES

desc = {"色":"00e0b","流感":"509f6","这边":"259df","弱":"8642d","嘴唇":"bc356","亲":"62901","开心":"477df","呲牙":"22677","憨笑":"ec152","猫":"b5ff6","皱眉":"8ace6","幽灵":"15bb7","蛋糕":"b7251","发怒":"52b3a","大哭":"b17a8","兔子":"76aea","星星":"8a5aa","钟情":"76d2e","牵手":"41762","公鸡":"9ec4e","爱意":"e341f","禁止":"56135","狗":"fccf6","亲亲":"95280","叉":"104e0","礼物":"312ec","晕":"bda92","呆":"557c9","生病":"38701","钻石":"14af6","拜":"c9d05","怒":"c4f7f","示爱":"0c368","汗":"5b7a4","小鸡":"6bee2","痛苦":"55932","撇嘴":"575cc","惶恐":"e10b4","口罩":"24d81","吐舌":"3cfe4","心碎":"875d3","生气":"e8204","可爱":"7b97d","鬼脸":"def52","跳舞":"741d5","男孩":"46b8e","奸笑":"289dc","猪":"6935b","圈":"3ece0","便便":"462db","外星":"0a22b","圣诞":"8e7","流泪":"01000","强":"1","爱心":"0CoJU","女孩":"m6Qyw","惊恐":"8W8ju","大笑":"d"};

def trans(codes):
    return ''.join(desc[one] for one in codes)

PUB = trans(["流泪", "强"])
PRI = trans(["憨笑", "弱"])

PUB = '10001'
PRI = '8e9912f6d3645894e8d38cb58c0db81ff516cf4c7e5a14c7f1eddb1459d2cded4d8d293fc97aee6aefb861859c8b6a3d1dfe710463e1f9ddc72048c09751971c4a580aa51eb523357a3cc48d31cfad1d4a165066ed92d4748fb6571211da5cb14bc11b6e2df7c1a559e6d5ac1cd5c94703a22891464fba23d0d965086277a161'
N = 'a5261939975948bb7a58dffe5ff54e65f0498f9175f5a09288810b8975871e99af3b5dd94057b0fc07535f5f97444504fa35169d461d0d30cf0192e307727c065168c788771c561a9400fb49175e9e6aa4e23fe11af69e9412dd23b0cb6684c4c2429bce139e848ab26d0829073351f4acd36074eafd036a5eb83359d2a698d3'

KEY = trans(["爱心", "女孩", "惊恐", "大笑"])

def fromCharCode(*b):
    return ''.join(chr(a) for a in b)

class LocalRSA(RSA):
    def __init__(self, pub, pri, module):
        super(LocalRSA, self).__init__()
        self.rsakp = self.RSAKeyPair(pub, pri, module)

    def _encrypt(self, n, t):
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

    def _decrypt(self, n, t):
        e = 0
        c = t.split(' ')
        d = ""
        while e < len(c):
            if n['radix'] == 16:
                h = self.biFromHex(c[e])
            else:
                h = self.biFromString(c[e], n['radix'])
            g = n['barrett']['powMod'](n['barrett'], h, n['d'])
            f = 0
            while f <= self.biHighIndex(g):
                d = d + fromCharCode(255 & g['digits'][f], g['digits'][f] >> 8)
                f = f + 1
            e = e + 1
        if 0 == ord(d[len(d) - 1]):
            d = d[:len(d) - 1]
        return d

    def encrypt(self, sentence):
        return self._encrypt(self.rsakp, sentence)

    def decrypt(self, sentence):
        return self._decrypt(self.rsakp, sentence)

rsa = LocalRSA(PUB, PRI, N)


def randomKey(length=16):
    ori = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    index = 0
    sentence = ''
    while index < length:
        sentence += ori[int(random.random() * len(ori))]
        index = index + 1
    sentence = '4iLCZMe8op5jkcc9'
    return sentence

def pad(data):
    length = 16 - (len(data) % 16)
    return data + chr(length)*length

def encrypt_crypto(sentence, key):
    generator = AES.new(key, AES.MODE_CBC, "0102030405060708")
    return base64.b64encode(generator.encrypt(pad(sentence)))


if __name__ == '__main__':
    # import requests
    # content = '{"a":"hao","b":"kuan"}'
    # print encrypt_163(content)
    print ',', encrypt_crypto('{"a":1}', '4iLCZMe8op5jkcc9')
    


    