import json
import re
import requests


def getHTMLText(url):
	try:
		headers = {
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
						  "Chrome/80.0.3987.163 Safari/537.36"}
		r = requests.get(url, timeout=30, headers=headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		data = re.search("\(+([^)]*)\)+", r.text).group(1)
		return data
	except:
		return ""


def getYqDate(lst, YqURL):
	html = getHTMLText(YqURL)
	hjson = json.loads(html)
	a = hjson['data']['list']
	for i in a:
		try:
			name = i['name']		# 省份
			value = i['value']		# 累计确诊
			econNum = i['econNum']		# 现存确诊
			conadd = i['conadd']		# 今日确诊
			deathNum = i['deathNum']		# 累计死亡人数
			cureNum = i['cureNum']	# 累计治愈
			zerodays = i['zerodays']		# 零增长天数
			jwsrNum = i['jwsrNum']	# 境外输入总数
			single_data = [name, value, econNum, conadd, deathNum, cureNum, zerodays, jwsrNum]
			lst.append(single_data)
		except:
			continue


def writeResult(lst, fpath):
	with open(fpath, 'a+', encoding='utf-8') as f:
		f.write('省份\t累计确诊\t现存确诊\t今日确诊\t累计死亡人数\t累计治愈\t零增长天数\t境外输入总数\n')
		for i in range(len(lst)):
			for j in range(len(lst[i])):
				f.write(str(lst[i][j]))
				f.write('\t')
			f.write('\n')
		lst.clear()
	f.close()


if __name__ == '__main__':
	pagenum = 1
	output_file = 'D:/Personal/Desktop/yq.xls'
	final_data = []
	url = "https://gwpre.sina.cn/interface/fymap2020_data.json?_=1588258367647&callback=dataAPIData"
	getYqDate(final_data, url)
	writeResult(final_data, output_file)