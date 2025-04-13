from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core import GroupMessage, PrivateMessage, message

from ncatbot.utils import config
from ncatbot.utils import get_log

from ncatbot.core import (
    MessageChain,  # 消息链，用于组合多个消息元素
    Text,          # 文本消息
    At,            # @某人
    AtAll,         # @全体成员
    Face,          # QQ表情
    Image,         # 图片
    Json,          # JSON消息
)

from .argParser import ArgParser

bot = CompatibleEnrollment  # 兼容回调函数注册器
_log = get_log()

class MaodiePlugin(BasePlugin):
    name = "MaodiePlugin" # 插件名
    version = "0.0.1" # 插件版本

    argParser = None # 参数解析器

    async def on_load(self):
        '''插件加载时执行的操作'''
        _log.info(f"{self.name} 插件已加载")
        _log.info(f"插件版本: {self.version}")
        
        # 载入参数解析器
        self.argParser = ArgParser(self.data)

        # 每日任务
        self.add_scheduled_task(
            job_func=self.recommend, 
            name="每日推荐", 
            interval="08:00",
        )
    
    async def on_close(self):
        '''插件卸载时执行的操作'''
        self.argParser.on_close()

        _log.info(f"{self.name} 插件已卸载")

    async def recommend(self):
        '''每日推荐任务'''
        _log.info("每日推荐任务")
        # 发送消息到指定群组
        group_list = [527017070, 926456624]
        for g_id in group_list:
            message = MessageChain([
                Text("主人们好呀~\n"),
                Text("今天的推荐来了哦~\n"),
                Text("(〃'▽'〃)\n"),
            ])
            message += self.argParser.imageManager.get_image_message()
            await self.api.post_group_msg(group_id=g_id, rtf=message)

    def get_text_and_at(self, msg: message):
        '''查找类型消息'''
        text_data = None
        at_data = None
        for i in msg.message:
            if i['type'] == 'text':
                text_data = i['data']
            elif i['type'] == 'at':
                at_data = i['data']
        
        return (text_data, at_data)
        
    @bot.group_event()
    async def on_group_message(self, msg: GroupMessage):
        '''群组消息处理'''
        # 查找类型消息
        text_data ,at_data = self.get_text_and_at(msg)
        if text_data is None or at_data is None or at_data['qq'] != config.bt_uin:
            return

        # 处理消息
        message = self.argParser.parse_text(text_data['text'], msg.user_id, True, msg.group_id)
        if message is not None:
            _log.info(msg)
            message += At(msg.user_id)
            await self.api.post_group_msg(group_id=msg.group_id, rtf=message)


    @bot.private_event()
    async def on_private_message(self, msg: PrivateMessage):
        '''私聊消息处理'''
        # 查找类型消息
        text_data , _ = self.get_text_and_at(msg)
        if text_data is None:
            return

        # 处理消息
        message = self.argParser.parse_text(text_data['text'], msg.user_id, False, 0)
        if message is not None:
            _log.info(msg)
            await self.api.post_private_msg(user_id=msg.user_id, rtf=message)
        
