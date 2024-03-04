
# %% 

import re
import pyperclip
import shutil
from info import info

# %% 
# 输入文本
text = '避免以符号开头'+pyperclip.paste()
# 正则表达式匹配中文字符
pattern = '[\u4e00-\u9fa5（）()]+'
matches = re.findall(pattern, text)

# 拆分符号
split_sign = re.split(pattern, text)
# split_sign = [s for s in split_sign if s]  # 去除空字符串

first = True
for sign,i in zip(split_sign[:-1],range(len(split_sign)-1)):
    if sign in ["+","-",'/'] and split_sign[i+1] in ["+","-",'/'] :
        i0=i
        while sign =='/':  # 保证sign 为 '+' or '-'
            sign=split_sign[i+1]
            i+=1
            # i0=i  # index of sign
        while split_sign[i+1]=='/':  # 保证split_sign[i+1]为 '+' or '-'
            i+=1
        if sign == split_sign[i+1] and first:  # 首次出现重复分隔符
            first = False
            mark = sign
            startidx = i0  # 起始索引
    elif not first:  # sign or next sign not in ["+","-",'/']且 not first
        endidx = i+2 # sign 要保留，同时索引是左闭右开故需要再多一位 
        break

try:
    keys = matches[startidx-1:endidx-1]
except NameError:
    try:
        keys = matches[startidx-1:]
    except NameError as e:
        print(e)
        print('剪贴板中未识别到类似于 "姓名-学校-专业" 或 "姓名+学校+专业" 的格式化描述... \n终止运行')
        exit()

# 输出原文关键部分便于检查
try:    
    oritext = text[max(text.find(keys[0])-6,0):text.find(keys[-1])+5]
except IndexError as e:
    print(e)
    print('剪贴板中未识别到类似于 "姓名-学校-专业" 或 "姓名+学校+专业" 的格式化描述... \n终止运行')
    exit()
# %% 
# 修改键值以生成内容
for key,i in zip(keys,range(len(keys))):
    toadd = True
    for truekey in info.keys():
        if key.find(truekey)>-1:
            keys[i]=truekey
            toadd=False
            break
    # keys[i]='???'  # 没有break说明没有匹配上
    if toadd:
        addinfo = input(f'请输入 {key} 所需要对应的信息：')
        keys[i] = key
        info[key] = addinfo
        with open('./info.py', 'r+', encoding='utf-8') as f:  # 更新info文件
            info_script = f.read()
            info_script = info_script[:info_script.find("}")]
            info_script += f"    '{key}':'{addinfo}',\n" + "}"
            f.seek(0)
            f.write(info_script)

anslist = [info[k] for k in keys]
signlist = split_sign[startidx:endidx-1]
signlist.append('')
output = ''
for s,a in zip(signlist,anslist):
    output += a
    output += s
pyperclip.copy(output)
print(f'已自动填充信息并复制到剪贴板，请根据输入的模板内容检查:\n')
print('------------------------------------------------------------')
print(f'\t{output}\n{oritext}')
print('------------------------------------------------------------\n')
while output.find('/')>-1:
    print(f'自动生成名称 "{output}" 中的 "/" 符号 不可用于文件命名, 替换为"-"')
    o = list(output)
    o[output.find('/')]='-'
    output = ''.join(o)
    
print(f'简历文件已经被重命名为 {output}.pdf 并保存到:')
shutil.copy('./cv.pdf',f'./renamed_cv/{output}.pdf')

# %%
