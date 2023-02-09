'''
Author: sk 2309620371@qq.com
Description: 
'''
from Crypto.Cipher import AES
import base64
import requests
import json
import pandas as pd
url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
in_path = '网易云热歌版.csv'
e = "010001"  
f  = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
g = "0CoJUm6Qyw8W8jud"
i = "fsdIht4skB1GpJ5N"  #"K1bsa6wlRuqEtPXD"  "fsdIht4skB1GpJ5N"
iv = '0102030405060708'

#获取params
def get_params(data):
    first = enc_params(data,g)
    second = enc_params(first,i)
    #返回params
    return second

#AES加密处理data
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad)*pad 
    return data
#加密过程
def enc_params(data,key):
    #按照b函数编写
    data = to_16(data)
    ase = AES.new(key=key.encode("utf-8"),iv=iv.encode("utf-8"),mode=AES.MODE_CBC)
    bs = ase.encrypt(data.encode("utf-8")) #加密 长度必须是16的倍数
    #转换成字符串返回
    return str(base64.b64encode(bs),"utf-8")

#获取encSecKey
def get_encSecKey():
    return "cfd91ad8f12ddd6184c0d513c298df72dd1d4d12e0bcc11c65c8e97c70494e693522622e9927de834a0a6114753a40ed1649ba97ff0a1754c8d2a18a3d26ffbe3125dacee2c437f87acd23c4c8107f4e98e680ea07daff12af05dfbcc8dcb4aded2637ccdf33a8a4dfc149b10ab52dbeaf56fbd7bb879143fbf0c7b396382559"


user_name = []
user_content = []
user_IP = []

for k in range(1,90):
    print(k)
    data = {
        "csrf_token": "",
        "cursor": "-1",
        "offset": "0",
        "orderType": "1",
        "pageNo": k,
        "pageSize": "20",
        "rid": "R_SO_4_185711",
        "threadId": "R_SO_4_185711"
        }
    result = requests.post(url,data={
        "params" : get_params(json.dumps(data)),
        "encSecKey" : get_encSecKey()
    })
    
    # 写入每首歌的评论者的相关信息
    r_dic = json.loads(result.text)
    # print(len((r_dic['data'])['hotComments']))
    for j in (r_dic['data'])['comments'] :
        user_name.append((j['user'])['nickname'])
        user_content.append(j['content'])
        user_IP.append((j['ipLocation'])['location'])
    assert len(user_content) == len(user_name)
dataframe = pd.DataFrame({"user_name":user_name,"user_content":user_content,"user_IP":user_IP})
out_filepath = "再见.csv"
dataframe.to_csv(out_filepath,index=False,sep=',')