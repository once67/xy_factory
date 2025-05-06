import os
import re

import streamlit as st
from pypinyin import Style, pinyin

# 设置页面配置（增加emoji图标与标题）
st.set_page_config(page_title="谐音成语CP名生成器 ❤️📜", page_icon="💘", layout="centered")

# 读取带情感分类的成语数据
def load_chengyu_with_emotion(file_path):
    chengyu_data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                chengyu, emotion = parts
                chengyu_data.append((chengyu.strip(), emotion.strip()))
    return chengyu_data

def get_pinyin(word):
    pinyin_list = pinyin(word, style=Style.NORMAL, heteronym=False)
    return pinyin_list[0][0] if pinyin_list else ''

def contains_both_name_pinyin(chengyu, name1, name2):
    py_chengyu = [get_pinyin(c) for c in chengyu]
    py_name1 = [get_pinyin(c) for c in name1]
    py_name2 = [get_pinyin(c) for c in name2]
    return any(p in py_chengyu for p in py_name1) and any(p in py_chengyu for p in py_name2)

def is_exact_char_match(chengyu, name1, name2):
    return any(c in chengyu for c in name1) and any(c in chengyu for c in name2)

def generate_modified_chengyu(chengyu, name1, name2):
    modified = ''
    for c in chengyu:
        py_c = get_pinyin(c)
        replaced = False
        for n in name1 + name2:
            if get_pinyin(n) == py_c and n != c:
                modified += n
                replaced = True
                break
        if not replaced:
            modified += c
    return modified if modified != chengyu else None

def highlight_name_chars(text, name1, name2):
    for char in set(name1 + name2):
        text = re.sub(f'({char})', r'<span style="color:red; font-weight:bold;">\1</span>', text)
    return text

# 主体程序
def main():
    st.title("谐音成语CP名生成器 ❤️📜")
    st.markdown("**基于双方名字生成有趣的成语组合谐音，支持情感分类筛选哦！**")
    st.divider()

    # 构建正确的文件路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chengyu_file_path = os.path.join(script_dir, '成语大全_情感分类.txt')

    # 上传并加载带情感的成语文件
    chengyu_data = load_chengyu_with_emotion(chengyu_file_path)

    # 选择情感分类
    emotion_choice = st.selectbox("🎭 请选择成语情感分类：", options=["全部", "中性", "褒义", "贬义"])

    name1 = st.text_input("🧑 请输入第一个名字：")
    name2 = st.text_input("👩 请输入第二个名字：")

    if name1 and name2:
        shown_set = set()
        st.markdown("### 📜 为你们找到的缘分成语：")

        for chengyu, emotion in chengyu_data:
            if emotion_choice != "全部" and emotion != emotion_choice:
                continue  # 跳过不符合筛选的情感类别

            if not contains_both_name_pinyin(chengyu, name1, name2):
                continue

            if is_exact_char_match(chengyu, name1, name2):
                if chengyu not in shown_set:
                    shown_set.add(chengyu)
                    highlighted = highlight_name_chars(chengyu, name1, name2)
                    st.markdown(f"🌟 {highlighted} <span style='color:#888;'>（{emotion}）</span>", unsafe_allow_html=True)
            else:
                modified = generate_modified_chengyu(chengyu, name1, name2)
                if modified and chengyu not in shown_set:
                    shown_set.add(chengyu)
                    highlighted = highlight_name_chars(modified, name1, name2)
                    st.markdown(f"💫 {highlighted} <span style='color:#888;'>（原：{chengyu}，{emotion}）</span>", unsafe_allow_html=True)

        if not shown_set:
            st.markdown("🥺 没有找到相关成语，换个名字试试吧！")
    else:
        st.markdown("📌 请输入两个名字，即可发现命中注定的成语缘分～")

if __name__ == "__main__":
    main()
