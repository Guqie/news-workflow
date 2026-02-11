# 新闻工作流异步优化规划

## 一、当前问题分析

### 1.1 工作流程问题

**当前流程：**
```
新闻聚合（700+条）
  ↓
内容提取（700+条，耗时5-10分钟）← 问题所在
  ↓
去重保存
  ↓
关键词筛选（300+条）
  ↓
质量筛选（200+条）
  ↓
大模型筛选（100+条）
```

**问题：**
- 在聚合阶段提取所有新闻内容（700+条）
- 大量无关新闻也被提取内容，浪费时间
- 导致聚合阶段耗时过长（10-15分钟）

### 1.2 异步实现问题

**当前异步实现：**
- 只在新闻聚合阶段实现了并行（3个爬虫）
- 但效果不明显（Google搜索占用大部分时间）
- 没有系统的异步架构

---

## 二、优化方案

### 2.1 调整工作流程

**优化后流程：**
```
新闻聚合（700+条，只收集标题+链接）
  ↓
去重（600+条）
  ↓
关键词筛选（300+条）
  ↓
质量筛选（200+条）
  ↓
内容提取（200+条）← 移到这里
  ↓
大模型筛选（100+条）
```

**优势：**
- 只提取筛选后的新闻内容（200+条 vs 700+条）
- 减少70%的内容提取工作量
- 聚合阶段耗时从10-15分钟降到3-5分钟

### 2.2 异步实现架构

**三层异步架构：**

**第一层：新闻聚合（并行）**
```
Google搜索（20个关键词）
  ↓ 并行
通用爬虫（5个新闻源）
  ↓ 并行
Newspaper4k（4个新闻源）
```

**第二层：内容提取（批量并行）**
```
筛选后的200+条新闻
  ↓
分批（每批50条）
  ↓
并行提取（10个worker）
```

**第三层：大模型筛选（批量并行）**
```
提取内容后的200+条新闻
  ↓
分批（每批100条）
  ↓
并行调用大模型（3个批次）
```

---

## 三、实施步骤

### 3.1 第一阶段：修复工作流程（优先）

**任务：**
1. 移除news_aggregator.py中的内容提取步骤
2. 创建独立的内容提取脚本（content_extractor_pipeline.py）
3. 在筛选后调用内容提取

**预期效果：**
- 聚合阶段耗时：10-15分钟 → 3-5分钟
- 总体耗时：15-20分钟 → 8-12分钟

### 3.2 第二阶段：优化Google搜索（重要）

**问题：**
- Google搜索是最耗时的环节（20个关键词，顺序执行）
- 每个关键词需要1-2秒

**优化方案：**
- 将20个关键词分批并行搜索
- 使用ThreadPoolExecutor（5个worker）
- 预期耗时：40秒 → 10秒

### 3.3 第三阶段：完善异步架构（长期）

**任务：**
1. 统一异步接口
2. 添加进度监控
3. 错误处理和重试机制
4. 性能监控和日志

---

## 四、技术方案

### 4.1 修改news_aggregator.py

**移除内容提取：**
```python
def run(self, parallel=True):
    # 1. 并行运行所有爬虫
    if parallel:
        self.run_all_crawlers_parallel()
    else:
        # 顺序执行
        ...
    
    # 2. 加载所有新闻
    self.load_all_news()
    
    # 3. 去重
    self.deduplicate_and_sort()
    
    # 4. 保存聚合结果（不提取内容）
    self.save_aggregated_results()
    
    # ❌ 移除内容提取步骤
    # extractor = NewsContentExtractor(max_workers=10)
    # self.all_news = extractor.process_news_list_async(self.all_news)
```

### 4.2 创建独立的内容提取脚本

**content_extractor_pipeline.py：**
```python
def extract_content_for_filtered_news(input_file, output_file):
    """为筛选后的新闻提取内容"""
    # 1. 读取筛选后的新闻
    news_list = load_json(input_file)
    
    # 2. 批量并行提取内容
    extractor = NewsContentExtractor(max_workers=10)
    news_with_content = extractor.process_news_list_async(news_list)
    
    # 3. 保存结果
    save_json(output_file, news_with_content)
```

### 4.3 优化Google搜索

**google_news_crawler.py：**
```python
def search_keywords_parallel(keywords, hours=24):
    """并行搜索多个关键词"""
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(search_single_keyword, kw, hours): kw 
            for kw in keywords
        }
        
        all_results = []
        for future in as_completed(futures):
            results = future.result()
            all_results.extend(results)
    
    return all_results
```

---

## 五、预期效果

### 5.1 性能提升

**当前性能：**
- 新闻聚合：10-15分钟
- 筛选流程：1-2分钟
- 内容提取：（已包含在聚合中）
- 大模型筛选：2-3分钟
- **总计：13-20分钟**

**优化后性能：**
- 新闻聚合：3-5分钟（移除内容提取）
- 筛选流程：1-2分钟
- 内容提取：2-3分钟（只提取200+条）
- 大模型筛选：2-3分钟
- **总计：8-13分钟**

**提升：** 约40%

### 5.2 资源优化

**当前：**
- 提取700+条新闻内容
- 大量无关新闻浪费资源

**优化后：**
- 只提取200+条筛选后的新闻
- 减少70%的网络请求
- 减少70%的内容提取时间

---

## 六、实施优先级

**P0（立即执行）：**
1. 移除news_aggregator.py中的内容提取
2. 测试聚合速度是否提升

**P1（本周完成）：**
1. 创建独立的内容提取脚本
2. 优化Google搜索（并行）
3. 完整测试工作流程

**P2（下周完成）：**
1. 完善异步架构
2. 添加进度监控
3. 错误处理和重试

---

**文档创建时间：** 2026-02-12 02:42
