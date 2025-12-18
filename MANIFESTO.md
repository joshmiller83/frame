# Frame Manifesto

Frame Version: 0.1.0
Status: Experimental
Methodology: SFP 0.1.0
License: CC-BY-4.0 (recommended)

## What is Frame?

Frame is a lightweight way to describe how a resource should be understood at a glance.

- A Frame is not a taxonomy of truth.
- It is not an ontology.
= It does not try to explain everything.

A Frame answers a simpler question:

> “From what perspective should this resource be understood?”

Frame exists to reduce cognitive load for both humans and language models when navigating large, diverse collections of content.

## Why Frame exists

Modern knowledge systems fail in two opposite ways:

 - Keyword systems are shallow and ambiguous.
 - Ontologies are precise but heavy, brittle, and unreadable.

LLMs sit uncomfortably between these extremes.

Frame is designed for this reality.

It provides:

 - Just enough structure to guide reasoning
 - Just enough constraint to reduce ambiguity
 - Just enough consistency to scale across domains

Nothing more.

## What Frame is (and is not)

Frame is:

 - composable
 - human-legible
 - prompt-scale
 - stable over time
 - compatible with existing schemas

Frame is not:

 - exhaustive
 - hierarchical by default
 - tied to a single domain
 - prescriptive about usage
 - a replacement for deep taxonomies

Frame describes how to look, not what to conclude.

## The SFP methodology

Frame uses the SFP v0.1.0 methodology (Semantic Frame Pattern):

 - Small, fixed sets of tags
 - Orthogonal dimensions
 - Whole words, not abbreviations
 - Optional precision
 - Designed for reasoning, not storage

Each Frame is composed of four facets:

```
Frame:
  Domain.*
  Object.*
  Mode.*
  Context.*
```

Rules:

 - Exactly one Domain
 - Exactly one Object
 - Zero or more Modes
 - Zero or more Contexts

If a facet is unclear or debatable, it is omitted.

## Acceptable tags (UTX 0.0.1)
Domain — what the resource is about

```
Domain.Business
Domain.Technology
Domain.Security
Domain.Science
Domain.Health
Domain.Education
Domain.Law
Domain.Civics
Domain.Finance
Domain.Environment
Domain.Arts
Domain.Life
```

Object — what kind of resource it is
```
Object.Document
Object.Data
Object.Code
Object.Api
Object.People
Object.Organization
Object.System
Object.Event
Object.Process
Object.Policy
Object.Product
Object.Media
```

Mode — the intrinsic reasoning posture encoded in the resource (optional)

A Mode is not how a resource might be used. It is the kind of thinking the resource itself embodies.
```
Mode.Orientation     — provides context or mental model
Mode.Definition      — establishes meaning or terms
Mode.Exposition      — explains internal workings
Mode.Interpretation  — explains significance or implications

Mode.Procedure       — ordered steps
Mode.Playbook        — conditional actions (“if X, then Y”)
Mode.Operation       — ongoing execution or maintenance

Mode.Evaluation      — assesses quality or fit
Mode.Comparison      — contrasts alternatives
Mode.Audit           — verifies against rules or standards

Mode.Design          — proposes structure or solution
Mode.Planning        — sequences work over time
Mode.Synthesis       — combines sources into a coherent whole

Mode.Diagnosis       — identifies cause of a problem
Mode.Risk            — surfaces threats and mitigations

Mode.Messaging       — crafts communication
Mode.Alignment       — builds shared understanding
```

Context — how the resource should be handled (optional)
```
Context.Public
Context.Internal
Context.Confidential
Context.TimeSensitive
Context.HighStakes
Context.LowStakes
```

## How Frame should be read

A Frame should read almost like a sentence.

Example:

```
Frame:
  Domain.Security
  Object.Process
  Mode.Playbook
  Context.HighStakes
```

Which means:

> “This resource should be understood as a high-stakes security process playbook.”

If the Frame does not read naturally, it is probably wrong.

## Design principles

1. Clarity beats precision
2. Whole words beat codes
3. Optional dimensions beat forced classification
4. Reasoning beats retrieval hacks
5. Stability beats cleverness

Frame is successful when:

 - two humans largely agree on a Frame
 - two different LLMs behave similarly when given it
 - the Frame still makes sense a year later

## Versioning philosophy

 - 0.x versions are experimental
 - Tags may be added, but meanings should not drift
 - Renaming is avoided; deprecation is preferred
 - Backward compatibility is a first-order concern
 - Frame should age slowly.

## Closing statement

Frame is deliberately small.

It assumes:

 - meaning is contextual
 - interpretation is inevitable
 - and clarity is more valuable than completeness

Frame does not tell models what to think. It tells them how to look.
