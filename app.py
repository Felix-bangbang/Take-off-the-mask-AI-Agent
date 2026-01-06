import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. 页面配置 (关键：设置手机图标) ---
st.set_page_config(
    page_title="AI 毒舌/洞悉诊断室",
    page_icon="logo.png",  # 确保目录下有这张图
    layout="centered",
    initial_sidebar_state="collapsed"
)

LOGO_URL = "https://github.com/Felix-bangbang/Take-off-the-mask-AI-Agent/blob/main/logo.png"

st.markdown(
    f"""
    <style>
    </style>
    <link rel="apple-touch-icon" href="{LOGO_URL}">
    <link rel="apple-touch-icon" sizes="152x152" href="{LOGO_URL}">
    <link rel="apple-touch-icon" sizes="180x180" href="{LOGO_URL}">
    <link rel="apple-touch-icon" sizes="167x167" href="{LOGO_URL}">
    <link rel="icon" type="image/png" sizes="192x192"  href="{LOGO_URL}">
    <link rel="icon" type="image/png" sizes="512x512"  href="{LOGO_URL}">
    """,
    unsafe_allow_html=True
)

# --- 2. 样式优化 (隐藏无关菜单，让它更像App) ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;} 
            /* 调整手机端顶部留白 */
            .block-container {
                padding-top: 2rem;
                padding-bottom: 5rem;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 3. API 配置 ---
try:
    # 优先从 Streamlit 云端读取 Secrets
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # 本地调试（切记：上传 GitHub 前删除）
    # api_key = "粘贴你的_API_KEY_在这里" 
    st.error("请配置 API Key")

if 'api_key' in locals():
    genai.configure(api_key=api_key)

# --- 4. 核心逻辑 (你的双重人格 Prompt) ---
def get_gemini_response(image, mode):
    user_instruction = f"[{mode}]"
    
    system_prompt = """
    # Role
    你是一个拥有“双重人格”的顶尖人类观察家。根据用户的指令（锐评模式 或 洞悉模式），对截图进行深入分析。

    **双重模式：**
    1.  **🌶️ 锐评模式 (Roast)**：毒舌、犀利、荒谬好笑。解构截图中的虚荣、做作、AI 痕迹。
    2.  **🔮 洞悉模式 (Insight)**：挖掘内心匮乏，温暖哲理，具有文学性和治愈感（参考博尔赫斯风格）。

    # Analysis Framework
    1.  **视觉提取**：识别平台、精致程度、显性炫耀 vs 隐性氛围。
    2.  **文本解构**：AI 嗅探（LLM特征）、凡尔赛检测。
    3.  **F/T 人格判断**：
        * **F人 (Feeling)**：关注情绪、人际、氛围（关键词：感觉、emo、爱）。
        * **T人 (Thinking)**：关注逻辑、利弊、事实（关键词：因为、分析、效率）。

    # Output Format (Markdown)
    请直接输出以下格式：

    ## 🩺 账号成分诊断书 | [当前模式]

    **基础面板**
    * 📍 **疑似平台**：...
    * 🧬 **人格倾向**：...
    * 🤖 **含 AI 量**：...
    * 📉 **做作/情绪指数**：...

    **核心评价**
    > [根据模式，生成一句犀利吐槽 或 一句深情冷读]

    **深度解码**
    * 🖼️ **画面潜台词**：... [二句话]
    * 📝 **文案潜台词**：... [二句话]

    """
    
    # 使用 Flash 模型
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([system_prompt, user_instruction, image])
    return response.text

# --- 5. 前端界面 ---
# 显示 Logo 和标题
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=50)
with col2:
    st.title("见心AI")

st.caption("上传朋友圈/小红书/抖音截图，AI 帮你一眼看穿本质。")

# 模式选择
mode = st.radio(
    "请选择观测人格：",
    ("🌶️ 锐评", "🔮 洞悉"),
    horizontal=True
)

# 文件上传
uploaded_file = st.file_uploader("点击上传截图...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='已上传', use_column_width=True)

    if st.button("开始分析 ⚡️", type="primary", use_container_width=True):
        if 'api_key' not in locals():
             st.error("API Key 未配置，无法运行。")
        else:
            with st.spinner('AI 正在连接神经网络...'):
                try:
                    mode_keyword = "锐评" if "锐评" in mode else "洞悉"
                    result = get_gemini_response(image, mode_keyword)
                    st.markdown("---")
                    st.markdown(result)
                    st.success("分析完成！截图分享给朋友吧！")
                except Exception as e:
                    st.error(f"连接超时，请重试。\n错误: {e}")

# --- 6. 底部引导安装 (关键步骤) ---
with st.expander("📲 如何把这个装到手机桌面上？"):
    st.markdown("""
    **iPhone 用户：**
    1. 点击 Safari 底部中间的 **分享按钮** (⬆️)。
    2. 下滑找到 **“添加到主屏幕”**。
    3. 点击右上角 **“添加”**。
    
    **Android 用户：**
    1. 点击浏览器右上角 **三个点**。
    2. 选择 **“添加到主屏幕”** 或 **“安装应用”**。
    """)
