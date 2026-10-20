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
from drawlib.diagrams.architecture import ArchitectureDiagram, AwsIcon, AzureIcon, Node, OriginalCloudIcon
from drawlib.icons import aws, azure, original_cloud
from drawlib.styles import Styles
from drawlib.types import Style


class TestAwsAndAzureIcons:
    """Tests for AWS, Azure, and Original Cloud icon providers and architecture diagram enums."""

    def test_aws_icons(self, tmp_path: Path) -> None:
        """Verify AWS service icons and category icons."""
        clear()
        aws.ec2(xy=(20, 70), width=15, style=Style())
        aws.simple_storage_service(xy=(40, 70), width=15, style=Style())
        aws.aws_lambda(xy=(60, 70), width=15, style=Style())
        aws.elastic_kubernetes_service(xy=(80, 70), width=15, style=Style())
        aws.rds(xy=(20, 30), width=15, style=Style())
        aws.dynamodb(xy=(40, 30), width=15, style=Style())
        aws.category_compute(xy=(60, 30), width=15, style=Style())
        aws.virtual_private_cloud(xy=(80, 30), width=15, style=Style())
        out = tmp_path / "test_aws.png"
        save(str(out))
        assert out.is_file()

    def test_azure_icons(self, tmp_path: Path) -> None:
        """Verify Azure service icons."""
        clear()
        azure.virtual_machine(xy=(20, 70), width=15, style=Style())
        azure.kubernetes_services(xy=(40, 70), width=15, style=Style())
        azure.function_apps(xy=(60, 70), width=15, style=Style())
        azure.openai(xy=(80, 70), width=15, style=Style())
        azure.cosmos_db(xy=(20, 30), width=15, style=Style())
        azure.sql_database(xy=(40, 30), width=15, style=Style())
        azure.entra_id(xy=(60, 30), width=15, style=Style())
        azure.key_vaults(xy=(80, 30), width=15, style=Style())
        out = tmp_path / "test_azure.png"
        save(str(out))
        assert out.is_file()

    def test_original_cloud_reorganized_icons(self, tmp_path: Path) -> None:
        """Verify newly added and renamed Original Cloud canonical icons."""
        clear()
        original_cloud.gpu_node(xy=(15, 75), width=12, style=Style())
        original_cloud.gpu_cluster(xy=(35, 75), width=12, style=Style())
        original_cloud.npu_node(xy=(55, 75), width=12, style=Style())
        original_cloud.bare_metal(xy=(75, 75), width=12, style=Style())
        original_cloud.virtualization_host(xy=(15, 50), width=12, style=Style())
        original_cloud.virtualization_cluster(xy=(35, 50), width=12, style=Style())
        original_cloud.virtualization_controller(xy=(55, 50), width=12, style=Style())
        original_cloud.directory_service(xy=(75, 50), width=12, style=Style())
        original_cloud.internet_gateway(xy=(15, 25), width=12, style=Style())
        original_cloud.nat_gateway(xy=(35, 25), width=12, style=Style())
        original_cloud.time_series_database(xy=(55, 25), width=12, style=Style())
        original_cloud.ids_ips(xy=(75, 25), width=12, style=Style())
        out = tmp_path / "test_original_cloud.png"
        save(str(out))
        assert out.is_file()

    def test_aws_azure_architecture_diagram_enums(self, tmp_path: Path) -> None:
        """Verify AwsIcon, AzureIcon, and OriginalCloudIcon work inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("EC2", width=20, height=20, icon=AwsIcon.EC2), (20, 50))
        n2 = diag.add(Node("AKS", width=20, height=20, icon=AzureIcon.KUBERNETES_SERVICES), (50, 50))
        n3 = diag.add(Node("NPU", width=20, height=20, icon=OriginalCloudIcon.NPU_NODE), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_aws_azure.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_aws_azure_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid AWS or Azure icon file."""
        with pytest.raises(FileNotFoundError):
            AWS_PROVIDER.get_icon_path("non_existent_aws_icon_xyz")
        with pytest.raises(FileNotFoundError):
            AZURE_PROVIDER.get_icon_path("non_existent_azure_icon_xyz")
