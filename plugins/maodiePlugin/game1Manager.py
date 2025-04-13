import random
from ncatbot.core import (
    MessageChain,  # 消息链，用于组合多个消息元素
    Text,          # 文本消息
    At,            # @某人
    AtAll,         # @全体成员
    Face,          # QQ表情
    Image,         # 图片
    Json,          # JSON消息
)

class Game1Manager:
    """游戏1类"""
    data = {}
    rate_shizi = 0.7
    change_to_win = 0.5

    last_uid = 0
    last_is_group = False
    last_gid = 0

    group_game = {}
    user_game = {}

    message = None
    
    def get_game_save(self):
        '''获取游戏存档'''
        if self.last_is_group:
            if self.last_gid not in self.group_game:
                self.message += Text("没有游戏哦!!!\n∑(ﾟДﾟノ)ノ\n")
                return None
            return self.group_game[self.last_gid]
        else:
            if self.last_uid not in self.user_game:
                self.message += Text("没有游戏哦!!!\n∑(ﾟДﾟノ)ノ\n")
                return None
            return self.user_game[self.last_uid]

    def parse_game_text(self, text: str, uid: int, is_group: bool, gid: int) -> MessageChain:
        """解析游戏文本命令"""
        self.last_uid = uid
        self.last_is_group = is_group
        self.last_gid = gid

        self.message = MessageChain([])
        if (text[0] == 'beg'):
            text = text[1:]
            if not text or len(text) != 3:
                self.message += Text("参数个数不对哦\n(*/ω＼*)\n")
                return self.message
            
            # 解析三个参数成数字
            try:
                n = int(text[0])
                k = int(text[1])
                is_your_go = int(text[2])
            except ValueError:
                self.message += Text("参数类型不对哦\n╮(╯﹏╰）╭\n")
                return self.message
            
            if is_your_go == 0:
                is_your_go = False
            elif is_your_go == 1:
                is_your_go = True
            else:
                self.message += Text("参数不在范围内哦\n(╯‵□′)╯︵┻━┻\n")
                return self.message
            
            # 检查范围
            if n < 6 or n > 30 or k < 2 or k > n // 3:
                self.message += Text("参数不在范围内哦\n(╯‵□′)╯︵┻━┻\n")
                return self.message
            
            self.start_game(n, k)

            self.show_game()
            if not is_your_go:
                strategy = self.cal_strategy()
                self.select_game(strategy)
                self.show_game()

        elif (text[0] == 'sl'):
            text = text[1:]
            if not text or len(text) == 0:
                self.message += Text("参数个数不对哦\n(*/ω＼*)\n")
                return self.message
            # 解析存档
            game_data = self.get_game_save()
            if game_data is None:
                return self.message
            shizi, k, is_win = self.user_game[uid]
            n = len(shizi)
            
            # 检查范围
            if len(text) < 1 or len(text) > k:
                self.message += Text("参数个数不对哦\n(*/ω＼*)\n")
                return self.message
            
            # 解析选择的石子
            # 查找第一个石子位置
            pos = 0
            for pos in range(len(shizi)):
                if shizi[pos] == 1:
                    break
            # 检查选择处
            select = []
            for i in text:
                try:
                    i = int(i)
                    if i < 1 or i > k or pos + i - 1 >= n or shizi[pos + i - 1] == 0:
                        self.message += Text("参数不在范围内哦\n(╯‵□′)╯︵┻━┻\n")
                        return self.message
                    select.append(pos + i - 1)
                except ValueError:
                    self.message += Text("参数类型不对哦\n╮(╯﹏╰）╭\n")
                    return self.message

            self.select_game(select)
            if not self.show_game():
                self.end_game(False, False)
                return self.message
            strategy = self.cal_strategy()
            self.select_game(strategy)
            if not self.show_game():
                self.end_game(False, True)
                return self.message
        
        elif (text[0] == 'show'):
            # 显示游戏
            game_data = self.get_game_save()
            if game_data is None:
                return self.message
            shizi, k, is_win = self.user_game[uid]
            n = len(shizi)
            self.show_game()
        
        elif (text[0] == 'end'):
            # 结束游戏
            game_data = self.get_game_save()
            if game_data is None:
                return self.message
            self.end_game(True, False)
        
        else:
            self.message += Text("参数有错哦\n╮(╯﹏╰）╭\n")
            return self.message
        
        return self.message

    
    def start_game(self, n: int, k: int):
        '''随机生成游戏,不能全0'''
        shizi = [0] * n
        
        # 随机生成石子
        while sum(shizi) == 0:
            for i in range(n):
                if random.random() < self.rate_shizi:
                    shizi[i] = 1
        
        # 记录游戏
        if self.last_is_group:
            self.group_game[self.last_gid] = (shizi, k, False)
        else:
            self.user_game[self.last_uid] = (shizi, k, False)

    def show_game(self) -> bool:
        '''显示游戏兼任检查是否胜利'''
        # 解析存档
        shizi, k, is_win = self.get_game_save()
        n = len(shizi)
        # 检查是否胜利
        if sum(shizi) == 0:
            return False
        # 找到第一个石子位置
        pos = 0
        for pos in range(len(shizi)):
            if shizi[pos] == 1:
                break
        # 显示游戏
        self.message += Text('-' * 10 + '\n')
        self.message += Text("当前局面: \n")
        # 显示石子
        for i in range(len(shizi)):
            if shizi[i] == 1:
                self.message += Text("+")
            else:
                self.message += Text("-")
        # 显示指标
        self.message += Text('\n' + '-' * pos + '+' * k + '-' * max(0, n - pos - k) + '\n\n')
        self.message += Text('-' * 10 + '\n')

        return True
    
    def cal_sure_to_win(self, shizi: list[int], k: int, last: bool):
        '''计算是否是必胜态'''
        if sum(shizi) == 0:
            return False
        n = len(shizi)
        # 找到第一个石子位置
        pos = 0
        for pos in range(len(shizi)):
            if shizi[pos] == 1:
                break
        
        # 如果有的选就赢了
        is_to_win = False
        for i in range(1, k):
            if pos + i >= n:
                break
            if shizi[pos + i] == 1:
                is_to_win = True
                break
        
        if is_to_win:
            if last:
                # 计算后两步是否必胜
                shizi_copy = shizi.copy()
                for i in range(k):
                    if pos + i >= n:
                        break
                    shizi_copy[pos + i] = 0
                # 需要给出策略
                if self.cal_sure_to_win(shizi_copy, k, False):
                    # 如果后两步必胜,就不拿完
                    strategy = [i + pos for i in range(1, k) if pos + i < n and shizi[pos + i] == 1]
                    return (True, strategy)
                else:
                    # 如果后两步必败,就拿完
                    strategy = [i + pos for i in range(k) if pos + i < n and shizi[pos + i] == 1]
                    return (True, True)
            else:
                return True
        
        # 否则取决于下一步
        shizi_copy = shizi.copy()
        shizi_copy[pos] = 0
        if last:
            return (not self.cal_sure_to_win(shizi_copy, k, False), [pos])
        else:
            return not self.cal_sure_to_win(shizi_copy, k, False)
    
    def random_strategy(self, shizi: list[int], k: int) -> list[int]:
        '''随机选择策略,不能全0'''
        n = len(shizi)
        # 找到第一个石子位置
        pos = 0
        for pos in range(len(shizi)):
            if shizi[pos] == 1:
                break
        
        # 随机选择策略
        strategy = [i + pos for i in range(k) if pos + i < n and shizi[pos + i] == 1]
        # 随机删除 strategy 中的元素，保证至少剩下一个
        while len(strategy) > 1:
            # 随机选择一个索引
            index_to_remove = random.randint(0, len(strategy) - 1)
            # 删除该索引对应的元素
            strategy.pop(index_to_remove)
            # 随机决定是否继续删除
            if random.random() > self.rate_shizi / 2:
                break
        
        return strategy

    def cal_strategy(self) -> list[int]:
        '''计算策略,不能全0'''
        # 解析存档
        shizi, k, is_win = self.get_game_save()
        # 计算策略
        is_to_win, strategy = self.cal_sure_to_win(shizi, k, True)
        # 输出策略
        if is_to_win:
            if (not is_win) and random.random() > self.change_to_win:
                # 随机选择策略
                strategy = self.random_strategy(shizi, k)
                self.message += Text("哎,作出了困难的选择~\n")
            else:
                # 采取必胜策略
                is_win = True
                self.message += Text("我觉得我找到必胜策略了呢\n(ﾉ´▽｀)ﾉ♪\n")
                
        else:
            self.message += Text("这把怎么如此艰难\n(╯‵□′)╯︵┻━┻\n")
            
        return strategy
    
    def select_game(self, select: list[int]):
        '''选择石子,需要经过检查'''
        # 解析存档
        shizi, k, is_win = self.get_game_save()

        for i in select:
            shizi[i] = 0
        
        if self.last_is_group:
            self.group_game[self.last_gid] = (shizi, k, is_win)
        else:
            self.user_game[self.last_uid] = (shizi, k, is_win)
    
    def end_game(self, is_force: bool, is_my_win: bool):
        '''结束游戏,需要经过检查'''
        if self.last_is_group:
            if self.last_gid in self.group_game:
                del self.group_game[self.last_gid]
        else:
            if self.last_uid in self.user_game:
                del self.user_game[self.last_uid]
        
        # 输出一些战败或获胜感言
        if is_force:
            self.message += Text("游戏结束了呢ヾ(=･ω･=)o\n")
        else:
            if is_my_win:
                self.message += Text("我赢了呢(ﾉ´▽｀)ﾉ♪\n")
            else:
                self.message += Text("我输了啊(╯‵□′)╯︵┻━┻\n")