# import streamlit as st
# import re
# from pypinyin import pinyin, Style
#
#
# # 读取成语大全.txt文件中的成语
# def load_chengyu(file_path):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         chengyu_list = f.readlines()
#     return [cy.strip() for cy in chengyu_list]
#
#
# # 获取一个字的拼音
# def get_pinyin(word):
#     pinyin_list = pinyin(word, style=Style.NORMAL, heteronym=False)  # 不带声调更适合匹配
#     return pinyin_list[0][0] if pinyin_list else ''
#
#
# # 检查成语是否包含两个人名字拼音：一人一个字
# def contains_both_name_pinyin(chengyu, name1, name2):
#     py_chengyu = [get_pinyin(c) for c in chengyu]
#     py_name1 = [get_pinyin(c) for c in name1]
#     py_name2 = [get_pinyin(c) for c in name2]
#     return any(p in py_chengyu for p in py_name1) and any(p in py_chengyu for p in py_name2)
#
#
# # 检查是否是同字命中（直接包含名字字）
# def is_exact_char_match(chengyu, name1, name2):
#     return any(c in chengyu for c in name1) and any(c in chengyu for c in name2)
#
#
# # 根据名字的拼音，替换成语中拼音相同的字，生成改编版成语
# def generate_modified_chengyu(chengyu, name1, name2):
#     modified = ''
#     for c in chengyu:
#         py_c = get_pinyin(c)
#         replaced = False
#         for n in name1 + name2:
#             if get_pinyin(n) == py_c and n != c:
#                 modified += n
#                 replaced = True
#                 break
#         if not replaced:
#             modified += c
#     return modified if modified != chengyu else None
#
#
# # 为名字中的字添加红色高亮
# def highlight_name_chars(text, name1, name2):
#     for char in set(name1 + name2):
#         text = re.sub(f'({char})', r'<span style="color:red">\1</span>', text)
#     return text
#
#
# # Streamlit应用程序
# def main():
#     st.title("谐音成语CP名生成器")
#
#     # 上传成语大全.txt文件
#     chengyu_list = load_chengyu(r'E:\project\xieyinzi\成语大全.txt')
#
#     # 输入两个名字
#     name1 = st.text_input("请输入第一个名字:")
#     name2 = st.text_input("请输入第二个名字:")
#
#     if name1 and name2:
#         shown_set = set()  # 记录已展示的成语（原始）
#         st.write("找到以下相关成语：")
#
#         for cy in chengyu_list:
#             if not contains_both_name_pinyin(cy, name1, name2):
#                 continue
#
#             if is_exact_char_match(cy, name1, name2):
#                 if cy not in shown_set:
#                     shown_set.add(cy)
#                     highlighted = highlight_name_chars(cy, name1, name2)
#                     st.markdown(highlighted, unsafe_allow_html=True)
#             else:
#                 modified = generate_modified_chengyu(cy, name1, name2)
#                 if modified and cy not in shown_set:
#                     shown_set.add(cy)
#                     highlighted = highlight_name_chars(modified, name1, name2)
#                     st.markdown(f"{highlighted}（{cy}）", unsafe_allow_html=True)
#
#         if not shown_set:
#             st.write("没有找到相关成语，换个名字试试吧！")
#     else:
#         st.write("请输入两个名字以开始查找成语。")
#
#
# if __name__ == "__main__":
#     main()
#
#
#








import streamlit as st
import re
from pypinyin import pinyin, Style

# 设置页面配置（增加emoji图标与标题）
st.set_page_config(page_title="谐音成语CP名生成器 ❤️📜", page_icon="💘", layout="centered")




# 读取成语大全.txt文件中的成语
def load_chengyu(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        chengyu_list = f.readlines()
    return [cy.strip() for cy in chengyu_list]


# 获取一个字的拼音
def get_pinyin(word):
    pinyin_list = pinyin(word, style=Style.NORMAL, heteronym=False)
    return pinyin_list[0][0] if pinyin_list else ''


# 检查成语是否包含两个人名字拼音
def contains_both_name_pinyin(chengyu, name1, name2):
    py_chengyu = [get_pinyin(c) for c in chengyu]
    py_name1 = [get_pinyin(c) for c in name1]
    py_name2 = [get_pinyin(c) for c in name2]
    return any(p in py_chengyu for p in py_name1) and any(p in py_chengyu for p in py_name2)


# 是否直接包含名字的字
def is_exact_char_match(chengyu, name1, name2):
    return any(c in chengyu for c in name1) and any(c in chengyu for c in name2)


# 生成替换后的成语
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


# 高亮名字字
def highlight_name_chars(text, name1, name2):
    for char in set(name1 + name2):
        text = re.sub(f'({char})', r'<span style="color:red; font-weight:bold;">\1</span>', text)
    return text


# 主体功能
def main():
    st.title("谐音成语CP名生成器 ❤️📜")
    st.markdown("**基于双方名字生成有趣的成语组合谐音，增加社交互动趣味性**")
    st.divider()
    # 上传成语文件
    chengyu_list = load_chengyu(r'pages\成语大全.txt')

    name1 = st.text_input("🧑 请输入第一个名字：")
    name2 = st.text_input("👩 请输入第二个名字：")

    if name1 and name2:
        shown_set = set()
        st.markdown("### 📜 为你们找到的缘分成语：")

        for cy in chengyu_list:
            if not contains_both_name_pinyin(cy, name1, name2):
                continue

            if is_exact_char_match(cy, name1, name2):
                if cy not in shown_set:
                    shown_set.add(cy)
                    highlighted = highlight_name_chars(cy, name1, name2)
                    st.markdown(f"🌟 {highlighted}", unsafe_allow_html=True)
            else:
                modified = generate_modified_chengyu(cy, name1, name2)
                if modified and cy not in shown_set:
                    shown_set.add(cy)
                    highlighted = highlight_name_chars(modified, name1, name2)
                    st.markdown(f"💫 {highlighted} <span style='color:#888;'>（原：{cy}）</span>", unsafe_allow_html=True)

        if not shown_set:
            st.markdown("🥺 没有找到相关成语，换个名字试试吧！")
    else:
        st.markdown("📌 请输入两个名字，即可发现命中注定的成语缘分～")


if __name__ == "__main__":
    main()
