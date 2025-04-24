import os
from PIL import Image as PILImage, ImageDraw, ImageFont

class Question:
    def __init__(self, qust: str, detail: str, answ: str, param1: int, param2: int, param3: int):
        self.qust = qust
        self.detail = detail
        self.answ = answ
        self.param1 = param1 # 问题类型 1 2 3 4 5 6
        self.param2 = param2 # 是否和公主连结相关 1 2
        self.param3 = param3 # 问题难度 1 2 3

class Guesser:
    def __init__(self, name: str, no2d: int, empType: str, ansNow: str, ansReal: str):
        self.name = name # 空表示是人机
        self.no2d = no2d
        self.empType = empType
        self.ansNow = ansNow
        self.ansReal = ansReal

class DrawState:
    def __init__(self, guesserList: list[Guesser], ansPart: str):
        self.guesserList = guesserList
        self.ansPart = ansPart

class DrawTool:
    def __init__(self, s2d: list[str]):
        self.pcrPath = os.path.join(os.path.dirname(__file__), 'static', 'pcr')
        self.s2d_path = os.path.join(self.pcrPath, 's2d')
        self.imgPartPath = os.path.join(self.pcrPath, 'imgPart')
        self.fontPath = os.path.join(self.pcrPath, 'txqyj-w3.ttf')
        self.tmpPath = os.path.join(self.pcrPath, 'tmp')
        # 读取s2d索引
        self.s2d = s2d

        self.problemFile = ["", "problemFight.png","problemStory.png", "problemCulture.png", "problemMath.png", "problemLife.png", "problemBiology.png"]

    def drawBlock(self, type: str, text: str) -> PILImage:
        '''绘制填写框'''
        if type == "Chs":
            # 绘制中文填写框
            image_path = os.path.join(self.imgPartPath, 'blockChs.png')
        elif type == "Dig":
            # 绘制数字填写框
            image_path = os.path.join(self.imgPartPath, 'blockDig.png')
        elif type == "Eng":
            # 绘制英文填写框
            image_path = os.path.join(self.imgPartPath, 'blockEng.png')

        image = PILImage.open(image_path)
        if text == "":
            return image

        # 创建一个绘图对象
        draw = ImageDraw.Draw(image)

        # 设置字体和大小
        font = ImageFont.truetype(self.fontPath, 85)  # 加载字体
        # 计算文本的边界框
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        # text_height = text_bbox[3] - text_bbox[1]

        # 计算文本的居中位置
        image_width, image_height = image.size
        text_x = (image_width - text_width) // 2
        # text_y = (image_height - text_height) // 2

        # 设置文本内容、位置和颜色
        text_color = (0, 0, 0)  # 黑色
        draw.text((text_x, 40), text, font=font, fill=text_color)

        # 保存图像
        # image.save(os.path.join(self.tmpPath, "tmp1.png"))
        return image
    
    def drawAllBlock(self, drawState: DrawState, is_end: bool) -> PILImage:
        '''绘制所有填写框并返回图片'''
        padding = 3
        guesserList, ansPart = drawState.guesserList, drawState.ansPart
        allBlockHeight = 154
        # 统计长度
        ansPartText = ""
        for i in range(len(ansPart)):
            if ansPart[i] != "#":
                ansPartText += ansPart[i]

        # 创建一个虚拟图像（可以是任意大小，因为我们不需要实际绘制文本）
        fakeImage = PILImage.new('RGBA', (1, 1))
        # 创建一个 ImageDraw 对象
        draw = ImageDraw.Draw(fakeImage)
        
        # 设置字体和大小
        font = ImageFont.truetype(self.fontPath, 55)  # 加载字体
        # 计算总长度
        text_bbox = draw.textbbox((0, 0), ansPartText, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        allBlockLength = text_width + 5 * 120 + (len(ansPart) - 1) * padding

        
        # 创建一个新的图像，带有透明背景
        image_mode = 'RGBA'
        image_size = (allBlockLength, allBlockHeight)
        background_color = (0, 0, 0, 0)
        image = PILImage.new(image_mode, image_size, background_color)

        # 创建一个绘图对象
        draw = ImageDraw.Draw(image)
        
        # 放置所有元素
        index_guesser = 0
        now_x = 0
        for i in range(len(ansPart)):
            if ansPart[i] == "#":
                # 绘制填写框
                if is_end:
                    blockImage = self.drawBlock(guesserList[index_guesser].empType, guesserList[index_guesser].ansReal)
                else:
                    blockImage = self.drawBlock(guesserList[index_guesser].empType, "")
                image.paste(blockImage, (now_x, 0), blockImage)

                now_x += 120 + padding
                index_guesser += 1
            else:
                # 绘制文字
                now_char = ansPart[i]
                # 计算文本的边界框
                text_bbox = draw.textbbox((0, 0), now_char, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                # text_height = text_bbox[3] - text_bbox[1]

                # 计算文本的居中位置
                # text_y = (allBlockHeight - text_height) // 2
                self.drawTextWithWhite(draw, now_char, font, now_x, 60)

                now_x += text_width + padding
        
        # 保存图像
        # image.save(os.path.join(self.tmpPath, "tmp1.png"))

        return image
    
    def drawTextWithWhite(self, draw: ImageDraw, text: str, font: ImageFont, x: int, y: int) -> None:
        '''绘制文字并添加白色阴影'''
        black_color = (0, 0, 0)  # 黑色
        white_color = (255, 255, 255)  # 白色
        w_size = 3
        draw.text((x+w_size, y+w_size), text, font=font, fill=white_color)
        draw.text((x+w_size, y-w_size), text, font=font, fill=white_color)
        draw.text((x-w_size, y+w_size), text, font=font, fill=white_color)
        draw.text((x-w_size, y-w_size), text, font=font, fill=white_color)
        draw.text((x, y), text, font=font, fill=black_color)

    def drawQueBoard(self, drawState: DrawState, question: Question, is_end: bool) -> PILImage:
        # 绘制所有填写框
        allBlockImg = self.drawAllBlock(drawState, is_end)
        # 根据题目类型读取不同背景
        image = PILImage.open(os.path.join(self.imgPartPath, self.problemFile[question.param1]))

        # 如果和公主连结相关
        if question.param2 == 1:
            # 绘制公主连结相关背景
            imagePCRtag = PILImage.open(os.path.join(self.imgPartPath, 'tagPCR.png'))
            image.paste(imagePCRtag, (30, 26), imagePCRtag)
        
        # 创建一个绘图对象
        draw = ImageDraw.Draw(image)

        # 填写题目描述
        # 设置字体和大小
        font = ImageFont.truetype(self.fontPath, 60)  # 加载字体
        text_color = (255, 255, 255)  # 白色
        draw.text((180, 67), question.qust, font=font, fill=text_color)

        # 绘制题目详细描述
        # 设置字体和大小
        font = ImageFont.truetype(self.fontPath, 55)  # 加载字体
        self.drawWrappedWithWhite(draw, question.detail, (40, 200), font, 1130)

        # 放置填写框
        # 计算水平坐标
        allBlockWidth, allBlockHeight = allBlockImg.size
        allBlockX = (image.size[0] - allBlockWidth) // 2
        image.paste(allBlockImg, (allBlockX, 630 - allBlockHeight), allBlockImg)

        # 保存图像
        # image.save(os.path.join(self.tmpPath, "tmp1.png"))
        return image
    
    def drawWrappedWithWhite(self, draw: ImageDraw, text: str, position: tuple[int, int], font: ImageFont, max_width: int) -> None:
        """
        在指定区域内自动换行绘制文本。
        """
        w_size = 3
        lines = []
        current_line = text[0]

        text_height = 0

        for word in text[1:]:
            test_line = current_line + word

            # 计算文本的边界框
            text_bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = max(text_bbox[3] - text_bbox[1], text_height)
            if text_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

        y_offset = position[1]
        for line in lines:
            draw.text((position[0]+w_size, y_offset+w_size), line, font=font, fill=(255, 255, 255))
            draw.text((position[0]+w_size, y_offset-w_size), line, font=font, fill=(255, 255, 255))
            draw.text((position[0]-w_size, y_offset+w_size), line, font=font, fill=(255, 255, 255))
            draw.text((position[0]-w_size, y_offset-w_size), line, font=font, fill=(255, 255, 255))
            draw.text((position[0], y_offset), line, font=font, fill=(0, 0, 0))
            y_offset += text_height + 3

    def drawChair(self, type: str, text: str, name: str) -> PILImage:
        '''绘制桌子'''
        if type == "Right":
            # 绘制正确桌子
            image_path = os.path.join(self.imgPartPath, 'chairRight.png')
        elif type == "Wrong":
            # 绘制错误桌子
            image_path = os.path.join(self.imgPartPath, 'chairWrong.png')
        elif type == "Unknow":
            # 绘制未知桌子
            image_path = os.path.join(self.imgPartPath, 'chairUnknow.png')

        image = PILImage.open(image_path)

        # 创建一个绘图对象
        draw = ImageDraw.Draw(image)

        # 设置字体和大小
        font = ImageFont.truetype(self.fontPath, 34)  # 加载字体
        # 计算文本的边界框
        text_bbox = draw.textbbox((0, 0), name, font=font)
        text_width = text_bbox[2] - text_bbox[0]

        # 计算文本的居中位置
        image_width, image_height = image.size
        text_x = (image_width - text_width) // 2

        # 设置文本内容、位置和颜色
        text_color = (255, 255, 255)  # 白色
        draw.text((text_x + 15, 213), name, font=font, fill=text_color)

        if type == "Unknow":
            return image

        # 设置字体和大小
        font = ImageFont.truetype(self.fontPath, 120)  # 加载字体
        # 计算文本的边界框
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        # text_height = text_bbox[3] - text_bbox[1]

        # 计算文本的居中位置
        image_width, image_height = image.size
        text_x = (image_width - text_width) // 2
        # text_y = (image_height - text_height) // 2

        # 设置文本内容、位置和颜色
        text_color = (255, 255, 255)  # 白色
        draw.text((text_x + 15, 50), text, font=font, fill=text_color)

        # 保存图像
        # image.save(os.path.join(self.tmpPath, "tmp1.png"))
        return image
    
    def drawAllChairAndPlayer(self, guesserList: list[Guesser], is_end: bool) -> PILImage:
        '''绘制所有桌子和人'''
        # 创建一个新的图像，带有透明背景
        image_mode = 'RGBA'
        image_size = (2200, 800)
        background_color = (0, 0, 0, 0)
        image = PILImage.new(image_mode, image_size, background_color)

        # 创建一个绘图对象
        draw = ImageDraw.Draw(image)

        # # 为人机随机分配2d编号和名字,截断太长名字
        # for i in range(len(guesserList)):
        #     if guesserList[i].name == "":
        #         # 随机分配2d编号和名字
        #         guesserList[i].no2d = random.randint(0, len(self.s2d) - 1)
        #         guesserList[i].name = self.s2d[guesserList[i].no2d].replace(".png", "")
        #     elif len(guesserList[i].name) > 8:
        #         guesserList[i].name = guesserList[i].name[:8]

        # 绘制五个桌子
        xPosList = [30, 0, 0, 0, 0]
        for i in range(1, 5):
            xPosList[i] = xPosList[i - 1] + 384 - 45

        # 绘制人
        for i in range(4, -1, -1):
            if guesserList[i].name == "":
                continue
            # 读取2d图片
            playerImg = PILImage.open(os.path.join(self.s2d_path, self.s2d[guesserList[i].no2d]))

            scale = 1.3
            playerImg = playerImg.resize((int(playerImg.size[0] / scale), int(playerImg.size[1] / scale)), PILImage.Resampling.LANCZOS)

            cenX2d = int(623 // scale)
            cenY2d = int(780 // scale)
            image.paste(playerImg, (int(xPosList[i] + 384 / 2 - cenX2d - 15), 800 - 286 - cenY2d), playerImg)

        # 绘制桌子
        for i in range(4, -1, -1):
            if is_end:
                if guesserList[i].ansNow == guesserList[i].ansReal:
                    chairImg = self.drawChair("Right", guesserList[i].ansNow, guesserList[i].name)
                else:
                    chairImg = self.drawChair("Wrong", guesserList[i].ansNow, guesserList[i].name)
            else:
                if guesserList[i].ansNow != "":
                    chairImg = self.drawChair("Right", guesserList[i].ansNow, guesserList[i].name)
                else:
                    chairImg = self.drawChair("Unknow", "", guesserList[i].name)
            image.paste(chairImg, (xPosList[i], 800 - 286), chairImg)
        
        # 保存图像
        # image.save(os.path.join(self.tmpPath, "tmp1.png"))
        return image
    
    def drawPng(self, drawState: DrawState, question: Question, is_end: bool) -> str:
        '''绘制图片并返回图片路径'''
        guesserList, ansPart = drawState.guesserList, drawState.ansPart
        # 绘制答题板
        queBoardImg = self.drawQueBoard(drawState, question, is_end)
        # 绘制答题桌和人
        chairImg = self.drawAllChairAndPlayer(guesserList, is_end)

        # 读取背景
        image = PILImage.open(os.path.join(self.imgPartPath, 'background.png'))

        # 答题板放置位置
        image.paste(queBoardImg, (30, 30), queBoardImg)

        # 答题桌和人放置位置
        image.paste(chairImg, (0, 1350 - 800), chairImg)

        if is_end:
            # 检查答案是否全对
            allCorrect = True
            for i in range(len(guesserList)):
                if guesserList[i].ansNow != guesserList[i].ansReal:
                    allCorrect = False
                    break
            
            if allCorrect:
                imageTag = PILImage.open(os.path.join(self.imgPartPath, 'ansRight.png'))
            else:
                imageTag = PILImage.open(os.path.join(self.imgPartPath, 'ansWrong.png'))
            # 计算位置
            tagCenX = 1760
            tagCenY = 400
            image.paste(imageTag, (tagCenX - imageTag.size[0] // 2, tagCenY - imageTag.size[1] // 2), imageTag)

        # 保存图像
        image.save(os.path.join(self.tmpPath, "tmp1.png"))
        return os.path.join(self.tmpPath, "tmp1.png")


import random
import json
from ncatbot.core import (
    MessageChain,  # 消息链，用于组合多个消息元素
    Text,          # 文本消息
    Image,         # 图片消息
)

class PcrMtManager:
    '''管理谜题的类'''
    def __init__(self):
        # 读取s2d索引
        self.pcrPath = os.path.join(os.path.dirname(__file__), 'static', 'pcr')
        with open(os.path.join(self.pcrPath, 's2d.json'), 'r', encoding='utf-8') as f:
            self.s2d = json.load(f)
        self.drawTool = DrawTool(self.s2d)
        # 反向字典
        self.s2d_dir = {self.s2d[i].replace(".png", "") : i for i in range(len(self.s2d))}
        # 读取所有谜题
        with open(os.path.join(self.pcrPath, 'mt.json'), 'r', encoding='utf-8') as f:
            mtList = json.load(f)
        # 转化为Question列表
        self.questionList = []
        for i in range(len(mtList)):
            self.questionList.append(Question(mtList[i][0], mtList[i][1], mtList[i][2], mtList[i][3], mtList[i][4], mtList[i][5]))
        
        # 谜题状态存储
        self.groupState = {}
        self.userState = {}

        # 持久化数据:每个uid的no2d
        self.userNo2d = {}
        if os.path.exists(os.path.join(self.pcrPath, 'userNo2d.json')):
            with open(os.path.join(self.pcrPath, 'userNo2d.json'), 'r', encoding='utf-8') as f:
                self.userNo2d = json.load(f)
        self.userNo2d = {int(k): v for k, v in self.userNo2d.items()}
        
        # 方便传参
        self.last_uid = ""
        self.last_uname = ""
        self.last_is_group = False
        self.last_gid = ""
    
    def begin_game(self, empty_num: int) -> MessageChain:
        '''开始游戏'''
        # 随机选择题目
        ques_no = random.randint(0, len(self.questionList) - 1)
        question = self.questionList[ques_no]
        # 给题目答案随机挖五个空
        ansOrigin = question.answ
        # 只在等号之后为汉字、英文，数字的题目挖空
        # 统计合法位置
        goodPos = []
        typePos = []
        begIndex = 0
        if "=" in ansOrigin:
            begIndex = ansOrigin.index("=") + 1
        for i in range(begIndex, len(ansOrigin)):
            if ansOrigin[i].isdigit():
                goodPos.append(i)
                typePos.append("Dig")
            elif ansOrigin[i].isalpha() and ansOrigin[i].isascii():
                goodPos.append(i)
                typePos.append("Eng")
            elif '\u4e00' <= ansOrigin[i] <= '\u9fff':
                goodPos.append(i)
                typePos.append("Chs")
        # 从合法位置中选5个
        if len(goodPos) < 5:
            return MessageChain([Text("题目答案长度不足:~\n" + question.answ)])
        allposIndex = [i for i in range(len(goodPos))]
        pos5Index = sorted(random.sample(allposIndex, 5))

        # 随机选择人机位置
        guesserList = [0] * 5
        random5pos = [0, 1, 2, 3, 4]
        random.shuffle(random5pos)
        for i in range(5 - empty_num):
            pos = random5pos[i]
            # 随机选择2d编号
            no2d = random.randint(0, len(self.s2d) - 1)
            # 选择名字
            name = self.s2d[no2d].replace(".png", "")
            realAns = ansOrigin[goodPos[pos5Index[pos]]]
            typeAns = typePos[pos5Index[pos]]
            guesserList[pos] = Guesser(name, no2d, typeAns, realAns, realAns)
        # 待作答位置
        for i in range(5 - empty_num, 5):
            pos = random5pos[i]
            realAns = ansOrigin[goodPos[pos5Index[pos]]]
            typeAns = typePos[pos5Index[pos]]
            guesserList[pos] = Guesser("", -1, typeAns, "", realAns)
        
        # 答案字符串内挖空
        ansPart = list(ansOrigin)
        for i in range(5):
            ansPart[goodPos[pos5Index[i]]] = "#"
        ansPart = ''.join(ansPart)  # 转换回字符串

        # 保存游戏状态
        if self.last_is_group:
            self.groupState[self.last_gid] = (guesserList, ansPart, ques_no, empty_num)
        else:
            self.userState[self.last_uid] = (guesserList, ansPart, ques_no, empty_num)
        
        # 绘制图片并返回图片路径
        image_path = self.drawTool.drawPng(DrawState(guesserList, ansPart), question, False)

        return MessageChain([Image(image_path)])
    
    def check_type(self, type: str, cha: str) -> bool:
        '''检查类型是否匹配'''
        if type == "Chs":
            return '\u4e00' <= cha <= '\u9fff'
        elif type == "Dig":
            return cha.isdigit()
        elif type == "Eng":
            return cha.isalpha() and cha.isascii()
        else:
            return False
    
    def parse_game_text(self, arg: list[str], uid: int, uname: str, is_group: bool, gid: int) -> MessageChain:
        '''解析游戏参数'''
        self.last_uid = uid
        self.last_uname = uname
        self.last_is_group = is_group
        self.last_gid = gid
        # 解析参数
        if arg[0] == "beg":
            # 检查参数
            if len(arg) != 2:
                return MessageChain([Text("参数数量不对哦\no(´^｀)o")])
            # 检查参数是否为数字
            try:
                empty_num = int(arg[1])  # 尝试将参数转换为整数
            except ValueError:
                return MessageChain([Text("参数有错喵\n(｀・ω・´)")])
            # 检查参数范围
            if empty_num < 1 or empty_num > 5:
                return MessageChain([Text("参数范围不对哦\no(╥﹏╥)o")])
            # 开始游戏
            return self.begin_game(empty_num)
        
        elif arg[0] == "ans":
            # 检查参数
            if len(arg) != 3:
                return MessageChain([Text("参数数量不对哦\no(´^｀)o")])
            # 检查参数是否为数字
            try:
                block_pos = int(arg[1])  # 尝试将参数转换为整数
            except ValueError:
                return MessageChain([Text("参数有错喵\n(｀・ω・´)")])
            # 检查参数范围
            if block_pos < 1 or block_pos > 5:
                return MessageChain([Text("参数范围不对哦\no(╥﹏╥)o")])
            if len(arg[2]) != 1:
                return MessageChain([Text("参数范围不对哦\no(╥﹏╥)o")])
            
            # 检查游戏状态
            if self.last_is_group:
                if self.last_gid not in self.groupState:
                    return MessageChain([Text("没有进行中的游戏哦\n(￣▽￣)ノ")])
                guesserList, ansPart, ques_no, empty_num = self.groupState[self.last_gid]
            else:
                if self.last_uid not in self.userState:
                    return MessageChain([Text("没有进行中的游戏哦\n(￣▽￣)ノ")])
                guesserList, ansPart, ques_no, empty_num = self.userState[self.last_uid]

            # 检查答案是否符合局面
            if guesserList[block_pos - 1].ansNow != "":
                return MessageChain([Text("这个位置已经有人答过了~\n╮(￣▽￣)╭")])
            if not self.check_type(guesserList[block_pos - 1].empType, arg[2]):
                return MessageChain([Text("这个位置的类型不对哦\n╮(￣▽￣)╭")])
            
            # 进行修改
            guesserList[block_pos - 1].ansNow = arg[2]
            if len(uname) > 8:
                uname = uname[:8]
            guesserList[block_pos - 1].name = uname
            # 检查该用户的no2d
            if uid not in self.userNo2d:
                # 初始分配2d编号
                self.userNo2d[uid] = 60
                guesserList[block_pos - 1].no2d = 60
            else:
                guesserList[block_pos - 1].no2d = self.userNo2d[uid]
            empty_num -= 1

            if empty_num == 0:
                # 游戏结束，绘制图片
                image_path = self.drawTool.drawPng(DrawState(guesserList, ansPart), self.questionList[ques_no], True)
                # 删除游戏状态
                if self.last_is_group:
                    del self.groupState[self.last_gid]
                else:
                    del self.userState[self.last_uid]
            else:
                # 游戏未结束，绘制图片
                image_path = self.drawTool.drawPng(DrawState(guesserList, ansPart), self.questionList[ques_no], False)
                # 更新游戏状态
                if self.last_is_group:
                    self.groupState[self.last_gid] = (guesserList, ansPart, ques_no, empty_num)
                else:
                    self.userState[self.last_uid] = (guesserList, ansPart, ques_no, empty_num)
            return MessageChain([Image(image_path)])
        
        elif arg[0] == "set":
            # 检查参数
            if len(arg) != 2:
                return MessageChain([Text("参数数量不对哦\no(´^｀)o")])
            find_name = arg[1]
            # 查找反向字典
            if find_name in self.s2d_dir:
                # 找到对应的2d编号
                no2d = self.s2d_dir[find_name]
                # 更新持久化数据
                if uid not in self.userNo2d:
                    self.userNo2d[uid] = no2d
                else:
                    self.userNo2d[uid] = no2d
                return MessageChain([Text("设置成功喵\n(￣▽￣)ノ")])
            else:
                return MessageChain([Text("没有这个名字哦\n╮(￣▽￣)╭")])
            
        else:
            return MessageChain([Text("指令有错喵\n╮(￣▽￣)╭")])
            
    def on_close(self):
        # 保存持久化数据
        with open(os.path.join(self.pcrPath, 'userNo2d.json'), 'w', encoding='utf-8') as f:
            json.dump(self.userNo2d, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    pcrMtManager = PcrMtManager()

    guesserList = []
    guesserList.append(Guesser("qin", 205, "Chs", "刘", "刘"))
    guesserList.append(Guesser("", 206, "Chs", "狗", "狗"))
    guesserList.append(Guesser("lhs", 61, "Chs", "摆", "卷"))
    guesserList.append(Guesser("", 207, "Chs", "麻", "麻"))
    guesserList.append(Guesser("ys", 145, "Chs", "了", "了"))

    ansPart = "#####"

    question = Question("这个生物的名称是？", "今天只玩了原神，没玩寒蝉，今天白天又是捐了一天。", "刘狗卷疯了", 6, 0, 1)

    pcrMtManager.drawTool.drawPng(DrawState(guesserList, ansPart), question, False)

    print("绘制完成")
    