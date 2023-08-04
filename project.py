#import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from collections import Counter
import statsmodels.api as sm
import matplotlib.font_manager as fm
from wordcloud import WordCloud
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import warnings; warnings.filterwarnings('ignore')
import tensorflow as tf
import matplotlib.ticker as ticker
from sklearn.model_selection import train_test_split
import unicodedata
import re
import os
import io
import time
plt.rc('font', family='NanumGothic')
import requests
from bs4 import BeautifulSoup

#크롤링
webpage = requests.get("https://pyony.com/search/")
soup = BeautifulSoup(webpage.content, "html.parser")
#페이지
page = soup.findAll("a", {"class":"page-link"})
last_page = page[len(page)-1].get('href')
_last_page = last_page.replace("?page=","")

#category, 제품명 크롤링
obj_result = []
category_result = []
for x in range(1, int(_last_page)):
    webpage = requests.get("https://pyony.com/search/?page="+str(x))
    soup = BeautifulSoup(webpage.content, "html.parser") 

                
    for j in range(0,20):
        cat = soup.findAll("div",{"class":"card-header"})[j].get_text().replace(" ", "").replace("\n", "|").split("|")
        _cat = []
        i= 0
        for cat_val in cat:
            if(cat_val):
                if(i < 4):
                    _cat.append(cat_val)
                    i = i+1
        category_result.append(_cat)
        obj = soup.findAll("div",{"class":"card-body"})[j].get_text().replace(" ", "").replace("\n", "|").split("|")
        _obj = []
        i = 0
        for val in obj:
            if(val):
                if(i < 4):
                    _obj.append(val)
                    i = i+1
        obj_result.append(_obj)
                    
#항목 분리 (브랜드명, 카테고리명, 제품명, 가격, 할인가격, 행사분류) 
stores = []
for i in category_result:
        i = i[:-2]
        stores.append(i)

categories = []
for i in category_result:
        i = i[1:-1]
        categories.append(i)


obj = []
for i in obj_result:
        i= i[0:1]
        obj.append(i)


price = []
for i in obj_result:
        i= i[1:2]
        price.append(i)

discount = []
for i in obj_result:
        i= i[2:3]
        discount.append(i)

event = []
for i in obj_result:
        i= i[3:4]
        event.append(i)

convenience_sales = pd.DataFrame(zip(stores, categories, obj, price, discount, event),
                                  columns=['stores', 'categories', 'obj', 'price', 'discount', 'event'])

#데이터 전처리
convenience_sales = convenience_sales.explode('stores')
convenience_sales = convenience_sales.explode('categories')
convenience_sales = convenience_sales.explode('obj')
convenience_sales = convenience_sales.explode('price')
convenience_sales = convenience_sales.explode('discount')
convenience_sales = convenience_sales.explode('event')
convenience_sales.discount =convenience_sales.discount.str.replace(',', '')
convenience_sales.price =convenience_sales.price.str.replace(',', '')
convenience_sales.discount =convenience_sales.discount.str.replace(')', '')
convenience_sales.discount =convenience_sales.discount.str.replace('(', '')
convenience_sales.price =convenience_sales.price.str.replace('원', '')
convenience_sales.discount =convenience_sales.discount.str.replace('원', '')
convenience_sales.price = convenience_sales.price.astype('int64')
convenience_sales.discount = convenience_sales.price.astype('int64')

#물품 하나당 가격에 대한 칼럼 추가 
convenience_sales.loc[convenience_sales['event'] == "2+1", 'each_price'] = convenience_sales["price"] * 2/3
convenience_sales.loc[convenience_sales['event'] == "1+1", 'each_price'] = convenience_sales["price"] * 1/2
len(convenience_sales['each_price'].isna())

#csv로 저장 후 파일 가져오기
convenience_sales.to_csv('./convenience_sales.csv', header=True, index=False)
convenience_sales = pd.read_csv('./convenience_sales.csv', encoding='cp949')

# 물품을 입력하면 가격 찾아주기 

product = input("사고싶은 물품을 입력하세요")
convenience_sales[convenience_sales['obj'].str.contains(product)].sort_values(by='each_price')