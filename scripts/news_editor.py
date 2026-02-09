#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻编辑器脚本
使用AI对新闻进行标题重写、关键词提取、摘要生成
"""

import argparse
import json
import os
from anthropic import Anthropic

class NewsEditor:
    def __init__(self, input_file):
        self.input_file = input_file
        self.config = self.load_config()
        self.client = Anthropic()
        
    def load_config(self):
        """加载配置"""
        config_path = os.path.join(os.path.dirname(__file__), '../references/config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def edit_news(self, news_item):
        """使用AI编辑单条新闻"""
        prompt = f"""
请对以下新闻进行编辑：

原标题：{news_item.get('title', '')}
原内容：{news_item.get('content', '')}

要求：
1. 重写标题：去除渲染性词汇，改为准确、简练的陈述性标题
2. 提取关键词：3-5个专有名词，不使用短语
3. 生成摘要：保留核心信息，删除冗余和宣传性内容

请以JSON格式返回：
{{
  "title": "重写后的标题",
  "keywords": ["关键词1", "关键词2", "关键词3"],
  "summary": "摘要内容"
}}
"""
        
        try:
            response = self.client.messages.create(
                model=self.config['ai_settings']['model'],
                max_tokens=self.config['ai_settings']['max_tokens'],
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = json.loads(response.content[0].text)
            return result
            
        except Exception as e:
            print(f"✗ 编辑失败: {e}")
            return None
    
    def process_all(self):
        """处理所有新闻"""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            news_list = json.load(f)
        
        edited_list = []
        for i, news in enumerate(news_list, 1):
            print(f"处理中 {i}/{len(news_list)}...")
            edited = self.edit_news(news)
            if edited:
                edited['source'] = news.get('source', '')
                edited['url'] = news.get('url', '')
                edited['date'] = news.get('date', '')
                edited_list.append(edited)
        
        return edited_list

def main():
    parser = argparse.ArgumentParser(description='新闻编辑器')
    parser.add_argument('--input', required=True, help='输入文件路径')
    args = parser.parse_args()
    
    editor = NewsEditor(args.input)
    results = editor.process_all()
    
    # 保存结果
    output_file = args.input.replace('raw', 'edited')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 已保存到: {output_file}")

if __name__ == '__main__':
    main()
