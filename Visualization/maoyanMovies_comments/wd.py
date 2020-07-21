#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：Ryan time:2018/11/20

import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from scipy.misc import imread


comments = []
with open('E:/spiderproject/maoyanMovies_comments/', 'r', encoding='utf-8')as f:
    rows = f.readlines()
    try:
        for row in rows:
            comment = row.split(',')[2]
            if comment != '':
               comments.append(comment)
            # print(city)
    except Exception as e:
        print(e)
comment_after_split = jieba.cut(str(comments), cut_all=False)
words = ' '.join(comment_after_split)
#多虑没用的停止词
stopwords = STOPWORDS.copy()
stopwords.add('电影')
stopwords.add('一部')
stopwords.add('一个')
stopwords.add('没有')
stopwords.add('什么')
stopwords.add('有点')
stopwords.add('感觉')
stopwords.add('毒液')
stopwords.add('就是')
stopwords.add('觉得')


bg_image = plt.imread('venmo1.jpg')
wc = WordCloud(width=1024, height=768, background_color='white', mask=bg_image, font_path='STKAITI.TTF',
               stopwords=stopwords, max_font_size=400, random_state=50)
wc.generate_from_text(words)
plt.imshow(wc)
plt.axis('off')
plt.show()

wc.to_file('词云图.jpg')