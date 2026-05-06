import os

import streamlit as st
from dotenv import load_dotenv

from src.summarizer import SummarizerConfig, summarize_notes


load_dotenv()

st.set_page_config(
    page_title="AI Notes Summarizer",
    page_icon="📝",
    layout="wide",
)

st.title("AI Notes Summarizer")
st.caption("把会议纪要、课堂笔记或长文本快速整理成摘要、要点和待办事项。")

with st.sidebar:
    st.header("设置")
    model = st.text_input("OpenAI 模型", value=os.getenv("OPENAI_MODEL", "gpt-5.2"))
    max_bullets = st.slider("最多要点数", min_value=3, max_value=10, value=6)
    tone = st.selectbox("输出风格", ["简洁", "详细", "行动导向"], index=0)
    use_ai = st.toggle(
        "使用 OpenAI API",
        value=bool(os.getenv("OPENAI_API_KEY")),
        help="未配置 OPENAI_API_KEY 时会自动使用本地演示模式。",
    )

sample_text = """项目周会记录：
- 本周完成了登录页面和用户资料页的初版。
- 数据库迁移脚本还没有合并，需要后端同学再 review 一次。
- 有用户反馈导出 CSV 时中文乱码，需要优先排查编码问题。
- 下周计划接入支付回调，并补充端到端测试。
- 产品希望首页增加一个简短的新手引导，避免新用户迷路。
"""

notes = st.text_area(
    "输入笔记内容",
    value=sample_text,
    height=280,
    placeholder="粘贴会议纪要、课堂笔记、访谈记录或任何长文本...",
)

uploaded_file = st.file_uploader("或上传 .txt / .md 文件", type=["txt", "md"])
if uploaded_file is not None:
    notes = uploaded_file.read().decode("utf-8", errors="ignore")
    st.text_area("已读取文件内容", value=notes, height=220)

col_generate, col_clear = st.columns([1, 5])
generate = col_generate.button("生成总结", type="primary", use_container_width=True)
clear = col_clear.button("清空", use_container_width=False)

if clear:
    st.rerun()

if generate:
    if not notes.strip():
        st.warning("请先输入或上传笔记内容。")
    else:
        config = SummarizerConfig(
            model=model.strip() or "gpt-5.2",
            max_bullets=max_bullets,
            tone=tone,
            use_ai=use_ai,
        )
        with st.spinner("正在整理笔记..."):
            result = summarize_notes(notes, config)

        st.subheader("总结结果")
        st.markdown(result)

        st.download_button(
            "下载 Markdown",
            data=result,
            file_name="notes-summary.md",
            mime="text/markdown",
        )
