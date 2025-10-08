---
layout: default
title: 首页
---

# 欢迎来到我的博客

{% for post in site.posts %}
## [{{ post.title }}]({{ post.url | relative_url }})
**发布日期：{{ post.date | date: "%Y年%m月%d日" }}**

{{ post.excerpt | truncate: 200 }}

---
{% endfor %}