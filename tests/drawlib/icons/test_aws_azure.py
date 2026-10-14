# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for AWS and Azure icons drawing."""

from pathlib import Path

import pytest

from drawlib._icons.png_icons.aws._base import AWS_PROVIDER
from drawlib._icons.png_icons.azure._base import AZURE_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, AwsIcon, AzureIcon, Node
from drawlib.icons import aws, azure
from drawlib.styles import Styles
from drawlib.types import Style


class TestAwsAndAzureIcons:
    """Tests for AWS and Azure icon providers and architecture diagram enums."""

    def test_aws_icons_and_aliases(self, tmp_path: Path) -> None:
        """Verify AWS service icons, category icons, and shorthand aliases."""
        clear()
        aws.ec2(xy=(20, 70), width=15, style=Style())
        aws.s3(xy=(40, 70), width=15, style=Style())
        aws.aws_lambda(xy=(60, 70), width=15, style=Style())
        aws.lambda_function(xy=(80, 70), width=15, style=Style())
        aws.rds(xy=(20, 30), width=15, style=Style())
        aws.dynamodb(xy=(40, 30), width=15, style=Style())
        aws.category_compute(xy=(60, 30), width=15, style=Style())
        aws.vpc(xy=(80, 30), width=15, style=Style())
        out = tmp_path / "test_aws.png"
        save(str(out))
        assert out.is_file()

    def test_azure_icons_and_aliases(self, tmp_path: Path) -> None:
        """Verify Azure service icons and shorthand aliases."""
        clear()
        azure.virtual_machine(xy=(20, 70), width=15, style=Style())
        azure.vm(xy=(40, 70), width=15, style=Style())
        azure.aks(xy=(60, 70), width=15, style=Style())
        azure.openai(xy=(80, 70), width=15, style=Style())
        azure.cosmos_db(xy=(20, 30), width=15, style=Style())
        azure.sql_database(xy=(40, 30), width=15, style=Style())
        azure.aad(xy=(60, 30), width=15, style=Style())
        azure.key_vault(xy=(80, 30), width=15, style=Style())
        out = tmp_path / "test_azure.png"
        save(str(out))
        assert out.is_file()

    def test_aws_azure_architecture_diagram_enums(self, tmp_path: Path) -> None:
        """Verify AwsIcon and AzureIcon work inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("EC2", width=20, height=20, icon=AwsIcon.EC2), (25, 50))
        n2 = diag.add(Node("AKS", width=20, height=20, icon=AzureIcon.AKS), (75, 50))
        diag.connect(n1, n2)
        diag.draw((10, 10))
        out = tmp_path / "test_arch_aws_azure.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_aws_azure_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid AWS or Azure icon file."""
        with pytest.raises(FileNotFoundError):
            AWS_PROVIDER.get_icon_path("non_existent_aws_icon_xyz")
        with pytest.raises(FileNotFoundError):
            AZURE_PROVIDER.get_icon_path("non_existent_azure_icon_xyz")
