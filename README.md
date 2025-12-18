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

## Usage

Frame provides two ways to consume its vocabulary:

1. **[LEGEND.yaml](LEGEND.yaml)**: The canonical, human-readable source of truth. It contains full definitions for every tag, composition rules, and stability policies. Use this for human reference or when providing a full mental model to a reasoning system.
2. **[LEGEND-minified.txt](LEGEND-minified.txt)**: A highly compact version (under 1KB) designed for prompt injection. It includes the core instruction and a plain list of tags.

**Note:** The minified version trades context for efficiency. It does not include the detailed tag definitions or the clarifying policies found in the main legend.

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