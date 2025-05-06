"""
谐音工坊 (PunCraft) LLM API调用工具函数

本模块提供与DeepSeek等大语言模型API交互的函数，用于生成谐音创意内容。
"""

import json
from typing import Any, Dict, List, Optional, Union

import openai


def get_openai_client(api_key: str, base_url: str = "https://api.deepseek.com/v1") -> openai.OpenAI:
    """
    初始化OpenAI客户端，配置为使用DeepSeek API
    
    Args:
        api_key: DeepSeek API密钥
        base_url: DeepSeek API基础URL
        
    Returns:
        配置好的OpenAI客户端实例
    """
    return openai.OpenAI(
        api_key=api_key,
        base_url=base_url
    )


def generate_brand_names(
    api_key: str,
    keyword: str,
    industry: str = "",
    positioning: str = "",
    style: List[str] = None,
    model: str = "deepseek-reasoner",
    temperature: float = 0.7,
    max_tokens: int = 1024
) -> Dict[str, Any]:
    """
    生成品牌谐音创意名称
    
    Args:
        api_key: DeepSeek API密钥
        keyword: 品牌关键词
        industry: 所属行业
        positioning: 品牌定位/描述
        style: 品牌风格列表，如["有趣幽默", "高端大气"]
        model: 使用的模型名称
        temperature: 生成多样性参数
        max_tokens: 最大生成token数
        
    Returns:
        包含生成结果的字典，包括多个品牌名称建议及其解析
    """
    client = get_openai_client(api_key)
    
    # 构建风格描述
    style_text = "、".join(style) if style else "无特定风格要求"
    
    # 构建提示词
    system_prompt = """你是一位品牌命名专家，精通中文谐音创意。你的任务是根据用户提供的关键词、行业和风格要求，生成富有创意的谐音品牌名称。
你需要提供多个谐音方案，每个方案都应包含谐音解析和寓意说明。确保你的回复是JSON格式，便于程序处理。"""

    user_prompt = f"""请为我生成品牌谐音创意名称，满足以下条件：
- 品牌关键词：{keyword}
- 所属行业：{industry}
- 品牌定位：{positioning}
- 期望风格：{style_text}

请生成至少3个不同的谐音名称方案，确保结果为以下JSON格式：
```json
{{
  "brand_names": [
    {{
      "name": "品牌名称1",
      "rating": 5,
      "slogan": "品牌口号/简介",
      "pun_explanation": "谐音解析，说明这个名字的谐音来源",
      "meaning": "品牌名称的寓意说明"
    }},
    {{
      "name": "品牌名称2",
      "rating": 4,
      "slogan": "品牌口号/简介",
      "pun_explanation": "谐音解析，说明这个名字的谐音来源",
      "meaning": "品牌名称的寓意说明"
    }},
    ...
  ],
  "other_candidates": [
    {{
      "name": "候选名称1",
      "pun_explanation": "谐音解析简述"
    }},
    ...
  ]
}}
```

请注意：
1. 创建的名称必须包含谐音元素，与原关键词或行业相关
2. 根据品牌风格需求调整创意风格
3. 保持名称简洁易记
4. rating评分从1到5，表示你对该名称的推荐程度"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {
            "error": True,
            "message": f"调用API出错: {str(e)}",
            "brand_names": [],
            "other_candidates": []
        }


def generate_cp_names(
    api_key: str,
    name1: str,
    name2: str,
    style: str = "甜蜜",
    model: str = "deepseek-reasoner",
    temperature: float = 0.7,
    max_tokens: int = 1024
) -> Dict[str, Any]:
    """
    生成CP谐音名称
    
    Args:
        api_key: DeepSeek API密钥
        name1: 第一个人的名字
        name2: 第二个人的名字
        style: CP风格，如"甜蜜"、"幽默"
        model: 使用的模型名称
        temperature: 生成多样性参数
        max_tokens: 最大生成token数
        
    Returns:
        包含生成结果的字典，包括推荐CP名及其解析
    """
    client = get_openai_client(api_key)
    
    system_prompt = """你是一位专业CP名称创作专家，精通中文谐音艺术。你的任务是根据用户提供的两个人名，创造既有趣又有含义的谐音CP名称。
你需要提供多个创意方案，每个方案都应包含完整的谐音解析和寓意说明。确保你的回复是JSON格式，便于程序处理。"""

    user_prompt = f"""请为以下两个人创造CP谐音名称：
- 名字一：{name1}
- 名字二：{name2}
- 感情风格：{style}

请生成至少3个不同的CP名称方案，确保结果为以下JSON格式：
```json
{{
  "main_suggestion": {{
    "name": "推荐CP名",
    "match_rate": 98,
    "explanation": "简短的说明这个名字如何结合两人名字",
    "pun_explanation": "详细的谐音解析，说明这个CP名的谐音来源",
    "characters_meaning": {{
      "char1": "第一个字的含义",
      "char2": "第二个字的含义"
    }},
    "combined_meaning": "整体寓意解析"
  }},
  "other_suggestions": [
    {{
      "name": "备选CP名1",
      "explanation": "简短的说明和谐音解析"
    }},
    {{
      "name": "备选CP名2",
      "explanation": "简短的说明和谐音解析"
    }},
    ...
  ],
  "analysis": "对两人名字特点的整体分析"
}}
```

请注意：
1. 创造的CP名必须包含谐音元素，尽量利用两人名字中的字或音
2. 根据感情风格({style})调整创意方向
3. 名称应简洁、朗朗上口，容易记忆
4. match_rate(匹配度)用百分比表示你认为这个名字与两人匹配的程度"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {
            "error": True,
            "message": f"调用API出错: {str(e)}",
            "main_suggestion": {"name": "", "explanation": ""},
            "other_suggestions": []
        }


def generate_pun_copy(
    api_key: str,
    theme: str,
    target_audience: str = "",
    selling_point: str = "",
    emotion: str = "幽默搞笑",
    purpose: str = "社交媒体宣传",
    length: str = "中等(10-20字)",
    options: Dict[str, bool] = None,
    more_requirements: str = "",
    model: str = "deepseek-reasoner",
    temperature: float = 0.7,
    max_tokens: int = 1024
) -> Dict[str, Any]:
    """
    生成包含谐音梗的创意文案
    
    Args:
        api_key: DeepSeek API密钥
        theme: 文案主题关键词
        target_audience: 目标受众画像
        selling_point: 核心卖点/特点
        emotion: 情感倾向
        purpose: 使用场景
        length: 文案长度
        options: 高级选项，如{"包含流行网络语": True}
        more_requirements: 更多需求说明
        model: 使用的模型名称
        temperature: 生成多样性参数
        max_tokens: 最大生成token数
        
    Returns:
        包含生成结果的字典，包括主推文案及备选方案
    """
    client = get_openai_client(api_key)
    
    # 处理高级选项
    options_text = ""
    if options:
        options_list = []
        for option, enabled in options.items():
            if enabled:
                options_list.append(option)
        if options_list:
            options_text = "、".join(options_list)
    
    system_prompt = """你是一位专业文案创作专家，精通中文谐音梗创作。你的任务是根据用户提供的主题和要求，创造包含谐音梗的创意文案。
你需要提供一个主推文案方案和多个备选创意。确保你的回复是JSON格式，便于程序处理。你的文案要有趣、创意，且谐音元素自然融入。
特别注意：
1. 文案要精准针对目标受众
2. 突出产品或服务的核心卖点
3. 确保谐音梗与主题和卖点紧密相关
4. 保持文案的趣味性和传播性"""

    user_prompt = f"""请为以下主题创作包含谐音梗的文案：
- 主题关键词：{theme}
- 目标受众：{target_audience}
- 核心卖点：{selling_point}
- 情感倾向：{emotion}
- 使用场景：{purpose}
- 文案长度：{length}
{f'- 高级要求：{options_text}' if options_text else ''}
{f'- 更多需求：{more_requirements}' if more_requirements else ''}

请生成一个主推文案和至少两个备选方案，确保结果为以下JSON格式：
```json
{{
  "main_copy": {{
    "title": "主标题/口号",
    "content": "完整文案内容",
    "pun_explanation": "谐音梗解析，详细说明谐音来源和巧妙之处",
    "target_audience": "目标受众分析",
    "emotional_effect": "预期情感效果",
    "selling_point_highlight": "如何突出核心卖点"
  }},
  "alternatives": [
    {{
      "title": "备选文案1",
      "content": "备选文案内容",
      "pun_explanation": "谐音解析简述",
      "target_audience": "目标受众分析",
      "selling_point_highlight": "如何突出核心卖点"
    }},
    {{
      "title": "备选文案2",
      "content": "备选文案内容",
      "pun_explanation": "谐音解析简述",
      "target_audience": "目标受众分析",
      "selling_point_highlight": "如何突出核心卖点"
    }}
  ],
  "application_suggestions": [
    "应用建议1",
    "应用建议2",
    "应用建议3"
  ]
}}
```

请注意：
1. 文案必须包含与主题相关的谐音梗元素
2. 根据情感倾向({emotion})调整文案风格
3. 文案长度要符合要求：{length}
4. 确保文案适合指定使用场景：{purpose}
5. 重点突出核心卖点：{selling_point}
6. 精准针对目标受众：{target_audience}"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {
            "error": True,
            "message": f"调用API出错: {str(e)}",
            "main_copy": {"title": "", "content": ""},
            "alternatives": []
        } 