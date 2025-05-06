import os
import sys

import streamlit as st

# 添加项目根目录到Python路径，以便导入utils模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_calls import generate_pun_copy

st.title("✍️ 谐音文案助手")
st.markdown("**让文案充满创意，让营销更具传播力**")

# 侧边栏 - 确保API Key可用
with st.sidebar:
    api_key = st.session_state.get("puncraft_api_key", "")
    if not api_key:
        api_key = st.text_input(
            "DeepSeek API Key",
            type="password",
            help="输入你的DeepSeek API Key以启用生成功能",
            key="copy_api_key"
        )

st.divider()

# 输入区域
st.header("🎯 输入文案需求")

# 定义Emoji及其描述
emoji_options = {
    '😂': '幽默搞笑', 
    '🥰': '温馨感人', 
    '😮': '惊喜意外', 
    '🧐': '专业严肃', 
    '💖': '浪漫甜蜜',
    '🥳': '活泼有趣'
}

# 初始化Session State
if 'emoji_selection' not in st.session_state:
    st.session_state.emoji_selection = {emoji: False for emoji in emoji_options}

# 定义回调函数
def toggle_emoji(emoji_key):
    st.session_state.emoji_selection[emoji_key] = not st.session_state.emoji_selection[emoji_key]

col1, col2 = st.columns(2)

with col1:
    theme = st.text_input("主题关键词", placeholder="输入文案主题，如'咖啡促销'、'新品发布'等")
    target_audience_desc = st.text_input("目标受众画像", placeholder="例如：年轻学生、职场白领、宝妈")
    
    # Emoji情感选择器
    st.markdown("##### 选择情感倾向 (可多选):")
    num_columns = 3
    cols = st.columns(num_columns)
    
    for i, (emoji, desc) in enumerate(emoji_options.items()):
        col_index = i % num_columns
        with cols[col_index]:
            btn_style = "primary" if st.session_state.emoji_selection[emoji] else "secondary"
            if st.button(f"{emoji} {desc}", key=f"emoji_btn_{emoji}", on_click=toggle_emoji, args=(emoji,), use_container_width=True):
                pass  # 按钮点击处理在回调函数中
    
    # 显示当前选择
    selected_emojis = [emoji for emoji, selected in st.session_state.emoji_selection.items() if selected]
    if selected_emojis:
        st.markdown(f"**已选情感:** {' '.join(selected_emojis)}")
    else:
        st.caption("请至少选择一种情感倾向")

with col2:
    purpose = st.selectbox(
        "使用场景",
        [
            "请选择使用场景",
            "社交媒体宣传",
            "短视频标题",
            "产品包装文案",
            "促销活动口号",
            "节日祝福文案",
            "其他场景"
        ]
    )
    core_selling_point = st.text_area("核心卖点/特点", placeholder="简述产品或服务的独特之处，如：纯天然、高效便捷、限时优惠等", height=100)
    length = st.radio("文案长度", ["短句(5-10字)", "中等(10-20字)", "长句(20字以上)"])

# 高级选项
advanced_options = {}
with st.expander("高级选项"):
    st.markdown("**文案风格定制**")
    col1, col2 = st.columns(2)
    
    with col1:
        advanced_options["包含流行网络语"] = st.checkbox("包含流行网络语")
        advanced_options["使用传统文化元素"] = st.checkbox("使用传统文化元素")
    
    with col2:
        advanced_options["强调品牌名称"] = st.checkbox("强调品牌名称")
        advanced_options["增加互动性/号召性"] = st.checkbox("增加互动性/号召性")
    
    more_requirements = st.text_area("更多需求说明", placeholder="如有特殊需求，请在此说明...", height=100)

# 生成按钮
if st.button("✨ 开始生成谐音文案", use_container_width=True):
    if not theme:
        st.warning("请至少输入主题关键词")
    elif not api_key:
        st.error("请在侧边栏输入DeepSeek API Key以启用生成功能")
    else:
        # 准备传递给API的情感数据
        selected_emotions_desc = [emoji_options[emoji] for emoji, selected in st.session_state.emoji_selection.items() if selected]
        emotion_str = ", ".join(selected_emotions_desc) if selected_emotions_desc else "幽默搞笑"  # 默认值
        
        with st.spinner("正在挖掘谐音创意..."):
            try:
                # 调用API生成文案
                result = generate_pun_copy(
                    api_key=api_key,
                    theme=theme,
                    target_audience=target_audience_desc,
                    selling_point=core_selling_point,
                    emotion=emotion_str,
                    purpose=purpose if purpose != "请选择使用场景" else "社交媒体宣传",
                    length=length,
                    options=advanced_options,
                    more_requirements=more_requirements
                )
                
                # 检查是否发生错误
                if result.get("error", False):
                    st.error(f"生成失败: {result.get('message', '未知错误')}")
                    st.stop()
                
                # 展示结果区域
                st.header("📝 创意文案")
                
                # 主推文案
                main_copy = result.get("main_copy", {})
                if main_copy:
                    # 主推文案卡片 - 使用Streamlit原生组件
                    st.markdown("### ✨ 主推方案", help="我们精选的最佳创意方案")
                    
                    # 标题
                    st.markdown(f"## {main_copy.get('title', '创意文案')}", unsafe_allow_html=True)
                    
                    # 主要内容框
                    st.info(f"**{main_copy.get('content', '')}**")
                    
                    # 复制按钮
                    copy_col1, copy_col2 = st.columns([3, 1])
                    with copy_col2:
                        st.button("📋 复制文案", key="copy_main_btn")
                        
                    # 解析信息
                    exp = st.expander("查看文案解析", expanded=True)
                    with exp:
                        st.markdown("##### 😉 谐音梗解析")
                        st.markdown(f"{main_copy.get('pun_explanation', '无谐音解析')}")
                        
                        st.markdown("##### 👥 目标人群")
                        st.markdown(f"{main_copy.get('target_audience', '目标受众')}")
                        
                        st.caption(f"适用场景: {purpose if purpose != '请选择使用场景' else '推广宣传'}")
                
                # 备选方案
                alternatives = result.get("alternatives", [])
                if alternatives:
                    st.markdown("---")
                    st.subheader("🎭 备选创意")
                    
                    # 确保至少有两个备选方案
                    if len(alternatives) >= 2:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            alt = alternatives[0]
                            alt_content = alt.get('content', '')
                            
                            st.markdown("#### 方案B1", help="备选创意方案1")
                            st.markdown(f"**{alt.get('title', '备选文案1')}**")
                            
                            # 使用success显示器
                            st.success(alt_content)
                            
                            with st.expander("谐音梗解析"):
                                st.markdown(f"{alt.get('pun_explanation', '无谐音解析')}")
                        
                        with col2:
                            alt = alternatives[1]
                            alt_content2 = alt.get('content', '')
                            
                            st.markdown("#### 方案B2", help="备选创意方案2")
                            st.markdown(f"**{alt.get('title', '备选文案2')}**")
                            
                            # 使用success显示器
                            st.success(alt_content2)
                            
                            with st.expander("谐音梗解析"):
                                st.markdown(f"{alt.get('pun_explanation', '无谐音解析')}")
                
                # 创意解析
                st.subheader("创意解析")
                if main_copy:
                    st.markdown(f"""
                    #### 「{main_copy.get('title', '主文案')}」解析：
                    
                    - **谐音关联**：
                      - {main_copy.get('pun_explanation', '无谐音解析')}
                    
                    - **目标群体共鸣**：
                      - 主打{main_copy.get('target_audience', '目标受众')}的痛点
                      - 预期情感效果：{main_copy.get('emotional_effect', '引起共鸣')}
                    """)
                
                # 应用建议
                application_suggestions = result.get("application_suggestions", [])
                if application_suggestions:
                    st.subheader("应用建议")
                    suggestions_md = ""
                    for suggestion in application_suggestions:
                        suggestions_md += f"- {suggestion}\n"
                    st.markdown(suggestions_md)
                
                # 保存和分享
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    if main_copy:
                        download_text = f"{main_copy.get('title', '')}\n\n{main_copy.get('content', '')}"
                        st.download_button("💾 保存文案", download_text, "creative_copy.txt")
                with col2:
                    st.button("✏️ 编辑微调", use_container_width=True)
            
            except Exception as e:
                st.error(f"处理过程中出错: {str(e)}")

# 页脚
st.divider()
st.caption("提示：尝试不同的主题和场景组合，探索更多创意可能！") 