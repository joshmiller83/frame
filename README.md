# Frame

Frame is a lightweight implementation of the Semantic Frame Pattern (SFP). It provides a structured way to describe how a resource should be understood at a glance, without imposing a rigid ontology.

## What Frame is

Frame is a tool for reasoning, designed to be read by both humans and large language models. It provides a consistent, minimal signal that tells a consumer "how to look" at a piece of information before processing it.

Frame is:
- **Composable**: Built from small, stable facets.
- **Human-legible**: Readability is a primary constraint.
- **Stable**: Designed to age slowly.

## What Frame is not

- **Not a taxonomy**: It does not attempt to classify all knowledge.
- **Not a replacement**: It coexists with existing schemas and metadata.
- **Not marketing**: It does not use hype or promotional language.

## Relation to SFP

Frame strictly follows the Semantic Frame Pattern (SFP) v0.1.0 specification. While SFP defines the abstract methodology for semantic framing—dimensions, orthogonality, and composition rules—Frame provides the concrete "Legend" (vocabulary) for general-purpose use.

See [docs/sfp.md](docs/sfp.md) for the underlying SFP specification.

## Example Frame

A Frame is composed of four facets: Domain, Object, Mode, and Context.

```
Frame:
  Domain.Security
  Object.Process
  Mode.Playbook
  Context.HighStakes
```

This Frame indicates that the resource should be understood as a high-stakes playbook within the security domain. It sets the interpretive posture before the content is even read.