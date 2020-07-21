import re

poemfile = open('../data/poem.txt',encoding='UTF-8').read()

p1 = r"[\u4e00-\u9fa5]{5,7}[\u3002|\uff0c]"  #[汉字]{重复5-7次}[中文句号|中文逗号]
pattern1 = re.compile(p1)        #编译正则表达式
result = pattern1.findall(poemfile)   #搜索匹配的字符串，得到匹配列表

with open('../data/zzcf.txt','w+',encoding='utf-8') as f: #打开输出文件
    for x in result:
        f.write(x)    #遍历输出
