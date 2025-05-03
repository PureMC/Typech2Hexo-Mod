# -*- coding: utf-8 -*-
# Typecho2Hexo Mod
# Mod by JiuXia2025
# 新增功能：更换数据库驱动器为pymysql、自动插入文章封面、迁移文章旧的永久链接ID（需要安装hexo插件abbrlink生效）
# 改自旧版:https://github.com/zhourongyu/Typecho2Hexo
import os
import re
import pymysql
import arrow
from flask import Flask
import urllib
import codecs

host = '127.0.0.1'
port = 3306
db = '数据库名'
user = '数据库用户名'
password = '数据库密码'

def main():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # 创建分类和标签
    cursor.execute("select type, slug, name from typecho_metas")
    for cate in cursor.fetchall():
        path = 'data/分类/%s' % urllib.parse.unquote(cate['slug'])
        if not os.path.exists(path):
            os.makedirs(path)
        f = codecs.open('%s/index.md' % path, 'w', "utf-8")
        f.write("title: %s\n" % urllib.parse.unquote(cate['slug']))
        f.write("date: %s\n" % arrow.now().format('YYYY-MM-DD HH:mm:ss'))
        # 区分分类和标签
        if cate['type'] == 'category':
            f.write('type: "categories"\n')
        elif cate['type'] == 'tags':
            f.write('type: "tags"\n')
        # 禁止评论
        f.write("comments: false\n")
        f.write("---\n")
        f.close()

    # 创建文章
    cursor.execute("select cid, title, slug, text, created from typecho_contents where type='post'")
    for e in cursor.fetchall():
        title = re.sub(r'[/:*?"<>|]', '-', e['title'].encode('raw_unicode_escape').decode("unicode-escape"))
        content = str(e['text'].replace('<!--markdown-->', ''))
        tags = []
        category = ""

        # 获取分类和标签
        cursor.execute(
            "select type, name, slug from `typecho_relationships` ts, typecho_metas tm where tm.mid = ts.mid and ts.cid = %s",
            e['cid'])
        for m in cursor.fetchall():
            if m['type'] == 'tag':
                tags.append(m['name'])
            if m['type'] == 'category':
                #category = urllib.parse.unquote(m['slug'])
                #使用真实名称做分类而不是slug缩写
                 category = m['name']

        # 新增：获取封面图片链接
        cursor.execute(
            "select str_value from typecho_fields where cid = %s and name = 'thumb'",
            e['cid']
        )
        cover_row = cursor.fetchone()
        cover_url = cover_row['str_value'] if cover_row else ''

        path = 'data/文章/'
        if not os.path.exists(path):
            os.makedirs(path)
        f = codecs.open('%s%s.md' % (path, title), 'w', "utf-8")
        f.write("---\n")
        f.write("title: %s\n" % title)
        f.write("abbrlink: %s\n" % e['cid'])
        f.write("date: %s\n" % arrow.get(e['created']).format('YYYY-MM-DD HH:mm:ss'))
        f.write("categories: %s\n" % category)
        f.write("tags: [%s]\n" % ','.join(tags))

        # 插入封面信息
        if cover_url:
            f.write("cover: %s\n" % cover_url.strip())

        f.write("---\n")
        f.write(content)
        f.close()


if __name__ == "__main__":
    main()