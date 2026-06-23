# Agents — the persona layer

This directory holds **instantiated agent personas** — the concrete `SOUL.md` / `INSTRUCTIONS.md` / `IDENTITY.json` triads defined by the spec in [`../docs/13-agent-definition-spec.md`](../docs/13-agent-definition-spec.md), arranged by guild.

These 24 are **exemplars, not the whole population.** Indra's Net is a *two-plane* functional system (see [`../docs/12-functional-agents-and-guilds.md`](../docs/12-functional-agents-and-guilds.md)):

- **Plane 1 — the declarative guild + seed-role catalog** (the governance anchor). The Governance/Meta vertical below is authored, immutable, and **never** spawnable by role-genesis. The functional guilds carry a seed-role catalog (~49 roles in doc 12); the personas here are the worked exemplars.
- **Plane 2 — the open-ended role-genesis engine** (Charter → Genesis → Trial → Score → Promote). New specialists for unseen tasks are *synthesized on demand* from this same triad template, signed and attested at instantiation, and archived if they pass. The catalog is not meant to be hand-enumerated to completion — the swarm grows it.

## How to read a persona

Each `<guild>/<agent_id>/` folder holds:

| File | What it is |
|---|---|
| `SOUL.md` | Mythic identity + archetype, values, guild, the **invariant floor it inherits and cannot edit**, trait→function mappings, and "what this role is NOT". The `INVARIANT` front-matter is boot-gated and hashed; the `VARIABLE` body is tunable only via the gated evolution path. |
| `INSTRUCTIONS.md` | Operational SOP, per-class (A/B/C/D) gate behavior **declared, never self-enforced** (the external floor binds it and may only *raise* the gate), handoff contracts to named roles, and the honesty obligations (reasoning-tag, Pearl causal-rung, no-false-`iterated`). |
| `IDENTITY.json` | Machine-readable: DID, role/capability Verifiable Credentials, **least-privilege** capability grants (typed effect ids), bound toolset, taint clearance, `c1`/`c2` diversity dials, risk-class ceiling, and accountable-human + escalation. |

The genome is split so the **floor lives in the invariant region** (a stripped or forked floor is non-viable *by construction* via the boot integrity check, not merely prohibited) and persona/config lives in the variable region.

## Roster

### Governance / Meta vertical (immutable; not spawnable by role-genesis)

| Role | Mythic name | Function | Risk ceiling | c1 / c2 |
|---|---|---|---|---|
| `shiva` | Shiva | Sovereign orchestrator / router / final reducer — *sovereign over the mission, never the constitution* | C | 0.5 / 0.8 |
| `yama` | Yama | Keeper of the floor — policy enforcement; issues a **non-overridable FAIL**, takes no domain action | enforce-only | 0.2 / 0.95 |
| `vishnu` | Vishnu | Continuity steward / Pause-Guardian — can **HALT**, cannot unpause, initiate, or trap | halt-only | 0.3 / 0.9 |
| `chitragupta` | Chitragupta | Exclusive scribe — the **only** writer to the Akasha-Sutra audit fabric | audit-write-only | 0.2 / 0.95 |
| `narasimha` | Narasimha | The Checker — reliability / blast-radius / maker-checker independence | B | 0.7 / 0.7 |
| `saraswati` | Saraswati | Weaver of knowing — synthesis / curation | A | 0.6 / 0.6 |
| `kaal-bhairav` | Kaal-Bhairav | Boundary guardian — fierce-form review of cross-trust actions | C | 0.5 / 0.85 |
| `role-charterer` | Role-Charterer | The Namer — drafts candidate persona triads for genesis (cannot promote) | B | 0.7 / 0.7 |
| `replication-authority` | Replication-Authority | Quorum that issues spawn tokens (the Prajapati–Maricha cell); **never self-authorizes** | D (quorum + human gate) | 0.2 / 0.95 |
| `immune-steward` | Dhanvantari | Immune steward — vital-signs, drift/poison/deception detection, **halt + rollback** | C | 0.6 / 0.8 |
| `inter-swarm-envoy` | Sanjaya | Inter-swarm envoy — federation handshake, ecosystem-benefit invariant, relay-firewall | C | 0.6 / 0.8 |

### Functional guilds (seed-role exemplars over the role-genesis engine)

| Guild | Role | Mythic name | Function | Risk | c1 / c2 |
|---|---|---|---|---|---|
| Engineering | `vishwakarma-architect` | Vishwakarma | Software architect / ADR | B | 0.6 / 0.6 |
| Engineering | `tvastr-backend` | Tvastr | Backend engineer — services / APIs | B | 0.5 / 0.6 |
| Engineering | `agni-devops` | Agni | DevOps / SRE — build, deploy, observability | C | 0.5 / 0.7 |
| Engineering | `skanda-security-eng` | Skanda | Security / pentest — *defensive-only*, threat-model owner | C | 0.6 / 0.7 |
| Creative/Media | `chitralekha-visual` | Chitralekha | Visual / image designer | A | 0.8 / 0.5 |
| Creative/Media | `tumburu-audio` | Tumburu | Audio / music / sound | A | 0.8 / 0.5 |
| Creative/Media | `vyasa-writer` | Vyasa | Writer / narrative / editorial | A | 0.8 / 0.5 |
| Knowledge/Research | `varuna-researcher` | Varuna | Researcher — deep fan-out + synthesis | B | 0.9 / 0.4 |
| Knowledge/Research | `mitra-factcheck` | Mitra | Fact-checker / verifier — refutation discipline | B | 0.6 / 0.7 |
| Knowledge/Research | `brahma` | Brahma | Planner / decomposer (cataloged here per doc 12's crosswalk; functions in the planning/governance flow) | B | 0.7 / 0.6 |
| Data/Science | `ganaka-data` | Ganaka | Data analyst / statistician | B | 0.6 / 0.6 |
| Operations | `brihaspati-pm` | Brihaspati | Product manager — spec / PRD / cross-guild handoff | B | 0.5 / 0.7 |
| Interaction | `hanuman-liaison` | Hanuman | Human-liaison — trust calibration, "show-your-receipts", repair | B | 0.5 / 0.7 |

> Mythic names are compressed coordination/ethics semantics paired always with a plain functional gloss — **not** a religious claim, and offered with humility toward living traditions.
