# Typecho博客迁移与数据修复工具

此仓库包含三个用于博客数据迁移和修复的Python脚本工具。

问题反馈 @[JiuXia2025](https://github.com/JiuXia2025)

## WalineDateFix.py

该脚本用于修复Waline导出的数据在重新导入时出现的日期格式问题。

**功能**：
- 解决Waline导出数据再重新导入时出现的`insertedAct`字段值类型不匹配问题
- 自动将`insertedAct`字段的字符串值转换为符合ISO 8601格式的日期对象
- 修复原始错误：`Invalid value type for field 'insertedAct'`

**使用方法**：
1. 将Waline导出的JSON文件命名为`waline.json`
2. 运行脚本：`python WalineDateFix.py`
3. 输出文件：`converted_data.json`

## Typecho2Hexo-Mod.py

由[JiuXia2025](https://github.com/JiuXia2025)基于原版[Typecho2Hexo](https://github.com/zhourongyu/Typecho2Hexo)的改进版本，用于将Typecho博客数据转换为Hexo格式。

**功能增强**：
- 更换数据库驱动为pymysql
- 自动插入文章封面
- 迁移文章旧的永久链接ID（需安装hexo插件abbrlink生效）
- 支持分类和标签迁移

**使用前配置**：
```python
host = '127.0.0.1'
port = 3306
db = '数据库名'
user = '数据库用户名'
password = '数据库密码'
```

**使用方法**：
1. 配置数据库连接信息
2. 运行脚本：`python Typecho2Hexo-Mod.py`
3. 生成的文章和分类将保存在`data`目录下

## WalineLCloudDateFix.py

修复Typecho导出JSON评论数据插件导出的Waline数据中时间字段格式问题。

**功能**：
- 将Waline数据中的时间字段转换为LeanCloud推荐的UTC格式
- 处理多种ISO格式日期字符串
- 修复LeanCloud原始报错：`Invalid date format, expect: yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`

**支持的时间格式**：
- 2024-10-30T15:37:15+08:00
- 2025-05-02T11:22:31.718Z

**使用方法**：
1. 将导出的评论数据命名为`valine.json`
2. 运行脚本：`python WalineLCloudDateFix.py`
3. 输出文件：`converted_data.json`
