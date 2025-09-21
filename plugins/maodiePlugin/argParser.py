from ncatbot.core import (
    MessageChain,  # 消息链，用于组合多个消息元素
    Text,          # 文本消息
    At,            # @某人
    Face,          # QQ表情
    Image,         # 图片
)

from .imageManager import ImageManager
from .game1Manager import Game1Manager
from .pcrMtManager import PcrMtManager

class ArgParser:
    """命令参数解析器"""
    def __init__(self):
        self.imageManager = ImageManager()
        self.game1Manager = Game1Manager()
        self.pcrMtManager = PcrMtManager()
    
    def on_close(self):
        self.pcrMtManager.on_close()

    def parse_text(self, text: str, uid: int, uname: str, is_group: bool, gid: int) -> MessageChain:
        '''解析文本命令'''
        self.last_uid = uid
        self.last_uname = uname
        self.last_is_group = is_group
        self.last_gid = gid

        text = text.strip()

        # 解析参数
        text = text.split()
        if text[0] == 'st':
            return self.handle_st(text[1:])
        elif text[0] == 'gm1':
            return self.handle_gm1(text[1:])
        elif text[0] == 'mt':
            return self.handle_mt(text[1:])
        
        # 有错
        return self.handle_help()
        
    def handle_st(self, arg: list[str] = None) -> MessageChain:
        '''处理st命令'''
        message = MessageChain([])
        if arg is None or len(arg) == 0:
            # 随机图片
            message += self.imageManager.get_image_message()
            message += Text("主人的图片喵~\n")
            
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
        else:
            # 错误参数
            message += Text("参数数量不对哦\n")
            message += self.handle_help()
        return message
        
    def handle_gm1(self, arg: list[str] = None) -> MessageChain:
        '''处理gm1命令'''
        message = MessageChain([])
        if arg is None or len(arg) == 0:
            # 帮助信息
            message += Text(
                "小游戏1规则: \n" \
                "路上从左到右有n个格子,有的格子上有石子\n" \
                "高松灯想和你比捡石子\n" \
                "每个人每轮可以站在最左边的石子处\n" \
                "捡走右侧k范围内的任意石子\n" \
                "谁捡完最后一个石子谁就赢了\n\n" \
                
                "指令: \n" \
                "gm1 beg <大于6小于30的整数n> <大于2小于n/3的整数k> <先后手:1,0> \n" \
                "gm1 sl <选择拿走哪些石子> \n" \
                "比如: gm1 sl 1 2 3 \n 表示拿走当前位置第1、2、3个石子\n" \
                "gm1 show \n显示当前局面 \n" \
                "gm1 end \n" \
                "结束游戏" \

            )
            
        elif len(arg) >= 1:
            message += self.game1Manager.parse_game_text(arg, self.last_uid, self.last_is_group, self.last_gid)

        return message
    
    def handle_mt(self, arg: list[str] = None) -> MessageChain:
        '''处理mt命令'''
        message = MessageChain([])
        if arg is None or len(arg) == 0:
            # 帮助信息
            message += Text(
                "pcr答题指令: \n" \
                "mt beg <1-5>\n" \
                "指定待填空数 开始游戏\n\n" \
                "mt ans <1-5> <答案>\n" \
                "指定位置进行填空\n\n" \
                "mt set <角色名字>\n" \
                "修改自己的角色"
            )
            
        elif len(arg) >= 1:
            message += self.pcrMtManager.parse_game_text(arg, self.last_uid, self.last_uname, self.last_is_group, self.last_gid)

        return message

    def handle_help(self, arg: list[str] = None) -> MessageChain:
        '''处理帮助命令'''
        message = MessageChain([
            Text(
            "使用方法：\n" \
            "随机图片 st <可选:指定图片id>\n" \
            "小游戏1 gm1 \n" \
            "兰德索尔谜题连结 mt \n" \
            "只有这些功能喵~"
            )
        ])
        return message