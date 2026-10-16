# Original Cloud Icons Reorganization & Expansion Plan (`drawlib.icons.original_cloud`)

## 1. Objective & Scope

Reorganize and expand `tools/icons_src/original_cloud/` into an orthogonal, comprehensive **87-icon** vendor-neutral cloud and hybrid architecture icon set (`drawlib.icons.original_cloud` / `OriginalCloudIcon`):

1. **Removed Obsolete/Redundant Icons (3)**:
   - `pub_sub` (consolidated into `message_queue`)
   - `service_bus` (consolidated into `message_queue`)
   - `vector_database` (removed from `original_cloud` to avoid overlap with `original_ai`)
2. **Renamed Icon (1)**:
   - `time_series_db` -> `time_series_database` (consistent `*_database` naming)
3. **Retained Existing Icons (52)**:
   - Kept intact in `tools/icons_src/original_cloud/*_default.py`
4. **Newly Authored Icons (34)**:
   - Covering Compute & Accelerators (`gpu_node`, `gpu_cluster`, `npu_node`, `bare_metal`), Virtualization Stack (`virtualization_host`, `virtualization_cluster`, `virtualization_controller`), Managed App/VDI (`app_service`, `virtual_desktop`), Storage/DR/Migration (`disaster_recovery`, `data_migration`), Data & Analytics (`distributed_database`, `blockchain_ledger`, `analytics_engine`, `data_catalog`), Networking & Hybrid (`internet_gateway`, `nat_gateway`, `transit_hub`, `network_peering`, `private_endpoint`, `reverse_proxy`, `service_discovery`, `dedicated_interconnect`), Security & Identity (`directory_service`, `key_management`, `bastion_host`, `security_center`), and Integration/IoT/Governance (`email_service`, `media_streaming`, `external_saas`, `iot_hub`, `digital_twin`, `organization_account`, `cost_management`).

---

## 2. Visual Language Rules (`original_cloud`)

All 34 new icons strictly follow the `original_cloud` visual language defined in `tools/icons_src/utils.py`:
- **Canvas**: `setup_icon()` (`100x100` coordinate space, `(0,0)` bottom-left, `(50,50)` center, `200` DPI supersampling -> normalized to `512x512` PNG with `460x460` inner bounding box).
- **Safe Margin**: Keep all strokes and shapes within `[10, 90]` on both axes.
- **Color Palette**:
  - Structural Outlines: `DARK` (`#323A48`), stroke width `w = ORIG_STROKE` (`2.7` units; `2.0–2.5` units for fine internal details).
  - Primary Fill: `PASTEL_BLUE` (`#86A4F7`) and `PASTEL_BLUE_LIGHT` (`#ACC2FA`).
  - Secondary / Focal Accent Fill: `PASTEL_GREEN` (`#7AD69E`).
  - Base / Card Surface Fill: `WHITE` (`#FFFFFF`).
- **No Text Labels**: Pure geometric silhouettes and crisp vector iconography that remain legible at both `64px` and `512px`.

---

## 3. Specifications for the 34 New Icons (4 Parallel Batches)

### Batch 1: Compute, Accelerators, Virtualization & VDI (9 Icons)
1. **`gpu_node`**:
   - IC chip frame (`WHITE` outer rounded square `56x56` with 12 pins on 4 sides) containing a `2x2` parallel shader core grid (`3` `PASTEL_BLUE` cores + `1` `PASTEL_GREEN` focal core).
2. **`gpu_cluster`**:
   - Three interconnected parallel accelerator blades/chips arranged in a cluster with high-speed interconnect buses (`DARK` lines + `PASTEL_GREEN` link nodes) and `PASTEL_BLUE` multi-core dies.
3. **`npu_node`**:
   - AI/Tensor processor chip (`WHITE` outer chip package with pins) featuring a diamond/hexagonal neural systolic array core (`PASTEL_GREEN` center diamond + `PASTEL_BLUE` surrounding tensor nodes connected by circuit traces).
4. **`bare_metal`**:
   - 3-tier physical rackmount server chassis (`WHITE` & `PASTEL_BLUE` horizontal server blades stacked vertically with drive bay slots and `PASTEL_GREEN` power LEDs, no hypervisor abstraction box).
5. **`virtualization_host`**:
   - Hypervisor physical host blade at the bottom (`PASTEL_BLUE` server unit with LED) supporting two isometric 3D VM cubes (`WHITE`/`PASTEL_BLUE`/`PASTEL_GREEN`) mounted directly above it.
6. **`virtualization_cluster`**:
   - Three virtualization host blades at the base bridged by a shared cluster interconnect bus, topped by a coordinated group of 3 isometric 3D VM cubes (`PASTEL_BLUE` & `PASTEL_GREEN`).
7. **`virtualization_controller`**:
   - Central management console / control hub (`WHITE` monitor/frame with `PASTEL_GREEN` control gear/hub in center) orchestrating 3 connected isometric VM/host nodes around/below it (vCenter metaphor).
8. **`app_service`**:
   - Browser/application window frame (`WHITE` card with `PASTEL_BLUE` top bar) with an embedded cloud/rocket deployment badge (`PASTEL_GREEN` play/launch emblem) representing managed Web App PaaS.
9. **`virtual_desktop`**:
   - Desktop monitor (`WHITE` screen with `PASTEL_BLUE` display workspace and stand) overlapped by a cloud badge (`PASTEL_GREEN`) in the upper-right corner representing Cloud VDI.

### Batch 2: Storage, DR, Migration, Databases & Analytics (6 Icons)
10. **`disaster_recovery`**:
   - Primary site cylinder/server (`PASTEL_BLUE`) and secondary standby site (`PASTEL_GREEN`) linked by a circular failover/recovery arrow with a protective shield/heartbeat accent.
11. **`data_migration`**:
   - Source database cylinder on the left (`WHITE`/`PASTEL_BLUE`) transferring data blocks across dynamic motion arrows into a target cloud database cylinder on the right (`PASTEL_GREEN`).
12. **`distributed_database`**:
   - Central globe/network ring (`WHITE`/`PASTEL_BLUE_LIGHT`) with 3 synchronized database cylinders (`PASTEL_BLUE` and `PASTEL_GREEN`) positioned at triangle vertices around the ring.
13. **`blockchain_ledger`**:
   - Chain of 3 isometric 3D blocks (`PASTEL_BLUE` and `PASTEL_GREEN` faces) linked sequentially by heavy cryptographic chain links (`DARK`).
14. **`analytics_engine`**:
   - Big data processing gear/turbine (`PASTEL_BLUE` outer gear ring) enclosing rising analytics bar chart columns and a `PASTEL_GREEN` spark/lightning node (Spark/EMR/Dataproc metaphor).
15. **`data_catalog`**:
   - Structured catalog book/binder (`WHITE` & `PASTEL_BLUE`with index tabs on the right) and a magnifying glass / metadata tag (`PASTEL_GREEN`) on the front cover.

### Batch 3: Networking & Hybrid Connectivity (8 Icons)
16. **`internet_gateway`**:
   - Wireframe globe (`WHITE` circle with latitude/longitude arcs in `DARK` and `PASTEL_BLUE` continents/hemisphere) with an entry/exit gateway arch or bidirectional portal arrow (`PASTEL_GREEN`).
17. **`nat_gateway`**:
   - Gateway translation router box (`WHITE`/`PASTEL_BLUE`) where 3 private input paths on the left converge into 1 public outbound arrow (`PASTEL_GREEN`) on the right.
18. **`transit_hub`**:
   - Central hexagonal/circular transit hub (`PASTEL_GREEN` core inside `WHITE` ring) with 6 radial spoke connections to surrounding `PASTEL_BLUE` VPC/network nodes.
19. **`network_peering`**:
   - Two overlapping/adjacent virtual network clouds or nodes (`PASTEL_BLUE` left, `PASTEL_GREEN` right) joined directly by a bidirectional horizontal peering bridge (`WHITE`/`DARK`).
20. **`private_endpoint`**:
   - Virtual network boundary bracket containing a locked private tunnel/keyhole socket (`PASTEL_BLUE` shield/socket + `PASTEL_GREEN` lock/plug connection).
21. **`reverse_proxy`**:
   - Single ingress shield/gateway node on the left (`PASTEL_GREEN`) inspecting and forwarding requests to 2 backend server boxes on the right (`PASTEL_BLUE`).
22. **`service_discovery`**:
   - Compass / radar directory dial (`WHITE` outer ring, `PASTEL_BLUE` inner ring, `PASTEL_GREEN` compass needle pointing to a discovered service node).
23. **`dedicated_interconnect`**:
   - High-speed fiber-optic trunk cable bundle (`PASTEL_BLUE` & `PASTEL_GREEN` parallel conduits) linking an on-premises building block (left) and cloud node (right).

### Batch 4: Security, Messaging, IoT & Cloud Management (11 Icons)
24. **`directory_service`**:
   - Hierarchical Active Directory / LDAP tree pyramid: top root diamond/hexagon (`PASTEL_GREEN`) branching down into middle organizational units (`PASTEL_BLUE`) and bottom user/object nodes (`WHITE`).
25. **`key_management`**:
   - Ornate cryptographic key (`PASTEL_GREEN` bow + `PASTEL_BLUE` shaft/teeth) inside a hexagonal security plate (`WHITE`).
26. **`bastion_host`**:
   - Fortified castle turret / watchtower gate (`WHITE` & `PASTEL_BLUE` battlements) with a secure SSH terminal prompt `>_` (`PASTEL_GREEN`) in the center.
27. **`security_center`**:
   - Large central security shield (`WHITE` & `PASTEL_BLUE` split shield) with a radar target / checkmark emblem (`PASTEL_GREEN`) at its core.
28. **`email_service`**:
   - Crisp postal envelope (`WHITE` body with `PASTEL_BLUE` flap) with a fast-delivery motion wing/badge (`PASTEL_GREEN`).
29. **`media_streaming`**:
   - Video player frame / signal waves (`WHITE` card with `PASTEL_BLUE` broadcast arcs) and a central play triangle button (`PASTEL_GREEN`).
30. **`external_saas`**:
   - Cloud silhouette (`WHITE`/`PASTEL_BLUE`) with an interlocking puzzle piece / external plug connector (`PASTEL_GREEN`).
31. **`iot_hub`**:
   - Central cloud/hexagon IoT hub (`PASTEL_BLUE`) receiving telemetry signals from 4 surrounding sensor/antenna nodes (`PASTEL_GREEN` & `WHITE`).
32. **`digital_twin`**:
   - Real-world 3D physical cube on the left (`PASTEL_BLUE`) mirrored across a symmetry axis into a virtual wireframe/hologram twin cube on the right (`PASTEL_GREEN`).
33. **`organization_account`**:
   - Top management account crown/root node (`PASTEL_GREEN`) organizing 3 child account cards (`PASTEL_BLUE` & `WHITE`) in a structured org hierarchy.
34. **`cost_management`**:
   - Financial coin / currency badge (`PASTEL_GREEN` circle with coin rim) paired with a cost optimization trend chart (`PASTEL_BLUE` & `WHITE` card).
