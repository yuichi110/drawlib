::: block (80, 40) (1760, 70)
# Application-Layer Tactics: Static JS Token Spoofing
:::

::: block (80, 140) (680, 810)
## Why "Secret" JS Logic Failed

- **Custom Header Verification**
  Added obfuscated frontend JS to compute `X-Client-Signature` on `/synthesize` calls.
- **3 Hours of Relief**
  Simple HTTP flood bots were dropped immediately (`403 Forbidden`).
- **Automated AST Reverse-Engineering**
  Within **3 hours**, the attacker parsed our JS bundle and replicated the exact HMAC algorithm in their headless bot scripts.
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
text((57.5, 83.5), "How the Adversary Reverse-Engineered Client JS Tokens in 3 Hours", style=Styles.BlackBold.patch(text_size=11.0))

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=9.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=9.5),
    node_card_style=Styles.White,
    autonumber=True,
    col_width=36.0,
    step_y=6.8,
)

bot = d.add(Participant((24, 15), "AI Bot Operator\n& Headless Swarm", icon=PhosphorIcon.ROBOT, icon_size=6.0, style=Styles.Accent, card_style=Styles.SecondaryNeutral))
edge = d.add(Participant((24, 15), "Frontend Bundle\n(app.min.js)", icon=PhosphorIcon.FILE_JS, icon_size=6.0, card_style=Styles.PrimaryNeutral))
api = d.add(Participant((24, 15), "Cloud Run API\n(/synthesize)", icon=GcpIcon.CLOUD_RUN, icon_size=6.0, card_style=Styles.White))

bot.request(api, "POST /synthesize (No Custom Header)")
api.reply(bot, "403 Forbidden (Missing X-Client-Signature)")

with d.loop("Attacker Automated Recon (< 3 Hours)"):
    bot.request(edge, "Fetch & De-obfuscate app.min.js AST")
    edge.reply(bot, "Extract Secret Salt & Token Function")

bot.request(api, "POST /synthesize + Spoofed X-Client-Signature")
api.reply(bot, "200 OK — Full TTS CPU Drain Resumes!")

d.draw(xy=(9.5, 5.0), scale=0.86)
```
:::

::: block (1720, 995) (140, 30)
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
