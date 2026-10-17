# Security Icons Plan (`drawlib.icons.security` & `drawlib.icons.original_security`)

## 1. Objective & Scope

Add a dedicated security icon suite under `drawlib.icons.security` (`SecurityIcon`) for official security vendor/OSS logos, and `drawlib.icons.original_security` (`OriginalSecurityIcon`) combining vendor-neutral security architecture concept icons with 2D pastel counterparts of the official logos.

- **Modules**:
  - `drawlib.icons.security` (`SecurityIcon`) — 60 official vendor/OSS security logos (+ shorthand aliases).
  - `drawlib.icons.original_security` (`OriginalSecurityIcon`) — 24 vendor-neutral security concept icons + 60 2D flat pastel vendor/OSS counterparts (84 canonical icons total + shorthand aliases).
- **Release Asset Packages**:
  - `icon_security` (`tools/release_assets/v0.3/icons/security/`)
  - `icon_original_security` (`tools/release_assets/v0.3/icons/original_security/`)
- **Overlap Policy**:
  - Allows targeted overlap with `network` (9 core security/SASE/PKI vendors: `palo_alto`, `fortinet`, `checkpoint`, `zscaler`, `cloudflare`, `f5`, `wireguard`, `lets_encrypt`, `digicert`) so security architecture diagrams can use a single `security` module.
  - Optional overlap candidates from `devops` / `cnative` / `server` (`splunk`, `vault`, `keycloak`, `snyk`, `trivy`, `falco`, `kali_linux`, etc.) are listed in Section 4 for user confirmation.

---

## 2. Canonical `security` Icons (60 Official Vendor & OSS Logos)

| Category | # | Canonical Name | Product / Brand | Overlap |
| :--- | :- | :--- | :--- | :--- |
| **1. IAM, SSO, PAM & Secrets** | 1 | `okta` | Okta Workforce Identity | — |
| | 2 | `auth0` | Auth0 Customer Identity (CIAM) | — |
| | 3 | `entra_id` | Microsoft Entra ID (Azure AD) | — |
| | 4 | `cyberark` | CyberArk Privileged Access (PAM) | — |
| | 5 | `ping_identity` | Ping Identity Federation / SSO | — |
| | 6 | `onelogin` | OneLogin IAM / SSO | — |
| | 7 | `duo` | Cisco Duo Multi-Factor Auth (MFA) | — |
| | 8 | `teleport` | Teleport Zero-Trust Infrastructure Access | — |
| | 9 | `onepassword` | 1Password Enterprise Password Manager | — |
| | 10 | `bitwarden` | Bitwarden Open-Source Password Manager | — |
| **2. Endpoint, EDR/XDR & AV** | 11 | `crowdstrike` | CrowdStrike Falcon EDR / XDR | — |
| | 12 | `sentinelone` | SentinelOne Singularity XDR | — |
| | 13 | `microsoft_defender` | Microsoft Defender XDR | — |
| | 14 | `trend_micro` | Trend Micro Vision One / Deep Security | — |
| | 15 | `sophos` | Sophos Intercept X / MDR | — |
| | 16 | `trellix` | Trellix (McAfee Enterprise + FireEye) | — |
| | 17 | `symantec` | Symantec Enterprise Security (Broadcom) | — |
| | 18 | `kaspersky` | Kaspersky Endpoint Security | — |
| | 19 | `malwarebytes` | Malwarebytes ThreatDown | — |
| | 20 | `wazuh` | Wazuh Open-Source XDR & SIEM | — |
| **3. Network, NGFW, SASE & VPN** | 21 | `palo_alto` | Palo Alto Networks NGFW / Prisma / Cortex | `network` |
| | 22 | `fortinet` | Fortinet FortiGate / Security Fabric | `network` |
| | 23 | `checkpoint` | Check Point Quantum / CloudGuard | `network` |
| | 24 | `zscaler` | Zscaler Zero Trust Exchange (SASE) | `network` |
| | 25 | `netskope` | Netskope One SASE / CASB / ZTNA | — |
| | 26 | `cloudflare` | Cloudflare WAF / DDoS / Zero Trust | `network` |
| | 27 | `imperva` | Imperva WAF / Data & API Security | — |
| | 28 | `f5` | F5 BIG-IP Advanced WAF / API Security | `network` |
| | 29 | `proofpoint` | Proofpoint Email Security & DLP | — |
| | 30 | `wireguard` | WireGuard Modern Encrypted VPN | `network` |
| **4. SIEM, SOAR, NDR & SecOps** | 31 | `qradar` | IBM Security QRadar SIEM / SOAR | — |
| | 32 | `google_secops` | Google Security Operations (Chronicle) | — |
| | 33 | `sumo_logic` | Sumo Logic Cloud SIEM | — |
| | 34 | `graylog` | Graylog Security / Log Management | — |
| | 35 | `darktrace` | Darktrace ActiveAI NDR | — |
| | 36 | `vectra_ai` | Vectra AI Network Detection & Response | — |
| | 37 | `suricata` | Suricata Open-Source IDS / IPS / NSM | — |
| | 38 | `zeek` | Zeek Network Security Monitor | — |
| | 39 | `snort` | Snort Intrusion Prevention System | — |
| | 40 | `wireshark` | Wireshark Packet & Protocol Analyzer | — |
| **5. Cloud (CNAPP), Vuln & AppSec** | 41 | `wiz` | Wiz Cloud Security (CNAPP) | — |
| | 42 | `aqua_security` | Aqua Cloud-Native Security | — |
| | 43 | `sysdig` | Sysdig Secure Cloud & Runtime | — |
| | 44 | `lacework` | Lacework FortiCNAPP | — |
| | 45 | `tenable` | Tenable Nessus / Vulnerability Mgmt | — |
| | 46 | `qualys` | Qualys VMDR / Cloud Platform | — |
| | 47 | `rapid7` | Rapid7 InsightVM / InsightIDR | — |
| | 48 | `checkmarx` | Checkmarx One SAST / AppSec | — |
| | 49 | `veracode` | Veracode Application Risk Mgmt | — |
| | 50 | `owasp` | OWASP Foundation / ZAP | — |
| **6. Pentest, Audit, PKI & Crypto** | 51 | `burp_suite` | PortSwigger Burp Suite | — |
| | 52 | `metasploit` | Metasploit Penetration Testing | — |
| | 53 | `nmap` | Nmap Security Scanner | — |
| | 54 | `osquery` | osquery Endpoint Visibility | — |
| | 55 | `lets_encrypt` | Let's Encrypt Open CA | `network` |
| | 56 | `digicert` | DigiCert Enterprise PKI & TLS | `network` |
| | 57 | `sectigo` | Sectigo Commercial SSL/TLS & PKI | — |
| | 58 | `venafi` | Venafi Machine Identity Management | — |
| | 59 | `yubico` | Yubico YubiKey Hardware FIDO2 Auth | — |
| | 60 | `gnupg` | GnuPG (GPG) OpenPGP Encryption | — |

### Planned Shorthand Aliases (`SECURITY_ALIASES`)
- `azure_ad` -> `entra_id`
- `entra` -> `entra_id`
- `ping` -> `ping_identity`
- `one_password` -> `onepassword`
- `cisco_duo` -> `duo`
- `falcon` -> `crowdstrike`
- `s1` -> `sentinelone`
- `defender` -> `microsoft_defender`
- `trend` -> `trend_micro`
- `mcafee` -> `trellix`
- `fireeye` -> `trellix`
- `panw` -> `palo_alto`
- `paloalto` -> `palo_alto`
- `fortigate` -> `fortinet`
- `check_point` -> `checkpoint`
- `bigip` -> `f5`
- `wg` -> `wireguard`
- `ibm_qradar` -> `qradar`
- `chronicle` -> `google_secops`
- `sumologic` -> `sumo_logic`
- `vectra` -> `vectra_ai`
- `aqua` -> `aqua_security`
- `nessus` -> `tenable`
- `burp` -> `burp_suite`
- `portswigger` -> `burp_suite`
- `letsencrypt` -> `lets_encrypt`
- `yubikey` -> `yubico`
- `gpg` -> `gnupg`

---

## 3. Canonical `original_security` Icons (24 Concept Icons + 60 Pastel Vendor Logos = 84 Icons)

### Part A: Vendor-Neutral Security Concept Icons (24 Icons)

| Category | # | Canonical Name | Shorthand Aliases | 2D Pastel Motif |
| :--- | :- | :--- | :--- | :--- |
| **1. Identity & Access** | 1 | `iam_sso` | `iam`, `sso`, `identity` | User badge + key & federated link nodes |
| | 2 | `mfa_auth` | `mfa`, `two_factor`, `passkey` | Shield + smartphone/token + checkmark badge |
| | 3 | `pam_bastion` | `pam`, `bastion`, `privileged_access` | Armored gate/server + admin crown/key badge |
| | 4 | `directory_service` | `active_directory`, `ldap` | Hierarchical directory tree + user profile cards |
| **2. Network & Edge** | 5 | `firewall` | `ngfw`, `network_firewall` | Staggered brick wall + front security shield |
| | 6 | `waf` | `web_application_firewall` | Browser HTTP window + front filter shield |
| | 7 | `ddos_protection` | `ddos`, `scrubbing_center` | Protective shield deflecting incoming arrow swarm |
| | 8 | `vpn_gateway` | `vpn`, `ipsec_vpn` | Encrypted tunnel pipe + central padlock |
| | 9 | `zero_trust` | `ztna`, `sase`, `sdp` | Continuous verification ring + policy gate & lock |
| **3. Endpoint & Data** | 10 | `edr_xdr` | `edr`, `xdr`, `endpoint_security` | Endpoint laptop/screen + pulse radar shield |
| | 11 | `ids_ips` | `ids`, `ips`, `ndr` | Packet stream + inspection lens & block shield |
| | 12 | `dlp` | `data_loss_prevention` | Document/DB card + padlock & outbound barrier |
| | 13 | `casb` | `cloud_access_security` | Cloud silhouette + central policy checkpoint lock |
| | 14 | `email_security` | `anti_phishing`, `seg` | Envelope + protective shield & blocked hook |
| **4. Crypto & PKI** | 15 | `pki_ca` | `certificate_authority`, `tls_cert` | Certificate scroll + ribbon seal & key pair |
| | 16 | `hsm_kms` | `hsm`, `kms`, `key_management` | Tamper-resistant hardware chip + master key |
| | 17 | `secret_vault` | `secrets_manager`, `password_vault` | Bank vault door + combination dial & lock |
| | 18 | `encryption` | `data_encryption`, `cipher` | Plaintext grid transforming via lock into cipher |
| **5. SecOps & Threat** | 19 | `siem` | `log_analytics`, `security_analytics` | Central log funnel + correlation alert dashboard |
| | 20 | `soar` | `security_automation`, `playbook` | Shield + automation gear & workflow branches |
| | 21 | `soc_center` | `soc`, `security_operations` | Multi-screen SOC console + global radar watch |
| | 22 | `threat_intel` | `cti`, `threat_hunting` | Global radar crosshair + threat indicator bug |
| | 23 | `vulnerability_scan` | `vuln_scanner`, `sast`, `dast` | Magnifying glass scanning server/code + alert |
| | 24 | `honeypot` | `deception`, `decoy` | Hexagonal honey cell node + trap radar rings |

### Part B: 2D Flat Pastel Vendor/OSS Logos (60 Icons)
- Every icon in `security` (1–60) has a matching 2D flat pastel counterpart in `original_security`.
- **Mandatory Brand Color Rule**: Each `original_security` vendor icon strictly preserves the official logo's color scheme softened into Drawlib pastel tones (`Colors.Blue1..6`, `Colors.Red1..6`, `Colors.Green1..6`, `Colors.Orange1..6`, `Colors.Amber1..6`, `Colors.Teal1..6`, `Colors.Purple1..6`, `Colors.Gray1..6`, or softened brand hex) with `DARK = "#323A48"` outlines (`w = 1.9`).

---

## 4. Cross-Suite Overlap Options (For User Review)

The base 60-icon plan overlaps with 9 core `network` icons. In addition, the following security-related icons already exist in other suites and can optionally be registered in `security` / `original_security` as well if desired:

| Suite | Existing Icons | Recommendation |
| :--- | :--- | :--- |
| **`network`** | `tailscale`, `openvpn`, `pfsense`, `opnsense`, `adguard`, `pi_hole` | Optional (can add if VPN/homelab firewall coverage is desired in `security`) |
| **`devops`** | `vault`, `keycloak`, `trivy`, `snyk`, `sonarqube`, `splunk` | Can reuse existing scripts in `security` if one-stop security access is desired |
| **`cnative`** | `falco`, `kyverno`, `opa`, `cert_manager` | Can reuse existing scripts in `security` or keep in `cnative` |
| **`server`** | `kali_linux` | Can reuse existing script in `security` for pentest diagrams |

---

## 5. Implementation & Verification Workflow

1. **Phase 1 — Official SVG Collection & Reference Sheet**:
   - Download/collect all 60 official full-color SVGs into `tools/original_assets/security/<name>/<name>.svg` (reusing the 9 overlapping `network` SVGs).
   - Rasterize `512x512` reference PNGs into `.drawlib/scratch/security_ref/<name>_ref.png` and inspect a reference contact sheet.
2. **Phase 2 — Provider Wiring**:
   - Register `security` (`SecurityIcon`) and `original_security` (`OriginalSecurityIcon`) in:
     - `src/drawlib/_icons/png_icons/{security,original_security}/`
     - `src/drawlib/icons.py` (`drawlib.icons.security`, `drawlib.icons.original_security`)
     - `src/drawlib/_diagrams/architecture/` & `sequence/` (`SecurityIcon`, `OriginalSecurityIcon`)
     - `tools/dcli/codegen/` (`icon-security`, `icon-original-security`)
3. **Phase 3 — Parallel Subagent Authoring (`security` Official Logos)**:
   - Compile/author `tools/icons_src/security/<name>_default.py` in parallel batches.
   - Run Stage 1 & Stage 2 grid inspection (`-g`) against `_ref.png` (ensuring pure Drawlib primitives, zero `image()`/`text()`, and transparent background cutout holes via `draw_compound_polygon()`).
4. **Phase 4 — Parallel Subagent Authoring (`original_security` Concept + Pastel Logos)**:
   - Author the 24 concept icons + 60 brand-faithful 2D pastel logos in `tools/icons_src/original_security/<name>_default.py`.
   - Flag any complex mascot/photo logos for Nano Banana 3-option comparison if needed.
5. **Phase 5 — Build, Codegen, Asset Sync & Final Review**:
   - Render `512x512` PNGs, run `./dcli codegen icon-security` and `./dcli codegen icon-original-security`, build `icon_security.zip` and `icon_original_security.zip`, run `./dcli release-assets sync`, add unit tests (`tests/drawlib/icons/test_security.py`, `test_original_security.py`), update rules, and run `./dcli code-check all` & `./dcli test target icons` / `diagrams`.
