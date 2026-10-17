# Workspace Icons Plan (`drawlib.icons.workspace` & `drawlib.icons.original_workspace`)

## 1. Objective & Scope

Add a dedicated workplace, productivity suite, collaboration, CRM/ERP, and business SaaS icon suite under `drawlib.icons.workspace` (`WorkspaceIcon`) for official brand logos, and `drawlib.icons.original_workspace` (`OriginalWorkspaceIcon`) combining vendor-neutral business/productivity concept icons with 2D flat pastel counterparts of the official logos.

- **Modules**:
  - `drawlib.icons.workspace` (`WorkspaceIcon`) — 50 official Microsoft 365, Google Workspace, collaboration, design, CRM/ERP, and business SaaS logos (+ shorthand aliases).
  - `drawlib.icons.original_workspace` (`OriginalWorkspaceIcon`) — 24 vendor-neutral workplace & business SaaS concept icons + 50 2D flat pastel vendor counterparts (74 canonical icons total + shorthand aliases).
- **Release Asset Packages**:
  - `icon_workspace` (`tools/release_assets/v0.3/icons/workspace/`)
  - `icon_original_workspace` (`tools/release_assets/v0.3/icons/original_workspace/`)
- **Code Reuse & Independent PNG Folders**:
  - Overlapping collaboration tools `slack` and `jira` reuse the Python drawing scripts from `devops` (`tools/icons_src/devops/{slack,jira}_default.py` and `tools/icons_src/original_devops/{slack,jira}_default.py`).
  - Rendered PNG files and manifests remain completely independent inside `workspace/` and `original_workspace/`.

---

## 2. Canonical `workspace` Icons (50 Official Workplace & Business SaaS Logos)

| Category | # | Canonical Name | Product / Brand | Shorthand Aliases / Overlap |
| :--- | :- | :--- | :--- | :--- |
| **1. Microsoft 365 & Power Platform** | 1 | `microsoft_365` | Microsoft 365 | `m365`, `office_365` |
| | 2 | `microsoft_teams` | Microsoft Teams | `teams`, `ms_teams` |
| | 3 | `outlook` | Microsoft Outlook | `ms_outlook` |
| | 4 | `word` | Microsoft Word | `ms_word` |
| | 5 | `excel` | Microsoft Excel | `ms_excel` |
| | 6 | `powerpoint` | Microsoft PowerPoint | `ms_powerpoint`, `ppt` |
| | 7 | `onedrive` | Microsoft OneDrive | `ms_onedrive` |
| | 8 | `sharepoint` | Microsoft SharePoint | `ms_sharepoint` |
| | 9 | `power_bi` | Microsoft Power BI | `powerbi` |
| | 10 | `power_automate` | Microsoft Power Automate | `power_apps`, `ms_flow` |
| **2. Google Workspace** | 11 | `google_workspace` | Google Workspace | `gsuite` |
| | 12 | `gmail` | Gmail | — |
| | 13 | `google_drive` | Google Drive | `gdrive` |
| | 14 | `google_docs` | Google Docs | `gdocs` |
| | 15 | `google_sheets` | Google Sheets | `gsheets` |
| | 16 | `google_slides` | Google Slides | `gslides` |
| | 17 | `google_calendar` | Google Calendar | `gcal` |
| | 18 | `google_meet` | Google Meet | `gmeet` |
| | 19 | `google_chat` | Google Chat | `gchat` |
| | 20 | `google_forms` | Google Forms | `gforms` |
| **3. Chat, Docs, PM & Design** | 21 | `slack` | Slack | Reuses `devops/slack` |
| | 22 | `zoom` | Zoom Workplace | — |
| | 23 | `webex` | Cisco Webex | `cisco_webex` |
| | 24 | `discord` | Discord | — |
| | 25 | `notion` | Notion | — |
| | 26 | `confluence` | Atlassian Confluence | — |
| | 27 | `jira` | Atlassian Jira | Reuses `devops/jira` |
| | 28 | `asana` | Asana | — |
| | 29 | `monday` | monday.com | `monday_com` |
| | 30 | `figma` | Figma | — |
| **4. Collab, Files, Sign & Workflow** | 31 | `miro` | Miro | — |
| | 32 | `canva` | Canva | — |
| | 33 | `adobe_acrobat` | Adobe Acrobat | `acrobat`, `adobe` |
| | 34 | `dropbox` | Dropbox | — |
| | 35 | `box` | Box | `box_storage` |
| | 36 | `docusign` | DocuSign | — |
| | 37 | `trello` | Trello | — |
| | 38 | `linear` | Linear | — |
| | 39 | `airtable` | Airtable | — |
| | 40 | `zapier` | Zapier | — |
| **5. CRM, ERP, ITSM, HR & FinTech** | 41 | `salesforce` | Salesforce | `sfdc` |
| | 42 | `hubspot` | HubSpot | — |
| | 43 | `zendesk` | Zendesk | — |
| | 44 | `servicenow` | ServiceNow | `snow` |
| | 45 | `sap` | SAP | — |
| | 46 | `workday` | Workday | — |
| | 47 | `dynamics_365` | Microsoft Dynamics 365 | `dynamics` |
| | 48 | `tableau` | Tableau | — |
| | 49 | `stripe` | Stripe | — |
| | 50 | `shopify` | Shopify | — |

---

## 3. Canonical `original_workspace` Icons (24 Concept Icons + 50 Pastel Logos = 74 Icons)

### Part A: Vendor-Neutral Workplace & Business SaaS Concept Icons (24 Icons)

| Category | # | Canonical Name | Shorthand Aliases | 2D Pastel Motif (`PASTEL_BLUE` / `PASTEL_GREEN` / `WHITE`) |
| :--- | :- | :--- | :--- | :--- |
| **1. Mail, Calendar & Comms** | 1 | `email` | `mail`, `inbox` | Envelope (`WHITE` / `PASTEL_BLUE`) + `PASTEL_GREEN` notification badge |
| | 2 | `calendar` | `schedule`, `meeting_invite` | Calendar page (`WHITE` body, `PASTEL_BLUE` header) + `PASTEL_GREEN` date cell |
| | 3 | `chat_message` | `instant_message`, `team_chat` | Dual overlapping chat bubbles (`PASTEL_BLUE` & `PASTEL_GREEN`) |
| | 4 | `video_meeting` | `video_call`, `online_meeting` | Video camera / meeting screen (`WHITE` / `PASTEL_BLUE`) + `PASTEL_GREEN` lens / user |
| | 5 | `voice_call` | `phone_call`, `voip` | Telephone handset (`PASTEL_BLUE`) + `PASTEL_GREEN` sound wave arcs |
| | 6 | `announcement` | `broadcast`, `newsletter` | Megaphone (`PASTEL_BLUE` / `WHITE`) + `PASTEL_GREEN` broadcast waves |
| **2. Documents, Sheets & Drive** | 7 | `document` | `word_doc`, `text_doc` | Folded-corner page (`WHITE` / `PASTEL_BLUE`) with text lines |
| | 8 | `spreadsheet` | `sheet`, `table_doc` | Grid table sheet (`WHITE` cells, `PASTEL_GREEN` header bar) |
| | 9 | `presentation` | `slide_deck`, `slides` | 16:9 slide board (`WHITE` / `PASTEL_BLUE`) + `PASTEL_GREEN` chart |
| | 10 | `pdf_document` | `pdf_file`, `report_pdf` | Document page (`WHITE`) + `PASTEL_BLUE` / `PASTEL_GREEN` ribbon badge |
| | 11 | `cloud_drive` | `shared_drive`, `file_sync` | Folder (`PASTEL_BLUE`) + `WHITE` / `PASTEL_GREEN` cloud sync mark |
| | 12 | `knowledge_base` | `wiki`, `internal_docs` | Open book / wiki binder (`WHITE` / `PASTEL_BLUE`) + `PASTEL_GREEN` bookmark |
| **3. Projects, Tasks & Workflow** | 13 | `kanban_board` | `task_board`, `agile_board` | 3-column board (`WHITE`) with `PASTEL_BLUE` & `PASTEL_GREEN` task cards |
| | 14 | `project_plan` | `gantt`, `roadmap` | Timeline bars (`PASTEL_BLUE` & `PASTEL_GREEN`) on `WHITE` schedule card |
| | 15 | `whiteboard` | `brainstorm`, `canvas_board` | Easel / canvas (`WHITE`) with `PASTEL_BLUE` & `PASTEL_GREEN` sticky notes |
| | 16 | `form_survey` | `questionnaire`, `feedback_form` | Checklist form (`WHITE` / `PASTEL_BLUE`) with `PASTEL_GREEN` check boxes |
| | 17 | `e_signature` | `contract_sign`, `digital_sign` | Contract page (`WHITE`) + `PASTEL_BLUE` pen & `PASTEL_GREEN` signature line |
| | 18 | `workflow_automation` | `no_code_flow`, `zap` | Connected trigger-action nodes (`PASTEL_BLUE`) + `PASTEL_GREEN` bolt |
| **4. CRM, ERP, HR & Commerce** | 19 | `crm` | `customer_management`, `sales_lead` | Contact card (`WHITE` / `PASTEL_BLUE`) + `PASTEL_GREEN` star / relationship |
| | 20 | `erp` | `enterprise_resource`, `back_office` | Central hub (`PASTEL_BLUE`) linking finance, inventory & ops modules (`PASTEL_GREEN`) |
| | 21 | `helpdesk` | `support_ticket`, `itsm` | Support headset / ticket tag (`PASTEL_BLUE` / `WHITE`) + `PASTEL_GREEN` check |
| | 22 | `hr_portal` | `human_resources`, `employee_directory` | ID badge / org directory (`WHITE` / `PASTEL_BLUE`) + `PASTEL_GREEN` user |
| | 23 | `billing_invoice` | `payment`, `accounting` | Invoice sheet (`WHITE`) + `PASTEL_BLUE` header & `PASTEL_GREEN` currency badge |
| | 24 | `ecommerce_store` | `online_shop`, `shopping_cart` | Shopping cart / bag (`PASTEL_BLUE` / `WHITE`) + `PASTEL_GREEN` tag |

### Part B: 2D Flat Pastel Logos (50 Icons)
- Every icon in `workspace` (1–50) has a matching 2D flat pastel counterpart in `original_workspace`.
- **Mandatory Brand Color Rule**: Each `original_workspace` vendor icon preserves its official brand color palette softened into Drawlib pastel tones with `DARK = "#323A48"` outlines (`w = 1.9`).

---

## 4. Implementation & Verification Workflow

1. **Phase 1 — Official Reference Collection**:
   - Download official SVG/PNG brand logos for all 50 `workspace` icons into `tools/original_assets/workspace/<name>/` and rasterize `.drawlib/scratch/workspace_ref/<name>_ref.png`.
   - Build a 50-icon reference contact sheet (`workspace_ref_contact_sheet.png`) and present it to the user for visual approval before authoring.
2. **Phase 2 — `workspace` Official Logos**:
   - Wire `workspace` (`WorkspaceIcon`) and `original_workspace` (`OriginalWorkspaceIcon`) across `src/drawlib/_icons/png_icons/`, `src/drawlib/icons.py`, `src/drawlib/diagrams/architecture.py`, `src/drawlib/diagrams/sequence.py`, and `tools/dcli/codegen/`.
   - Reuse `slack_default.py` and `jira_default.py` from `devops` and author the remaining 48 scripts in `tools/icons_src/workspace/<name>_default.py`.
3. **Phase 3 — `original_workspace` Concepts (24) & Pastel Logos (50)**:
   - Author the 24 concept icons and 48 new 2D flat pastel vendor logos (reusing `slack` and `jira` from `original_devops`).
   - Run `./dcli codegen icon-workspace` and `./dcli codegen icon-original-workspace`, sync `_cached_assets` and `_release_assets.py`, run `./dcli code-check all` and `./dcli test target icons diagrams`.
