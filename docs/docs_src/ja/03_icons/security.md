# セキュリティ・ゼロトラストアイコン (`security` & `original_security`)

Drawlib は、サイバーセキュリティ、ID・アクセス管理（IAM/SSO）、ネットワーク防御、エンドポイント保護（EDR/XDR）、および SIEM/SOAR 運用向けに 2 つのペアとなるアイコンモジュールを提供しています。公式セキュリティベンダーおよび OSS ツールロゴ **74 種**を収録した **`drawlib.icons.security`**（`SecurityIcon`）と、全 **74 種**のブランドツインに **29 種**のベンダー中立なセキュリティ・ゼロトラストコンセプトアイコンを加えた合計 **103 種**のフラット 2D パステルアイコンを収録した **`drawlib.icons.original_security`**（`OriginalSecurityIcon`）です。両モジュールとも **[アイコン概要](./overview.md)** に記載された統一 API に準拠しており、**[アーキテクチャ図](../06_diagrams/architecture.md)** とシームレスに連携します。

```drawlib code=fold align=center file=icons_security_hero.png caption="公式セキュリティベンダーロゴ (security) とオリジナル 2D パステルアイコン (original_security) の比較"
from drawlib.canvas import save, setup
from drawlib.icons import original_security, security
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=148, height=68)

columns = [
    ("IAM & SSO", "okta", security.okta, original_security.okta),
    ("Edge & WAF", "cloudflare", security.cloudflare, original_security.cloudflare),
    ("NGFW Defense", "palo_alto", security.palo_alto, original_security.palo_alto),
    ("EDR / XDR", "crowdstrike", security.crowdstrike, original_security.crowdstrike),
    ("CNAPP / Cloud", "wiz", security.wiz, original_security.wiz),
]

for col_idx, (cat_label, _, _, _) in enumerate(columns):
    cx = 43.0 + col_idx * 22.8
    text((cx, 62.0), cat_label, style=Styles.DarkBold.patch(text_size=10.5))

rows = [
    (43.5, "Official Suite", "security (74)", Styles.Neutral),
    (17.5, "2D Pastel Suite", "original_security (103)", Styles.PrimaryNeutral),
]

for row_idx, (cy, row_title, row_sub, row_style) in enumerate(rows):
    rectangle((16.5, cy), width=25.0, height=22.0, style=row_style.patch(shape_r=2))
    text((16.5, cy + 3.0), row_title, style=Styles.DarkBold.patch(text_size=10.0))
    text((16.5, cy - 3.5), row_sub, style=Styles.Muted.patch(text_size=10.0))

    for col_idx, (_, fn_name, fn_off, fn_orig) in enumerate(columns):
        cx = 43.0 + col_idx * 22.8
        rectangle((cx, cy), width=20.5, height=22.0, style=row_style.patch(shape_r=2))
        icon_fn = fn_off if row_idx == 0 else fn_orig
        icon_fn((cx, cy + 3.2), width=8.5, style=Styles.Primary)
        text((cx, cy - 6.8), fn_name, style=Styles.DarkBold.patch(text_size=10.0))

save()
```

---

## 1. API シグネチャとツインモジュール構成

`drawlib.icons.security` および `drawlib.icons.original_security` のすべてのアイコン関数は、中心座標 `xy=(cx, cy)`、キャンバス単位での水平幅 `width`（`1:1` の正方形アスペクト比）、および必須の `style` を受け取ります。

```python
from drawlib.diagrams.architecture import Node, OriginalSecurityIcon, SecurityIcon
from drawlib.icons import (
    original_security,
    original_security_icon,
    security,
    security_icon,
)
from drawlib.styles import Styles

# 1. Direct module function calls (74 shared brand icons + 29 concept icons in original_security)
security.okta((30, 25), width=10.0, style=Styles.Primary)
original_security.okta((55, 25), width=10.0, style=Styles.Primary)
original_security.zero_trust((80, 25), width=10.0, style=Styles.Primary)
original_security.waf((105, 25), width=10.0, style=Styles.Primary)

# 2. Dynamic string lookup helpers
security_icon((30, 10), width=9.0, name="crowdstrike", style=Styles.Primary)
original_security_icon((55, 10), width=9.0, name="ddos_protection", style=Styles.Primary)

# 3. Strongly typed Enums for ArchitectureDiagram & SequenceDiagram
idp_node = Node("Okta IdP", icon=SecurityIcon.OKTA)
waf_node = Node("Edge WAF", icon=OriginalSecurityIcon.WAF)
```

| 機能・項目 | `drawlib.icons.security` | `drawlib.icons.original_security` |
| :--- | :--- | :--- |
| **ビジュアルスタイル** | セキュリティベンダーおよび OSS プロジェクトの公式ロゴ | 統一感のある 2D パステルブランドツイン + ベンダー中立のセキュリティコンセプトアイコン |
| **正規アイコン総数** | 公式ブランドアイコン **74** 種 | **103** 種（ブランドツイン `74` 種 + セキュリティコンセプトアイコン `29` 種） |
| **ダイアグラム Enum** | `SecurityIcon.<NAME>` | `OriginalSecurityIcon.<NAME>` |
| **動的ディスパッチャ** | `security_icon(xy, width, name=..., style=...)` | `original_security_icon(xy, width, name=..., style=...)` |
| **アセットパッケージ** | `icon_security` | `icon_original_security` |

---

## 2. ブランド・ベンダーセキュリティアイコン (両モジュール共通の 74 種)

`security` と `original_security` は、ID プロバイダ、ハードウェアセキュリティキー、次世代ファイアウォール（NGFW）、SASE/ZTNA ゲートウェイ、エンドポイント検知・対応（EDR）、クラウドセキュリティ（CNAPP）、アプリケーションセキュリティテスト（SAST/DAST）を網羅する **74 種の正規ブランドおよび OSS ツール名**を共有しています。

```drawlib code=fold align=center file=icons_security_brands.png caption="security と original_security の両方で利用可能な代表的ブランド・OSS セキュリティアイコン 10 選"
from drawlib.canvas import save, setup
from drawlib.icons import security
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=66)

row1 = [
    ("okta", "IAM / SSO", security.okta, Styles.Neutral),
    ("entra_id", "Directory / IdP", security.entra_id, Styles.PrimaryNeutral),
    ("auth0", "Customer IAM", security.auth0, Styles.Neutral),
    ("yubico", "Hardware Key", security.yubico, Styles.SecondaryNeutral),
    ("cloudflare", "WAF & DDoS", security.cloudflare, Styles.Neutral),
]

row2 = [
    ("palo_alto", "NGFW / SASE", security.palo_alto, Styles.Neutral),
    ("zscaler", "Zero-Trust", security.zscaler, Styles.SecondaryNeutral),
    ("crowdstrike", "EDR / XDR", security.crowdstrike, Styles.PrimaryNeutral),
    ("wiz", "Cloud CNAPP", security.wiz, Styles.Neutral),
    ("wazuh", "Open XDR/SIEM", security.wazuh, Styles.Neutral),
]

for row_idx, items in enumerate([row1, row2]):
    cy = 48.0 if row_idx == 0 else 18.0
    for col_idx, (fn_name, cat, icon_fn, card_st) in enumerate(items):
        cx = 16.0 + col_idx * 28.0
        rectangle((cx, cy), width=25.5, height=26.0, style=card_st.patch(shape_r=2))
        icon_fn((cx, cy + 5.0), width=8.5, style=Styles.Primary)
        text((cx, cy - 3.2), fn_name, style=Styles.DarkBold.patch(text_size=10.0))
        text((cx, cy - 8.5), cat, style=Styles.Muted.patch(text_size=10.0))

save()
```

### 2.1. 共通ブランドアイコン全 74 種一覧

以下のすべての関数名は、`security.<name>()`（`SecurityIcon.<NAME>`）および `original_security.<name>()`（`OriginalSecurityIcon.<NAME>`）の両方で同一の名前として利用できます。

| カテゴリ | 数 | 正規関数名 (`security.*` & `original_security.*`) |
| :--- | :---: | :--- |
| **ID 管理・SSO・MFA・認可** | 16 | `auth0`, `authelia`, `authentik`, `cerbos`, `clerk`, `duo`, `entra_id`, `okta`, `onelogin`, `openfga`, `ory`, `permit_io`, `ping_identity`, `stytch`, `supertokens`, `workos` |
| **パスワード管理・PAM・踏み台・ハードウェアキー** | 5 | `bitwarden`, `cyberark`, `onepassword`, `teleport`, `yubico` |
| **PKI・TLS 証明書・暗号技術** | 5 | `digicert`, `gnupg`, `lets_encrypt`, `sectigo`, `venafi` |
| **ネットワーク防御・NGFW・WAF・SASE・VPN** | 9 | `checkpoint`, `cloudflare`, `f5`, `fortinet`, `imperva`, `netskope`, `palo_alto`, `wireguard`, `zscaler` |
| **エンドポイント保護 (EDR/XDR)・アンチウイルス** | 10 | `crowdstrike`, `kaspersky`, `malwarebytes`, `microsoft_defender`, `osquery`, `sentinelone`, `sophos`, `symantec`, `trellix`, `trend_micro` |
| **クラウドセキュリティ (CNAPP)・脆弱性管理** | 8 | `aqua_security`, `lacework`, `prisma_cloud`, `qualys`, `rapid7`, `sysdig`, `tenable`, `wiz` |
| **SIEM・SOAR・NDR・IDS/IPS・メールセキュリティ** | 12 | `crowdsec`, `darktrace`, `google_secops`, `graylog`, `proofpoint`, `qradar`, `snort`, `sumo_logic`, `suricata`, `vectra_ai`, `wazuh`, `zeek` |
| **AppSec (SAST/DAST)・ペネトレーションテスト・パケット解析** | 9 | `burp_suite`, `checkmarx`, `gitleaks`, `metasploit`, `nmap`, `owasp`, `semgrep`, `veracode`, `wireshark` |

---

## 3. ベンダー中立セキュリティコンセプトアイコン (`original_security` 収録の 29 種)

ベンダーに依存しないセキュリティアーキテクチャ、脅威モデル、OAuth2/OIDC 認証フロー、SOC プレイブックを設計する際のために、`drawlib.icons.original_security`（`OriginalSecurityIcon`）には **29 種の専用セキュリティコンセプトアイコン**が用意されています。

```drawlib code=fold align=center file=icons_security_concepts.png caption="drawlib.icons.original_security に収録された代表的なベンダー中立セキュリティコンセプトアイコン 10 選"
from drawlib.canvas import save, setup
from drawlib.icons import original_security
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=66)

row1 = [
    ("zero_trust", "Zero-Trust", original_security.zero_trust, Styles.PrimaryNeutral),
    ("iam_sso", "Identity / SSO", original_security.iam_sso, Styles.Neutral),
    ("mfa_auth", "Multi-Factor", original_security.mfa_auth, Styles.Neutral),
    ("passkey", "WebAuthn", original_security.passkey, Styles.SecondaryNeutral),
    ("waf", "Web Firewall", original_security.waf, Styles.Neutral),
]

row2 = [
    ("ddos_protection", "DDoS Scrubbing", original_security.ddos_protection, Styles.Neutral),
    ("firewall", "Network FW", original_security.firewall, Styles.SecondaryNeutral),
    ("secret_vault", "Secrets Vault", original_security.secret_vault, Styles.Neutral),
    ("siem", "Log Analytics", original_security.siem, Styles.PrimaryNeutral),
    ("soc_center", "SOC Operations", original_security.soc_center, Styles.Neutral),
]

for row_idx, items in enumerate([row1, row2]):
    cy = 48.0 if row_idx == 0 else 18.0
    for col_idx, (fn_name, cat, icon_fn, card_st) in enumerate(items):
        cx = 16.0 + col_idx * 28.0
        rectangle((cx, cy), width=25.5, height=26.0, style=card_st.patch(shape_r=2))
        icon_fn((cx, cy + 5.0), width=8.5, style=Styles.Primary)
        text((cx, cy - 3.2), fn_name, style=Styles.DarkBold.patch(text_size=10.0))
        text((cx, cy - 8.5), cat, style=Styles.Muted.patch(text_size=10.0))

save()
```

### 3.1. ベンダー中立セキュリティコンセプトアイコン全 29 種一覧

| カテゴリ | 数 | 正規関数名 (`original_security.*` / `OriginalSecurityIcon.*`) |
| :--- | :---: | :--- |
| **ID・認証プロトコル・トークン** | 8 | `directory_service`, `iam_sso`, `jwt`, `mfa_auth`, `oauth2`, `oidc`, `passkey`, `saml` |
| **ゼロトラスト・境界防御・ネットワーク防御** | 9 | `casb`, `ddos_protection`, `firewall`, `honeypot`, `ids_ips`, `pam_bastion`, `vpn_gateway`, `waf`, `zero_trust` |
| **データ保護・暗号化・シークレット管理** | 5 | `dlp`, `encryption`, `hsm_kms`, `pki_ca`, `secret_vault` |
| **SOC・エンドポイント・脅威オペレーション** | 7 | `edr_xdr`, `email_security`, `siem`, `soar`, `soc_center`, `threat_intel`, `vulnerability_scan` |

---

## 4. 実践的なアーキテクチャ図

以下の図は、**[`ArchitectureDiagram`](../06_diagrams/architecture.md)** と `OriginalSecurityIcon` を用いて、ゼロトラストエッジ防御および SOC テレメトリパイプラインを表現した例です。

```drawlib code=show align=center file=icons_security_arch.png caption="ArchitectureDiagram と OriginalSecurityIcon によるゼロトラストエッジ防御＆SOC パイプライン"
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    Node,
    NodeGroup,
    OriginalSecurityIcon,
)
from drawlib.styles import Styles

clear()
setup(width=144, height=74)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    title="Zero-Trust Edge Scrubbing, OIDC Access & SOC Telemetry Architecture",
)

ddos = d.add(
    Node(
        "DDoS Edge\nProtection",
        width=24,
        height=18,
        icon=OriginalSecurityIcon.DDOS_PROTECTION,
        icon_size=7.5,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(10.0, 38.0),
)

perimeter = d.add(NodeGroup(title="Zero-Trust Perimeter & SOC Enclave", padding=5.0), xy=(40.0, 4.0))

waf = perimeter.add(
    Node(
        "Managed\nWAF",
        width=24,
        height=18,
        icon=OriginalSecurityIcon.WAF,
        icon_size=7.5,
    ),
    xy=(12.0, 34.0),
)
sso = perimeter.add(
    Node(
        "OIDC / MFA\nIdentity Gate",
        width=24,
        height=18,
        icon=OriginalSecurityIcon.MFA_AUTH,
        icon_size=7.5,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(12.0, 6.0),
)
siem = perimeter.add(
    Node(
        "Central\nSIEM",
        width=24,
        height=18,
        icon=OriginalSecurityIcon.SIEM,
        icon_size=7.5,
        card_style=Styles.SecondaryNeutral,
    ),
    xy=(60.0, 34.0),
)
vault = perimeter.add(
    Node(
        "HSM & Secret\nVault",
        width=24,
        height=18,
        icon=OriginalSecurityIcon.SECRET_VAULT,
        icon_size=7.5,
    ),
    xy=(60.0, 6.0),
)

d.connect(ddos, waf, label="Clean TLS", padding=1.5)
d.connect(waf, sso, label="Verify JWT", padding=1.5)
d.connect(waf, siem, label="Audit Logs", padding=1.5)
d.connect(sso, vault, label="KMS Grant", padding=1.5)

d.draw(xy=(4.0, 4.0))
save()
```

> [!TIP]
> 物理セキュリティゲートや監視カメラについては **[データセンター・ファシリティアイコン (`facility` & `original_facility`)](./facility.md)** を、DevSecOps および CI/CD パイプラインツール（`vault`、`trivy`、`sonarqube`）については **[DevOps・オブザーバビリティアイコン (`devops` & `original_devops`)](./devops.md)** を参照してください。
