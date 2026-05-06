import os
import re
from dataclasses import dataclass

from .prompts import SYSTEM_PROMPT, build_user_prompt


@dataclass(frozen=True)
class SummarizerConfig:
    model: str = "gpt-5.2"
    max_bullets: int = 6
    tone: str = "简洁"
    use_ai: bool = True


def summarize_notes(notes: str, config: SummarizerConfig | None = None) -> str:
    config = config or SummarizerConfig()
    cleaned_notes = notes.strip()
    if not cleaned_notes:
        raise ValueError("notes must not be empty")

    if config.use_ai and os.getenv("OPENAI_API_KEY"):
        return _summarize_with_openai(cleaned_notes, config)

    return _summarize_locally(cleaned_notes, config)


def _summarize_with_openai(notes: str, config: SummarizerConfig) -> str:
    from openai import OpenAI

    client = OpenAI()
    response = client.responses.create(
        model=config.model,
        instructions=SYSTEM_PROMPT,
        input=build_user_prompt(notes, config.max_bullets, config.tone),
    )
    return response.output_text.strip()


def _summarize_locally(notes: str, config: SummarizerConfig) -> str:
    sentences = _split_sentences(notes)
    bullets = _extract_bullets(notes)
    candidates = bullets or sentences
    key_points = candidates[: config.max_bullets]
    todos = _extract_todos(candidates)
    risks = _extract_risks(candidates)

    overview_source = " ".join(sentences[:2]) if sentences else notes[:120]
    overview = overview_source.strip()

    return "\n".join(
        [
            "## 概览",
            overview or "已根据输入内容生成本地演示总结。",
            "",
            "## 关键要点",
            *[f"- {point}" for point in key_points],
            "",
            "## 待办事项",
            *([f"- {todo}" for todo in todos] or ["- 待确认：根据关键要点补充下一步行动。"]),
            "",
            "## 风险或需要确认的问题",
            *([f"- {risk}" for risk in risks] or ["- 暂未从文本中识别出明显风险。"]),
            "",
            "> 当前为本地演示模式。配置 `OPENAI_API_KEY` 后可获得更自然的 AI 总结。",
        ]
    )


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[。！？!?；;])\s+|\n+", text)
    return [part.strip(" -\t") for part in parts if part.strip(" -\t")]


def _extract_bullets(text: str) -> list[str]:
    bullets: list[str] = []
    for line in text.splitlines():
        normalized = line.strip()
        if re.match(r"^([-*+]|\d+[.)、])\s+", normalized):
            bullets.append(re.sub(r"^([-*+]|\d+[.)、])\s+", "", normalized).strip())
    return bullets


def _extract_todos(items: list[str]) -> list[str]:
    keywords = ("计划", "需要", "待", "下周", "todo", "TODO", "补充", "接入", "排查", "完成")
    return [f"待确认：{item}" for item in items if any(keyword in item for keyword in keywords)]


def _extract_risks(items: list[str]) -> list[str]:
    keywords = ("风险", "问题", "阻塞", "没有", "未", "乱码", "失败", "延迟", "bug", "Bug")
    return [item for item in items if any(keyword in item for keyword in keywords)]
