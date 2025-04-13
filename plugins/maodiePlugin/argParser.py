import os
import json

from ncatbot.core import (
    MessageChain,  # 消息链，用于组合多个消息元素
    Text,          # 文本消息
    At,            # @某人
    AtAll,         # @全体成员
    Face,          # QQ表情
    Image,         # 图片
    Json,          # JSON消息
)

from .imageManager import ImageManager

class ArgParser:
    """命令参数解析器"""
    data = {}
    imageManager = None

    counter = {}
    last_uid = 0
    last_is_group = False

    def __init__(self, data: dict):
        self.data = data
        self.imageManager = ImageManager()
        if 'counter' in self.data:
            self.counter = self.data['counter']
    
    def __del__(self):
        self.data['counter'] = self.counter
    
    def add_count(self, inst: str):
        '''增加计数器'''
        if inst not in self.counter:
            self.counter[inst] = {}
        if self.last_uid not in self.counter[inst]:
            self.counter[inst][self.last_uid] = [0, 0]
        if self.last_is_group:
            self.counter[inst][self.last_uid][1] += 1
        else:
            self.counter[inst][self.last_uid][0] += 1

    def parse_text(self, text: str, uid: int, is_group: bool) -> MessageChain:
        '''解析文本命令'''
        self.last_uid = uid
        self.last_is_group = is_group

        text = text.strip()
        if (text[0] == '/'):
            text = text[1:]
            # 解析参数
            text = text.split()
            if text[0] == 'st':
                return self.handle_st(text[1:])
            
            # 有错
            return self.handle_help()
        
        else:
            return None
        
    def handle_st(self, arg: list[str] = None) -> MessageChain:
        '''处理st命令'''
        message = MessageChain([])
        if arg is None or len(arg) == 0:
            # 随机图片
            message += self.imageManager.get_image_message()
            message += Text("主人的图片喵~\n")
            self.add_count("st")
            
        elif len(arg) == 1:
            # 指定图片id
            # 检查参数是否为数字
            try:
                image_id = int(arg[0])  # 尝试将参数转换为整数
            except ValueError:
                message += Text("参数有错喵\n")
                message += self.handle_help()
                return message
            message += self.imageManager.get_image_message(image_id)
            message += Text("主人的图片喵~\n")
            self.add_count("st")
        else:
            # 错误参数
            message += Text("参数数量不对哦\n")
            message += self.handle_help()
        return message
        
    def handle_help(self, arg: list[str] = None) -> MessageChain:
        '''处理帮助命令'''
        message = MessageChain([
            Text(
            "使用方法：\n" \
            "随机图片 /st <可选:指定图片id>\n" \
            "只有这些功能喵~"
            )
        ])
        return message