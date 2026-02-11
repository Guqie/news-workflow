# Google News重定向URL解决方案

## 问题分析

**Google News URL格式：**
```
https://news.google.com/rss/articles/CBMi...?oc=5&hl=en-US&gl=US&ceid=US:en
```

**问题：**
- 这不是实际的新闻页面URL
- 是Google News的重定向链接
- Trafilatura无法直接提取内容

## 解决方案

### 方案1：跟随重定向获取实际URL（推荐）

**原理：**
访问Google News URL → 自动跟随重定向 → 获取实际新闻URL

**实现：**
```python
import requests

def resolve_google_news_url(google_url):
    """解析Google News重定向，获取实际URL"""
    try:
        # 发送请求，允许重定向
        response = requests.get(
            google_url,
            allow_redirects=True,
            timeout=10,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        # 返回最终URL
        return response.url
    except:
        return None
```

