import random
import pinyin

#生成藏头诗
def Line5_Head(str):
    noun = open('../data/freqword_n.txt', encoding='utf-8').readlines()
    verb = open('../data/freqword_v.txt', encoding='utf-8').readlines()

    nounlist = []
    for word in noun:
        # outfile.write(pinyin.get(word, format="strip")+" ")
        i = 0
        while i<len(word):
            if word[i:i+2]!="\n":
                nounlist.append(word[i:i+2])
            i=i+3

    verblist = []
    for word in verb:
        i = 0
        while i<len(word):
            if word[i:i+2]!="\n":
                verblist.append(word[i:i+2])
            i=i+3

    # sentence = ""
    count = 0
    num = 0

    rhythm = ""
    rhythmList = ["a", "e", "i", "o", "u"]
    while num < 4:
        for x in range(len(nounlist)):
            if nounlist[x][0] == str[num]:
                i = x

        i1 = random.randint(1, len(nounlist)-1)
        j = random.randint(1, len(verblist)-1)

        ind = 0
        ind1 = 0
        if (num == 1):
            rhythm = ""
            verse = pinyin.get(nounlist[i1][1], format="strip")
            for p in range(len(verse)-1, -1, -1):
                if verse[p] in rhythmList:
                    ind = p

            rhythm = verse[ind:len(verse)]

        if (num == 3):
            ind1 = 0
            verse1 = pinyin.get(nounlist[i1][1], format="strip")
            for p in range(len(verse1)-1, -1, -1):
                    if verse1[p] in rhythmList:
                        ind1 = p

            while verse1[ind1: len(verse1)] != rhythm:
                i1 = random.randint(1, len(nounlist)-1)
                verse1 = pinyin.get(nounlist[i1][1], format="strip")
                for p in range(len(verse1)-1, -1, -1):
                    if verse1[p] in rhythmList:
                        ind1 = p

        print(nounlist[i]+verblist[j][1]+nounlist[i1])
        num += 1


if __name__ == '__main__':
    head = input()
    Line5_Head(head)


