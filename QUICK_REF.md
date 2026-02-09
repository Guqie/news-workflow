# 快速参考 - 新闻自动化工作流

## 🚀 常用命令

### 爬取新闻
```bash
cd /root/clawd/news-workflow/scripts

# 医疗健康板块
python3 enhanced_crawler.py --sector healthcare --count 10

# 教育人才板块
python3 enhanced_crawler.py --sector education --count 10

# 滚动新闻（关键词过滤）
python3 rolling_news_crawler.py --sector healthcare \
  --url "http://finance.people.com.cn/GB/70846/index.html" \
  --pages 3
```

### 编辑内容
```bash
# 编辑医疗健康新闻
python3 news_editor.py --input ../data/raw/healthcare_20260206.json

# 编辑教育人才新闻
python3 news_editor.py --input ../data/raw/education_20260206.json
```

### 生成审核报告
```bash
python3 generate_review.py --date 20260206
```

---

## 📊 新闻源列表

### 医疗健康板块
1. 健康报行业快讯 - https://www.jkb.com.cn/news/industryNews
2. 医药网最新资讯 - https://news.pharmnet.com.cn/news/hyyw/news/index0.html
3. 北京卫健委 - https://wjw.beijing.gov.cn/sy_20013/
4. 中国财经医药滚动 - https://finance.china.com.cn/industry/medicine/live.shtml

### 教育人才板块
1. 人民网教育 - http://edu.people.com.cn/GB/1053/index.html
2. 科学网 - https://news.sciencenet.cn/

### 滚动新闻（通用）
1. 人民网滚动 - http://finance.people.com.cn/GB/70846/index.html
2. 中国经济网即时 - http://www.ce.cn/cysc/newmain/yc/jsxw/
3. 中国科技网滚动 - https://www.stdaily.com/web/gdxw/node_324_2.html

---

## 🔑 关键词配置

### 医疗健康
医疗、健康、医药、生物医药、医院、医疗器械、健康产业、医保

### 教育人才
教育、人才、高校、职业教育、培训、招聘、就业、人才政策

---

## 📁 文件路径

- 配置文件: `/root/clawd/news-workflow/references/config.json`
- 原始数据: `/root/clawd/news-workflow/data/raw/`
- 编辑数据: `/root/clawd/news-workflow/data/edited/`
- 审核报告: `/root/clawd/news-workflow/data/review_*.md`

---

## ⚠️ 注意事项

1. 每次爬取间隔 1-2 秒
2. 标题长度：10-100 字符
3. 自动去重
4. 关键词严格匹配
