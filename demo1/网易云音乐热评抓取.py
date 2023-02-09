'''
Author: sk 2309620371@qq.com
Description: 
'''
#1、找到未加密参数
#2、参数加密(参考网易的逻辑)
#3、获取评论
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


def get_rid(id):
    rid = "R_SO_4_%s"%(str(id))
    return rid



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




def get_KeyItem(in_path):
    id_nums = pd.read_csv(in_path)
    music_id_name = []
    music_id = []
    for i in id_nums['data']:
        # 获取歌曲名称
        music_id_name.append(str(eval(i)['musicname'])) 
        # 获取歌曲ID
        music_id.append(str(eval(i)['musicid']))
    # return zip(music_id_name,music_id)
    return music_id_name,music_id
# music_id_list = get_KeyItem(in_path)
music_id_name,music_id = get_KeyItem(in_path)
# data = {
#         "csrf_token": "",
#         "cursor": "-1",
#         "offset": "0",
#         "orderType": "1",
#         "pageNo": "1",
#         "pageSize": "20",
#         "rid": get_rid(music_id[3]),
#         "threadId": get_rid(music_id[3])
#         }
# result = requests.post(url,data={
#         "params" : get_params(json.dumps(data)),
#         "encSecKey" : get_encSecKey()
#     })
    
#     # 写入每首歌的评论者的相关信息
# user_name = []
# user_content = []

# r_dic = json.loads(result.text)
#     # print(len((r_dic['data'])['hotComments']))
# for i in (r_dic['data'])['hotComments'] :
#     user_name.append((i['user'])['nickname'])
#     user_content.append(i['content'])
# assert len(user_content) == len(user_name)
# dataframe = pd.DataFrame({"user_name":user_name,"user_content":user_content})
# out_filepath = '歌名_%s_HotComment.csv'%(str(music_id_name[3]))
# dataframe.to_csv(out_filepath,index=False,sep=',')

for k in range(len(music_id_name)):
    # print(i)
    id = get_rid(music_id[k])
    data = {
        "csrf_token": "",
        "cursor": "-1",
        "offset": "0",
        "orderType": "1",
        "pageNo": "1",
        "pageSize": "20",
        "rid": id,
        "threadId": id
        }
    result = requests.post(url,data={
        "params" : get_params(json.dumps(data)),
        "encSecKey" : get_encSecKey()
    })
    
    # 写入每首歌的评论者的相关信息
    user_name = []
    user_content = []

    r_dic = json.loads(result.text)
    # print(len((r_dic['data'])['hotComments']))
    for j in (r_dic['data'])['hotComments'] :
        user_name.append((j['user'])['nickname'])
        user_content.append(j['content'])
    assert len(user_content) == len(user_name)
    dataframe = pd.DataFrame({"user_name":user_name,"user_content":user_content})
    out_filepath = '歌名_%s_HotComment.csv'%(str(music_id_name[k]))
    dataframe.to_csv(out_filepath,index=False,sep=',')












# for i in (r_dic['data'])['comments'] :
#     print((i['user'])['nickname'],"  ",i['content'])
#     print()
# sortTypeList hotComments
# comments = r_dic['data']
# print(len(comments))
# for comment in comments:
#     print(comment)
# # json1 = json.dumps(json.loads(result.text), indent=4, sort_keys=False, ensure_ascii=False)
# with open('./dct.csv', 'w',encoding='utf-8-sig') as f:  
#     writer = csv.writer(f)
#     for k, v in json.loads(result.text).items():
#         writer.writerow([k, v])
# print(json1)
# print(type(result.text))  #str
# print(type(json.loads(result.text))) #dict
# print(type(json.dumps(json.loads(result.text)))) #str

'''
加密区间
var bMr1x = window.asrsea(JSON.stringify(i0x), bsg8Y(["流泪", "强"]), bsg8Y(TH5M.md), bsg8Y(["爱心", "女孩", "惊恐", "大笑"]));
            e0x.data = j0x.cr0x({
                params: bMr1x.encText,
                encSecKey: bMr1x.encSecKey
            })
        }

加密函数区间
function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,  #偏移量
            mode: CryptoJS.mode.CBC  #加密模式
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {
        var h = {}
          , i = a(16);   #随机值
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),  #返回的是Parma
        h.encSecKey = c(i, e, f),   #返回encSecKey  确定i，encSecKey则固定
        h
    }
window.asrsea = d
# ! 定值 
#e
bsg8Y(["流泪", "强"]

#f
bsg8Y(TH5M.md)
#g
bsg8Y(["爱心", "女孩", "惊恐", "大笑"]) 
i0x 为data
var bMr1x = window.asrsea(JSON.stringify(i0x), bsg8Y(["流泪", "强"]), bsg8Y(TH5M.md), bsg8Y(["爱心", "女孩", "惊恐", "大笑"]));

e0x.data = j0x.cr0x({
                params: bMr1x.encText,
                encSecKey: bMr1x.encSecKey
            })
'''