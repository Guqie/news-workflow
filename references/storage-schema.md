# 数据存储方案

## 一、存储架构

### 1.1 三层存储结构

```
data/
├── raw/              # 原始数据（爬取后未处理）
│   ├── education_20260205.json
│   └── healthcare_20260205.json
│
├── edited/           # 编辑后数据（AI处理后）
│   ├── education_20260205.json
│   └── healthcare_20260205.json
│
└── archive/          # 归档数据（已上传的历史数据）
    ├── 2026/
    │   ├── 02/
    │   │   ├── education_20260205.json
    │   │   └── healthcare_20260205.json
```

### 1.2 设计原则

- **分层存储**: 原始、编辑、归档三层分离
- **日期命名**: 文件名包含日期，便于追溯
- **JSON格式**: 结构化存储，易于处理
- **版本控制**: 保留原始数据，可回溯

---

## 二、数据格式定义

### 2.1 原始数据格式（raw/）


```json
{
  "sector": "education",
  "date": "2026-02-05",
  "source": "rss",
  "total": 15,
  "items": [
    {
      "id": "raw_001",
      "title": "原始标题",
      "content": "原始正文内容...",
      "source_name": "人民网教育频道",
      "source_url": "http://edu.people.com.cn/...",
      "published_time": "2026-02-05 08:30:00",
      "crawled_time": "2026-02-05 09:00:00",
      "keywords_raw": ["教育", "改革"],
      "category": "政策类"
    }
  ]
}
```


### 2.2 编辑后数据格式（edited/）

```json
{
  "sector": "education",
  "date": "2026-02-05",
  "edited_time": "2026-02-05 10:00:00",
  "total": 8,
  "items": [
    {
      "id": "edit_001",
      "raw_id": "raw_001",
      "title_edited": "重写后的标题",
      "title_original": "原始标题",
      "keywords": ["关键词1", "关键词2", "关键词3"],
      "summary": "AI生成的摘要内容...",
      "content_original": "原始正文...",
      "source_name": "人民网教育频道",
      "source_url": "http://...",
      "published_time": "2026-02-05 08:30:00",
      "quality_score": 85,
      "status": "pending_review"
    }
  ]
}
```


### 2.3 字段说明

#### 原始数据字段
- `id`: 唯一标识符
- `title`: 原始标题
- `content`: 原始正文
- `source_name`: 来源网站名称
- `source_url`: 原文链接
- `published_time`: 发布时间
- `crawled_time`: 爬取时间
- `keywords_raw`: 原始关键词
- `category`: 新闻分类

#### 编辑后数据字段
- `raw_id`: 关联原始数据ID
- `title_edited`: AI重写的标题
- `title_original`: 保留原始标题对比
- `keywords`: AI提取的关键词
- `summary`: AI生成的摘要
- `quality_score`: 质量评分（0-100）
- `status`: 状态（pending_review/approved/rejected）


---

## 三、数据库上传格式

### 3.1 上传字段映射

```json
{
  "title": "title_edited",
  "keywords": "keywords (逗号分隔)",
  "summary": "summary",
  "source": "source_name",
  "url": "source_url",
  "date": "published_time",
  "sector": "education/healthcare"
}
```

### 3.2 批量上传格式

```json
{
  "batch_id": "20260205_education",
  "upload_time": "2026-02-05 11:00:00",
  "items": [...]
}
```

---

## 四、数据管理策略

### 4.1 清理策略

- **raw/**: 保留7天后删除
- **edited/**: 上传后移至archive/
- **archive/**: 按月归档，保留1年

### 4.2 备份策略

- 每日自动备份到OneDrive
- 每周完整备份到本地

