import jieba

content = open('../data/freqword_v.txt', encoding='utf-8').read()
result = jieba.cut_for_search(content)
print("/ ".join(result))  # 全模式
