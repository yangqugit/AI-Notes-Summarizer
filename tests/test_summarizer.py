import pytest

from src.summarizer import SummarizerConfig, summarize_notes


def test_local_summary_contains_expected_sections():
    notes = """
    - 本周完成登录页面。
    - 导出 CSV 有中文乱码，需要排查。
    - 下周计划补充端到端测试。
    """

    result = summarize_notes(notes, SummarizerConfig(use_ai=False, max_bullets=3))

    assert "## 概览" in result
    assert "## 关键要点" in result
    assert "## 待办事项" in result
    assert "## 风险或需要确认的问题" in result
    assert "CSV" in result


def test_empty_notes_raise_error():
    with pytest.raises(ValueError):
        summarize_notes("   ", SummarizerConfig(use_ai=False))
