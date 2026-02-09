#!/bin/bash
# 每日新闻自动化工作流

echo "=========================================="
echo "每日新闻自动化工作流"
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

cd /root/clawd/news-workflow/scripts

# 1. 医疗健康板块
echo ""
echo "📰 开始爬取医疗健康新闻..."
python3 news_aggregator.py --sector healthcare --hours 24

# 2. 教育人才板块
echo ""
echo "📰 开始爬取教育人才新闻..."
python3 news_aggregator.py --sector education --hours 24

echo ""
echo "=========================================="
echo "✅ 所有任务完成！"
echo "结束时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
