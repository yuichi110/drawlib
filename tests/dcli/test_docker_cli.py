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
    _is_daemon_running,
    app,
)

runner = CliRunner()


def test_check_docker_cli_found() -> None:
    """Test _check_docker_cli passes when docker is in PATH."""
    with patch("shutil.which", return_value="/usr/bin/docker"):
        _check_docker_cli()  # Should not raise


def test_daemon_status_running() -> None:
    """Test status output when Docker daemon is running."""
    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("tools.dcli.docker._is_daemon_running", return_value=True),
    ):
        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "Docker daemon is running" in result.output


def test_daemon_status_not_running() -> None:
    """Test daemon-status output when Docker daemon is stopped."""
    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("tools.dcli.docker._is_daemon_running", return_value=False),
    ):
        result = runner.invoke(app, ["daemon-status"])
        assert result.exit_code == 0
        assert "NOT running" in result.output


def test_build_image_command() -> None:
    """Test build-image command constructs docker build correctly."""
    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("tools.dcli.docker._is_daemon_running", return_value=True),
        patch("tools.dcli.docker.run_command") as mock_run,
    ):
        result = runner.invoke(app, ["build-image", "-v", "0.3.0", "--python", "3.12"])
        assert result.exit_code == 0
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "docker" in cmd
        assert "build" in cmd
        assert "tools/docker/Dockerfile.pypi_test" in cmd
        assert "DRAWLIB_VERSION=0.3.0" in " ".join(cmd)


def test_list_images_command() -> None:
    """Test list-images command invokes docker images."""
    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("tools.dcli.docker.run_command") as mock_run,
    ):
        result = runner.invoke(app, ["list-images"])
        assert result.exit_code == 0
        mock_run.assert_called_once_with(["docker", "images", "test-drawlib"], desc="Listing test-drawlib images...")


def test_prune_images_command() -> None:
    """Test prune-images command removes docker images when found."""
    mock_proc = MagicMock()
    mock_proc.stdout = "img1\nimg2\n"

    with (
        patch("shutil.which", return_value="/usr/bin/docker"),
        patch("subprocess.run", return_value=mock_proc),
        patch("tools.dcli.docker.run_command") as mock_run,
    ):
        result = runner.invoke(app, ["prune-images"])
        assert result.exit_code == 0
        mock_run.assert_called_once_with(["docker", "rmi", "img1", "img2"], desc="Removing test-drawlib images...")
