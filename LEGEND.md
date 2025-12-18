# Frame Core Legend

- **Implementation Identifier:** Frame-Core
- **Version:** 0.0.1
- **License:** Apache 2.0
- **Maintainers:** Frame Maintainers
- **Created:** 2025-12-18
- **Updated:** 2025-12-18

This document defines the canonical vocabulary for Frame Core v0.0.1, complying with the Semantic Frame Pattern (SFP) Legend format.

## Facets

### Domain
*What the resource is about.*

- `Domain.Business` — Concerns commercial, corporate, or market activities.
- `Domain.Technology` — Concerns hardware, software, engineering, or digital systems.
- `Domain.Security` — Concerns protection, safety, threats, or defense.
- `Domain.Science` — Concerns empirical study, research, or natural phenomena.
- `Domain.Health` — Concerns medicine, well-being, fitness, or biology.
- `Domain.Education` — Concerns learning, teaching, training, or pedagogy.
- `Domain.Law` — Concerns legal codes, regulations, compliance, or justice.
- `Domain.Civics` — Concerns government, policy, society, or citizenship.
- `Domain.Finance` — Concerns money, investment, banking, or economic value.
- `Domain.Environment` — Concerns nature, climate, ecology, or sustainability.
- `Domain.Arts` — Concerns culture, creativity, aesthetics, or entertainment.
- `Domain.Life` — Concerns personal, lifestyle, household, or family matters.

### Object
*What kind of resource it is.*

- `Object.Document` — A textual record, report, or prose.
- `Object.Data` — Raw or structured information, numbers, or statistics.
- `Object.Code` — Source code, scripts, or executable logic.
- `Object.Api` — An interface definition, endpoint, or schema.
- `Object.People` — Information about individuals or groups.
- `Object.Organization` — Information about companies, institutions, or bodies.
- `Object.System` — A complex entity, architecture, or infrastructure.
- `Object.Event` — An occurrence, meeting, incident, or milestone.
- `Object.Process` — A workflow, sequence of steps, or method.
- `Object.Policy` — A rule, guideline, or governance requirement.
- `Object.Product` — A good, service, tool, or deliverable.
- `Object.Media` — Audio, video, image, or multimedia content.

### Mode (Optional)
*The intrinsic reasoning posture.*

- `Mode.Orientation` — Provides context or a mental model.
- `Mode.Definition` — Establishes meanings or terms.
- `Mode.Exposition` — Explains internal workings or details.
- `Mode.Interpretation` — Explains significance or implications.
- `Mode.Procedure` — Describes ordered steps to achieve a goal.
- `Mode.Playbook` — Describes conditional actions ("if X, then Y").
- `Mode.Operation` — Describes ongoing execution or maintenance.
- `Mode.Evaluation` — Assesses quality, fit, or performance.
- `Mode.Comparison` — Contrasts alternatives or options.
- `Mode.Audit` — Verifies against rules or standards.
- `Mode.Design` — Proposes structure, form, or solution.
- `Mode.Planning` — Sequences work over time.
- `Mode.Synthesis` — Combines sources into a coherent whole.
- `Mode.Diagnosis` — Identifies the cause of a problem.
- `Mode.Risk` — Surfaces threats and mitigations.
- `Mode.Messaging` — Crafts communication or narrative.
- `Mode.Alignment` — Builds shared understanding or consensus.

### Context (Optional)
*How the resource should be handled.*

- `Context.Public` — Open for general consumption.
- `Context.Internal` — Restricted to the organization or group.
- `Context.Confidential` — Highly sensitive, restricted access.
- `Context.TimeSensitive` — Urgent or time-bound relevance.
- `Context.HighStakes` — Critical consequences for error.
- `Context.LowStakes` — Minimal consequences for error.

## Rules

### Composition
- **Domain:** Exactly 1
- **Object:** Exactly 1
- **Mode:** Zero or 1
- **Context:** Zero or 1
- **Maximum 5 tags total.**

### Policies
- **Ambiguity:** When uncertain, omit the facet.
- **Stability:** Meanings MUST NOT drift without a version bump.
