# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Official AI & ML ecosystem icons drawing."""

from pathlib import Path

import pytest

from drawlib._icons.png_icons.ai._base import AI_PROVIDER
from drawlib._icons.png_icons.original_ai._base import ORIGINAL_AI_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import AiIcon, ArchitectureDiagram, Node, OriginalAiIcon
from drawlib.diagrams.sequence import Participant, SequenceDiagram
from drawlib.icons import ai, original_ai
from drawlib.styles import Styles
from drawlib.types import Style


class TestAiIcons:
    """Tests for AI icon provider, aliases, and diagram enums."""

    def test_ai_llm_and_agent_icons(self, tmp_path: Path) -> None:
        """Verify LLM provider and Agent framework icons."""
        clear()
        ai.openai(xy=(15, 75), width=12, style=Style(), variant="default")
        ai.claude(xy=(35, 75), width=12, style=Style())
        ai.gemini(xy=(55, 75), width=12, style=Style())
        ai.meta_llama(xy=(75, 75), width=12, style=Style())

        ai.langchain(xy=(15, 50), width=12, style=Style())
        ai.langgraph(xy=(35, 50), width=12, style=Style())
        ai.llamaindex(xy=(55, 50), width=12, style=Style())
        ai.semantic_kernel(xy=(75, 50), width=12, style=Style())

        ai.mcp(xy=(15, 25), width=12, style=Style())
        ai.a2a(xy=(35, 25), width=12, style=Style())
        ai.huggingface(xy=(55, 25), width=12, style=Style())
        ai.ollama(xy=(75, 25), width=12, style=Style())

        out = tmp_path / "test_ai_llm_agent.png"
        save(str(out))
        assert out.is_file()

    def test_ai_ml_and_mlops_icons(self, tmp_path: Path) -> None:
        """Verify ML library, MLOps, and UI icons."""
        clear()
        ai.pytorch(xy=(15, 65), width=12, style=Style())
        ai.tensorflow(xy=(35, 65), width=12, style=Style())
        ai.jax(xy=(55, 65), width=12, style=Style())
        ai.scikit_learn(xy=(75, 65), width=12, style=Style())

        ai.mlflow(xy=(15, 35), width=12, style=Style())
        ai.wandb(xy=(35, 35), width=12, style=Style())
        ai.gradio(xy=(55, 35), width=12, style=Style())
        ai.nvidia(xy=(75, 35), width=12, style=Style())

        out = tmp_path / "test_ai_ml_mlops.png"
        save(str(out))
        assert out.is_file()

    def test_ai_architecture_diagram_enum(self, tmp_path: Path) -> None:
        """Verify AiIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("LangGraph", width=22, height=20, icon=AiIcon.LANGGRAPH), (20, 50))
        n2 = diag.add(Node("MCP Server", width=22, height=20, icon=AiIcon.MCP), (50, 50))
        n3 = diag.add(Node("Claude", width=22, height=20, icon=AiIcon.CLAUDE), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_ai.png"
        save(str(out))
        assert out.is_file()

    def test_ai_sequence_diagram_enum(self, tmp_path: Path) -> None:
        """Verify AiIcon works inside SequenceDiagram participants."""
        clear()
        seq = SequenceDiagram(
            node_style=Styles.Neutral,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        p1 = seq.add(Participant("OpenHands", icon=AiIcon.OPENHANDS))
        p2 = seq.add(Participant("Gemini", icon=AiIcon.GEMINI))
        seq.request(p1, p2, "Generate patch")
        seq.draw((10, 10))
        out = tmp_path / "test_seq_ai.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_ai_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid AI icon file."""
        with pytest.raises(FileNotFoundError):
            AI_PROVIDER.get_icon_path("non_existent_ai_icon_xyz")

    def test_original_ai_stylized_icons(self, tmp_path: Path) -> None:
        """Verify Drawlib-stylized Original AI icons."""
        clear()
        original_ai.openai(xy=(15, 75), width=12, style=Style())
        original_ai.claude(xy=(35, 75), width=12, style=Style())
        original_ai.gemini(xy=(55, 75), width=12, style=Style())
        original_ai.mcp(xy=(75, 75), width=12, style=Style())

        original_ai.ai_agent(xy=(15, 45), width=12, style=Style())
        original_ai.langchain(xy=(35, 45), width=12, style=Style())
        original_ai.semantic_kernel(xy=(55, 45), width=12, style=Style())
        original_ai.llamaindex(xy=(75, 45), width=12, style=Style())

        diag = ArchitectureDiagram(
            node_style=Styles.Neutral,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("Agent", width=22, height=20, icon=OriginalAiIcon.AI_AGENT), (25, 18))
        n2 = diag.add(Node("LlamaIndex", width=22, height=20, icon=OriginalAiIcon.LLAMAINDEX), (65, 18))
        diag.connect(n1, n2)
        diag.draw((5, 5))

        out = tmp_path / "test_original_ai_stylized.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_original_ai_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid Original AI icon file."""
        with pytest.raises(FileNotFoundError):
            ORIGINAL_AI_PROVIDER.get_icon_path("non_existent_original_ai_icon_xyz")
