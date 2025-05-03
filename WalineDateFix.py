import json
# WalineDateFix by JiuXia2025
# 解决Waline导出的数据再重新导入时报错insertedAct的值类型不匹配
# 原始报错信息：Invalid value type for field 'insertedAct',value '"2023-08-07T02:19:45.000Z"',expect type is {:type "Date"},but it is '{:type "String"}'. [400 POST https://yotmhin5.api.lncldglobal.com/1.1/classes/Comment]
# 执行脚本自动将 insertedAct 字段的值转换为 ISO 8601 格式的日期对象 或符合后端要求的日期格式

# 加载你的 JSON 文件
with open('waline.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 遍历 Comment 表中的每一条记录
for comment in data['data']['Comment']:
    if 'insertedAct' in comment and isinstance(comment['insertedAct'], str):
        comment['insertedAct'] = {
            "__type": "Date",
            "iso": comment['insertedAct']
        }

# 保存修改后的数据到新文件
with open('converted_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)