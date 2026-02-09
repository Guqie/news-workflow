# 项目缓存配置

## 项目信息
- **项目名称**: news-workflow (新闻自动化工作流)
- **项目路径**: /root/clawd/news-workflow
- **创建时间**: 2026-02-06
- **负责人**: 小顾姥爷

---

## 项目概述

这是一个自动化新闻收集、编辑和发布的工作流系统。

**核心功能：**
1. 新闻爬虫 - 从多个新闻源自动爬取新闻
2. 内容编辑 - AI 自动改写标题、提取关键词、生成摘要
3. 审核报告 - 生成易于审核的报告
4. 自动推送 - 定时推送到 Telegram

**目标板块：**
- 教育人才（每日 6 条）
- 医疗健康（每日 8 条）

---

## 项目结构

```
news-workflow/
├── scripts/              # 脚本目录
│   ├── enhanced_crawler.py       # 增强版爬虫（专业网站）
│   ├── rolling_news_crawler.py   # 滚动新闻爬虫（关键词过滤）
│   ├── news_editor.py            # 内容编辑器（AI）
│   └── generate_review.py        # 审核报告生成
├── references/           # 配置和参考
│   ├── config.json              # 主配置文件
│   └── sources.md               # 新闻源列表
├── data/                # 数据目录
│   ├── raw/                     # 原始爬取数据
│   └── edited/                  # 编辑后数据
└── SKILL.md             # 技能说明文档
```

---

## 已完成的功能

### ✅ 1. 增强版爬虫 (enhanced_crawler.py)

**支持的新闻源：**
- 健康报行业快讯（JSON 提取）
- 医药网最新资讯
- 北京卫健委
- 中国财经医药滚动新闻
- 国家卫健委（待完善）
- 国家医保局（待完善）

**使用方法：**
```bash
python3 enhanced_crawler.py --sector healthcare --count 10
python3 enhanced_crawler.py --sector education --count 10
```

---

### ✅ 2. 滚动新闻爬虫 (rolling_news_crawler.py)

**核心功能：**
- 关键词过滤（根据板块自动匹配）
- 翻页支持（可爬取多页）
- 多网站支持（人民网、中国经济网等）

**支持的网站：**
- 人民网滚动新闻 ✓
- 中国经济网即时新闻 ✓
- 中国科技网滚动新闻（开发中）
- 中国西藏网即时新闻（开发中）

**使用方法：**
```bash
python3 rolling_news_crawler.py \
  --sector healthcare \
  --url "http://finance.people.com.cn/GB/70846/index.html" \
  --pages 3
```

---

### ⏳ 3. 内容编辑器 (news_editor.py)

**功能：**
- AI 改写标题（去除渲染性词汇）
- 提取关键词（3-5 个专有名词）
- 生成摘要（保留核心信息）

**状态：** 框架已完成，待测试

---

### ⏳ 4. 审核报告生成 (generate_review.py)

**功能：**
- 整理编辑后的新闻
- 生成 Markdown 格式报告
- 便于人工审核

**状态：** 框架已完成，待测试

---

## 配置文件

### config.json

**关键配置：**
- 板块配置（教育人才、医疗健康）
- 关键词列表
- 新闻源配置
- AI 设置（模型、温度、最大 tokens）
- 爬虫设置（超时、重试、User-Agent）

**路径：** `/root/clawd/news-workflow/references/config.json`

---

## 待完成的任务

### 🔲 短期任务（本周）
1. 完善滚动新闻爬虫（添加更多网站支持）
2. 测试内容编辑器
3. 测试审核报告生成
4. 创建自动化脚本（一键运行完整流程）

### 🔲 中期任务（本月）
1. 设置定时任务（cron）
2. Telegram 推送功能
3. 国家卫健委和国家医保局的爬取（浏览器自动化）
4. 错误处理和日志系统

### 🔲 长期优化
1. 数据库存储
2. Web 界面
3. 性能优化
4. 更多新闻源

---

## 技术栈

- **语言**: Python 3
- **爬虫**: requests, BeautifulSoup4
- **AI**: Anthropic Claude API
- **数据格式**: JSON
- **报告格式**: Markdown

---

## 使用说明

### 每日工作流程

1. **爬取新闻**
   ```bash
   cd /root/clawd/news-workflow/scripts
   python3 enhanced_crawler.py --sector healthcare --count 10
   python3 enhanced_crawler.py --sector education --count 10
   ```

2. **编辑内容**
   ```bash
   python3 news_editor.py --input ../data/raw/healthcare_20260206.json
   python3 news_editor.py --input ../data/raw/education_20260206.json
   ```

3. **生成审核报告**
   ```bash
   python3 generate_review.py --date 20260206
   ```

4. **人工审核**
   - 查看 `data/review_20260206.md`
   - 确认新闻质量

5. **发布**
   - 上传到数据库
   - 推送到 Telegram

---

## 注意事项

### 爬虫礼仪
- 每次请求间隔 1-2 秒
- 使用真实的 User-Agent
- 遵守 robots.txt
- 不要过度请求

### 数据质量
- 标题长度：10-100 字符
- 去重：根据标题去重
- 关键词匹配：严格匹配配置的关键词

### 错误处理
- 网络超时：10 秒
- 重试次数：3 次
- 失败记录：保存到日志

---

## 更新日志

### 2026-02-06
- ✅ 创建项目结构
- ✅ 完成增强版爬虫（4 个新闻源）
- ✅ 完成滚动新闻爬虫（关键词过滤 + 翻页）
- ✅ 配置文件和新闻源列表
- ⏳ 内容编辑器（待测试）
- ⏳ 审核报告生成（待测试）

---

**最后更新**: 2026-02-06 03:10
**版本**: v0.2.0-beta

---

## 🌙 夜间迭代更新（2026-02-06 02:57 - 03:10）

### ✅ 新增功能

#### 1. Google 新闻搜索集成
- **文件**: `google_news_crawler.py`
- **功能**: 使用 GNews 库搜索 Google 新闻
- **特点**: 
  - 支持24小时内新闻过滤
  - 支持多关键词搜索
  - 自动去重
- **测试结果**:
  - 医疗健康：46条/次
  - 教育人才：52条/次
  - 时效性：100% 24小时内

#### 2. 统一新闻聚合器
- **文件**: `news_aggregator.py`
- **功能**: 整合所有新闻源
- **包含**:
  - Google 新闻搜索
  - RSS 新闻爬取
  - 滚动新闻爬取
- **特点**:
  - 自动去重
  - 统一输出格式
  - 一键运行

#### 3. 每日自动化脚本
- **文件**: `daily_workflow.sh`
- **功能**: 一键运行完整工作流
- **使用**: `./daily_workflow.sh`

---

## 📊 数据统计（截至 2026-02-06 03:10）

### 新闻获取能力
- **Google 新闻**: 50-100条/板块/天
- **RSS 新闻**: 300条/板块/天
- **滚动新闻**: 10-20条/板块/天
- **总计**: 360-420条/板块/天

### 时效性
- **24小时内新闻**: 100%（Google 新闻）
- **实时新闻**: 支持（RSS）
- **历史新闻**: 支持（滚动新闻）

---

**最后更新**: 2026-02-06 01:45
**版本**: v0.1.0-alpha
