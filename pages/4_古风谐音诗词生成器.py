# import streamlit as st
# import pickle
# import sys
# import os
#
# sys.path.append(os.path.abspath(".."))  # 添加项目根路径
#
# from pages.sentencetopoem import main
#
# # 加载模型（只加载一次）
#
# import os
#
# @st.cache_resource
# def load_models():
#     base_dir = os.path.dirname(__file__)  # 获取当前文件所在路径
#
#     with open(os.path.join(base_dir, 'sentencetopoem', 'model_1d.pickle'), 'rb') as f:
#         temp_1 = pickle.load(f)
#         model_1d = main.Model_ND(temp_1, 1)
#
#     with open(os.path.join(base_dir, 'sentencetopoem', 'model_2d.pickle'), 'rb') as f:
#         temp_2 = pickle.load(f)
#         model_2d = main.Model_ND(temp_2, 2)
#
#     return model_1d, model_2d
#
#
# model_1d, model_2d = load_models()
#
# # 页面标题
# st.title("🎭 古诗词风格谐音生成器")
#
# # 文本输入框
# user_input = st.text_input("请输入一段话（支持中文）：", "")
#
# # 当有输入时
# if user_input:
#     try:
#         output = main.generate_by_text(user_input, model_1d, model_2d)
#         st.success("🎉 生成结果如下：")
#         st.markdown(f"**原始输入：** {user_input}")
#         st.markdown(f"**谐音改写：** {output}")
#     except Exception as e:
#         st.error(f"生成失败：{e}")


import streamlit as st
import pickle
import sys
import os

sys.path.append(os.path.abspath(".."))  # 添加项目根路径
from pages.sentencetopoem import main

st.title("📜古诗词风格谐音生成器")
# 页面装饰 - 顶部视觉
st.markdown("**将现代语言转化为中国古诗词风格的谐音版本，融合马尔科夫链与全概率公式打造生成与评价一体的创作体验**")

# ---- 加载模型 ----
@st.cache_resource
def load_models():
    base_dir = os.path.dirname(__file__)  # 当前目录

    with open(os.path.join(base_dir, 'sentencetopoem', 'model_1d.pickle'), 'rb') as f:
        temp_1 = pickle.load(f)
        model_1d = main.Model_ND(temp_1, 1)

    with open(os.path.join(base_dir, 'sentencetopoem', 'model_2d.pickle'), 'rb') as f:
        temp_2 = pickle.load(f)
        model_2d = main.Model_ND(temp_2, 2)

    return model_1d, model_2d


model_1d, model_2d = load_models()

# ---- 输入区 ----
st.markdown("### 🖋️ 输入你想转换的文本：")
user_input = st.text_area("示例：我思君不见君，梦魂绕千年", "", height=120, help="可输入中文句子，系统将自动进行古风谐音转换")

# ---- 生成区 ----
if user_input.strip():
    if user_input.strip():
        try:
            # === Step 1：记录逗号位置 ===
            comma_indices = [i for i, c in enumerate(user_input) if c == '，']
            cleaned_input = user_input.replace('，', '')

            # === Step 2：传入模型生成 ===
            output = main.generate_by_text(cleaned_input, model_1d, model_2d)

            # === Step 3：插回逗号 ===
            output_with_commas = list(output)
            for idx in comma_indices:
                if idx < len(output_with_commas):
                    output_with_commas.insert(idx, '，')
                else:
                    output_with_commas.append('，')
            output_final = ''.join(output_with_commas)

            # === 展示结果 ===
            st.markdown("### ✨ 转换结果如下：")
            st.markdown(f"📌 <span style='color:#555'><b>原始输入：</b> {user_input}</span>", unsafe_allow_html=True)
            st.markdown(f"📜 <span style='color:#8B008B;font-size:18px;'><b>古风改写：</b>{output_final}</span>",
                        unsafe_allow_html=True)

        except Exception as e:
            st.error(f"生成失败：{e}")

else:
    st.info("🌸 请输入一段内容，唤醒文字的古韵回响～")

# ---- 页脚 ----
st.markdown("<hr><div style='text-align:center; color:gray;'>© 2025 · 谐音诗心工坊 · 灵感源于你的每一句话 💖</div>", unsafe_allow_html=True)
