# Drawlib Security Icons Guidelines (`lib-icons-security`)

API specification and complete catalog for `drawlib.icons.security` (`SecurityIcon`, **74** official IAM/SSO, NGFW, EDR/XDR, CNAPP, SIEM, and AppSec vendor/OSS logos) and `drawlib.icons.original_security` (`OriginalSecurityIcon`, **103** flat 2D pastel icons: **74** brand twins + **29** vendor-neutral security and Zero-Trust concept icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature & Twin Module Structure

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import Node, OriginalSecurityIcon, SecurityIcon
from drawlib.icons import original_security, original_security_icon, security, security_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
security.okta((30, 25), width=9.0, style=Styles.Primary)
original_security.okta((55, 25), width=9.0, style=Styles.Primary)
original_security.zero_trust((80, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
security_icon((30, 10), width=9.0, name="crowdstrike", style=Styles.Primary)
original_security_icon((55, 10), width=9.0, name="ddos_protection", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
idp_node = Node("Okta IdP", width=24, height=18, icon=SecurityIcon.OKTA, icon_size=7.5)
waf_node = Node("Managed WAF", width=24, height=18, icon=OriginalSecurityIcon.WAF, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.security` | `SecurityIcon` | **74** | `icon_security` | Official security vendor & open-source logos for IAM, PAM, PKI, NGFW, EDR, CNAPP, SIEM, and AppSec. |
| `drawlib.icons.original_security` | `OriginalSecurityIcon` | **103** (`74` + `29`) | `icon_original_security` | Flat 2D pastel twins for all 74 brands plus **29 vendor-neutral Zero-Trust, auth, and SOC concept icons**. |

---

## 2. Complete 74 Shared Brand Icons (`security.*` & `original_security.*`)

| Category | Count | Canonical Function Names (`security.*` & `original_security.*`) |
| :--- | :---: | :--- |
| **Identity, SSO, MFA & Authorization** | 16 | `auth0`, `authelia`, `authentik`, `cerbos`, `clerk`, `duo`, `entra_id`, `okta`, `onelogin`, `openfga`, `ory`, `permit_io`, `ping_identity`, `stytch`, `supertokens`, `workos` |
| **Password Managers, PAM, Bastion & Hardware Keys** | 5 | `bitwarden`, `cyberark`, `onepassword`, `teleport`, `yubico` |
| **PKI, TLS Certificates & Cryptography** | 5 | `digicert`, `gnupg`, `lets_encrypt`, `sectigo`, `venafi` |
| **Network Security, NGFW, WAF, SASE & VPN** | 9 | `checkpoint`, `cloudflare`, `f5`, `fortinet`, `imperva`, `netskope`, `palo_alto`, `wireguard`, `zscaler` |
| **Endpoint Protection (EDR/XDR) & Antivirus** | 10 | `crowdstrike`, `kaspersky`, `malwarebytes`, `microsoft_defender`, `osquery`, `sentinelone`, `sophos`, `symantec`, `trellix`, `trend_micro` |
| **Cloud Security (CNAPP), Vulnerability & VM** | 8 | `aqua_security`, `lacework`, `prisma_cloud`, `qualys`, `rapid7`, `sysdig`, `tenable`, `wiz` |
| **SIEM, SOAR, NDR, IDS/IPS & Email Security** | 12 | `crowdsec`, `darktrace`, `google_secops`, `graylog`, `proofpoint`, `qradar`, `snort`, `sumo_logic`, `suricata`, `vectra_ai`, `wazuh`, `zeek` |
| **AppSec (SAST/DAST), Pentesting & Packet Analysis** | 9 | `burp_suite`, `checkmarx`, `gitleaks`, `metasploit`, `nmap`, `owasp`, `semgrep`, `veracode`, `wireshark` |

---

## 3. Complete 29 Vendor-Neutral Security Concept Icons (`original_security.*` Only)

| Category | Count | Canonical Function Names (`original_security.*` / `OriginalSecurityIcon.*`) |
| :--- | :---: | :--- |
| **Identity, Auth Protocols & Tokens** | 8 | `directory_service`, `iam_sso`, `jwt`, `mfa_auth`, `oauth2`, `oidc`, `passkey`, `saml` |
| **Zero-Trust, Perimeter & Network Defense** | 9 | `casb`, `ddos_protection`, `firewall`, `honeypot`, `ids_ips`, `pam_bastion`, `vpn_gateway`, `waf`, `zero_trust` |
| **Data Protection, Cryptography & Secrets** | 5 | `dlp`, `encryption`, `hsm_kms`, `pki_ca`, `secret_vault` |
| **SOC, Endpoint & Threat Operations** | 7 | `edr_xdr`, `email_security`, `siem`, `soar`, `soc_center`, `threat_intel`, `vulnerability_scan` |

```drawlib code=fold align=center file=icons_security_rules_arch.png caption="Zero-Trust Edge Defense & SOC Pipeline Using SecurityIcon and OriginalSecurityIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    Node,
    NodeGroup,
    OriginalSecurityIcon,
    SecurityIcon,
)
from drawlib.styles import Styles

setup(width=136, height=58)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

ddos = d.add(
    Node("DDoS Edge\nScrubbing", width=24, height=18, icon=OriginalSecurityIcon.DDOS_PROTECTION, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
enclave = d.add(NodeGroup(title="Zero-Trust Perimeter & SOC", padding=4.5), xy=(42, 4))
waf = enclave.add(Node("Managed\nWAF", width=24, height=18, icon=OriginalSecurityIcon.WAF, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
idp = enclave.add(Node("Okta OIDC\nIdentity Gate", width=24, height=18, icon=SecurityIcon.OKTA, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(ddos, waf, label="Clean TLS", padding=1.5)
d.connect(waf, idp, label="Verify JWT", padding=1.5)
d.draw(xy=(4, 4))
save()
```
