#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大模型精细筛选模块
"""

import json
import requests

class LLMFilter:
    """大模型筛选器"""
    
    def __init__(self, model="claude-opus-4-5"):
        """初始化"""
        self.model = model
        self.api_url = "https://code.newcli.com/claude/droid/v1/messages"
        self.api_key = "sk-ant-oat01-ZVDyB76jYE8S1CXE9tLXXhbF_cnTU4Lu5PQ6BXeBJCYq4cOMqWXSs3-SXYJzGOBgv8DxuMX3VplIKWSnUw_2LRBTfmV4CAA"
        
        print(f"初始化LLM客户端:")
        print(f"  模型: {self.model}")
        print(f"  API URL: {self.api_url}")
        
        # 系统提示词
        self.system_prompt = """你是一个新闻质量评估专家，专注于战略新兴产业和高科技产业领域。

你的任务是判断新闻是否值得保留用于智库研究。

【保留标准】
1. 政策动态（国家部委、地方政府产业政策、产业集群）
2. 龙头企业动态（重大投融资、战略合作、技术突破）
3. 重大技术突破（商业化应用、全球/全国首创）
4. 产业趋势分析（行业发展、市场规模、产业链）
5. 重点数据（市场规模、增长率、产能产量）

【排除标准】
1. 软文/广告/推广内容
2. 标题党/低质量内容
3. 纯粹的股市分析/投资建议
4. 与战略新兴产业/高科技无关

【判断原则】
- 宁可多保留，不要漏掉重要信息
- 有疑问时倾向于保留
- 理由简短明确（5-10字）"""
    
    def filter_all(self, news_list, batch_size=50):
        """分批处理所有新闻"""
        total = len(news_list)
        all_filtered = []
        all_results = []
        
        print(f"\n将分{(total + batch_size - 1) // batch_size}批处理，每批{batch_size}条")
        
        for batch_idx in range(0, total, batch_size):
            batch = news_list[batch_idx:batch_idx + batch_size]
            batch_num = batch_idx // batch_size + 1
            total_batches = (total + batch_size - 1) // batch_size
            
            print(f"\n处理第{batch_num}/{total_batches}批（{len(batch)}条）...")
            
            filtered, stats, results = self._filter_batch(batch, batch_idx)
            all_filtered.extend(filtered)
            all_results.extend(results)
        
        # 汇总统计
        final_stats = {
            'total': total,
            'kept': len(all_filtered),
            'excluded': total - len(all_filtered),
            'reasons': {}
        }
        
        for result in all_results:
            if not result['keep']:
                reason = result['reason']
                final_stats['reasons'][reason] = final_stats['reasons'].get(reason, 0) + 1
        
        print(f"\n总体筛选结果:")
        print(f"  原始数量: {final_stats['total']}")
        print(f"  保留: {final_stats['kept']}")
        print(f"  排除: {final_stats['excluded']}")
        
        return all_filtered, final_stats, all_results
    
    def _filter_batch(self, news_list, offset=0):
        """处理单批新闻"""
        # 构造输入数据
        input_data = []
        for i, news in enumerate(news_list):
            input_data.append({
                "id": offset + i + 1,
                "title": news.get('title', ''),
                "source": news.get('source', '')
            })
        
        # 构造用户提示词
        user_prompt = f"""请判断以下新闻列表中每条新闻是否值得保留。

新闻列表：
{json.dumps(input_data, ensure_ascii=False, indent=2)}

请返回JSON数组，格式如下：
[
  {{"id": 1, "keep": true, "reason": "政策动态"}},
  {{"id": 2, "keep": false, "reason": "软文广告"}},
  ...
]

要求：
1. 必须返回所有新闻的判断结果
2. id必须与输入一致
3. reason简短说明（5-10字）
4. 只返回JSON数组，不要其他内容"""
        
        # 调用大模型
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "max_tokens": 8192,
            "system": self.system_prompt,
            "messages": [{"role": "user", "content": user_prompt}]
        }
        
        response = requests.post(self.api_url, headers=headers, json=payload, timeout=180)
        
        if response.status_code != 200:
            print(f"API调用失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return news_list, {}, []
        
        result = response.json()
        result_text = result['content'][0]['text']
        
        # 解析结果
        return self.parse_result(result_text, news_list)
    
    def parse_result(self, result_text, news_list):
        """解析大模型返回的结果"""
        try:
            # 提取JSON数组
            result_text = result_text.strip()
            if result_text.startswith('```'):
                # 移除markdown代码块标记
                lines = result_text.split('\n')
                result_text = '\n'.join(lines[1:-1])
            
            results = json.loads(result_text)
            
            # 统计
            filtered = []
            stats = {
                'total': len(news_list),
                'kept': 0,
                'excluded': 0,
                'reasons': {}
            }
            
            for result in results:
                idx = result['id'] - 1
                if result['keep']:
                    filtered.append(news_list[idx])
                    stats['kept'] += 1
                else:
                    stats['excluded'] += 1
                    reason = result['reason']
                    stats['reasons'][reason] = stats['reasons'].get(reason, 0) + 1
            
            print(f"\n大模型筛选结果:")
            print(f"  原始数量: {stats['total']}")
            print(f"  保留: {stats['kept']}")
            print(f"  排除: {stats['excluded']}")
            print(f"  排除原因分布:")
            for reason, count in stats['reasons'].items():
                print(f"    - {reason}: {count}")
            
            return filtered, stats, results
            
        except Exception as e:
            print(f"解析结果失败: {e}")
            print(f"原始返回: {result_text[:500]}")
            return news_list, {}, []
