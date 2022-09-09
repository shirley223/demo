# Start writing code here...
import requests
import re
import pandas as pd
import jieba
import wordcloud
from bs4 import BeautifulSoup
import time
import json
from stylecloud import gen_stylecloud
import matplotlib.pyplot as plt
import os
from PIL import Image
import numpy as np
import imageio


url =" https://www.missevan.com/sound/6149849" #输入单集网页地址
request1 = requests.get(url)
result1 = request1.text
#print(result1)
pattern1 = re.compile(r'<div class="text-playtimes">(.+?)</div>')
pattern2 = re.compile(r'<div class="cover-title">(.+?)</div>')
title = re.findall(pattern2,result1)
playtime = re.findall(pattern1,result1)
getdm_url = 'https://www.missevan.com/sound/getdm?soundid='
sound_url = getdm_url+url.split("/")[4]
request = requests.get(sound_url) 
result = request.text
#print(result)
pattern = re.compile(r'p="(.+?)"')
pattern1 = re.compile(r'<d(.+?)</d>')
dm1 = re.findall(pattern, result)
dmw1  = re.findall(pattern1,result)
dm2 = pd.DataFrame(dm1,columns=['data'])['data'].str.split('>',expand=True)[0]
dmw2 = pd.DataFrame(dmw1,columns=['data'])['data'].str.split('>',expand=True)[1] 

uid = dm2.str.split(',',expand=True)[6]
print(title,"实时ID为:",len(uid.unique()))
print(title,"实时弹幕数量为:",len(uid))
print(title,"实时播放量为：",playtime)


with open('弹幕.txt',mode='a',encoding='utf-8')as f:
    for j in range(0,len(uid)):
        f.write(str(dmw2[j]))
        f.write('\n')


py=imageio.imread('python.png')
f=open('弹幕.txt',encoding='utf-8')
txt=f.read()
txt_list=jieba.lcut(txt)
string=''.join(txt_list)
print(string)
wc=wordcloud.WordCloud(width=500,height=500,background_color='white',
                       font_path='msyh.ttc',mask=py,stopwords={'了','这个','我','啊','的'},collocations=False)
wc.generate(string)
wc.to_file('output2.png')
