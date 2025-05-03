import json
from datetime import datetime, timezone, timedelta
import re
# WalineLCloudDateFix by JiuXia2025
# 修复Typecho导出JSON评论数据插件，导出的 Waline 数据中时间字段格式的问题
# 该脚本将 Waline 数据中的时间字段转换为 LeanCloud 推荐的 UTC 格式
# 原始LeanCloud报错信息：Invalid date format, expect: yyyy-MM-dd'T'HH:mm:ss.SSS'Z'

def clean_string(s):
    """清理字符串中的非法空白字符"""
    return re.sub(r'\s+', ' ', s.strip())

def parse_iso_date(iso_str):
    """
    将 ISO 格式字符串解析为 datetime 对象，并转换为 UTC 时间
    支持格式如：
        - 2024-10-30T15:37:15+08:00
        - 2025-05-02T11:22:31.718Z
    """
    try:
        iso_str = clean_string(iso_str)
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))  # 处理 Z 时区
        return dt.astimezone(timezone.utc)
    except Exception as e:
        print(f"[ERROR] Failed to parse date: '{iso_str}' - {e}")
        raise

def format_utc_date(dt):
    """将 datetime 对象格式化为 LeanCloud 推荐格式：yyyy-MM-dd'T'HH:mm:ss.000Z"""
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")

def convert_date_field(value):
    """通用时间字段转换器"""
    if isinstance(value, str):
        return format_utc_date(parse_iso_date(value))
    elif isinstance(value, dict) and "iso" in value:
        value["iso"] = format_utc_date(parse_iso_date(value["iso"]))
        return value
    else:
        return value

def fix_dates_in_data(data):
    """递归遍历所有对象并转换时间字段"""
    if isinstance(data, list):
        for item in data:
            fix_dates_in_data(item)
    elif isinstance(data, dict):
        for key in ["createdAt", "updatedAt", "insertedAct"]:
            if key in data:
                data[key] = convert_date_field(data[key])
        for value in data.values():
            fix_dates_in_data(value)

    return data

if __name__ == "__main__":
    input_file = "valine.json"
    output_file = "converted_data.json"

    # 读取原始数据
    with open(input_file, "r", encoding="utf-8") as f:
        raw_content = f.read()
        data = json.loads(raw_content)

    # 转换时间字段
    fixed_data = fix_dates_in_data(data)

    # 写出新文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 时间字段已成功转换，输出到 {output_file}")