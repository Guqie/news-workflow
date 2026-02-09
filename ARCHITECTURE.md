# 新闻工作流项目架构文档

**版本：** v1.0  
**更新时间：** 2026-02-09  
**维护者：** 哈雷酱

---

## 📋 项目概述

自动化新闻采集、筛选、格式化工作流系统。

**目标：** 将每日4-6小时的手动工作缩短至30分钟。

**覆盖领域：**
- 医疗健康（医药产业、生物医药、医疗健康、医保改革）
- 教育人才（人才政策、教育改革、人才培养、职业教育）

---

## 📁 目录结构

```
news-workflow/
├── scripts/              # 核心脚本目录
│   ├── daily_workflow.sh              # 主入口脚本
│   ├── news_aggregator.py             # 新闻聚合器
│   ├── google_news_crawler.py         # Google新闻爬虫
│   ├── rolling_news_crawler.py        # 滚动新闻爬虫
│   ├── newspaper_crawler.py           # Newspaper4k提取器
│   ├── filter_quality_news.py         # 智能筛选器
│   ├── format_filtered_markdown.py    # Markdown生成器
│   └── [其他辅助脚本]
│
├── data/                 # 数据存储目录
│   └── raw/             # 原始数据和输出
│       ├── healthcare_google_YYYYMMDD.json      # 医疗健康-Google
│       ├── healthcare_rolling_YYYYMMDD.json     # 医疗健康-滚动
│       ├── healthcare_aggregated_YYYYMMDD.json  # 医疗健康-聚合
│       ├── healthcare_filtered_YYYYMMDD.json    # 医疗健康-筛选
│       ├── education_google_YYYYMMDD.json       # 教育人才-Google
│       ├── education_rolling_YYYYMMDD.json      # 教育人才-滚动
│       ├── education_aggregated_YYYYMMDD.json   # 教育人才-聚合
│       ├── education_filtered_YYYYMMDD.json     # 教育人才-筛选
│       └── daily_news_filtered_YYYYMMDD.md      # 最终报告
│
├── references/           # 参考文档目录
│   ├── config.json                    # 配置文件
│   ├── healthcare_titles.md           # 医疗健康标题参考库
│   ├── education_titles.md            # 教育人才标题参考库
│   ├── selection-criteria.md          # 筛选标准
│   └── [其他参考文档]
│
└── 文档文件
    ├── SKILL.md          # 技能说明
    ├── USAGE.md          # 使用说明
    └── ARCHITECTURE.md   # 架构文档（本文件）
```

---

## 🔄 数据流向图

```
[1. 数据采集]
    ↓
Google新闻API → healthcare_google_YYYYMMDD.json (111条)
滚动新闻爬取 → healthcare_rolling_YYYYMMDD.json (14条)
    ↓
[2. 数据聚合]
    ↓
news_aggregator.py → healthcare_aggregated_YYYYMMDD.json (125条)
                   → education_aggregated_YYYYMMDD.json (108条)
    ↓
[3. 智能筛选]
    ↓
filter_quality_news.py → healthcare_filtered_YYYYMMDD.json (11条)
                       → education_filtered_YYYYMMDD.json (12条)
    ↓
[4. 格式化输出]
    ↓
format_filtered_markdown.py → daily_news_filtered_YYYYMMDD.md (23条)
    ↓
[5. 分发]
    ↓
邮件发送 → Guqie1@outlook.com
本地存储 → /root/clawd/news-workflow/data/raw/
OneDrive → (待配置)
```

---

## 🎯 核心模块说明

### 1. 主工作流（daily_workflow.sh）

**功能：** 一键运行完整工作流

**调用顺序：**
```bash
1. news_aggregator.py --sector healthcare --hours 24
2. news_aggregator.py --sector education --hours 24
```

**执行时间：** 约2分钟

---

### 2. 新闻聚合器（news_aggregator.py）

**功能：** 调用各个爬虫，聚合数据

**流程：**
```python
1. run_google_news_crawler()      # Google新闻
2. run_rolling_news_crawler()     # 滚动新闻
3. run_newspaper_crawler()        # Newspaper4k
4. load_all_news()                # 加载数据
5. deduplicate_and_sort()         # 去重排序
6. save_aggregated_results()      # 保存结果
```

**输入：** 无  
**输出：** `{sector}_aggregated_YYYYMMDD.json`

---

### 3. 智能筛选器（filter_quality_news.py）

**功能：** 按照参考标题库标准筛选高质量新闻

**评分维度：**
- 相关性：30分（关键词匹配）
- 权威性：25分（来源可信度）
- 时效性：20分（发布时间）
- 价值性：25分（数据、地区、措施）

**筛选阈值：** ≥60分

**输入：** `{sector}_aggregated_YYYYMMDD.json`  
**输出：** `{sector}_filtered_YYYYMMDD.json`

---

### 4. Markdown生成器（format_filtered_markdown.py）

**功能：** 生成标准格式的markdown报告

**格式：**
```markdown
## 标题

**标题：** xxx
**来源：** xxx
**所属类别：** xxx
**关键词：** xxx
**发布时间：** xxx
**链接：** xxx
**摘要：** xxx
```

**输入：** `{sector}_filtered_YYYYMMDD.json`  
**输出：** `daily_news_filtered_YYYYMMDD.md`

---

## 📊 数据统计

### 典型数据量（每日）

| 阶段 | 医疗健康 | 教育人才 | 总计 |
|------|---------|---------|------|
| 原始采集 | 125条 | 108条 | 233条 |
| 智能筛选 | 11条 | 12条 | 23条 |
| 保留率 | 8.8% | 11.1% | 9.9% |

### 文件大小

| 文件类型 | 大小 |
|---------|------|
| 聚合JSON | 50-130KB |
| 筛选JSON | 8-9KB |
| Markdown报告 | 16-17KB |

---

## ⚙️ 配置文件（references/config.json）

```json
{
  "sectors": {
    "healthcare": {
      "name": "医疗健康",
      "keywords": ["医药产业", "生物医药", "医疗健康", "医保改革"]
    },
    "education": {
      "name": "教育人才",
      "keywords": ["人才政策", "教育改革", "人才培养", "职业教育"]
    }
  }
}
```

---

## 🚀 使用方法

### 快速开始

```bash
# 1. 进入项目目录
cd /root/clawd/news-workflow/scripts

# 2. 运行主工作流
./daily_workflow.sh

# 3. 智能筛选
python3 filter_quality_news.py

# 4. 生成报告
python3 format_filtered_markdown.py

# 5. 发送邮件
mail -s "每日新闻汇总" Guqie1@outlook.com < ../data/raw/daily_news_filtered_YYYYMMDD.md
```

### 单独运行某个模块

```bash
# 只爬取医疗健康
python3 news_aggregator.py --sector healthcare --hours 24

# 只爬取教育人才
python3 news_aggregator.py --sector education --hours 24
```

---

## 🔧 待优化项

1. **关键词提取** - 集成AI自动提取
2. **OneDrive同步** - 配置自动同步
3. **数据库上传** - 开发API接口
4. **定时任务** - 设置cron自动运行

---

## 📝 更新日志

### v1.0 (2026-02-09)
- ✅ 禁用RSS爬取（过滤旧新闻）
- ✅ 实现智能筛选（保留率10%）
- ✅ 生成markdown格式报告
- ✅ 邮件自动发送

---

**文档结束**
