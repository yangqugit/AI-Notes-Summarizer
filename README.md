<!--
╔══════════════════════════════════════════════════════════════════════╗
║  DreamSeed 种梦计划 — AI创造者大赛  官方 README 模板                ║
║                                                                      ║
║  使用说明：                                                          ║
║  1. 将本模板放在参赛仓库根目录 README.md 的顶部                       ║
║  2. 头图使用 DreamField 官方公开活动图片地址                         ║
║  3. 请保留 DREAMFIELD_README_HEADER_START / END 标识                 ║
║  4. 分割线以下供创作者自由编写项目内容                               ║
╚══════════════════════════════════════════════════════════════════════╝
-->

<!-- DREAMFIELD_README_HEADER_START -->

<p align="center">
  <a href="https://www.dreamfield.top">
    <img src="https://www.dreamfield.top/dream-field/contest-readme/assets/dreamseed-readme-banner.png" alt="DreamSeed 种梦计划参赛作品" width="100%" />
  </a>
</p>

<!-- DREAMFIELD_README_HEADER_END -->

# AI Notes Summarizer

一个使用 Python 和 Streamlit 构建的 AI 笔记总结工具。它可以把会议纪要、课堂笔记、访谈记录或长文本整理成中文摘要、关键要点、待办事项和风险问题。

项目适合作为 GitHub 上的 AI 入门项目：结构清晰、功能完整，并且没有 API Key 时也能使用本地演示模式。

## 功能

- 粘贴长文本并生成结构化中文总结
- 上传 `.txt` 或 `.md` 文件
- 输出概览、关键要点、待办事项、风险或待确认问题
- 支持下载 Markdown 总结
- 支持 OpenAI API
- 未配置 API Key 时自动使用本地演示模式

## 技术栈

- Python
- Streamlit
- OpenAI Python SDK
- python-dotenv
- pytest

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/ai-notes-summarizer.git
cd ai-notes-summarizer
```

如果你是在本地刚创建项目，可以直接进入项目目录。

### 2. 创建虚拟环境

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux：

```bash
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制示例环境变量文件：

```bash
cp .env.example .env
```

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

然后编辑 `.env`：

```env
OPENAI_API_KEY=你的_OpenAI_API_Key
OPENAI_MODEL=gpt-5.2
```

如果你暂时没有 API Key，也可以跳过这一步，应用会自动进入本地演示模式。

### 5. 启动应用

```bash
streamlit run app.py
```

浏览器打开终端显示的本地地址，一般是：

```text
http://localhost:8501
```

## 运行测试

```bash
pytest
```

## 项目结构

```text
ai-notes-summarizer/
├── app.py
├── src/
│   ├── __init__.py
│   ├── prompts.py
│   └── summarizer.py
├── tests/
│   └── test_summarizer.py
├── examples/
│   └── sample_notes.md
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## GitHub 上传建议

```bash
git init
git add .
git commit -m "Initial commit"
```

然后在 GitHub 创建一个新仓库，比如 `ai-notes-summarizer`，再执行：

```bash
git remote add origin https://github.com/你的用户名/ai-notes-summarizer.git
git branch -M main
git push -u origin main
```

## 后续可扩展方向

- 增加 PDF / Word 文档上传
- 增加多语言总结
- 增加总结历史记录
- 增加标签、优先级和负责人识别
- 部署到 Streamlit Community Cloud
