import glob
import json
import pandas as pd
# 获取所有 JSON 文件的路径
json_files = glob.glob('./分类结果/*.json')

# 读取所有 JSON 文件的内容
json_data = []
for file in json_files:
    json_data.append(file)
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        json_data.append(data)

import re
def get_data(df):
    data = []
    for i in range(len(df)):
        type = df.iloc[i, 2]
        title = df.iloc[i, 3]
        options = df.iloc[i, 4]
        answer = df.iloc[i, 6]
        
        # print(type,title,options,answer)
        if type == '单选题':
            # 使用正则表达式处理括号中间的空格
            content = re.sub(r'（\s+', '（', title)  # 处理中文左括号后的空格
            content = re.sub(r'\s+）', '）', content)  # 处理中文右括号前的空格
            content = re.sub(r'\(\s+', '(', content)  # 处理英文左括号后的空格
            content = re.sub(r'\s+\)', ')', content)  # 处理英文右括号前的空格
            content = content.replace('（）', '____').replace('()', '____').replace('【单选题】','')
            choices = []
            for option in options:
                choices.append(option)
            ansIndex = []
            for ans in answer:
                ansIndex.append(ord(ans)-ord('A'))
            question = '--- 选择题\n' + '### '+ content + '\n' 
            for i, choice in enumerate(choices):
                question += '- [' 
                if i in ansIndex:
                    question += 'x'
                else:
                    question += ' '
                question += '] ' + list(choice.values())[0] + '\n'
            data.append(question)
        elif type == '多选题':
            # 使用正则表达式处理括号中间的空格
            content = re.sub(r'（\s+', '（', title)  # 处理中文左括号后的空格
            content = re.sub(r'\s+）', '）', content)  # 处理中文右括号前的空格
            content = re.sub(r'\(\s+', '(', content)  # 处理英文左括号后的空格
            content = re.sub(r'\s+\)', ')', content)  # 处理英文右括号前的空格
            content = content.replace('（）', '____').replace('()', '____').replace('【多选题】','')
            choices = []
            for option in options:
                choices.append(option)
            ansIndex = []
            for ans in answer:
                ansIndex.append(ord(ans)-ord('A'))
            question = '--- 选择题\n' + '### '+ content + '\n'
            for i, choice in enumerate(choices):
                question += '- [' 
                if i in ansIndex:
                    question += 'x'
                else:
                    question += ' '
                question += '] ' + list(choice.values())[0] + '\n'
            data.append(question)
        elif type == '判断题':
            # 使用正则表达式处理括号中间的空格
            content = re.sub(r'（\s+', '（', title)  # 处理中文左括号后的空格
            content = re.sub(r'\s+）', '）', content)  # 处理中文右括号前的空格
            content = re.sub(r'\(\s+', '(', content)  # 处理英文左括号后的空格
            content = re.sub(r'\s+\)', ')', content)  # 处理英文右括号前的空格
            # content = content.replace('（）', '____').replace('()', '____').replace('【判断题】','')
            content = content.replace('【判断题】','')
            answer = answer[0]
            question = '--- 判断题\n' + '### '+ content + '\n'
            question += '- '
            if answer == '对':
                question += 'T\n'
            else:
                question += 'F\n' 
            data.append(question)
    print(data)
    return data
            
    return data
# 生成 Markdown 文件
def generate_md(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(line)

for i in range(1,len(json_data),2):
    df = pd.DataFrame(json_data[i]['questions'])
    generate_md(get_data(df), json_data[i-1].replace('.json','.txt'))
