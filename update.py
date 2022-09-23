import requests
import os
import time
import re

class URL:
	MOST_RECENT = "https://steamcommunity.com/workshop/browse/?appid=322330&browsesort=mostrecent&section=readytouseitems&actualsort=mostrecent&p="
	LAST_UPDATE = "https://steamcommunity.com/workshop/browse/?appid=322330&browsesort=lastupdated&section=readytouseitems&actualsort=lastupdated&p="
	MOST_SUBSCRIBED = "https://steamcommunity.com/workshop/browse/?appid=322330&browsesort=totaluniquesubscribers&section=readytouseitems&actualsort=totaluniquesubscribers&p="

if __name__ == '__main__':
	print("开始更新..")
	f = open("imglinks/{}.csv".format(int(time.time())), "w")

	for i in range(1, 100):
		print("Page:", i)
		r = requests.get(URL.LAST_UPDATE + str(i))
		if r.status_code != 200:
			print("警告: 请求失败")
			continue

		linenumber = -100
		for i, line in enumerate(r.text.split("\n")):
			m = re.search(r"<div id=\"sharedfile_(\d+)\"[^>]*>", line)
			if m != None:
				linenumber = i
				mod = m.group(1)

			if i == linenumber + 1:
				m = re.search(r"src=\"([^?\"]+)", line)
				if m == None:
					print("警告: 模组图片无法获取", mod)
				else:
					imgurl = m.group(1)
					f.write(mod + "\t" + imgurl + "\n")
					f.flush()
					mod = None

		
		time.sleep(5)