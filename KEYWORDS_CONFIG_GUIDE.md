# 关键词配置说明

## 📁 配置文件位置
`/root/clawd/news-workflow/config/keywords_config.json`

## 📝 配置结构

```json
{
  "exclude_keywords": [...],    // 排除关键词（股票类）
  "exclude_domains": [...],     // 排除领域
  "include_keywords": [...]     // 必须包含关键词
}
```

## 🔧 如何修改

### 1. 编辑配置文件
```bash
nano /root/clawd/news-workflow/config/keywords_config.json
```

### 2. 添加/删除关键词
直接在对应数组中添加或删除关键词

### 3. 测试效果
```bash
cd /root/clawd/news-workflow/scripts
python3 test_keyword_filter.py
```

## 💡 建议补充的关键词

### include_keywords（建议添加）：
- "产业链", "供应链", "产业集群"
- "低空经济", "通用航空"
- "工业互联网", "智慧城市"
- "产业基金", "产业投资"
- "技术创新", "科技创新"
- "数字化转型", "智能化"
