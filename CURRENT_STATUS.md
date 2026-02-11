## 🎯 核心脚本说明

### 主采集器（news_aggregator.py）
- **功能**：多源新闻聚合的核心引擎
- **流程**：
  1. run_google_news_crawler() - Google新闻采集
  2. run_rolling_news_crawler() - 滚动新闻采集
  3. run_newspaper_crawler() - 深度内容提取
  4. load_all_news() - 加载所有数据
  5. deduplicate_and_sort() - 去重排序
  6. save_aggregated_results() - 保存结果

### 工具脚本
- **quick_news_fetcher.py**：快速采集（单一来源）
- **convert_json_to_csv.py**：格式转换工具
- **test_optimized_config.py**：配置测试工具

## 📋 配置文件结构（config.json）

```json
{
  "sectors": {
    "strategic_emerging": {
      "keywords": [30+个关键词],
      "news_sources": [9个信源]
    },
    "hightech": {
      "keywords": [30+个关键词],
      "news_sources": [9个信源]
    }
  },
  "filter_criteria": {
    "categories": [7类筛选标准],
    "exclude_keywords": [排除关键词]
  }
}
```

## 📈 当前状态

**采集能力：**
- 战略新兴产业：737条/次
- 高科技产业：617条/次
- 总计：1300+条/次

**信源配置：**
- 科创板日报、财联社、东方财富网等9个财经媒体
- Google新闻RSS
- 多个政府和门户网站

**优化成果：**
- ✅ 关键词优化（30+个新关键词）
- ✅ 排除过滤（新能源汽车、风电等）
- ✅ 7类筛选标准
- ✅ 自动化上传OneDrive
