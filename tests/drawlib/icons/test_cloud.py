# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Cloud and Original Cloud brand icons."""

from pathlib import Path

from drawlib._icons.png_icons.cloud._base import CLOUD_PROVIDER
from drawlib._icons.png_icons.original_cloud._base import ORIGINAL_CLOUD_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, CloudIcon, Node, OriginalCloudIcon
from drawlib.icons import cloud, original_cloud
from drawlib.styles import Styles
from drawlib.types import Style


class TestCloudIcons:
    """Tests for official Cloud icon provider and diagram enum."""

    def test_cloud_all_icons(self, tmp_path: Path) -> None:
        """Verify all 40 official cloud brand icons render cleanly."""
        clear()
        names = [
            "aws",
            "google_cloud",
            "azure",
            "oracle_cloud",
            "ibm_cloud",
            "alibaba_cloud",
            "tencent_cloud",
            "huawei_cloud",
            "amazon",
            "google",
            "microsoft",
            "oracle",
            "ibm",
            "alibaba",
            "tencent",
            "huawei",
            "cloudflare",
            "fastly",
            "akamai",
            "digitalocean",
            "linode",
            "vultr",
            "hetzner",
            "ovhcloud",
            "scaleway",
            "ionos",
            "vercel",
            "netlify",
            "heroku",
            "render",
            "fly_io",
            "railway",
            "firebase",
            "supabase",
            "sakura",
            "conoha",
            "xserver",
            "nifcloud",
            "idcf",
            "kagoya",
        ]
        for idx, name in enumerate(names):
            col = idx % 8
            row = idx // 8
            fn = getattr(cloud, name)
            fn(xy=(8 + col * 11, 82 - row * 16), width=8, style=Style(), variant="default")

        out = tmp_path / "test_cloud_all.png"
        save(str(out))
        assert out.is_file()

    def test_cloud_architecture_enum(self, tmp_path: Path) -> None:
        """Verify CloudIcon and OriginalCloudIcon work inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("Cloudflare", width=20, height=20, icon=CloudIcon.CLOUDFLARE), (20, 60))
        n2 = diag.add(Node("AWS", width=20, height=20, icon=CloudIcon.AWS), (50, 60))
        n3 = diag.add(Node("Multi-Cloud", width=20, height=20, icon=OriginalCloudIcon.MULTI_CLOUD), (80, 60))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_cloud.png"
        save(str(out))
        assert out.is_file()

    def test_cloud_provider_metadata(self) -> None:
        """Verify provider package name."""
        assert CLOUD_PROVIDER.name == "cloud"
        assert CLOUD_PROVIDER.package_name == "icon_cloud"
        assert ORIGINAL_CLOUD_PROVIDER.name == "original_cloud"
        assert ORIGINAL_CLOUD_PROVIDER.package_name == "icon_original_cloud"

    def test_original_cloud_pure_and_brand_icons(self, tmp_path: Path) -> None:
        """Verify new pure cloud concepts and brand icons in original_cloud."""
        clear()
        original_cloud.cloud(xy=(12, 70), width=9, style=Style())
        original_cloud.public_cloud(xy=(28, 70), width=9, style=Style())
        original_cloud.private_cloud(xy=(44, 70), width=9, style=Style())
        original_cloud.hybrid_cloud(xy=(60, 70), width=9, style=Style())
        original_cloud.multi_cloud(xy=(76, 70), width=9, style=Style())

        original_cloud.aws(xy=(12, 40), width=9, style=Style())
        original_cloud.google_cloud(xy=(28, 40), width=9, style=Style())
        original_cloud.azure(xy=(44, 40), width=9, style=Style())
        original_cloud.cloudflare(xy=(60, 40), width=9, style=Style())
        original_cloud.sakura(xy=(76, 40), width=9, style=Style())

        out = tmp_path / "test_original_cloud_new.png"
        save(str(out))
        assert out.is_file()
