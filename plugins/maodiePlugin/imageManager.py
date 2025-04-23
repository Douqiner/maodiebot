import os
import json
import random
from ncatbot.core import message

from ncatbot.core import (
    MessageChain,  # 消息链，用于组合多个消息元素
    Text,          # 文本消息
    At,            # @某人
    AtAll,         # @全体成员
    Face,          # QQ表情
    Image,         # 图片
    Json,          # JSON消息
)
from ncatbot.utils import get_log
_log = get_log()

class ImageManager:
    '''图片管理器类'''
    def __init__(self):
        self.image_dir = {}
        self.image_path = os.path.join(os.path.dirname(__file__), "static", "images")
        self.dir_path = os.path.join(os.path.dirname(__file__), "static", "image_dir.json")
        # 读取image_dir
        with open(self.dir_path, "r", encoding="utf-8") as f:
            self.image_dir = json.load(f)
            _log.info(f"读取图片数: {len(self.image_dir)}")

    def get_image_message(self, id: int = None) -> message:
        '''获取图片信息消息'''
        message = MessageChain([])
        if id is None:
            id = random.randint(0, len(self.image_dir) - 1)
        if id < 0 or id >= len(self.image_dir):
            message += Text("参数超出范围了>_<\n")
            message += self.handle_help()
            return message
            
        '''获取图片路径'''
        image_name = self.image_dir[(str)(id)]
        pid = image_name.split('_')[0]
        message += Image(os.path.join(self.image_path, image_name))
        message += Text("pid: " + (str)(pid) + "\n")
        return message