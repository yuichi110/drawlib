# Presentation Content Planning: Real-World DDoS Incident Response & Remediation Report

This document records the complete storyline, factual incident timeline, slide-by-slide structure, and diagram designs for the presentation: **"DDoS Incident Response: From Cloud Run Bill Shock to Multi-Layered Edge Defense"**.

---

## 1. Presentation Meta Information

- **Topic**: Real-World DDoS Attack Experience on a Text-to-Speech (TTS) Service, Economic Denial of Sustainability (EDoS), Proof-of-Work Challenge Defense, Cloud WAF Pricing Traps, and Multi-Layered Edge Defense.
- **Language**: English
- **Style Theme**: Google Style (`GoogleStyles` & `GoogleColors`, 16:9 widescreen format)
- **Target Audience**: Infrastructure engineers, SREs, cloud architects, and security practitioners.
- **Tone**: Pragmatic, transparent, incident post-mortem style with actionable engineering lessons.
- **Format**: 16 slides with presenter speech notes (`::: note`) and pure-Python Drawlib diagrams.

---

## 2. Factual Incident Timeline & Context

### Phase 1: Background & Legacy Architecture (2015–2025)
- **Service Profile**:
  - Personal web service running continuously since circa 2015.
  - **Workload**: Text-to-Speech (TTS) speech synthesis. Takes user text input and synthesis parameters, computes audio waveforms, and returns synthesized speech.
  - **Traffic Scale**: Modest personal project with approximately several hundred Daily Active Users (DAU).
- **Legacy VPS Era (2015–2025)**:
  - Operated on a traditional VPS for nearly a decade. Low operational complexity, predictable flat monthly hosting fee.
- **2025 Cloud Migration**:
  - As the multi-year VPS contract expired in 2025, the application was containerized.
  - Migrated to **Google Cloud (Cloud Run)** with a custom domain directly mapped to the Cloud Run service URL over the public Internet.
  - *Architectural Gap*: Direct public exposure of Cloud Run without an edge proxy, CDN, or WAF.

### Phase 2: The Attack Onset & EDoS Shock (2026)
- **Global Context**:
  - Global proliferation of automated AI-driven scanning, scraping, and botnet activity in 2026. The personal site was caught in broad-spectrum targeting.
- **Attack Signature**:
  - Direct Layer 7 DDoS attack focused specifically on the computationally expensive **TTS Synthesis API**.
  - **Parameter Permutation/Fuzzing**: The attacker subtly mutated request parameters on every call, bypassing naive caching or request deduplication.
- **Impact (Economic Denial of Sustainability / EDoS)**:
  - Heavy TTS audio synthesis immediately pushed Cloud Run instances to 100% CPU.
  - Cloud Run scaled out to its configured maximum limit (**4 instances**) and pinned there continuously.
  - Massive logging generated gigabytes of log entries.
  - A service that previously cost pocket change exploded to **hundreds of dollars in a single week**.

### Phase 3: Immediate Emergency Triage
- **Financial Firefighting**:
  - Clamped down on max instance counts and reduced concurrent requests per container to stop runaway billing.
- **Architectural Bottleneck Identified**:
  - A directly Internet-exposed Cloud Run service has no native Layer 7 WAF inspection.
  - Cloud Run alone cannot filter malicious requests before TLS termination and container execution. Fundamental defense required an architectural change.

### Phase 4: Introducing WAF & The Cat-and-Mouse Escalation
- **Infrastructure Overhaul**:
  - Provisioned a **Google Cloud External Application Load Balancer (GCLB)** in front of Cloud Run.
  - Enabled **Google Cloud Armor (WAF)** with per-IP rate limiting and global volume rate limiting.
- **The Cat-and-Mouse Escalation**:
  1. **Wave 1 (China Concentrated)**: Attack traffic originated predominantly from Chinese IPs -> Blocked China (`CN`). Simultaneously configured per-IP and global rate limits.
  2. **Wave 2 (Southeast Asian Shift)**: Attackers routed traffic through Malaysia and neighboring Asian countries -> Expanded geo-blocklist to multiple Asian nations.
  3. **Wave 3 (Global Distribution)**: Attackers dispersed requests through proxy networks across North America, Europe, and Latin America -> Adopted extreme whitelist: blocked all countries except Japan.
  4. **Wave 4 (Domestic Japanese Proxies)**: Attackers switched egress to Japanese domestic residential IPs / proxies -> Geo-blocking completely collapsed as a defense strategy!

### Phase 5: Application-Level Quick Fixes (CORS & Custom Headers)
- **Implementation**:
  - Enforced strict Cross-Origin Resource Sharing (CORS) policy.
  - Required a custom HTTP request header dynamically attached by frontend JavaScript; server rejected requests lacking this header with HTTP 403 Forbidden.
- **Outcome & Attacker Adaptation**:
  - Temporarily succeeded in short-circuiting TTS computation with 403 responses.
  - Shortly after, attackers analyzed client-side JavaScript, extracted header requirements, and updated bot scripts to emulate genuine browser request headers.

### Phase 6: Application-Level Redesign: The Proof-of-Work (PoW) Challenge
- **Core Diagnosis**:
  - The attacker was actively seeking free, unauthorized speech synthesis computation (resource theft).
- **Asymmetric Proof-of-Work (PoW) Architecture**:
  - Introduced a two-step API flow:
    1. Client calls `/challenge` API to receive an ephemeral cryptographic seed.
    2. Client browser executes SHA-256 hashing in JavaScript to find a nonce yielding four leading zeros (`0000...`).
  - **Asymmetric Economics**:
    - For legitimate human users: Single calculation takes <100ms in the background—completely imperceptible.
    - For botnets: Multiplying millions of requests by heavy SHA-256 CPU cycles makes high-volume synthesis economically unviable for the attacker.
  - **Dynamic Difficulty Penalty**:
    - Suspicious or high-frequency request profiles were penalized with mandatory multiple-round PoW challenges.
- **Outcome**:
  - Unauthorized TTS synthesis API consumption plummeted to near zero. The primary resource theft objective was successfully defeated!

### Phase 7: The Attacker's Pivot: From Compute Theft to Pure EDoS Harassment
- **The Shift to Malice**:
  - Blocked from abusing the TTS engine, the attacker lost interest in speech synthesis and pivoted to **pure economic harassment (Economic Denial of Sustainability / EDoS)**.
  - The botnet began blasting **hundreds of millions of requests per day** directly at the front door and the lightweight `/challenge` endpoint.
- **The Cloud Armor WAF Pricing Trap**:
  - Google Cloud Armor bills per request evaluation (standard rate: ~$0.75 per million requests).
  - At hundreds of millions of requests per day, **the WAF request evaluation fee alone exploded into hundreds of dollars per day**!
  - Even though Cloud Armor successfully blocked 99%+ of attack traffic at the perimeter, **the defense mechanism itself was bankrupting the service**.
- **Emergency Action**:
  - To stop the immediate financial bleeding from WAF evaluation fees, **deleted the External Load Balancer (GCLB) entirely**.
  - Began formulating an emergency migration plan to a fixed-rate, unmetered DDoS defense architecture.

### Phase 8: Migration to Fixed-Price WAF & CDN (Cloudflare Free -> Pro)
- **Migrating Front Door**:
  - Placed Cloudflare in front of Cloud Run to replace the pay-per-request Cloud Armor model with unmetered DDoS protection.
- **Free Plan Bottleneck**:
  - Free tier provided basic Layer 3/4 volumetric absorption, but lacked granular WAF rules, advanced rate limiting, and bot score thresholds, leaving a defense gap.
- **Cloudflare Pro Plan ($20/month fixed)**:
  - Unlocked robust WAF rule configuration, IP rate limiting, and Managed Challenges under predictable, capped pricing ($20/mo fixed vs. hundreds/day on Cloud Armor).
- **The Next Attacker Evasion (Sub-Threshold Bot Swarms)**:
  - Attackers detected Cloudflare's presence.
  - Coordinated thousands of distributed bot nodes to fire requests **just below the configured per-IP rate limit thresholds**.
  - While 75% of traffic was blocked, the remaining 25% leaking through was still enough to overwhelm budget Cloud Run instances.
- **Traffic Decomposition & Attacker Profiling**:
  - Deep log analysis revealed two distinct attack fleets:
    1. **Datacenter Attack Instances**: Cloud VMs and bulletproof hosting providers with high bandwidth.
    2. **Compromised Residential/Personal Bots**: Infected home computers, IoT devices, and residential proxies with low individual compute power.

### Phase 9: The Multi-Layered Defense Masterclass (The Final Resolution)
A holistic, defense-in-depth posture was deployed across 5 specialized fronts, achieving complete and lasting mitigation:

1. **Edge Hygiene & Client Anomaly Filtering**:
   - Dropped traffic with unknown/unidentified country tags or originating from known Tor exit nodes.
   - Identified and blocked OS/Browser fingerprint mismatches (e.g. requests claiming to run Safari on a Linux OS).
   - Dropped malformed, suspicious, or spoofed HTTP headers.
2. **Datacenter ASN Blacklisting**:
   - Blacklisted Autonomous System Numbers (ASNs) belonging to major hosting and cloud datacenters where real human consumer traffic never originates.
3. **Deprecating Legacy HTTP/1.1 (Requiring HTTP/2+)**:
   - Bot scripts on compromised machines used rudimentary HTTP/1.1 libraries.
   - Legitimate modern human visitors almost universally use browsers negotiating HTTP/2 or HTTP/3.
   - Dropped HTTP/1.1 support entirely, cutting off legacy bot client engines at the TLS/protocol handshake.
4. **Dual-Speed Rate Limiting (Burst & Slow-Probe Protection)**:
   - Extended the cooldown block duration for offenders.
   - Configured high-velocity burst banning (catching sudden floods) alongside long-interval slow-leak banning (catching botnets attempting to stay under per-minute thresholds over hours).
5. **Edge-Native Managed Challenge Gating**:
   - Solved the flaw of the custom PoW challenge (which still required origin execution) by leveraging **Cloudflare Managed Challenges / Turnstile**.
   - Placed Managed Challenges on static page entry: clients must pass the edge challenge once before the browser is issued credentials to call backend API endpoints.
   - Enabled **Cloudflare Super Bot Fight Mode**.

### Phase 10: Profiling the Modern Autonomous Threat Actor
- **Autonomous AI-Assisted Attackers**:
  - Attackers exhibited dynamic adaptation: reverse-engineering client JavaScript constraints, extracting headers, and tuning bot behaviors within hours. This strongly indicates autonomous AI agents conducting reconnaissance and tool configuration rather than slow manual human scripting.
- **Sacrificial Recon Probes**:
  - Attacker launched periodic batch attacks, using sacrificial probe nodes to find the exact thresholds of active rate limits before unleashing the wider swarm.
- **Why Target a Personal Voice Synthesis Service?**:
  - A live public web service with heavy compute (TTS), non-trivial user traffic, and an active defender responding in real-time serves as an **ideal training ground / live benchmark target** for botnet operators to stress-test and refine automated evasion techniques.
  - The objective was never financial extortion or ransomware—the site was treated as an empirical sandbox.

---

## 3. The 16-Slide Masterclass Outline

```text
Act 1: The Incident Onset (Slides 1–4)
  Slide 1: Title & Hook (Surviving a Targeted EDoS Attack)
  Slide 2: Background: 10 Years of Peace & The Cloud Run Migration
  Slide 3: The Attack: L7 Parameter Fuzzing & Cloud Bill Explosion
  Slide 4: First Triage: Clamping Compute & The Missing Edge WAF

Act 2: The Perimeter & The Cat-and-Mouse Escalation (Slides 5–8)
  Slide 5: Perimeter Defense: Deploying GCLB + Cloud Armor WAF
  Slide 6: The Cat-and-Mouse Game: The Collapse of Geo-Blocking
  Slide 7: Application Tactical Defense: CORS & Custom Header Spoofing
  Slide 8: The Game Changer: Asymmetric Proof-of-Work (PoW) Challenge

Act 3: The EDoS Pivot & The Pricing Trap (Slides 9–11)
  Slide 9: The Attacker's Pivot: From Resource Theft to Pure Malice
  Slide 10: The Cloud Armor Pricing Trap: Bankrupt by Defense Fees ($0.75/M)
  Slide 11: The Emergency Takedown: Deleting GCLB & The Architecture Pivot

Act 4: The Final Battle & Multi-Layered Victory (Slides 12–16)
  Slide 12: Fixed-Rate Edge: Cloudflare Pro vs. Sub-Threshold Swarms
  Slide 13: Traffic Decomposition: Datacenter VMs vs. Hijacked Personal PCs
  Slide 14: The Multi-Layered Masterclass: 5 Pillars of Final Mitigation
  Slide 15: Profiling the Threat Actor: Autonomous AI Botnets & Sandbox Targets
  Slide 16: Engineering Takeaways & Incident Post-Mortem Checklist
```

### Detailed Slide Specifications & Planned Drawlib Diagrams

#### Slide 1: Title & Hook
- **Title**: Surviving a Targeted EDoS Attack on Cloud Run
- **Subtitle**: Real-World Incident Response: From Cloud Bill Shock to Multi-Layered Edge Defense
- **Presenter**: Yuichi Ito
- **Presenter Note**: Welcome everyone. Today I'm sharing an unfiltered, deeply practical post-mortem of how a personal speech synthesis service survived a relentless, multi-stage DDoS attack that evolved from compute theft to an economic bankruptcy attack.

#### Slide 2: Background: 10 Years of Peace & The Cloud Run Migration
- **Story**: 2015–2025 legacy VPS era. A Text-to-Speech service with several hundred DAU. 2025 containerization and direct Cloud Run deployment.
- **Diagram (`slide02_pre_attack_architecture.png`)**: Direct public Internet to Cloud Run topology, highlighting the total absence of edge inspection or WAF.
- **Presenter Note**: For 10 years, this service ran happily on a cheap VPS. When the contract expired in 2025, I migrated it to Cloud Run. But direct public exposure created a dangerous blind spot: no WAF, no edge buffering.

#### Slide 3: The Attack: L7 Parameter Fuzzing & Cloud Bill Explosion
- **Story**: In 2026, targeted by global automated botnets. Layer 7 TTS API flood with subtle parameter permutations bypassing caching. 4 instances maxed at 100% CPU. Massive logs. Hundreds of dollars in one week (EDoS).
- **Diagram (`slide03_attack_spike_chart.png`)**: Dual-axis chart showing RPS baseline vs. attack surge, paired with the exponential cost spike.
- **Presenter Note**: Text-to-Speech is computationally intensive. The attackers sent L7 requests with slightly mutated parameters to defeat caching. Cloud Run pinned at my max limit of 4 instances, generating gigabytes of logs and exploding my bill by hundreds of dollars in days.

#### Slide 4: First Triage: Clamping Compute & The Missing Edge WAF
- **Story**: Emergency throttling of max instances and concurrency. Financial bleeding slowed, but legitimate users suffered 504 Gateway Timeouts. The realization: directly exposed Cloud Run cannot defend itself against L7 floods.
- **Diagram (`slide04_triage_tradeoffs.png`)**: Trade-off card comparison: Compute Clamping vs. Upstream Edge Inspection.
- **Presenter Note**: My first move was to clamp container instances down. That stopped the bill from doubling again, but it created widespread 504 timeouts. Cloud Run has no native L7 WAF. Without an edge proxy, you cannot drop malicious traffic before TLS termination.

#### Slide 5: Perimeter Defense: Deploying GCLB + Cloud Armor WAF
- **Story**: Introducing Google Cloud External Application Load Balancer (GCLB) + Cloud Armor WAF. Configuring baseline per-IP and global rate limits.
- **Diagram (`slide05_gclb_cloud_armor_topology.png`)**: Architecture topology: Internet -> GCLB Edge + Cloud Armor WAF -> Serverless NEG -> Private Cloud Run.
- **Presenter Note**: I deployed GCLB in front of Cloud Run and activated Cloud Armor WAF. Traffic was now inspected at Google's edge with rate-limiting policies.

#### Slide 6: The Cat-and-Mouse Game: The Collapse of Geo-Blocking
- **Story**: The 4-wave geo-blocking escalation: China -> Malaysia/SE Asia -> Global Proxy Botnet -> Japanese Residential IPs. Geo-blocking completely failed.
- **Diagram (`slide06_geo_blocking_cat_and_mouse.png`)**: Multi-stage flowchart showing the attacker systematically evading geographical filters across 4 waves.
- **Presenter Note**: Geo-blocking feels intuitive, but against modern botnets, it is an illusion. Every time I blocked a region, the attackers shifted egress within hours—eventually routing through domestic Japanese residential IPs.

#### Slide 7: Application Tactical Defense: CORS & Custom Header Spoofing
- **Story**: Quick fixes: Enforcing CORS and requiring a custom client-side JavaScript header. Initial 403 block success, followed by rapid reverse-engineering and header emulation by the botnet.
- **Diagram (`slide07_header_spoofing_bypass.png`)**: Sequence flow showing client header validation and the botnet's reverse-engineering loop.
- **Presenter Note**: I tried quick application fixes: CORS and a custom header injected by JavaScript. It worked for a few hours, returning 403s. But the attackers analyzed my frontend JS, spoofed the exact headers, and blew past the filter.

#### Slide 8: The Game Changer: Asymmetric Proof-of-Work (PoW) Challenge
- **Story**: Realizing the motive was TTS compute theft. Implementing client-side SHA-256 PoW challenge (`/challenge` -> seed -> `0000...` hash). Asymmetric cost: <100ms for humans, millions of CPU cycles for botnets. Dynamic difficulty penalties. Unauthorized TTS compute dropped to near zero!
- **Diagram (`slide08_pow_challenge_handshake.png`)**: Detailed protocol flow: Seed handshake, client hashing loop, token verification, and dynamic penalty multiplier.
- **Presenter Note**: The breakthrough was understanding the attacker's motive: they wanted free voice synthesis. I implemented an asymmetric Proof-of-Work challenge in JavaScript. Legitimate users solve a 4-zero SHA-256 hash in 50ms without noticing. For a botnet sending millions of calls, the compute cost became mathematically prohibitive. Voice compute dropped to zero!

#### Slide 9: The Attacker's Pivot: From Resource Theft to Pure Malice
- **Story**: Blocked from stealing compute, the attacker pivoted from resource theft to pure economic malice: flooding the front door and `/challenge` endpoint with hundreds of millions of requests per day.
- **Diagram (`slide09_edos_traffic_shift_chart.png`)**: Chart showing TTS API requests flatlining at zero while edge/challenge endpoint requests explode into hundreds of millions.
- **Presenter Note**: But the battle wasn't over. Having lost access to the TTS engine, the attacker was furious. Their motive pivoted from resource theft to pure economic spite: blasting hundreds of millions of requests per day directly at my front door.

#### Slide 10: The Cloud Armor Pricing Trap: Bankrupt by Defense Fees ($0.75/M)
- **Story**: Cloud Armor's pricing model: ~$0.75 per million evaluated requests. At hundreds of millions of requests/day, WAF inspection fees alone surged to hundreds of dollars per day. The WAF was 99% effective, but mathematically bankrupting the project.
- **Diagram (`slide10_waf_pricing_trap_breakdown.png`)**: Financial breakdown comparing compute savings against runaway WAF evaluation billing.
- **Presenter Note**: Here is the most dangerous trap in cloud architecture. Cloud Armor charges $0.75 per million evaluated requests. When an attacker sends 300 million requests a day, you owe $225 a day just for Cloud Armor to say "Blocked"! Even though 99% of requests were dropped at the edge, the bill was bankrupting me.

#### Slide 11: The Emergency Takedown: Deleting GCLB & The Architecture Pivot
- **Story**: The drastic measure: deleting GCLB to immediately sever traffic and halt WAF billing. Formulating an emergency migration plan to unmetered edge defense.
- **Diagram (`slide11_emergency_takedown_flow.png`)**: Decision tree leading to LB deletion and the requirement for fixed-price unmetered DDoS mitigation.
- **Presenter Note**: I had to make a drastic choice: I literally deleted the Load Balancer to sever traffic and stop the catastrophic billing bleed. I realized pay-per-request WAFs are untenable under large-scale EDoS attacks. I needed unmetered DDoS protection.

#### Slide 12: Fixed-Rate Edge: Cloudflare Pro vs. Sub-Threshold Swarms
- **Story**: Migrating to Cloudflare. Free plan had insufficient filtering. Upgrading to Cloudflare Pro ($20/month fixed). Attacker adjusted: spraying requests from thousands of machines just below the rate limit thresholds. 25% still leaked through.
- **Diagram (`slide12_sub_threshold_swarm_evasion.png`)**: Visualization of thousands of bot nodes carefully calibrated below per-IP rate limit ceilings.
- **Presenter Note**: I migrated the domain to Cloudflare Pro for a fixed $20 a month. No more per-request WAF fees! But the attackers adapted again: they distributed the flood across thousands of IPs, keeping each IP just below my rate limit thresholds. 25% of the flood was still leaking into Cloud Run.

#### Slide 13: Traffic Decomposition: Datacenter VMs vs. Hijacked Personal PCs
- **Story**: Log forensic analysis revealed two distinct attacker fleets: Datacenter attack instances (high bandwidth) and compromised personal/IoT devices (residential proxies, low compute).
- **Diagram (`slide13_attacker_fleet_decomposition.png`)**: Two-column comparison of Datacenter Infrastructure vs. Residential Bot Swarms.
- **Presenter Note**: I analyzed the traffic logs deeply. The attack wasn't monolithic. It was split into two distinct fleets: high-bandwidth cloud VMs in bulletproof datacenters, and low-spec compromised residential computers running automated bots.

#### Slide 14: The Multi-Layered Masterclass: 5 Pillars of Final Mitigation
- **Story**: The comprehensive 5-pillar defense that permanently resolved the attack:
  1. Anomaly & Fingerprint Filtering (Tor, Unknown Geo, Linux+Safari mismatch).
  2. Datacenter ASN Blacklisting.
  3. Deprecating HTTP/1.1 (Requiring modern HTTP/2+).
  4. Dual-Speed Rate Limiting (Fast burst & Slow continuous leaks).
  5. Cloudflare Managed Challenge on static page entry + Super Bot Fight Mode.
- **Diagram (`slide14_five_pillars_defense_matrix.png`)**: Comprehensive 5-pillar architectural defense matrix.
- **Presenter Note**: This multi-layered strategy permanently won the war. We dropped datacenter ASNs, blocked OS/browser fingerprint anomalies like Linux running Safari, deprecated HTTP/1.1 since modern users use HTTP/2+, added dual-speed rate limiting, and placed Cloudflare Managed Challenges on static page entry.

#### Slide 15: Profiling the Threat Actor: Autonomous AI Botnets & Sandbox Targets
- **Story**: The attacker profile: Autonomous AI agents analyzing client JS and tuning evasion. Batch attacks with sacrificial probes to measure rate limits. The service served as an empirical sandbox / training ground rather than an extortion target.
- **Diagram (`slide15_threat_actor_profiling.png`)**: Analytical diagram showing the AI botnet feedback loop, sacrificial probe testing, and live sandbox targeting.
- **Presenter Note**: Who was doing this? The speed of their adaptation strongly points to autonomous AI-driven agents reverse-engineering frontend code. They used sacrificial probe machines to measure rate limits. Why my site? A public service with heavy compute and an active defender is the perfect live training ground for attackers to benchmark their tools.

#### Slide 16: Engineering Takeaways & Incident Post-Mortem Checklist
- **Story**: The enduring architectural lessons:
  1. Beware of Pay-Per-Request WAFs under EDoS.
  2. Geo-blocking is dead against residential botnets.
  3. Protocol gating (HTTP/2+) and fingerprinting outperform simple IP rules.
  4. Move challenges to the edge—never challenge at the origin.
- **Diagram (`slide16_key_takeaways_summary.png`)**: 4-card summary of foundational engineering takeaways.
- **Presenter Note**: In closing: never expose origins directly, beware of pay-per-request WAF billing traps during EDoS attacks, drop HTTP/1.1, and always shift challenges to the unmetered edge. Thank you, and I look forward to your questions.
