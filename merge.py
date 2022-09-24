# 合并所有的csv文件内的链接

import os
import requests
import json

urldata = {}

def tojs():
	return "var steamModURLS = {\n" + "\n".join([
		"'{}': '{}',".format(mod, url) for mod, url in urldata.items()
		]) + "\n}"

def loadcsv(path):
	for line in open(path):
		yield line.strip().split("\t")

def sort_by_time(path):
	return int(path.split(".")[0])

if __name__ == '__main__':
	add = False
	csvfiles = ["imglinks/" + path for path in sorted(os.listdir("imglinks"), key = sort_by_time, reverse = True)]

	def trim(url):
		if url.startswith("https://steamuserimages-a.akamaihd.net/ugc/"):
			url = "*" + url[43:]
		return url

	for path in csvfiles:
		print("Load:", path)
		for mod, imgurl in loadcsv(path):
			if mod in urldata: continue

			add = True
			urldata[mod] = trim(imgurl)

		if not add:
			print("文件{}无效，可删除".format(path))

	open("url.js", "w").write(tojs())