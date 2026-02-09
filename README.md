# 新闻自动化工作流系统

自动化新闻采集、筛选、格式化工作流系统，专注于医疗健康和教育人才领域。

## 📋 项目简介

将每日4-6小时的手动新闻检索工作缩短至30分钟，效率提升85-90%。

**覆盖领域：**
- 🏥 医疗健康（医药产业、生物医药、医疗健康、医保改革）
- 🎓 教育人才（人才政策、教育改革、人才培养、职业教育）

## ✨ 核心功能

- ✅ 自动采集：Google新闻 + 滚动新闻
- ✅ 智能筛选：AI评分系统，保留率10%
- ✅ 格式化输出：标准markdown格式
- ✅ 邮件发送：自动推送到邮箱

## 🚀 快速开始

```bash
# 1. 进入项目目录
cd news-workflow/scripts

# 2. 运行完整工作流
./daily_workflow.sh

# 3. 智能筛选
python3 filter_quality_news.py

# 4. 生成报告
python3 format_filtered_markdown.py
```

## 📊 效率对比

| 模式 | 时间 | 说明 |
|------|------|------|
| 手动 | 4.5-6.5小时/天 | 检索、筛选、整理、上传 |
| 自动化 | 35分钟/天 | 运行脚本 + 人工审核 |
| **提升** | **85-90%** | 节省4-6小时/天 |

## 📁 项目结构

```
news-workflow/
├── scripts/          # 核心脚本
├── data/raw/         # 数据存储
├── references/       # 参考文档
└── ARCHITECTURE.md   # 架构文档
```

## 📖 文档

- [架构文档](ARCHITECTURE.md) - 完整的项目架构说明
- [使用说明](USAGE.md) - 详细的使用指南
- [技能说明](SKILL.md) - Clawdbot技能集成

## 🔧 依赖

```bash
pip install requests beautifulsoup4 feedparser newspaper3k
```

## 📝 更新日志

### v1.0 (2026-02-09)
- ✅ 禁用RSS爬取（过滤旧新闻）
- ✅ 实现智能筛选（保留率10%）
- ✅ 生成markdown格式报告
- ✅ 邮件自动发送

## 📄 License

MIT License

## 👤 作者

顾姥爷 - 智库助理研究员
