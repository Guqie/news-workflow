# Newspaper4k 集成方案

**规划时间：** 2026-02-10 19:35
**目标：** 将newspaper4k集成到新闻采集项目

---

## 一、集成策略

### 方案A：作为主要采集引擎（推荐）⭐⭐⭐⭐⭐

**思路：**
- 使用newspaper4k的Source类爬取整个新闻网站
- 替代当前的滚动新闻爬虫
- 利用其多线程能力提高性能

**优势：**
- 自动发现文章链接
- 自动提取结构化数据
- 多线程并发
- 支持多种网站

**实现：**
```python
# 新建：newspaper_crawler.py
import newspaper
from newspaper import Config

class NewspaperCrawler:
    def __init__(self, sector):
        self.sector = sector
        self.config = Config()
        self.config.language = 'zh'
        self.config.number_threads = 5
        
    def crawl_source(self, url, max_articles=50):
        """爬取整个新闻网站"""
        source = newspaper.build(url, config=self.config)
        
        articles = []
        for article in source.articles[:max_articles]:
            try:
                article.download()
                article.parse()
                
                articles.append({
                    'title': article.title,
                    'url': article.url,
                    'text': article.text,
                    'authors': article.authors,
                    'publish_date': article.publish_date,
                    'top_image': article.top_image,
                    'source': url
                })
            except Exception as e:
                continue
        
        return articles
```

---

## 二、集成架构

### 新的采集流程

```
┌─────────────────────────────────────┐
│  1. 配置新闻源列表                   │
│  - 新浪财经                          │
│  - 东方财富                          │
│  - 政府网站                          │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  2. Newspaper4k 多源并发爬取         │
│  - Source.build() 每个网站           │
│  - 多线程下载文章                    │
│  - 自动提取结构化数据                │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  3. Google新闻补充                   │
│  - 使用现有google_news_crawler       │
│  - 补充关键词搜索结果                │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  4. 数据合并和去重                   │
│  - 合并所有来源                      │
│  - 按URL去重                         │
│  - 保存CSV                           │
└─────────────────────────────────────┘
```

---

**下一部分：具体实施步骤**
