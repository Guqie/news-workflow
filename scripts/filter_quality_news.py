#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能筛选高质量新闻
根据参考标题库的标准，过滤出符合要求的新闻
"""

import json
import re
from pathlib import Path
from datetime import datetime

class NewsFilter:
    """新闻质量筛选器"""
    
    def __init__(self):
        # 必选关键词（高优先级）
        self.must_include_keywords = {
            'healthcare': [
                # 政策类
                '政策', '发布', '出台', '印发', '通知', '意见', '方案', '规划',
                '医保局', '卫健委', '药监局', '国家', '省', '市',
                # 产业类
                '产业', '发展', '建设', '推进', '启动', '落地', '投入运行',
                '基金', '投资', '融资', '上市', '获批',
                # 改革类
                '改革', '创新', '试点', '示范', '联盟', '平台',
            ],
            'education': [
                # 政策类
                '政策', '发布', '出台', '印发', '通知', '意见', '方案', '规划',
                '教育部', '教育厅', '教育局', '国家', '省', '市',
                # 人才类
                '人才', '引进', '培养', '招聘', '就业', '创业',
                # 教育类
                '高校', '大学', '学院', '职业教育', '招生', '考试',
                '改革', '创新', '试点', '示范', '联盟', '平台',
            ]
        }
        
        # 排除关键词（低质量标志）
        self.exclude_keywords = [
            # 投资理财类
            'ETF', '股票', '基金份额', '涨停', '跌停', '行情', '板块机会',
            '投资机会', '买入', '卖出', '持仓', '收益',
            # 企业宣传类
            '签约仪式', '圆满举行', '隆重召开', '盛大开幕',
            '献唱', '礼赞', '慰问', '走访',
            # 娱乐八卦类
            '明星', '网红', '直播', '带货',
        ]
        
        # 权威来源（加分）
        self.authority_sources = [
            '人民网', '新华网', '央视网', '中国政府网',
            '健康报', '医药经济报', '中国教育报',
            '财新', '第一财经', '经济日报',
        ]
    
    def calculate_score(self, news_item, sector):
        """计算新闻质量分数"""
        title = news_item.get('title', '')
        source = news_item.get('source', '')
        
        score = 0
        reasons = []
        
        # 1. 检查排除关键词（直接淘汰）
        for keyword in self.exclude_keywords:
            if keyword in title:
                return 0, [f"包含排除关键词: {keyword}"]
        
        # 2. 检查必选关键词（相关性 30分）
        keyword_count = 0
        matched_keywords = []
        for keyword in self.must_include_keywords.get(sector, []):
            if keyword in title:
                keyword_count += 1
                matched_keywords.append(keyword)
        
        if keyword_count > 0:
            relevance_score = min(30, keyword_count * 10)
            score += relevance_score
            reasons.append(f"相关性: {relevance_score}分 (匹配: {', '.join(matched_keywords[:3])})")
        else:
            return 0, ["相关性不足"]
        
        # 3. 权威性评分（25分）
        authority_score = 0
        if any(auth in source for auth in self.authority_sources):
            authority_score = 25
            reasons.append(f"权威来源: {authority_score}分")
        elif '政府' in source or '官网' in source:
            authority_score = 20
            reasons.append(f"官方来源: {authority_score}分")
        else:
            authority_score = 10
            reasons.append(f"一般来源: {authority_score}分")
        score += authority_score
        
        # 4. 时效性评分（20分）
        # 这里简化处理，假设都是24小时内
        time_score = 20
        score += time_score
        reasons.append(f"时效性: {time_score}分")
        
        # 5. 价值性评分（25分）
        value_score = 0
        # 包含数据
        if re.search(r'\d+%|\d+亿|\d+万', title):
            value_score += 10
            reasons.append("包含数据")
        # 包含地区
        if re.search(r'北京|上海|广东|浙江|江苏|山东|河南|四川|湖北|湖南|福建|安徽|河北|陕西|重庆|天津|辽宁|吉林|黑龙江|山西|江西|贵州|云南|甘肃|青海|宁夏|新疆|西藏|广西|内蒙古|海南', title):
            value_score += 10
            reasons.append("包含地区")
        # 包含具体措施
        if any(word in title for word in ['推进', '启动', '落地', '建设', '发展', '改革', '创新']):
            value_score += 5
            reasons.append("包含具体措施")
        score += value_score
        
        return score, reasons
    
    def filter_news(self, news_list, sector, threshold=60):
        """筛选新闻"""
        filtered_news = []
        
        for news in news_list:
            score, reasons = self.calculate_score(news, sector)
            
            if score >= threshold:
                news['quality_score'] = score
                news['filter_reasons'] = reasons
                filtered_news.append(news)
        
        # 按分数排序
        filtered_news.sort(key=lambda x: x['quality_score'], reverse=True)
        
        return filtered_news

def main():
    """主函数"""
    filter_obj = NewsFilter()
    
    # 数据文件路径
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    date_str = datetime.now().strftime("%Y%m%d")
    
    # 处理医疗健康
    healthcare_file = data_dir / f"healthcare_aggregated_{date_str}.json"
    if healthcare_file.exists():
        with open(healthcare_file, 'r', encoding='utf-8') as f:
            healthcare_data = json.load(f)
        
        filtered_healthcare = filter_obj.filter_news(healthcare_data, 'healthcare', threshold=60)
        
        output_file = data_dir / f"healthcare_filtered_{date_str}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_healthcare, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 医疗健康: {len(healthcare_data)} → {len(filtered_healthcare)} 条")
        print(f"   保存到: {output_file}")
    
    # 处理教育人才
    education_file = data_dir / f"education_aggregated_{date_str}.json"
    if education_file.exists():
        with open(education_file, 'r', encoding='utf-8') as f:
            education_data = json.load(f)
        
        filtered_education = filter_obj.filter_news(education_data, 'education', threshold=60)
        
        output_file = data_dir / f"education_filtered_{date_str}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_education, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 教育人才: {len(education_data)} → {len(filtered_education)} 条")
        print(f"   保存到: {output_file}")

if __name__ == "__main__":
    main()
