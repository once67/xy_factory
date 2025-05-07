import os
import sys

import streamlit as st

# 添加项目根目录到Python路径，以便导入utils模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_calls import generate_brand_names


def generate_logo_by_prompt(prompt: str, api_key: str) -> str:
    import time

    import requests

    create_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"
    }
    payload = {
        "model": "wanx2.1-t2i-turbo",
        "input": {"prompt": prompt},
        "parameters": {
            "size": "1024*1024",
            "n": 1
        }
    }

    # Step 1: 创建任务
    response = requests.post(create_url, headers=headers, json=payload)
    task_id = response.json()["output"]["task_id"]

    # Step 2: 轮询结果
    status_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    while True:
        time.sleep(3)
        resp = requests.get(status_url, headers={"Authorization": f"Bearer {api_key}"})
        data = resp.json()
        status = data["output"]["task_status"]
        if status == "SUCCEEDED":
            return data["output"]["results"][0]["url"]
        elif status == "FAILED":
            raise RuntimeError("图像生成失败")



st.title("🏭 品牌创意工坊")
st.markdown("**智能挖掘品牌谐音，创造记忆点与传播力**")

# 侧边栏 - 确保API Key可用
with st.sidebar:
    # 优先从环境变量获取 API Key
    env_api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    
    if env_api_key:
        # 环境变量中有 API Key，直接使用
        api_key = env_api_key
        st.session_state["puncraft_api_key"] = env_api_key
        st.success("✅ 已从环境变量加载 DeepSeek API Key")
    else:
        # 尝试从 session_state 获取
        api_key = st.session_state.get("puncraft_api_key", "")
        if not api_key:
            # 都没有，提示用户输入
            api_key = st.text_input(
                "DeepSeek API Key",
                type="password",
                help="输入你的DeepSeek API Key以启用生成功能",
                key="brand_api_key"
            )
            if api_key:
                st.session_state["puncraft_api_key"] = api_key
            else:
                st.warning("⚠️ 请输入 DeepSeek API Key 或设置环境变量 DEEPSEEK_API_KEY")

st.divider()

# 输入区域
st.header("🔍 输入品牌信息")

col1, col2 = st.columns(2)

with col1:
    brand_keyword = st.text_input("品牌关键词", placeholder="输入核心关键词，如'咖啡'、'健身'等")
    industry = st.selectbox(
        "所属行业",
        [
            "请选择行业",
            "餐饮美食",
            "教育培训",
            "健康健身",
            "科技数码",
            "美妆护肤",
            "服装服饰",
            "家居生活",
            "文创设计",
            "其他行业"
        ]
    )

with col2:
    positioning = st.text_area("品牌定位", placeholder="简述品牌的核心价值、目标受众等", height=100)
    style = st.multiselect(
        "品牌风格",
        ["有趣幽默", "高端大气", "亲民友好", "创新科技", "传统文化", "小清新", "潮流时尚"]
    )

# 生成按钮
if st.button("🚀 开始生成品牌创意", use_container_width=True):
    if not brand_keyword:
        st.warning("请至少输入品牌关键词")
    elif not api_key:
        st.error("请在侧边栏输入DeepSeek API Key以启用生成功能")
    else:
        with st.spinner("AI正在为您创造品牌创意..."):
            # 调用API生成品牌名称
            try:
                result = generate_brand_names(
                    api_key=api_key,
                    keyword=brand_keyword,
                    industry=industry if industry != "请选择行业" else "",
                    positioning=positioning,
                    style=style
                )
                
                # 检查是否发生错误
                if result.get("error", False):
                    st.error(f"生成失败: {result.get('message', '未知错误')}")
                    st.stop()
                
                # 显示生成结果
                st.success("创意生成完成！")
                
                # 展示结果区域
                st.header("✨ 创意结果")
                
                tab1, tab2, tab3 = st.tabs(["品牌名称", "Logo参考", "命名解析"])
                
                with tab1:
                    st.subheader("品牌名称方案")
                    
                    # 显示主要品牌名称建议
                    if "brand_names" in result and result["brand_names"]:
                        col1, col2 = st.columns(2) # 在循环开始前定义好两列
                        
                        for i, brand in enumerate(result["brand_names"][:2]):  # 仅显示前两个主要建议
                            column_to_use = col1 if i == 0 else col2
                            with column_to_use:
                                st.markdown(f"#### 方案{i+1}：「{brand['name']}」")
                                st.markdown("⭐" * int(brand.get("rating", 3)))
                                st.markdown(f"*{brand.get('slogan', '')}*")
                    
                    # 其他候选方案
                    st.markdown("---")
                    st.markdown("#### 其他候选方案")
                    
                    other_candidates = result.get("other_candidates", [])
                    for candidate in other_candidates:
                        st.markdown(f"""- **「{candidate['name']}」** - {candidate.get('pun_explanation', '')}""")

                with tab2:
                    st.subheader("Logo设计参考")
                    st.markdown("*基于生成的品牌名称，AI为您创建的Logo概念*")

                    try:
                        # 组合 Prompt（用第一个品牌名）
                        if result["brand_names"]:
                            brand_name = result["brand_names"][0]["name"]
                            prompt = f"{style}风格的logo设计，品牌名：{brand_name}，关键词：{brand_keyword}，行业：{industry}，定位：{positioning}"

                            # 从环境变量获取 DashScope API 密钥
                            dashscope_api_key = os.environ.get("DASHSCOPE_API_KEY", "")
                            if not dashscope_api_key:
                                st.warning("⚠️ 未设置环境变量 DASHSCOPE_API_KEY，Logo生成功能不可用")
                            else:
                                with st.spinner("正在生成Logo，请稍候..."):
                                    image_url = generate_logo_by_prompt(prompt, dashscope_api_key)
                                    st.image(image_url, caption=f"品牌名{brand_name}的Logo概念", use_container_width=True)
                        else:
                            st.warning("无法获取品牌名生成Logo")
                    except Exception as e:
                        st.error(f"Logo生成出错：{e}")

                with tab3:
                    st.subheader("命名解析")
                    
                    # 显示第一个品牌名称的详细解析
                    if "brand_names" in result and result["brand_names"]:
                        brand = result["brand_names"][0]
                        st.markdown(f"#### 「{brand['name']}」解析")
                        st.markdown(f"""
                        - **谐音关联**：{brand.get('pun_explanation', '暂无解析')}
                        - **语义关联**：{brand.get('meaning', '暂无解析')}
                        - **记忆点**：品牌名称简洁易记，谐音巧妙自然
                        - **目标群体**：{positioning or '暂无定位信息'}
                        - **传播潜力**：高频词汇，易于传播，具有话题性
                        """)
            except Exception as e:
                st.error(f"处理过程中出错: {str(e)}")

# 页脚
st.divider()
st.caption("提示：尝试不同的关键词和行业组合，探索更多创意可能！") 