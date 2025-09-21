# 故障机器人
### 1 环境

[NcatBot文档](https://docs.ncatbot.xyz/guide/dto79lp7/)

(这玩意目前失效了)

launch.py中修改登录用户

运行launch.py启动

需要python库:

* 文档中框架 `pip install ncatbot -U -i https://mirrors.aliyun.com/pypi/simple/`
* 图像处理 `pillow`
* （不是主程序用到的）繁体转简体 `zhconv`


### 2 功能说明
### 2.1 发送本地图片

`st`

**前置：下载本地图片到static/images下**

static/getpicture.py
以未登录用户的名义下载P站图片，所以有些图片是看不见的

代码来自[pixiv-web-crawler](https://github.com/llnkwell/pixiv-web-crawler)

完成以下功能：

* 读取`static/uid.txt`中的元组列表 (uid,下载插画数(时间顺序，0表示全部读取)), 下载所有插画
* 遍历`static/images`文件夹为每个文件编号,保存在`static/image_dir.json`


`static/image_dir.json`示例如下:

```json
{
    "0": "109576125_p0.png",
    "1": "109927265_p0.png",
    "2": "109927294_p0.png"
}
```

**使用：见ImageManager模块**

输入指令经过ArgParser模块解析，向下调用更详细的功能模块

---

### 2.2 进行交互小游戏

一个知道原理就没啥意思的小游戏，通过字符显示，详情见`gm1`指令

**必胜原理**：

如果当前状态有选择，那么必胜。

由于有选择，我们可以把除了第一个之外的石子拿掉，考虑这个转移后状态s：

s状态没有选择，只能拿第一个石子，之后转移到状态t。

* 如果状态t是必胜态，即又轮到我必胜，那么我的策略就是把除了第一个之外的石子拿掉。

* 如果状态t是必败态，那么我的策略就是把所有石子拿掉，使对手直接转移到t状态。

---

### 2.3 兰德索尔谜题连结

具体规则见`mt`指令，一人到五人的填空题，一个人可以填多个空。

`static/pcr/userNo2d.json`是存储每个用户使用哪个2d模型编号数据。


接下来主要介绍数据来源。

#### 2.3.1 题目来源：[兰德索尔谜题连结·档案](https://wiki.biligame.com/pcr/Taq)

原始网页（修改部分错漏）在`static/pcr/oringin.html`，答案挖空的逻辑是在第一个`=`后的数字、英文、中文处挖空，至少5个空，所以把有很多个等号的答案去掉了。此外答案中不能含有`#`

之后通过`static/pcr/tran_mt.py`转化为`static/pcr/mt.json`，如果想加题的话可以从这里加，三个参数是：题目类型/是否和公主连结有关/难度

#### 2.3.2 2d小人来源：[wthee网站播放器](https://wthee.xyz/spine/)

这部分比较繁琐，截出来的图位置不一，代码我已经按我的位置写死了，处理后的图像都上传了。

这里介绍一下我怎么做的。

首先网页中勾选透明背景。

在网页f12打开控制台，粘贴`static/pcr/get2d.js`中内容，可以进行自动下载，原理就是使用js模拟在网页中与各个组件的交互。

但是这里有各种奇怪的bug，有时会全部截出空白图。这里建议在js循环中每次只截一定范围内的图（比如0-100张），运行前先预加载那个位置附近的模型。

最麻烦的是这里面有些模型的初始位置和放缩比例本身就和其他人不一样，需要下载后手工调整。

随后，把没有汉语翻译的删了，再通过`static/pcr/tran_t2s.py`去掉几星的前缀并转化为简体，成为`static/pcr/s2d.json`

#### 2.3.3 图像字体来源

b站截图，自行抠图，存放在`static/pcr/imagPart`下

字体：[腾祥沁圆简-W3](https://www.ttfont.com/font-details/182535/)存放在`static/pcr/txqyj-w3.ttf`

---
