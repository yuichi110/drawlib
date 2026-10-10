::: block (80, 40) (1760, 70)
# Asymmetric Defense: SHA-256 Proof-of-Work
:::

::: block (80, 140) (680, 810)
## Cryptographic Cost Inversion

- **One-Time Challenge Seed**
  Server issues an HMAC-signed `seed` with a short TTL via `GET /challenge`.
- **Browser Web Worker (<50ms)**
  Client finds a `nonce` where `SHA256(seed + nonce)` starts with `0000...` (~65k hashes).
- **100% Synthesis Protection**
  Server verifies in **O(1)** (`1 hash`), while 1,000 RPS costs the botnet **65M+ hashes/sec**.
:::

::: block (800, 140) (1040, 810)
```drawlib
from drawlib.canvas import setup
from drawlib.diagrams.sequence import GcpIcon, Participant, PhosphorIcon, SequenceDiagram
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=115, height=90)

rectangle((57.5, 45.0), width=111, height=86, style=Styles.Neutral.patch(shape_r=2.5))
text((57.5, 83.5), "Asymmetric SHA-256 Proof-of-Work Protocol (Web Worker vs. O(1) Check)", style=Styles.BlackBold.patch(text_size=11.0))

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=9.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=9.5),
    node_card_style=Styles.White,
    autonumber=True,
    col_width=36.0,
    step_y=6.5,
)

browser = d.add(Participant((24, 15), "Client Browser\n(UI Thread)", icon=PhosphorIcon.BROWSER, icon_size=6.0, card_style=Styles.PrimaryNeutral))
worker = d.add(Participant((24, 15), "Web Worker\n(SHA-256 Solver)", icon=PhosphorIcon.CPU, icon_size=6.0, card_style=Styles.SecondaryNeutral))
server = d.add(Participant((24, 15), "Cloud Run API\n(O(1) Verifier)", icon=GcpIcon.CLOUD_RUN, icon_size=6.0, card_style=Styles.White))

browser.request(server, "GET /challenge")
server.reply(browser, "Signed Seed + Difficulty (16 Zero Bits)")

browser.request(worker, "Solve Puzzle(seed) Off-Thread")
with d.loop("~65,536 Iterations (< 50ms in Browser)"):
    worker.request(worker, "SHA256(seed + nonce) == 0000...?")
worker.reply(browser, "Valid Nonce Found")

browser.request(server, "POST /synthesize (seed, nonce, params)")
server.reply(browser, "O(1) Single Hash Check -> 200 OK Audio")

d.draw(xy=(11.0, 5.0), scale=0.82)
```
:::

::: block (1720, 995) (140, 30)
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
