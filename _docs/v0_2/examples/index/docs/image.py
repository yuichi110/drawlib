from drawlib.apis import *

# Import styles like HTML reference CSS
import docs.style

# Configure drawing canvas size
config(width=100, height=50)

# Apply predefined styles
circle(xy=(25, 30), radius=10, style="mystyle")
text(xy=(25, 10), text="Circle", style="mystyle")
rectangle(xy=(75, 30), width=20, height=20, style="mystyle")
text(xy=(75, 10), text="Rectangle", style="mystyle")

# Save canvas
save()
