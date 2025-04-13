from ncatbot.core import BotClient
from ncatbot.utils import config

config.set_bot_uin("3887885356")  # 设置 bot qq 号 (必填)
config.set_root("3198882955")  # 设置 bot 超级管理员账号 (建议填写)
config.token = "666zhegerushigui"

bot = BotClient()

if __name__ == "__main__":
    bot.run()