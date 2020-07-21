import time
import jieba
import jieba.analyse

jieba.enable_parallel(8)

poetry_file ='../data/zzcf.txt'

n_file = '../data/freqword_n.txt'
v_file = '../data/freqword_v.txt'
a_file = '../data/freqword_a.txt'
ag_file = '../data/freqword_ag.txt'

content = open(poetry_file, encoding='utf-8').read()

result_n = open(n_file,'w+',encoding='utf-8')
result_v = open(v_file,'w+',encoding='utf-8')
result_a = open(a_file,'w+',encoding='utf-8')
result_ag = open(ag_file,'w+',encoding='utf-8')
t1 = time.time()

count = 0
for x in jieba.analyse.textrank(content, topK=600, allowPOS=('n', 'nr', 'ns', 'nt', 'nz', 'm')):
    result_n.writelines(x+" ")
    count+=1
    if count%10==0:
        result_n.write("\n")

count = 0
for x in jieba.analyse.textrank(content,topK=400, allowPOS=('Vg')):
    result_v.writelines(x+" ")
    count+=1
    if count%10==0:
        result_v.write("\n")

count = 0
for x in jieba.analyse.textrank(content,topK=400, allowPOS=('a', 'ad', 'an')):
    result_a.writelines(x+" ")
    count+=1
    if count%10==0:
        result_a.write("\n")
        
count = 0
for x in jieba.analyse.textrank(content,topK=400, allowPOS=('ag')):
    result_ag.writelines(x+" ")
    count+=1
    if count%10==0:
        result_ag.write("\n")

t2 = time.time()
tm_cost = t2-t1

print("time cost: " + str(tm_cost) + "秒")
