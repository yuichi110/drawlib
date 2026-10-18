# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Cloud Native (Kubernetes & CNCF ecosystem) icons drawing."""

from pathlib import Path

import pytest

from drawlib._icons.png_icons.cnative._base import CNATIVE_PROVIDER
from drawlib._icons.png_icons.original_cnative._base import ORIGINAL_CNATIVE_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, CnativeIcon, Node, OriginalCnativeIcon
from drawlib.diagrams.sequence import Participant, SequenceDiagram
from drawlib.icons import cnative, original_cnative
from drawlib.styles import Styles
from drawlib.types import Style


class TestCnativeIcons:
    """Tests for Cloud Native icon provider, aliases, and diagram enums."""

    def test_cnative_k8s_icons(self, tmp_path: Path) -> None:
        """Verify Kubernetes resource and control-plane icons."""
        clear()
        cnative.k8s_control_plane(xy=(15, 75), width=12, style=Style(), variant="default")
        cnative.k8s_api_server(xy=(35, 75), width=12, style=Style())
        cnative.k8s_node(xy=(55, 75), width=12, style=Style())
        cnative.k8s_namespace(xy=(75, 75), width=12, style=Style())

        cnative.k8s_pod(xy=(15, 50), width=12, style=Style())
        cnative.k8s_deployment(xy=(35, 50), width=12, style=Style())
        cnative.k8s_statefulset(xy=(55, 50), width=12, style=Style())
        cnative.k8s_daemonset(xy=(75, 50), width=12, style=Style())

        cnative.k8s_service(xy=(15, 25), width=12, style=Style())
        cnative.k8s_ingress(xy=(35, 25), width=12, style=Style())
        cnative.k8s_configmap(xy=(55, 25), width=12, style=Style())
        cnative.k8s_secret(xy=(75, 25), width=12, style=Style())

        out = tmp_path / "test_cnative_k8s.png"
        save(str(out))
        assert out.is_file()

    def test_cnative_project_icons(self, tmp_path: Path) -> None:
        """Verify CNCF and Cloud Native ecosystem project icons."""
        clear()
        cnative.kubernetes(xy=(15, 75), width=12, style=Style(), variant="default")
        cnative.prometheus(xy=(35, 75), width=12, style=Style())
        cnative.grafana(xy=(55, 75), width=12, style=Style())
        cnative.opentelemetry(xy=(75, 75), width=12, style=Style())

        cnative.argo(xy=(15, 50), width=12, style=Style())
        cnative.flux(xy=(35, 50), width=12, style=Style())
        cnative.helm(xy=(55, 50), width=12, style=Style())
        cnative.istio(xy=(75, 50), width=12, style=Style())

        cnative.cilium(xy=(15, 25), width=12, style=Style())
        cnative.envoy(xy=(35, 25), width=12, style=Style())
        cnative.crossplane(xy=(55, 25), width=12, style=Style())
        cnative.knative(xy=(75, 25), width=12, style=Style())

        out = tmp_path / "test_cnative_projects.png"
        save(str(out))
        assert out.is_file()

    def test_cnative_aliases(self, tmp_path: Path) -> None:
        """Verify Cloud Native shorthand aliases (pod, deploy, svc, k8s, otel, argocd)."""
        clear()
        cnative.pod(xy=(20, 60), width=12, style=Style())
        cnative.deploy(xy=(40, 60), width=12, style=Style())
        cnative.svc(xy=(60, 60), width=12, style=Style())
        cnative.ing(xy=(80, 60), width=12, style=Style())

        cnative.k8s(xy=(20, 30), width=12, style=Style())
        cnative.otel(xy=(40, 30), width=12, style=Style())
        cnative.argocd(xy=(60, 30), width=12, style=Style())
        cnative.gatekeeper(xy=(80, 30), width=12, style=Style())

        out = tmp_path / "test_cnative_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_cnative_k8s_distributions(self, tmp_path: Path) -> None:
        """Verify Kubernetes distribution icons and their shorthand aliases."""
        clear()
        cnative.openshift(xy=(15, 75), width=10, style=Style())
        cnative.rancher(xy=(35, 75), width=10, style=Style())
        cnative.tanzu(xy=(55, 75), width=10, style=Style())
        cnative.okd(xy=(75, 75), width=10, style=Style())

        cnative.k3s(xy=(15, 50), width=10, style=Style())
        cnative.microk8s(xy=(35, 50), width=10, style=Style())
        cnative.talos(xy=(55, 50), width=10, style=Style())
        cnative.k0s(xy=(75, 50), width=10, style=Style())

        cnative.minikube(xy=(15, 25), width=10, style=Style())
        cnative.kind(xy=(35, 25), width=10, style=Style())
        cnative.kubevirt(xy=(55, 25), width=10, style=Style())
        cnative.vcluster(xy=(75, 25), width=10, style=Style())

        # Shorthand aliases
        cnative.ocp(xy=(15, 10), width=8, style=Style())
        cnative.rke(xy=(30, 10), width=8, style=Style())
        cnative.rke2(xy=(45, 10), width=8, style=Style())
        cnative.tkg(xy=(60, 10), width=8, style=Style())
        cnative.talos_linux(xy=(75, 10), width=8, style=Style())

        out = tmp_path / "test_cnative_k8s_distros.png"
        save(str(out))
        assert out.is_file()

    def test_cnative_architecture_diagram_enum(self, tmp_path: Path) -> None:
        """Verify CnativeIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("Ingress", width=20, height=20, icon=CnativeIcon.K8S_INGRESS), (20, 50))
        n2 = diag.add(Node("Service", width=20, height=20, icon=CnativeIcon.K8S_SERVICE), (50, 50))
        n3 = diag.add(Node("Pod", width=20, height=20, icon=CnativeIcon.K8S_POD), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_cnative.png"
        save(str(out))
        assert out.is_file()

    def test_cnative_sequence_diagram_enum(self, tmp_path: Path) -> None:
        """Verify CnativeIcon works inside SequenceDiagram participants."""
        clear()
        seq = SequenceDiagram(
            node_style=Styles.Neutral,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        p1 = seq.add(Participant("Argo CD", icon=CnativeIcon.ARGO))
        p2 = seq.add(Participant("API Server", icon=CnativeIcon.K8S_API_SERVER))
        seq.request(p1, p2, "Sync manifest")
        seq.draw((10, 10))
        out = tmp_path / "test_seq_cnative.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_cnative_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid Cloud Native icon file."""
        with pytest.raises(FileNotFoundError):
            CNATIVE_PROVIDER.get_icon_path("non_existent_cnative_icon_xyz")


class TestOriginalCnativeIcons:
    """Tests for Drawlib Original Cloud Native icon provider, aliases, and diagram enums."""

    def test_original_cnative_k8s_icons(self, tmp_path: Path) -> None:
        """Verify Original Kubernetes resource and control-plane icons."""
        clear()
        original_cnative.k8s_control_plane(xy=(15, 75), width=12, style=Style(), variant="default")
        original_cnative.k8s_api_server(xy=(35, 75), width=12, style=Style())
        original_cnative.k8s_node(xy=(55, 75), width=12, style=Style())
        original_cnative.k8s_namespace(xy=(75, 75), width=12, style=Style())

        original_cnative.k8s_pod(xy=(15, 50), width=12, style=Style())
        original_cnative.k8s_deployment(xy=(35, 50), width=12, style=Style())
        original_cnative.k8s_statefulset(xy=(55, 50), width=12, style=Style())
        original_cnative.k8s_daemonset(xy=(75, 50), width=12, style=Style())

        original_cnative.k8s_service(xy=(15, 25), width=12, style=Style())
        original_cnative.k8s_ingress(xy=(35, 25), width=12, style=Style())
        original_cnative.k8s_configmap(xy=(55, 25), width=12, style=Style())
        original_cnative.k8s_secret(xy=(75, 25), width=12, style=Style())

        out = tmp_path / "test_original_cnative_k8s.png"
        save(str(out))
        assert out.is_file()

    def test_original_cnative_project_icons(self, tmp_path: Path) -> None:
        """Verify Original CNCF and Cloud Native ecosystem project icons."""
        clear()
        original_cnative.kubernetes(xy=(15, 75), width=12, style=Style(), variant="default")
        original_cnative.prometheus(xy=(35, 75), width=12, style=Style())
        original_cnative.grafana(xy=(55, 75), width=12, style=Style())
        original_cnative.opentelemetry(xy=(75, 75), width=12, style=Style())

        original_cnative.argo(xy=(15, 50), width=12, style=Style())
        original_cnative.flux(xy=(35, 50), width=12, style=Style())
        original_cnative.helm(xy=(55, 50), width=12, style=Style())
        original_cnative.istio(xy=(75, 50), width=12, style=Style())

        original_cnative.cilium(xy=(15, 25), width=12, style=Style())
        original_cnative.envoy(xy=(35, 25), width=12, style=Style())
        original_cnative.crossplane(xy=(55, 25), width=12, style=Style())
        original_cnative.knative(xy=(75, 25), width=12, style=Style())

        out = tmp_path / "test_original_cnative_projects.png"
        save(str(out))
        assert out.is_file()

    def test_original_cnative_aliases(self, tmp_path: Path) -> None:
        """Verify Original Cloud Native shorthand aliases (pod, deploy, svc, k8s, otel, argocd)."""
        clear()
        original_cnative.pod(xy=(20, 60), width=12, style=Style())
        original_cnative.deploy(xy=(40, 60), width=12, style=Style())
        original_cnative.svc(xy=(60, 60), width=12, style=Style())
        original_cnative.ing(xy=(80, 60), width=12, style=Style())

        original_cnative.k8s(xy=(20, 30), width=12, style=Style())
        original_cnative.otel(xy=(40, 30), width=12, style=Style())
        original_cnative.argocd(xy=(60, 30), width=12, style=Style())
        original_cnative.gatekeeper(xy=(80, 30), width=12, style=Style())

        out = tmp_path / "test_original_cnative_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_original_cnative_k8s_distributions(self, tmp_path: Path) -> None:
        """Verify Original Kubernetes distribution icons and their shorthand aliases."""
        clear()
        original_cnative.openshift(xy=(15, 75), width=10, style=Style())
        original_cnative.rancher(xy=(35, 75), width=10, style=Style())
        original_cnative.tanzu(xy=(55, 75), width=10, style=Style())
        original_cnative.okd(xy=(75, 75), width=10, style=Style())

        original_cnative.k3s(xy=(15, 50), width=10, style=Style())
        original_cnative.microk8s(xy=(35, 50), width=10, style=Style())
        original_cnative.talos(xy=(55, 50), width=10, style=Style())
        original_cnative.k0s(xy=(75, 50), width=10, style=Style())

        original_cnative.minikube(xy=(15, 25), width=10, style=Style())
        original_cnative.kind(xy=(35, 25), width=10, style=Style())
        original_cnative.kubevirt(xy=(55, 25), width=10, style=Style())
        original_cnative.vcluster(xy=(75, 25), width=10, style=Style())

        # Shorthand aliases
        original_cnative.ocp(xy=(15, 10), width=8, style=Style())
        original_cnative.rke(xy=(30, 10), width=8, style=Style())
        original_cnative.rke2(xy=(45, 10), width=8, style=Style())
        original_cnative.tkg(xy=(60, 10), width=8, style=Style())
        original_cnative.talos_linux(xy=(75, 10), width=8, style=Style())

        out = tmp_path / "test_original_cnative_k8s_distros.png"
        save(str(out))
        assert out.is_file()

    def test_original_cnative_architecture_diagram_enum(self, tmp_path: Path) -> None:
        """Verify OriginalCnativeIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("Ingress", width=20, height=20, icon=OriginalCnativeIcon.K8S_INGRESS), (20, 50))
        n2 = diag.add(Node("Service", width=20, height=20, icon=OriginalCnativeIcon.K8S_SERVICE), (50, 50))
        n3 = diag.add(Node("Pod", width=20, height=20, icon=OriginalCnativeIcon.K8S_POD), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_original_cnative.png"
        save(str(out))
        assert out.is_file()

    def test_original_cnative_sequence_diagram_enum(self, tmp_path: Path) -> None:
        """Verify OriginalCnativeIcon works inside SequenceDiagram participants."""
        clear()
        seq = SequenceDiagram(
            node_style=Styles.Neutral,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        p1 = seq.add(Participant("Argo CD", icon=OriginalCnativeIcon.ARGO))
        p2 = seq.add(Participant("API Server", icon=OriginalCnativeIcon.K8S_API_SERVER))
        seq.request(p1, p2, "Sync manifest")
        seq.draw((10, 10))
        out = tmp_path / "test_seq_original_cnative.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_original_cnative_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid Original Cloud Native icon file."""
        with pytest.raises(FileNotFoundError):
            ORIGINAL_CNATIVE_PROVIDER.get_icon_path("non_existent_original_cnative_icon_xyz")
