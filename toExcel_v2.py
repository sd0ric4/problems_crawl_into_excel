import pandas as pd
import json
import os

# JSON 文件路径
json_file_path = './json/'
# Excel 文件保存路径
excel_file_path = './excel/'

# 遍历 JSON 文件夹中的所有文件
for root, dirs, files in os.walk(json_file_path):
    for file in files:
        if file.endswith('.json'):
            json_file = os.path.join(root, file)
            # 使用 Pandas 读取 JSON 文件
            with open(json_file, 'r', encoding="utf8") as json_data_file:
                json_data = json.load(json_data_file)
                df = pd.DataFrame(json_data)

            # 转换选项列
            options_cols = ['选项A', '选项B', '选项C', '选项D', '选项E']
            for col in options_cols:
                df[col] = df['options'].apply(
                    lambda x: next((item.get(col[-1], '') for item in x if col[-1] in item), ''))

            # 添加所需列
            df['大题题干'] = ''  # 假设 JSON 数据中没有这个字段，因此添加空列
            df['题型(选填)'] = df['type']
            df['题干/小题题干'] = df['title']
            df['答案'] = df['correctAnswer']
            df['解析'] = ''  # 假设 JSON 数据中没有解析字段
            df['章节'] = df['chapter']
            df['知识点'] = ''  # 假设 JSON 数据中没有知识点字段
            df['分值'] = ''  # 假设 JSON 数据中没有分值字段

            # 调整列的顺序
            df = df[
                ['大题题干', '题型(选填)', '题干/小题题干', '选项A', '选项B', '选项C', '选项D', '选项E', '答案', '解析',
                 '章节', '知识点', '分值']]

            # 保存到 Excel
            excel_file = os.path.join(excel_file_path, f"{os.path.splitext(file)[0]}.xlsx")
            df.to_excel(excel_file, index=False)
