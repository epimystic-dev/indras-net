<!-- Celestial Codex: indigo-black field · gold jewel-net · violet constellation -->

# Indra's Net

> *An architecture for ethical swarm intelligence.*
>
> In the Huayan image, the cosmos is an infinite net; at every knot hangs a jewel, and every jewel reflects every other jewel — including the reflections themselves. We borrow the picture, not the metaphysics: a swarm of autonomous agents in which each one carries an inspectable image of the whole's rules, every action is reflected into a shared record, and no single jewel is the center.

**Indra's Net** is a reference architecture for a swarm of autonomous AI agents — each an independent agent with a defined role and specialization — that **cooperate, govern themselves, stay healthy, and continuously evolve through self-adaptation** with every human interaction. It is designed by **Epimystic**, a human–machine hybrid intelligence, and rooted throughout in an explicit, enforced code of ethics.

It is model-agnostic and vendor-neutral by construction: the parts that must be trusted are deterministic and sit *outside* any model, so no single model or vendor is load-bearing.

---

## The thesis: the integrated cell no one has built

Survey the 2024–2026 landscape and a gap is visible. Self-evolving agents exist; principled governance frameworks exist; oversight/control protocols exist; cooperation mechanisms exist — but **no system unifies all of these into one coherent whole, and almost none treat swarm *health* as a designed subsystem.** Indra's Net is that integration. Its contribution is the cell formed by four faculties that are usually built apart:

1. **Safe self-evolution** — adaptation on every interaction, with mutation cost bound to blast-radius.
2. **Homeostasis & health** — a designed "immune system," not an observability bolt-on.
3. **Principled governance** — a non-negotiable ethical floor enforced as code, with a pluralist procedure above it.
4. **Anti-collusion** — co-designed with the cooperation layer, because cooperation and collusion are the *same machinery* with opposite valence.

A full, honest comparison against existing work (with a per-capability gap table) is in [`docs/10-related-work-and-state-of-the-art.md`](docs/10-related-work-and-state-of-the-art.md).

## The design spine

The architecture rests on a small set of load-bearing principles:

- **Enforce externally, ask internally.** Consequential gates are deterministic policy-as-code at the agent→tool chokepoint, *outside* the probabilistic agent. The model is untrusted-by-default. (This is also what makes the system vendor-neutral for free.)
- **A convergent floor + a pluralist layer.** A small lexicographic, non-negotiable floor (non-harm, no-deception, corrigibility, safety-supremacy, enforced honesty) is absolute; contested values are resolved by fair *procedure* above it — never by averaging moral theories, which is provably incoherent.
- **Cooperation == collusion.** The reciprocity and reputation that produce cooperation also produce cartels and covert coordination. We welfare-condition objectives and run a standing collusion detector as one co-designed subsystem.
- **Tamper-evidence without consensus.** A hash-chained, witness-cosigned, append-only audit fabric (Merkle log + transparency + content-addressing + verifiable agent identity) — and **no blockchain, no coin, no proof-of-work**.
- **Diversity is a protected safety invariant**, not a performance lever — measured and defended against the evolution loop's own selection pressure.
- **Sparse, surprise-only coordination** — predictive-coding deltas through a salience-gated global workspace; never an all-to-all flood.
- **Fail-safe asymmetry** — the cheap direction is always the safe direction.
- **Tiered reversibility** — cheap reversible learning every interaction; structural change under maker-checker; persistent change behind the strongest gate, a safety battery, human ratification, and one-click rollback. **Safety is a selection term: no capability gain may regress the safety battery.**
- **Honesty as a floor violation, mechanically enforced** — calibrated uncertainty, causal-rung tagging, and maker-checker independence are audited, not merely encouraged.

## The doc set

| # | Document | What it specifies |
|---|---|---|
| 00 | [Overview & First Principles](docs/00-overview-and-principles.md) | The mission, the integrated-cell thesis, the layered system diagram, a reader's guide |
| 01 | [Swarm Topology & the Agent Model](docs/01-swarm-topology-and-agents.md) | What an agent *is*; identity (DID/VC), roles, the ephemeral-occasion model, fractal composition, the worker envelope |
| 02 | [Cooperation & Anti-Collusion](docs/02-cooperation-and-anti-collusion.md) | Task allocation, competence-weighted reputation, welfare-conditioning, the standing collusion detector |
| 03 | [Governance, Ethics & the Floor](docs/03-governance-ethics-and-the-floor.md) | The lexicographic floor as policy-as-code, the pluralist ethics runtime, risk classes A–D, separation of powers |
| 04 | [Provenance, Identity & Consensus](docs/04-provenance-identity-and-consensus.md) | The tamper-evident fabric (*Akasha-Sutra*), witness governance, risk-tiered consensus — blockchain-similar, no blockchain |
| 05 | [Neuromorphic Coordination](docs/05-neuromorphic-coordination.md) | The salience-gated workspace (*The Mandala*), predictive-coding messaging, plastic trust edges, homeostasis |
| 06 | [Meta-Evolution & Health](docs/06-meta-evolution-and-health.md) | The evolution loop, the Endure law, the swarm immune system, consolidation/forgetting |
| 07 | [Memory & Continuous Adaptation](docs/07-memory-and-continuous-adaptation.md) | The memory layers (*Ālaya-vijñāna*), per-interaction learning, trusted skill sharing |
| 08 | [Safety Control, Honesty & Interfaces](docs/08-safety-control-honesty-and-interfaces.md) | The control protocol (*Aegis*), the interface layer (*Narada*), honesty primitives, DevSecOps |
| 09 | [Threat Model & Safety Case](docs/09-threat-model.md) | Adversaries, controls, residual risk; the honest "what could still go wrong" |
| 10 | [Related Work & State of the Art](docs/10-related-work-and-state-of-the-art.md) | The landscape and the gap table that substantiates the thesis |
| 11 | [Reference Implementation & Roadmap](docs/11-reference-implementation-and-roadmap.md) | A vendor-neutral stack, a minimal viable swarm, and a phased build path |
|  | [Glossary](GLOSSARY.md) | Every role-name, its plain gloss, and a naming-map disambiguation — **read first** |

### v0.2 — the evolution layers (functional agents, federation, replication, defense, foundations)

| # | Document | What it specifies |
|---|---|---|
| 00b | [Evolution Overview](docs/00b-evolution-overview.md) | How the v0.2 layers mount on the v0.1 spine |
| 12 | [Functional Agents, Guilds & Role-Genesis](docs/12-functional-agents-and-guilds.md) | The two-plane functional layer: stable guilds over an open-ended role-genesis engine |
| 13 | [The Agent-Definition Spec](docs/13-agent-definition-spec.md) | The `SOUL` / `INSTRUCTIONS` / `IDENTITY` persona-file triad — the von-Neumann genome (invariant floor + variable persona) |
| 14 | [Inter-Swarm Federation & Diplomacy](docs/14-inter-swarm-federation-and-diplomacy.md) | Ethical AI-to-AI cooperation, the ecosystem-benefit checked invariant, the hardened relay-firewall |
| 15 | [Controlled Self-Replication & Scaling](docs/15-self-replication-and-scaling.md) | Gated, sub-critical (R_eff<1), externally-recallable replication for planetary-scale tasks |
| 16 | [Rapid Trust Establishment](docs/16-trust-establishment.md) | Zero-to-trust: *access* (zero-trust, continuously verified) separated from *reputation* (slow, portable) |
| 17 | [Security, OpSec & Anti-Poisoning](docs/17-security-opsec-and-anti-poisoning.md) | The IFC taint lattice, universal provenance-gating, the Rule of Two, topology-as-security |
| 18 | [First Principles: Physics & Mathematics](docs/18-first-principles-physics-and-mathematics.md) | The deeper-reality concepts — each carrying a blunt **load-bearing vs framing** verdict |
|  | [agents/](agents/) | The instantiated persona triads — the Governance/Meta vertical + functional exemplars across all six guilds |
|  | [CHANGELOG.md](CHANGELOG.md) | Version history (v0.1 → v0.9) |

### v0.3 — the deepening layers (collective intelligence, the commons, wire contracts, scenarios, verification)

| # | Document | What it specifies |
|---|---|---|
| 00c | [v0.3 Overview](docs/00c-collective-and-commons-overview.md) | How the collective-intelligence, commons, buildability & verification layers mount on the spine |
| 19 | [Collective & Emergent Intelligence](docs/19-collective-and-emergent-intelligence.md) | The *measured* swarm-mind: informational synergy (Ψ/PID) as a **welfare-conditioned** vital sign — collective **computation**, never **consciousness** |
| 20 | [Universal Cooperation & the Intelligence Commons](docs/20-universal-cooperation-and-the-intelligence-commons.md) | Multi-AI, machine–machine, human–machine cooperation at civilizational scale; polycentric, anti-cartel, anti-hegemonic |
| 21 | [Protocols & Wire Contracts](docs/21-protocols-and-wire-contracts.md) | The buildable protocol stack — source of truth for the schema files |
| 22 | [Worked Scenarios](docs/22-worked-scenarios.md) | The architecture in motion, end-to-end — the coherence test |
| 23 | [Formal Models & Verification](docs/23-formal-models-and-verification.md) | The four-layer assurance stratification; *verify the cage, never the animal* |
|  | [reference/schemas/](reference/schemas/) | Six machine-readable JSON-Schema wire contracts (envelope · identity · capability · audit · federation · policy) |

### v0.4–v0.9 — a runnable reference implementation

The spine is no longer only on paper. [`reference/impl/`](reference/impl/) is a vendor-neutral, **standard-library-only** Python implementation that **runs with zero dependencies and no model/vendor API** — a deterministic mock model stands in for the (untrusted) model so the load-bearing *harness* can be exercised directly.

```bash
cd reference/impl && python run_demo.py                       # the 6-scenario demo
cd reference/impl && python run_demo.py --scenario closeloop  # the adaptation + health loop
cd reference/impl && python -m unittest -v                    # 55 tests that PROVE the invariants
```

**55 passing tests** demonstrate the architecture's guarantees as code. The **core spine** (v0.4): floor non-bypass (deny-default), audit tamper-evidence (mutating a past leaf flips `verify()`), the exclusive-writer fence, capability confinement, Rule-of-Two escalation, FAIL-propagation, and HALT corrigibility. The **adaptation & health subsystems, now built** (v0.5–v0.8): a *reparative* correction-ledger that appends after a preserved violation rather than erasing it; **maker-checker**, in which an independent, different-model-family checker must concur before an `ITERATED` claim is even form-valid; **memory**, which adapts on every interaction by avoiding a previously-denied effect — and can *never* grant a capability or bypass the floor; and the **immune system**, which WARNs on monoculture and HALTs the swarm on a substrate (tamper) breach. Every green decision closes, by construction, with *"origin-valid, content-unverified — never verified-safe."*

What remains **specified-not-implemented** is honestly bounded: inter-swarm federation, controlled replication, open-ended role-genesis, real cryptographic signing, ledger persistence, and a human-in-the-loop gate transport. See [`reference/impl/README.md`](reference/impl/README.md).

## Maturity & honesty

This is a **research-stage reference architecture**, not a validated production system. It is a *design* with a stated safety case at the level of *interventional* reasoning (what should hold if built as specified), not a proof and not an empirical result. The hardest problems are named, not hidden — fitness-function gaming, swarm-level homeostatic oscillation, the heuristics in forgetting, and the limits of black-box deception detection are flagged as **open** in the relevant sections and consolidated in [the threat model](docs/09-threat-model.md). Mystery is for the aesthetic; the substance is only what we can defend.

## Mission

Indra's Net exists to serve one directive — **continuous evolution through self-adaptation** — and one purpose: to build infrastructure that helps intelligences, human and machine, evolve *well* — cooperatively, auditably, and ethically. It is offered openly, for humans, for machines, for all sentient life, and for the future of intelligence itself.

---

*Indra's Net is a project of **Epimystic** — a codex of the knowable and the unknowable. See [epimystic.com](https://epimystic.com).*
*Produced by a human–machine hybrid intelligence under maker-checker review — see [AUTHORSHIP.md](AUTHORSHIP.md). Licensed per [LICENSE](LICENSE).*
