# 测试爬取 pixiv 图片
# import requests
# import re

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                          "Chrome/97.0.4692.71 Safari/537.36", 'referer': "https://www.pixiv.net/"}

# rec = requests.get(url="https://www.pixiv.net/ajax/illust/135358110/pages", headers=headers)

# rule = re.compile(r'"original":"(?P<LINK>.*?)"', re.S)
# d_url = re.findall(rule, rec.text)
# d_url = [u.replace("\\/", "/") for u in d_url]

# # print(d_url)
# ill_rec = requests.get(d_url[0], headers=headers)
# ill_file = ill_rec.content
# ill_rec.close()
# with open("./test.png", "wb") as image:
#     image.write(ill_file)
#     image.close()


# 测试 RSS 解析
import feedparser
rss_url = "https://www.chinanews.com.cn/rss/world.xml"

# 2. 使用 feedparser 解析该 URL
feed = feedparser.parse(rss_url)

print(feed.entries)