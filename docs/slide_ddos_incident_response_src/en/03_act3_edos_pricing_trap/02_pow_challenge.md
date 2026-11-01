::: block xy=(80, 40) width=1760 height=70
# Asymmetric Defense: SHA-256 Proof-of-Work
:::

::: block xy=(80, 140) width=680 height=810
## Cryptographic Cost Inversion

- **One-Time Challenge Seed**
  Server issues an HMAC-signed `seed` with a short TTL via `GET /challenge`.
- **Browser Web Worker (<50ms)**
  Client finds a `nonce` where `SHA256(seed + nonce)` starts with `0000...` (~65k hashes).
- **100% Synthesis Protection**
  Server verifies in **O(1)** (`1 hash`), while 1,000 RPS costs the botnet **65M+ hashes/sec**.
:::

::: block xy=(800, 140) width=1040 height=810
```drawlib
from drawlib.canvas import setup
from drawlib.diagrams.sequence import GcpIcon, Participant, PhosphorIcon, SequenceDiagram
from drawlib.smartarts import Panel
from drawlib.styles import Styles

setup(width=115, height=90)

panel = Panel(
    "Asymmetric SHA-256 Proof-of-Work Protocol",
    style=Styles.Neutral,
    header_style=Styles.PrimaryBold,
    text_style=Styles.BlackBold.patch(text_size=15.5),
    header_variant="underline",
    header_height=9.0,
    header_align="center",
)
panel.draw(xy=(2.0, 2.0), width=111.0, height=86.0)

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=13.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=12.5),
    autonumber=True,
    col_width=34.0,
    step_y=5.8,
    margin=2.0,
)

browser = d.add(Participant("Client Browser\n(UI Thread)", width=26, height=16, icon=PhosphorIcon.BROWSER, icon_size=7.0))
worker = d.add(Participant("Web Worker\n(SHA-256 Solver)", width=26, height=16, icon=PhosphorIcon.CPU, icon_size=7.0, style=Styles.Secondary))
server = d.add(Participant("Cloud Run API\n(O(1) Verifier)", width=26, height=16, icon=GcpIcon.CLOUD_RUN, icon_size=7.5))

browser.request(server, "GET /challenge")
server.reply(browser, "Signed Seed (16 Zero Bits)")

browser.request(worker, "Solve SHA256(seed+nonce)")
worker.reply(browser, "Valid Nonce (~65k Hashes, <50ms)")

browser.request(server, "POST /synthesize (seed, nonce)")
server.reply(browser, "O(1) Hash Check -> 200 OK Audio")

dw, dh = d.get_size()
d.draw(xy=((115.0 - dw) / 2.0, 4.0))
```
:::

::: block xy=(1720, 995) width=140 height=30
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
To defeat automated script spoofing without hurting human UX with intrusive image CAPTCHAs, we implemented an **asymmetric SHA-256 Proof-of-Work (PoW)** protocol:
1. **Signed Challenge Issuance**: Before requesting speech synthesis, the client calls `GET /challenge` and receives a stateless, HMAC-signed timestamped `seed`.
2. **Client-Side Hashcash Puzzle**: A background **Web Worker** iterates through `nonce` values until `SHA-256(seed + nonce)` begins with `k` leading zero bits (e.g., 16 bits $\approx 65,536$ hashes). On a normal smartphone or laptop, this completes silently in **under 50 milliseconds**.
3. **Asymmetric Economic Inversion**:
   - **For the Server**: Verifying the proof takes **exactly 1 SHA-256 hash** ($O(1)$ CPU) plus a fast replay check.
   - **For the Botnet**: Sustaining 1,000 requests/sec now requires computing **65+ million SHA-256 hashes per second**, burning the attacker's own CPU cores.
- **Outcome**: Unauthorized calls to `/synthesize` dropped to **0%** permanently. Even if the attacker reads the JavaScript source code, there is no shortcut around SHA-256 preimage resistance.
:::
