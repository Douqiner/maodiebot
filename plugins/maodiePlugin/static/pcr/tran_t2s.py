'''处理文件名，包括去除不必要字符和转化成简体'''
'''还有保存图片编号'''
import zhconv
import os

filePath = os.path.dirname(__file__)
dir_s2d = []

def tran_fun(is_tran: bool):

    # 获取当前目录下的所有文件
    s2d_path = os.path.join(filePath, 's2d')  # 指定 's2d' 文件夹路径
    files = os.listdir(s2d_path)

    # 遍历文件列表
    for file in files:
        if is_tran:
            old_file = os.path.join(s2d_path, file)  # 原文件的完整路径

            # 转换为简体中文
            new_file_name = zhconv.convert(file[2:], 'zh-cn')
            new_file = os.path.join(s2d_path, new_file_name)  # 转换后的完整路径

            # 重命名文件
            os.rename(old_file, new_file)
        else:
            # 直接使用文件名，不进行转换
            new_file_name = file
        # 保存图片编号
        dir_s2d.append(new_file_name)


if __name__ == '__main__':
    tran_fun(False)
    print("2d文件数量: ", len(dir_s2d))
    # 保存文件
    import json
    with open(os.path.join(filePath, 's2d.json'), 'w', encoding='utf-8') as f:
        json.dump(dir_s2d, f, ensure_ascii=False, indent=4)