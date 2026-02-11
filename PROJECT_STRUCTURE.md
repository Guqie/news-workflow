# 项目架构总结

## 📁 项目结构

```
news-workflow/
├── scripts/              # 核心脚本目录
│   ├── news_aggregator.py          # 主采集器（多源聚合）
│   ├── google_news_crawler.py      # Google新闻爬虫
│   ├── rolling_news_crawler.py     # 滚动新闻爬虫
│   ├── newspaper_crawler.py        # Newspaper4k深度提取
│   ├── quick_news_fetcher.py       # 快速采集工具
│   ├── convert_json_to_csv.py      # 格式转换工具
│   └── test_optimized_config.py    # 配置测试工具
│
├── data/                 # 数据存储目录
│   └── raw/             # 原始数据（JSON + CSV）
│
├── references/          # 配置和参考文档
│   ├── config.json                 # 核心配置文件
│   ├── 高科技战略新兴产业工作交接.docx  # 工作交接文档
│   └── *.md                        # 各类参考文档
│
└── *.md                 # 项目文档
    ├── README.md                   # 项目说明
    ├── ARCHITECTURE.md             # 架构文档
    └── USAGE.md                    # 使用指南
```

## 🏗️ 核心架构

### 1. 数据采集层
- **Google新闻爬虫**：基于RSS的快速采集
- **滚动新闻爬虫**：从财经媒体网站爬取
- **Newspaper4k爬虫**：深度内容提取

### 2. 数据处理层
- **聚合器**：合并多源数据，去重排序
- **格式转换**：JSON → CSV
- **筛选过滤**：基于7类标准筛选

### 3. 数据输出层
- **CSV导出**：标准格式输出
- **OneDrive上传**：自动云端同步

## 🔄 数据流向

```
配置文件(config.json)
    ↓
采集器启动
    ↓
多源并行采集 → [Google新闻] [滚动新闻] [Newspaper4k]
    ↓
数据聚合 → 去重 → 排序
    ↓
JSON存储 → CSV转换
    ↓
OneDrive上传
```
