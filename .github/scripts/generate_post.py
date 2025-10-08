#!/usr/bin/env python3
import os
import re
from datetime import datetime
from github import Github

def main():
    # 获取环境变量
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')
    
    if not token or not repo_name:
        print("Missing environment variables")
        return
        
    # 初始化 GitHub API
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    # 获取所有带有 'blog' 标签的 issues
    issues = repo.get_issues(state='all', labels=['blog'])
    
    # 确保 _posts 目录存在
    os.makedirs('_posts', exist_ok=True)
    
    for issue in issues:
        # 跳过已关闭的 issues（如果你想保留已关闭的博客，可以移除这个条件）
        if issue.state == 'closed':
            continue
            
        # 生成文件名：日期-标题.md
        title = issue.title
        # 清理文件名中的非法字符
        clean_title = re.sub(r'[^\w\s-]', '', title)
        clean_title = re.sub(r'[-\s]+', '-', clean_title)
        
        # 使用 issue 创建日期
        create_date = issue.created_at.strftime('%Y-%m-%d')
        filename = f"{create_date}-{clean_title}.md"
        filepath = os.path.join('_posts', filename)
        
        # 生成 Front Matter
        front_matter = f"""---
layout: post
title: "{title}"
date: {create_date}
issue_url: {issue.html_url}
issue_number: {issue.number}
---

"""
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(front_matter)
            f.write(issue.body)
            
        print(f"Generated: {filepath}")
        
    print("Blog generation completed!")

if __name__ == '__main__':
    main()