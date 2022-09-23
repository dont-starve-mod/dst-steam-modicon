# 下载图片

import os
import requests
import json

LastURL = json.load(open("imgs/lasturl.json"))

def savelasturl():
	with open("imgs/lasturl.json", "w") as f:
		json.dump(LastURL, f)

def download(mod, url):
	if LastURL.get(mod) == url:
		return

	LastURL[mod] = url
	r = requests.get(url)
	if r.status_code != 200:
		print("警告: 请求失败", mod, url)
		return

	with open("imgs/" + mod, "wb") as f: f.write(r.content)

def loadcsv(path):
	for line in open(path):
		yield line.strip().split("\t")

def sort_by_time(path):
	return int(path.split(".")[0])

if __name__ == '__main__':
	ids = set()
	csvfiles = ["imglinks/" + path for path in sorted(os.listdir("imglinks"), key = sort_by_time)]
	count = 0
	for path in csvfiles:
		for mod, imgurl in loadcsv(path):
			if mod in ids: continue

			ids.add(mod)
			download(mod, imgurl)
			count += 1
			if count % 100 == 0:
				print("***", count, "***")
				savelasturl()
