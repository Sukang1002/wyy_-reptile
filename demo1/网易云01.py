'''
Author: sk 2309620371@qq.com
Description: 
'''
import json
import requests
import pandas as pd

def Hot_ranking_list(out_filepath):
    url = "https://api.wer.plus/api/wytop?t=4"
    data = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    result = requests.get(url,data=data)
    dataframe = pd.DataFrame(json.loads(result.text))
    dataframe.to_csv(out_filepath,index=False,sep=',')
    return 1

out_filepath = '网易云热歌版.csv'

