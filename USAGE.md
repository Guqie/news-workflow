# 新闻自动化工作流 - 使用说明

**版本：** v0.2.0-beta  
**更新时间：** 2026-02-06 03:10

---

## 🚀 快速开始

### 一键运行（推荐）
```bash
cd /root/clawd/news-workflow/scripts
./daily_workflow.sh
```

这将自动运行：
1. 医疗健康板块新闻聚合
2. 教育人才板块新闻聚合

---

## 📋 单独运行各个爬虫

### 1. Google 新闻搜索（24小时内）
```bash
# 医疗健康
python3 google_news_crawler.py --sector healthcare --hours 24

# 教育人才
python3 google_news_crawler.py --sector education --hours 24
```

**特点：**
- ✅ 100% 24小时内新闻
- ✅ 50-100条/次
- ✅ 包含来源和发布时间

---

### 2. RSS 新闻爬取
```bash
# 医疗健康
python3 rss_news_crawler.py --sector healthcare

# 教育人才
python3 rss_news_crawler.py --sector education
```

**特点：**
- ✅ 300条/次
- ✅ 实时新闻
- ⚠️ 可能包含旧新闻

---

### 3. 滚动新闻爬取（关键词过滤）
```bash
# 医疗健康
python3 rolling_news_crawler.py --sector healthcare \
  --url "http://www.ce.cn/cysc/newmain/yc/jsxw/" \
  --pages 3

# 教育人才
python3 rolling_news_crawler.py --sector education \
  --url "http://www.ce.cn/cysc/newmain/yc/jsxw/" \
  --pages 3
```

**特点：**
- ✅ 关键词匹配
- ✅ 10-20条/次
- ✅ 匹配率 22-26%

---

### 4. 统一新闻聚合器（推荐）
```bash
# 医疗健康
python3 news_aggregator.py --sector healthcare --hours 24

# 教育人才
python3 news_aggregator.py --sector education --hours 24
```

**特点：**
- ✅ 整合所有新闻源
- ✅ 自动去重
- ✅ 360-420条/次

---

## 📊 查看测试报告

```bash
python3 test_report_generator.py
```

输出示例：
```
【医疗健康板块】
  Google: ✅ 46条
  Rss: ✅ 299条
  Rolling: ✅ 13条
  Aggregated: ✅ 350条
  去重率: 2.2%
```

---

## 📁 输出文件位置

所有新闻数据保存在：
```
/root/clawd/news-workflow/data/raw/
```

文件命名格式：
- `{sector}_google_{date}.json` - Google 新闻
- `{sector}_rss_{date}.json` - RSS 新闻
- `{sector}_rolling_{date}.json` - 滚动新闻
- `{sector}_aggregated_{date}.json` - 聚合结果

---

## ⚙️ 配置文件

配置文件位置：
```
/root/clawd/news-workflow/references/config.json
```

可配置项：
- 关键词列表
- 新闻源列表
- AI 设置
- 爬虫设置

---

## 🔧 故障排查

### 问题1：Google 新闻返回0条
**原因：** 关键词太具体或网络问题  
**解决：** 更换关键词或检查网络

### 问题2：RSS 新闻返回0条
**原因：** RSS 源失效  
**解决：** 更新 RSS 源列表

### 问题3：聚合器运行失败
**原因：** 某个爬虫失败  
**解决：** 单独运行各个爬虫，定位问题

---

**最后更新：** 2026-02-06 03:10
