# !/usr/bin/env python3

import os
import re
from datetime import datetime

def sanitize_filename(title):
    """将标题转换为安全的文件名"""
    # 移除特殊字符，只保留字母、数字、空格
    cleaned_title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
    # 将空格替换为短横线，并转换为小写
    return cleaned_title.strip().replace(' ', '-').lower()

def generate_post(i_issue_number, i_issue_title, i_issue_body):
    # 获取当前日期
    today = datetime.now().strftime("%Y-%m-%d")

    # 生成文件名：日期-标题.md
    filename = f"{today}-{sanitize_filename(i_issue_title)}.md"
    filepath = f"_posts/{filename}"

    # 创建 Front Matter（Jekyll 的文章头信息）
    front_matter = f"""---
layout: post
title: "{i_issue_title}"
date: {today}
issue_id: {i_issue_number}
categories: blog
---

"""

    # 组合完整内容：Front Matter + 文章正文
    content = front_matter + i_issue_body

    # 确保 _posts 目录存在
    os.makedirs("_posts", exist_ok=True)

    # 写入文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"生成博客文章: {filepath}")

if __name__ == "__main__":
    # 从环境变量获取 Issue 信息
    issue_number = os.getenv("ISSUE_NUMBER")
    issue_title = os.getenv("ISSUE_TITLE")
    issue_body = os.getenv("ISSUE_BODY")

    if issue_number and issue_title and issue_body:
        generate_post(issue_number, issue_title, issue_body)
    else:
        print("缺少环境变量")
