# 故障机器人
### 1 环境

[NcatBot文档](https://docs.ncatbot.xyz/guide/dto79lp7/)

launch.py中修改登录用户

运行launch.py启动

### 2 功能说明
### 2.1 发送本地图片
**前置：下载本地图片到static/images下**

static/getpicture.py
以未登录用户的名义下载P站图片，所以有些图片是看不见的
代码来自[pixiv-web-crawler
](https://github.com/llnkwell/pixiv-web-crawler)

完成以下功能：

* 读取static/uid.txt 中的元组列表 (uid,下载插画数(时间顺序，0表示全部读取)), 下载所有插画
* 遍历images文件夹为每个文件编号,保存在static/image_dir.json


static/image_dir.json示例如下:

```json
{
    "0": "109576125_p0.png",
    "1": "109927265_p0.png",
    "2": "109927294_p0.png"
}
```

**使用：见ImageManager模块**

输入指令经过ArgParser模块解析，向下调用更详细的功能模块

### 2.2 没有
