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
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import AiIcon, ArchitectureDiagram, Node
from drawlib.diagrams.sequence import Participant, SequenceDiagram
from drawlib.icons import ai
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

    def test_ai_aliases(self, tmp_path: Path) -> None:
        """Verify AI shorthand aliases (anthropic, chatgpt, hf, llama, sk, sklearn, tf)."""
        clear()
        ai.anthropic(xy=(15, 60), width=12, style=Style())
        ai.chatgpt(xy=(35, 60), width=12, style=Style())
        ai.hf(xy=(55, 60), width=12, style=Style())
        ai.llama(xy=(75, 60), width=12, style=Style())

        ai.sk(xy=(20, 30), width=12, style=Style())
        ai.sklearn(xy=(45, 30), width=12, style=Style())
        ai.tf(xy=(70, 30), width=12, style=Style())

        out = tmp_path / "test_ai_aliases.png"
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
