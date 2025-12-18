# Frame Extensions

Extensions allow Frame to scale into specific domains without bloating the core Legend. They provide specialized vocabularies that plug into the Semantic Frame Pattern (SFP).

## What is a Frame Extension?
A Frame Extension is a set of files that defines a specialized vocabulary (namespace) extending a core Frame facet (usually `Domain.*`).

An extension consists of:
- **`LEGEND.md`**: The generated vocabulary list (human/LLM readable).
- **`extension.yml`**: The configuration file used to generate the legend.
- **`SOURCE.md`**: Provenance data ensuring the vocabulary is traceable to a trusted source.

## How the Generator Works
The `tools/generate_extension.py` script is a developer utility. It reads an `extension.yml`, fetches data from an upstream source (via an adapter), and generates the `LEGEND.md` file.

This ensures:
1.  **Decoupling:** The generated files are standalone. The consumer does not need the tool or the upstream source to use the extension.
2.  **Stability:** The vocabulary is snapshotted. It doesn't change unless you re-run the generator.
3.  **Provenance:** We know exactly where the terms came from and when.

## Adding a New Extension

1.  Create a folder: `extensions/<my_extension>/`
2.  Create `extension.yml` (see `schemas/extension_config.schema.json`).
3.  If a new source type is needed, add an adapter in `tools/adapters/`.
4.  Run the generator:

    ```bash
    python3 tools/generate_extension.py --config extensions/<my_extension>/extension.yml --outdir extensions/<my_extension>
    ```

## Directory Structure

```
extensions/
├── tools/                  # The generator and adapters
├── schemas/                # JSON schemas for config
├── <extension_name>/       # The extension artifacts
│   ├── extension.yml       # Config
│   ├── LEGEND.md           # Generated Legend
│   ├── SOURCE.md           # Generated Provenance
│   └── README.md           # Documentation
```
