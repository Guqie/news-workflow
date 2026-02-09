---
name: news-workflow
description: Automate daily news collection, editing, and upload workflow for education/talent and healthcare/medical sectors. Use when you need to (1) collect news from specified sources, (2) edit titles and extract keywords, (3) generate summaries, (4) prepare content for database upload. Handles 6+ education news and 8+ healthcare news daily.
---

# News Workflow Automation

Automate the daily news collection and processing workflow for education/talent and healthcare/medical sectors.

## Overview

This skill automates the complete workflow for maintaining the industry database:
- **Education & Talent**: Minimum 6 news items daily
- **Healthcare & Medical**: Minimum 8 news items daily

## Workflow Steps

### 1. News Collection

Collect news from configured sources using the crawler script:

```bash
python3 scripts/news_crawler.py --sector education --count 10
python3 scripts/news_crawler.py --sector healthcare --count 12
```

The crawler will:
- Fetch news from RSS feeds and news sites
- Filter by relevance and date
- Save raw data to `data/raw/`


### 2. Content Editing

Process collected news with AI editing:

```bash
python3 scripts/news_editor.py --input data/raw/education_YYYYMMDD.json
```

The editor will:
- Rewrite titles (remove clickbait, make concise)
- Extract keywords (proper nouns, domain-specific terms)
- Generate summaries (remove redundancy, keep core info)
- Save edited content to `data/edited/`

**Editing Standards:**
- Titles: Accurate, concise, declarative
- Keywords: Proper nouns, no phrases
- Summaries: Core information only, no promotional content


### 3. Review and Upload

Review edited content and prepare for upload:

```bash
python3 scripts/generate_review.py --date YYYYMMDD
```

This generates a review file with all edited news for manual inspection.

**Manual Review Checklist:**
- Verify title accuracy
- Check keyword relevance
- Confirm summary completeness
- Validate source credibility


### 4. Database Upload (Semi-automated)

After review, upload to the industry database:

```bash
python3 scripts/upload_to_db.py --file data/edited/education_YYYYMMDD.json
```

**Note:** Full automation requires database credentials. Current version generates upload-ready format for manual submission.

## Configuration

Edit `references/config.json` to customize:
- News sources (RSS feeds, websites)
- Keywords for filtering
- AI model settings
- Database connection (optional)

See [references/sources.md](references/sources.md) for detailed source configuration.


## Quick Start

Run the complete daily workflow:

```bash
# 1. Collect news
python3 scripts/news_crawler.py --sector education --count 10
python3 scripts/news_crawler.py --sector healthcare --count 12

# 2. Edit content
python3 scripts/news_editor.py --input data/raw/education_*.json
python3 scripts/news_editor.py --input data/raw/healthcare_*.json

# 3. Generate review
python3 scripts/generate_review.py --date $(date +%Y%m%d)

# 4. Review and upload (manual step)
```

## Time Savings

- **Before automation**: 4-5 hours daily
- **After automation**: ~1 hour daily (30min review + 30min upload)
- **Time saved**: 75%

