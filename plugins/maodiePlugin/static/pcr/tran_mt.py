'''处理oringin.html的内容，生成mt.json'''
import os
import json

filedir = os.path.dirname(__file__)

mt = []
def tran_mt():
    '''处理oringin.html的内容，生成mt.json'''
    # 读取HTML文件内容
    with open(os.path.join(filedir, 'oringin.html'), 'r', encoding='utf-8') as file:
        # 遍历每一行
        is_read = False
        lines = file.readlines()
        cnt = 0
        while cnt < len(lines):
            line = lines[cnt]
            # 去除前导和后续空格
            line = line.strip()
            # 判断起始和开始
            if line == "<tbody style=\"\">":
                is_read = True
                cnt += 1
                continue
            elif line == "</tbody>":
                break
            # 接下来6行
            if is_read:
                # 第一行<tr data-param1="1" data-param2="1" data-param3="1" style="">
                params = line.split('"')
                # 取出参数
                data = ["", "", "", int(params[1]), int(params[3]), int(params[5])]
                # 第二行<td>这个的名称是什么？</td>
                cnt += 1
                data[0] = lines[cnt].strip().split('>')[1].split('<')[0]
                # 第三行<td>「宫子」的口头禅，同时也是其连结爆发名称。</td>
                cnt += 1
                data[1] = lines[cnt].strip().split('>')[1].split('<')[0]
                # 第四行<td>把你变成布丁
                cnt += 1
                data[2] = lines[cnt].strip().split('>')[1]
                # 第五第六行
                cnt += 3
                # 添加到mt列表中
                mt.append(data.copy())
            else:
                cnt += 1
    

if __name__ == '__main__':
    tran_mt()
    print("mt文件数量: ", len(mt))
    # 保存文件
    with open(os.path.join(filedir, 'mt.json'), 'w', encoding='utf-8') as f:
        json.dump(mt, f, ensure_ascii=False, indent=4)
    print("mt.json文件生成完毕")

    