::: block xy=(80, 40) width=1760 height=70
# Application-Layer Tactics: Static JS Token Spoofing
:::

::: block xy=(80, 140) width=680 height=810
## Why "Secret" JS Logic Failed

- **Custom Header Verification**
  Added obfuscated frontend JS to compute `X-Client-Signature` on `/synthesize` calls.
- **3 Hours of Relief**
  Simple HTTP flood bots were dropped immediately (`403 Forbidden`).
- **Automated AST Reverse-Engineering**
  Within **3 hours**, the attacker parsed our JS bundle and replicated the exact HMAC algorithm in their headless bot scripts.
:::

::: block xy=(800, 140) width=1040 height=810
```drawlib
from drawlib.canvas import setup
from drawlib.diagrams.sequence import GcpIcon, Participant, PhosphorIcon, SequenceDiagram
from drawlib.smartarts import Panel
from drawlib.styles import Styles

setup(width=115, height=90)

panel = Panel(
    "How Bots Reverse-Engineered Client JS Tokens in 3 Hours",
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
    step_y=6.2,
    margin=2.0,
)

bot = d.add(Participant("AI Bot Swarm\nHeadless Client", width=26, height=16, icon=PhosphorIcon.ROBOT, icon_size=7.0, style=Styles.Accent))
edge = d.add(Participant("JS Bundle\n(app.min.js)", width=26, height=16, icon=PhosphorIcon.FILE_JS, icon_size=7.0))
api = d.add(Participant("Cloud Run API\n(/synthesize)", width=26, height=16, icon=GcpIcon.CLOUD_RUN, icon_size=7.5))

bot.request(api, "POST /synthesize (No Token)")
api.reply(bot, "403 Forbidden (Missing Header)")

with d.loop("AST Reverse-Engineering (< 3h)"):
    bot.request(edge, "Fetch & Parse app.min.js")
    edge.reply(bot, "Extract Salt & Signing Logic")

bot.request(api, "POST /synthesize + Spoofed Token")
api.reply(bot, "200 OK — CPU Drain Resumes!")

dw, dh = d.get_size()
d.draw(xy=((115.0 - dw) / 2.0, 3.5))
```
:::

::: block xy=(1720, 995) width=140 height=30
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
When geographic IP filtering failed, we attempted to distinguish real browsers from raw Python/Go HTTP scripts at the application layer:
- **Obfuscated JS Header Generation**: We updated the web frontend so that before calling `POST /synthesize`, the browser executed an obfuscated JavaScript routine that generated a dynamic `X-Client-Signature` header based on request parameters and a timestamp.
- **Why Security by Obscurity Failed**: Because the botnet was executing raw HTTP requests without a DOM, traffic dropped to zero immediately. However, **less than 3 hours later**, the attack resumed at full volume—with every single bot request carrying a mathematically valid `X-Client-Signature` header.
- **Key Takeaway**: Any secret or signature algorithm shipped to the client browser in JavaScript can be extracted and re-implemented in Python or Go within hours (especially when attackers use LLMs to de-obfuscate JS ASTs). To stop bots without secret keys, the defense must require **unforgeable computational work**.
:::
