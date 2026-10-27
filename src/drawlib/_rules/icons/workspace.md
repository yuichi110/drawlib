# Drawlib Workspace Icons Guidelines (`lib-icons-workspace`)

API specification and complete catalog for `drawlib.icons.workspace` (`WorkspaceIcon`, **40** official Google Workspace, Microsoft 365, Slack, Notion, Jira, Figma, and BI brand icons) and `drawlib.icons.original_workspace` (`OriginalWorkspaceIcon`, **57** flat 2D pastel icons: **40** brand twins + **17** vendor-neutral collaboration and document concept icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature & Twin Module Structure

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import Node, OriginalWorkspaceIcon, WorkspaceIcon
from drawlib.icons import original_workspace, original_workspace_icon, workspace, workspace_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
workspace.slack((30, 25), width=9.0, style=Styles.Primary)
original_workspace.slack((55, 25), width=9.0, style=Styles.Primary)
original_workspace.knowledge_base((80, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
workspace_icon((30, 10), width=9.0, name="notion", style=Styles.Primary)
original_workspace_icon((55, 10), width=9.0, name="kanban_board", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
chat_node = Node("Slack Bot", width=24, height=18, icon=WorkspaceIcon.SLACK, icon_size=7.5)
wiki_node = Node("Team Wiki", width=24, height=18, icon=OriginalWorkspaceIcon.KNOWLEDGE_BASE, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.workspace` | `WorkspaceIcon` | **40** | `icon_workspace` | Official product logos for Google Workspace, Microsoft 365, Slack, Zoom, Notion, Jira, Figma, and BI tools. |
| `drawlib.icons.original_workspace` | `OriginalWorkspaceIcon` | **57** (`40` + `17`) | `icon_original_workspace` | Flat 2D pastel twins for all 40 brands plus **17 vendor-neutral collaboration, document & workflow concepts**. |

---

## 2. Complete 40 Shared Brand Icons (`workspace.*` & `original_workspace.*`)

| Category | Count | Canonical Function Names (`workspace.*` & `original_workspace.*`) |
| :--- | :---: | :--- |
| **Google Workspace Suite** | 10 | `gmail`, `google_calendar`, `google_chat`, `google_docs`, `google_drive`, `google_forms`, `google_meet`, `google_sheets`, `google_slides`, `google_workspace` |
| **Microsoft 365 Productivity Suite** | 8 | `excel`, `microsoft_365`, `microsoft_teams`, `onedrive`, `outlook`, `powerpoint`, `sharepoint`, `word` |
| **Team Messaging & Video Conferencing** | 4 | `discord`, `slack`, `webex`, `zoom` |
| **Project Management, Issue Tracking & Wiki** | 7 | `asana`, `confluence`, `jira`, `linear`, `monday`, `notion`, `trello` |
| **Cloud Storage, PDF & Collaborative Design** | 6 | `adobe_acrobat`, `box`, `canva`, `dropbox`, `figma`, `miro` |
| **No-Code Databases, BI & Workflow Automation** | 5 | `airtable`, `power_automate`, `power_bi`, `tableau`, `zapier` |

---

## 3. Complete 17 Vendor-Neutral Workspace Concept Icons (`original_workspace.*` Only)

| Canonical Function (`original_workspace.*`) | `OriginalWorkspaceIcon` Enum | Collaboration Role |
| :--- | :--- | :--- |
| `announcement` | `ANNOUNCEMENT` | Company-wide broadcast, release bulletin, or incident banner |
| `calendar` | `CALENDAR` | Shared team calendar, on-call rotation schedule, or booking service |
| `chat_message` | `CHAT_MESSAGE` | Instant messaging channel, ChatOps webhook, or bot notification |
| `cloud_drive` | `CLOUD_DRIVE` | Enterprise file sync and share (EFSS) repository |
| `document` | `DOCUMENT` | Collaborative word processing document or technical specification |
| `email` | `EMAIL` | Corporate email inbox, SMTP relay target, or digest notification |
| `form_survey` | `FORM_SURVEY` | User feedback form, intake questionnaire, or survey portal |
| `kanban_board` | `KANBAN_BOARD` | Sprint backlog, issue triage board, or task tracking workflow |
| `knowledge_base` | `KNOWLEDGE_BASE` | Internal engineering wiki, runbook portal, or RAG document corpus |
| `pdf_document` | `PDF_DOCUMENT` | Portable Document Format (PDF) report, contract, or export artifact |
| `presentation` | `PRESENTATION` | Slide deck, executive briefing, or architecture review presentation |
| `project_plan` | `PROJECT_PLAN` | Roadmap timeline, milestone plan, or delivery schedule |
| `spreadsheet` | `SPREADSHEET` | Tabular financial model, CSV export, or operational data sheet |
| `video_meeting` | `VIDEO_MEETING` | Multiparty video conference bridge, webinar, or virtual war room |
| `voice_call` | `VOICE_CALL` | VoIP audio call, SIP softphone, or conference bridge |
| `whiteboard` | `WHITEBOARD` | Infinite canvas for architecture brainstorming and retrospectives |
| `workflow_automation` | `WORKFLOW_AUTOMATION` | Event-driven webhook trigger, low-code connector, or iPaaS flow |

```drawlib code=fold align=center file=icons_workspace_rules_arch.png caption="ChatOps Incident Triage & Knowledge Sync Pipeline Using WorkspaceIcon and OriginalWorkspaceIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    Node,
    NodeGroup,
    OriginalWorkspaceIcon,
    WorkspaceIcon,
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

slack = d.add(
    Node("Slack Ops\nChannel", width=24, height=18, icon=WorkspaceIcon.SLACK, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
hub = d.add(NodeGroup(title="Workspace Automation & Wiki Hub", padding=4.5), xy=(42, 4))
jira = hub.add(Node("Jira Sprint\nBacklog", width=24, height=18, icon=WorkspaceIcon.JIRA, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
kb = hub.add(Node("Internal\nKnowledge Base", width=24, height=18, icon=OriginalWorkspaceIcon.KNOWLEDGE_BASE, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(slack, jira, label="Triage", padding=1.5)
d.connect(jira, kb, label="Postmortem", padding=1.5)
d.draw(xy=(4, 4))
save()
```
