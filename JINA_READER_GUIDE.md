# Jina Reader 使用指南

## 📖 什么是 Jina Reader

Jina Reader 是一个 API 服务，可以将任何网页 URL 转换为 LLM 友好的格式（主要是 Markdown）。

**核心价值：**
- 输入：任何网页 URL
- 输出：干净的 Markdown 文本（无广告、无导航、无杂乱 HTML）

## 🔧 工作原理

```
网页URL → Jina Reader API → 清洁的Markdown文本
```

**处理流程：**
1. 接收 URL
2. 爬取网页内容
3. 智能提取正文
4. 清理广告、导航等无关内容
5. 转换为 Markdown 格式
6. 返回结果

## ✨ 核心优势

### 1. 通用性强
- 支持几乎所有网站
- 自动处理 JavaScript 渲染
- 无需为每个网站写规则

### 2. 输出质量高
- 自动识别正文内容
- 保留文章结构（标题、段落）
- 清理广告和无关内容

### 3. 使用简单
- 只需一个 API 调用
- 无需配置
- 返回标准 Markdown

### 4. 稳定可靠
- 官方维护
- 高可用性
- 持续更新

## 🚀 如何使用

### 基础用法

**最简单的方式：**
```bash
# 在URL前加上 r.jina.ai/
curl https://r.jina.ai/https://example.com/article
```

**Python示例：**
```python
import requests

def fetch_with_jina(url):
    jina_url = f"https://r.jina.ai/{url}"
    response = requests.get(jina_url)
    return response.text  # 返回Markdown格式

# 使用示例
url = "https://www.xinhuanet.com/tech/20260211/abc123.html"
content = fetch_with_jina(url)
print(content)
```

### 高级选项

**添加请求头（可选）：**
```python
headers = {
    'X-Return-Format': 'markdown',  # 返回格式
    'X-Timeout': '30',  # 超时时间（秒）
}
response = requests.get(jina_url, headers=headers)
```

## 💰 成本说明

**免费额度：**
- 每天免费调用次数有限
- 适合测试和小规模使用

**付费方案：**
- 按调用次数计费
- 约 $0.001-0.002/次（估算）
- 对于我们的场景：
  - 每天处理100条新闻
  - 成本约 $0.1-0.2/天
  - 月成本约 $3-6

**成本对比：**
- 人工处理：4-6小时/天
- Jina Reader：$0.1-0.2/天
- **性价比极高**

## 📦 在我们项目中的应用

### 集成方案

**场景：**
- 已有1354条新闻标题和URL
- 需要获取完整正文内容

**实现步骤：**

```python
def enrich_news_with_content(news_list):
    """为新闻列表添加正文内容"""
    enriched_news = []
    
    for news in news_list:
        try:
            # 使用Jina Reader获取内容
            jina_url = f"https://r.jina.ai/{news['url']}"
            response = requests.get(jina_url, timeout=30)
            
            if response.status_code == 200:
                news['content'] = response.text
                news['has_content'] = True
            else:
                news['content'] = ''
                news['has_content'] = False
                
        except Exception as e:
            print(f"获取内容失败: {news['url']}, 错误: {e}")
            news['content'] = ''
            news['has_content'] = False
        
        enriched_news.append(news)
    
    return enriched_news
```

### 优化策略

**批量处理：**
- 使用多线程/异步加速
- 设置合理的超时时间
- 失败重试机制

**成本控制：**
- 只对筛选后的新闻获取内容
- 先标题筛选（1354→500）
- 再获取内容（500条）
- 最后深度筛选（500→100）

## ⚖️ 优缺点对比

### 优点
- ✅ 通用性强：支持几乎所有网站
- ✅ 质量高：自动提取正文，清理杂质
- ✅ 简单易用：一行代码搞定
- ✅ 稳定可靠：官方维护
- ✅ 处理JS渲染：无需Selenium

### 缺点
- ❌ 有成本：需要付费（但很便宜）
- ❌ 依赖网络：需要API调用
- ❌ 速度较慢：比直接爬取慢（但可接受）

### 与其他方案对比

| 方案 | 成功率 | 速度 | 成本 | 维护成本 |
|------|--------|------|------|----------|
| Jina Reader | 95%+ | 中 | 低 | 极低 |
| Newspaper4k | 30-50% | 快 | 免费 | 低 |
| BeautifulSoup | 70-80% | 快 | 免费 | 高 |
| Playwright | 95%+ | 慢 | 免费 | 高 |

## 📝 总结和建议

**推荐使用场景：**
- ✅ 需要处理多种不同网站
- ✅ 对内容质量要求高
- ✅ 希望降低维护成本
- ✅ 可以接受少量API成本

**我们项目的建议：**
1. **主力方案**：Jina Reader（处理大部分新闻）
2. **备用方案**：Newspaper4k（免费，处理简单网站）
3. **策略**：先用Newspaper4k尝试，失败则用Jina Reader

**预期效果：**
- 内容获取成功率：95%+
- 每天处理100条新闻
- 成本：$0.1-0.2/天（$3-6/月）
- 时间：节省4-6小时/天

---

**文档创建时间：** 2026-02-11
**下次更新：** 集成完成后更新实际效果