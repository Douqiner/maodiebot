import os
import feedparser
import random
from ncatbot.core import message

from ncatbot.core import (
    MessageChain,  # 消息链，用于组合多个消息元素
    Text,          # 文本消息
    At,            # @某人
    Face,          # QQ表情
    Image,         # 图片
)

class NewsManager:
    '''新闻管理器类'''
    def __init__(self):
        # self.china_url = "https://rsshub.rssforever.com/zaobao/realtime/china"
        # self.world_url = "https://rsshub.rssforever.com/zaobao/realtime/world"
        self.china_url = "https://plink.anyfeeder.com/zaobao/realtime/china"
        self.world_url = "https://plink.anyfeeder.com/zaobao/realtime/world"

    def parse_text(self, arg: list[str]) -> MessageChain:
        if arg[0] not in ["china", "world", "mixed"]:
            return MessageChain([Text("参数错误(；´д｀)ゞ\n可选world/china/mixed\n")])
        if (len(arg) == 1):
            cnt = 6
        elif (len(arg) == 2):
            try:
                cnt = int(arg[1])
            except:
                return MessageChain([Text("参数错误ε(┬┬﹏┬┬)3\n数量应为整数\n")])
            if cnt <= 0:
                return MessageChain([Text("参数错误(；′⌒`)\n数量应为正数\n")])
        
        return self.get_news_message(type=arg[0], cnt=cnt)
    
    def fetch_news(self, url : str, cnt: int) -> list:
        '''获取新闻'''
        feed = feedparser.parse(url)
        entries = feed.entries
        num = min(cnt, len(entries))
        # 随机选择 num 个新闻
        return random.sample(entries, num) if num > 0 else []

    def get_news_message(self, type: str = "mixed", cnt: int = 6) -> MessageChain:
        '''获取新闻信息消息'''
        message = MessageChain([])

        news_list = []
        if type == "china":
            news_list = self.fetch_news(self.china_url, cnt)
        elif type == "world":
            news_list = self.fetch_news(self.world_url, cnt)
        elif type == "mixed":
            china_list = self.fetch_news(self.china_url, cnt//2)
            world_list = self.fetch_news(self.world_url, cnt//2)
            news_list = china_list + world_list
        
        for i in range(len(news_list)):
            message += Text(str(i + 1) + '.' + news_list[i].title + "\n" + news_list[i].link + "\n\n")

        return message