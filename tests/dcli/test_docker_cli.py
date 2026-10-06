# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for tools/dcli/docker.py."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from tools.dcli.docker import (
    _check_docker_cli,
    app,
)

runner = CliRunner()


def test_check_docker_cli_found() -> None:
    """Test _check_docker_cli passes when docker is in PATH."""
    with patch("shutil.which", return_value="/usr/bin/docker"):
        _check_docker_cli()  # Should not raise


def test_status_running() -> None:
    """Test status output when Docker daemon is running."""
    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("tools.dcli.docker._is_daemon_running", return_value=True),
    ):
        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "Docker daemon is running" in result.output


def test_status_not_running() -> None:
    """Test status output when Docker daemon is stopped."""
    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("tools.dcli.docker._is_daemon_running", return_value=False),
    ):
        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "NOT running" in result.output


def test_build_slim_command() -> None:
    """Test 'docker build' default slim image build."""
    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("tools.dcli.docker._is_daemon_running", return_value=True),
        patch("tools.dcli.docker.run_command") as mock_run,
    ):
        result = runner.invoke(app, ["build"])
        assert result.exit_code == 0
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        cmd_str = " ".join(cmd)
        assert "tools/docker/Dockerfile.prod" in cmd
        assert "WITH_PDF=false" in cmd_str
        assert "WITH_ASSETS=false" in cmd_str
        assert "drawlib:slim" in cmd


def test_build_full_and_pdf_variants() -> None:
    """Test 'docker build --pdf', '--assets', and '--full' variants."""
    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("tools.dcli.docker._is_daemon_running", return_value=True),
        patch("tools.dcli.docker.run_command") as mock_run,
    ):
        res_pdf = runner.invoke(app, ["build", "--pdf"])
        assert res_pdf.exit_code == 0
        cmd_pdf = " ".join(mock_run.call_args[0][0])
        assert "WITH_PDF=true" in cmd_pdf
        assert "WITH_ASSETS=false" in cmd_pdf
        assert "drawlib:pdf" in cmd_pdf

        res_full = runner.invoke(app, ["build", "--full", "--pypi", "0.3.0"])
        assert res_full.exit_code == 0
        cmd_full = " ".join(mock_run.call_args[0][0])
        assert "WITH_PDF=true" in cmd_full
        assert "WITH_ASSETS=true" in cmd_full
        assert "INSTALL_SOURCE=pypi" in cmd_full
        assert "DRAWLIB_VERSION=0.3.0" in cmd_full
        assert "drawlib:full" in cmd_full


def test_test_local_command() -> None:
    """Test 'docker test' builds local test image and runs pytest container."""
    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("tools.dcli.docker._is_daemon_running", return_value=True),
        patch("tools.dcli.docker.run_command") as mock_run,
    ):
        result = runner.invoke(app, ["test", "--python", "3.12"])
        assert result.exit_code == 0
        assert mock_run.call_count == 2
        build_cmd = mock_run.call_args_list[0][0][0]
        run_cmd = mock_run.call_args_list[1][0][0]
        assert "tools/docker/Dockerfile.test_local" in build_cmd
        assert "test-drawlib:p3.12_local" in build_cmd
        assert run_cmd == ["docker", "run", "--rm", "test-drawlib:p3.12_local"]


def test_test_pypi_command() -> None:
    """Test 'docker test --pypi <VER>' builds PyPI test image and runs container."""
    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("tools.dcli.docker._is_daemon_running", return_value=True),
        patch("tools.dcli.docker.run_command") as mock_run,
    ):
        result = runner.invoke(app, ["test", "--pypi", "0.3.0"])
        assert result.exit_code == 0
        assert mock_run.call_count == 2
        build_cmd = " ".join(mock_run.call_args_list[0][0][0])
        run_cmd = mock_run.call_args_list[1][0][0]
        assert "tools/docker/Dockerfile.test_pypi" in build_cmd
        assert "DRAWLIB_VERSION=0.3.0" in build_cmd
        assert run_cmd == ["docker", "run", "--rm", "test-drawlib:p3.12_pypi_d0.3.0"]


def test_test_conflicting_flags() -> None:
    """Test 'docker test' rejects specifying both --pypi and --test-pypi."""
    result = runner.invoke(app, ["test", "--pypi", "0.3.0", "--test-pypi", "0.3.0"])
    assert result.exit_code == 1
    assert "Cannot specify both" in result.output


def test_list_command() -> None:
    """Test 'docker list' command invokes docker images with filters."""
    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("tools.dcli.docker.run_command") as mock_run,
    ):
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        mock_run.assert_called_once_with(
            [
                "docker",
                "images",
                "--filter",
                "reference=drawlib",
                "--filter",
                "reference=test-drawlib",
            ],
            desc="Listing drawlib Docker images...",
        )


def test_prune_command() -> None:
    """Test 'docker prune' command removes docker images when found."""
    mock_proc = MagicMock()
    mock_proc.stdout = "img1\nimg2\nimg1\n"

    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("subprocess.run", return_value=mock_proc),
        patch("tools.dcli.docker.run_command") as mock_run,
    ):
        result = runner.invoke(app, ["prune"])
        assert result.exit_code == 0
        mock_run.assert_called_once_with(
            ["docker", "rmi", "-f", "img1", "img2"],
            desc="Removing drawlib Docker images...",
        )
