import streamlit as st

# ---- 页面基本设置 ----
st.set_page_config(page_title="谐音工坊 (PunCraft)", page_icon="✨", layout="wide")

# ---- API Key设置（侧边栏） ----
with st.sidebar:
    st.title("🔑 API设置")
    api_key = st.text_input(
        "DeepSeek API Key",
        type="password",
        help="输入你的DeepSeek API Key以启用生成功能",
        key="puncraft_api_key"
    )
    
    st.caption("""
    ### 如何获取API Key
    1. 访问[DeepSeek官网](https://deepseek.com)注册账号
    2. 在个人设置中创建API Key
    3. 复制API Key填入此处
    
    API Key仅在当前会话有效，刷新页面后需重新输入。
    """)
    
    st.divider()
    
    st.markdown("### 关于谐音工坊")
    st.markdown("谐音工坊(PunCraft)是一个基于AI和深度学习NLP技术的谐音创意生成平台，让语言成为创意的游乐场！")


# ---- 顶部标题 ----
st.title("🎨 谐音工坊 (PunCraft) ✨")
st.subheader("🤖 基于 NLP 的创意谐音梗生成平台")
st.markdown("🧠 **让语言成为创意的游乐场 | 用谐音连接灵感**")


st.divider()

st.header("谐音梗可别念“邪”了")

st.markdown("""
<div style='font-size:17px; line-height:1.8; color:#333;'>

🧩 **谐音梗**，作为一种别具一格的语言表达方式,已悄然融入我们日常的点点滴滴中——

🍊 打碎东西，念一句 <span style='color:#D2691E; font-weight:bold;'>“碎碎（岁岁）平安”</span>，求个好彩头;💬 网络社交中流行的 <span style='color:#8B008B;'>“886（拜拜啦）”</span>、<span style='color:#FF1493;'>“520（我爱你）”</span>，简单直白、妙趣横生；  
📛 办公桌上的摆件 “<span style='color:#4682B4;'>禁止蕉（焦）绿（虑）</span>”，不仅是谐音游戏,也是打工人 <strong style='color:#2E8B57;'>“自嘲式生存美学”</strong> 的一角落。

🌀 这些轻巧的表达，构成了我们语言中的“小彩蛋”，既能缓解压力，又让人忍俊不禁地说出一句：**“懂的都懂”** 😌

</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.image("image/1.jpg", caption="🍌 禁止蕉绿", use_container_width=True)

with col2:
    st.image("image/2.jpg", caption="文创帆布包", use_container_width=True)

with col3:
    st.image("image/3.jpg", caption="谐音祝福语", use_container_width=True)



st.markdown("""
<div style='font-size:17px; line-height:1.8; color:#333;'>

📝 **然而，近年来，谐音梗的“滥用”现象引发了社会担忧。**  

将谐音**不分场合、随意乱用**的情况越来越普遍,一些网络黑话、烂梗甚至“渗透”到青少年群体，引发了语言环境的混乱与担忧。

📢 不久前，**中央网信办、教育部联合开展**  
“清朗·规范网络语言文字使用”专项行动,聚焦语言文字**不规范、不文明**现象,重点整治 **歪曲音、形、义，编造网络黑话烂梗**，以及**滥用隐晦表达**等突出问题。


> ❓ **不禁想问**：  
> 谐音这一语言现象是如何兴起的？  
> 又该如何**合理、巧妙而有创意地使用它**？

</div>
""", unsafe_allow_html=True)
st.divider()

st.header("🎭什么是谐音梗？")




st.markdown("""
<div style="font-size:17px; line-height:1.8">

🔤 <strong>谐音梗</strong>指使用 <span style="color:#DC143C;">声韵相同或相近</span> 的字来代替本字，以达成某种意趣效果。
</div>
<p style="line-height:2.5">&nbsp;</p>
""", unsafe_allow_html=True)

# 第二段：“古已有之”图文并排
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div style="font-size:17px; line-height:1.8">


    <h3>🏮 古已有之，源远流长</h3>

    📜 早在宋朝，百姓过年把柏树枝、甜柿和橘子当供品，分别取“柏”“柿”“橘”三字，寓意：<span style="color:#4169E1;"><strong>百事吉</strong></span> ✅。<br>

    📖 古人的诗歌、对联、歇后语等文学形式中，为了押韵或暗含含义，也常使用“<strong>谐音双关</strong>”来丰富表达。<br>

    🌐 如今的谐音梗，形式更是不断演化，涵盖：

    - 🔢 数字谐音（如“886” 表示拜拜了）
    - 🔤 中英文混合（如“U 你真棒”）
    - 🔄 同义替换等变体
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("image/4.jpg", caption="“百事吉”供品", use_container_width=True,width=300)

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div style="font-size:17px; line-height:1.8">

    <h3>✨ 为何谐音梗越来越火？</h3>
    <h4>🧠 言此意彼，多一点含蓄</h4>

    📌 中国文化讲究“含蓄、委婉”，用<strong>谐音字替代直白表达</strong>，恰恰符合国人的文化审美：<br><br>

    💌 <strong>唐代温庭筠：</strong><br>
    “井底点灯深烛（嘱）伊，共郎长行莫围棋（违期）”，寄托女子对情郎的期盼之情。<br><br>

    🧵 <strong>明朝民歌：</strong><br>
    “梭子里无丝（思）空来往，有针无线枉相缝（逢）”，含蓄透露<strong style="color:#8B0000;">“空相思”</strong>的落寞与无奈。
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("image/5.jpg", caption="温柔含蓄", width=300)  # 去掉 use_container_width



col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        <div style="font-size:17px; line-height:1.8">

        <h4>🎉 调味生活，多一些乐趣</h4>

        😁 一个恰到好处的谐音梗，往往能让场合更轻松：

        <ul>
            <li>💻 程序员自嘲：<strong>“码”不停蹄地工作</strong> → 巧妙融合“代码”与“马不停蹄”</li>
            <li>📣 广告文案：“骑”乐无穷、“无‘胃’不治” → 通俗又吸睛</li>
        </ul>

        🎯 谐音让表达 <span style="color:#2E8B57;"><strong>更有趣、更传播、更具记忆点</strong></span>。

        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.image("image/6.jpg", caption="打工人", width=400)


col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        <div style="font-size:17px; line-height:1.8">

        <h4>🌐 社交货币，拉近点距离</h4>

        <p>👾 Z世代的“网络原住民”乐于用<strong>语言梗</strong>展现个性。</p>

        <p>🗝 在社交网络中，谐音梗成为一种
        <strong style="color:#C71585;">“社交密码”</strong>：</p>

        <blockquote>🤝 只要你也会这个梗，就能感受到：<br>
        “确认过眼神，我们是同道中人”。</blockquote>

        <p>👨‍💻 像“程序猿”、“研究僧”这样的谐音称呼，
        已成为身份标签和社交标识。</p>

        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.image("image/7.jpg", caption="家庭主厨", width=400)



col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        <div style="font-size:17px; line-height:1.8">

        <h4>🏛 政务宣传，化繁为简</h4>

        <p>📲 一些政务平台也开始借用谐音“入圈”：</p>

        <ul>
            <li>浙江的 <strong>“浙里办”</strong></li>
            <li>湖南的 <strong>“新湘事成”</strong></li>
        </ul>

        <p>🧩 利用地方简称 + 谐音创意，不仅让名字
        <span style="color:#4682B4;">更好记</span>，也
        <span style="color:#2E8B57;">拉近了政府与百姓</span> 的距离，收获好评。</p>

        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.image("image/8.jpg", caption="江苏城市谐音", width=400)













st.divider()

st.markdown("""
<hr style="border: none; height: 3px; background: linear-gradient(to right, #FF6347, #FFA500, #32CD32); margin-top: 30px; margin-bottom: 10px;" />

<div style="font-size:30px; font-weight:bold; text-align:center; color:#4682B4; padding: 10px 0;">
🔍 本产品的核心功能
</div>

<hr style="border: none; height: 2px; background-color: #ccc; margin-top: 0px;" />
""", unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 🏭 品牌创意工坊")
    st.markdown("为品牌创业者提供创意谐音名称，提升记忆点和传播力")
    st.markdown("[立即体验 →](品牌创意工坊)")

with col2:
    st.markdown("### 💑 CP名生成器")
    st.markdown("基于双方名字生成有趣的组合谐音，增加社交互动趣味性")
    st.markdown("[立即体验 →](CP名生成器)")

with col3:
    st.markdown("### ✍️ 谐音文案助手")
    st.markdown("为内容创作者提供谐音梗灵感，轻松打造富有创意的文案")
    st.markdown("[立即体验 →](谐音文案助手)")

with col4:
    st.markdown("### 🏯 古风谐音诗词生成器")
    st.markdown("将现代语言转化为中国古诗词风格的谐音版本，融合马尔科夫链与全概率公式打造生成与评价一体的创作体验")
    st.markdown("[立即体验 →](古风谐音诗词生成器)")



# 创建四列布局
col1, col2, col3, col4 = st.columns(4)

# 在每一列中插入图片
with col1:
    st.image("image/9.jpg",use_container_width=True)

with col2:
    st.image("image/10.jpg", use_container_width=True)

with col3:
    st.image("image/11.jpg", use_container_width=True)

with col4:
    st.image("image/12.jpg", use_container_width=True)

st.divider()
















# ---- 用户价值强调 ----
st.header("为什么选择谐音工坊？")
st.markdown("""
- 🚀 **节省80%的机械式头脑风暴时间**
- 🌈 **获得超出人类单一文化背景的跨维度创意**
- 🔗 **让谐音梗成为连接商业价值与社交传播的桥梁**
""")

st.divider()










# ---- 成功案例展示 ----
st.header("成功案例")
case_col1, case_col2 = st.columns(2)

with case_col1:
    st.markdown("#### 品牌案例")
    st.markdown("""- **咖啡店「解暑咖」** - 既是"解暑"也谐音"解数学"，受到学生群体喜爱""")
    st.markdown("""- **健身工作室「型体验」** - 谐音"行体验"，强调服务体验与健身效果并重""")

with case_col2:
    st.markdown("#### 文案案例")
    st.markdown("""- **网红奶茶「乌龙袭来」** - 乌龙茶谐音"乌龙事件"，引发社交媒体讨论""")
    st.markdown("""- **情侣CP名「柠暮」** - 由"宁"和"暮"组成，谐音"柠檬"，甜蜜中带点酸""")

st.divider()

# ---- 行动号召 ----
st.header("开始创造你的谐音梗")
st.markdown("选择下方功能，立即开始你的创意之旅！")

# ---- 跳转按钮区域 ----
cta_col1, cta_col2, cta_col3, cta_col4 = st.columns(4)

with cta_col1:
    st.button("🏭 品牌创意工坊", use_container_width=True, on_click=lambda: st.switch_page("pages/1_品牌创意工坊.py"))

with cta_col2:
    st.button("💑 CP名生成器", use_container_width=True, on_click=lambda: st.switch_page("pages/2_CP名生成器.py"))

with cta_col3:
    st.button("✍️ 谐音文案助手", use_container_width=True, on_click=lambda: st.switch_page("pages/3_谐音文案助手.py"))

with cta_col4:
    st.button("🏯 古风谐音诗词生成器", use_container_width=True, on_click=lambda: st.switch_page("pages/4_古风谐音诗词生成器.py"))

# ---- 页脚 ----
st.divider()
st.markdown(
    "<p style='text-align: center; color: grey;'>"
    "© 2025 谐音工坊 (PunCraft) | 让创意更有趣 | 让传播更高效"
    "</p>",
    unsafe_allow_html=True
)
