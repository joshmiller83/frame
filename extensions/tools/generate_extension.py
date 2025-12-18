import argparse
import yaml
import json
import os
import sys
import importlib
from datetime import datetime

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def validate_config(config):
    required = ['id', 'adapter', 'version', 'source', 'output', 'namespace']
    for req in required:
        if req not in config:
            raise ValueError(f"Missing required config field: {req}")

def get_adapter_module(adapter_name):
    try:
        # Assumes adapters are in extensions.tools.adapters package
        module_name = f"extensions.tools.adapters.{adapter_name}"
        # We need to ensure the script can find the module. 
        # Since we are running as python extensions/tools/generate_extension.py,
        # we might need to adjust path.
        sys.path.append(os.getcwd())
        return importlib.import_module(f"extensions.tools.adapters.{adapter_name}")
    except ImportError as e:
        raise RuntimeError(f"Could not load adapter '{adapter_name}': {e}")

def generate_legend(items, config, provenance):
    lines = []
    # Header
    lines.append(f"# Extension: {config['id']}")
    lines.append(f"")
    lines.append(f"- **Version:** {config['version']}")
    lines.append(f"- **License:** {config['license']}")
    lines.append(f"- **Maintainers:** {config['maintainers']}")
    lines.append(f"- **Namespace:** {config['namespace']}")
    lines.append(f"- **Extends:** {config.get('extends', 'None')}")
    lines.append(f"- **Created:** {provenance['generated_at']}")
    lines.append(f"")
    
    # Composition Guidance
    lines.append("## Usage")
    lines.append(f"Use 1–3 {config['namespace']}:* tags per resource.")
    lines.append("Frames remain interpretable without this extension.")
    lines.append("")
    
    # Tags
    lines.append("## Tags")
    
    # Sort
    sort_key = config['output'].get('sort_by', 'id')
    sorted_items = sorted(items, key=lambda x: x.get(sort_key, ''))
    
    include_labels = config['output'].get('include_labels', True)
    
    for item in sorted_items:
        tag = f"{config['namespace']}:{item['id']}"
        label = item.get('label', '(label omitted)')
        if include_labels:
            lines.append(f"- `{tag}` — {label}")
        else:
            lines.append(f"- `{tag}`")
            
    return "\n".join(lines)

def generate_source_md(provenance):
    lines = []
    lines.append("# Source Provenance")
    lines.append("")
    lines.append(f"Generated at: {provenance['generated_at']}")
    lines.append(f"Index URL: {provenance['index_url']}")
    lines.append("")
    lines.append("## Collections Used")
    
    for src in provenance['sources']:
        lines.append(f"### {src['collection']}")
        lines.append(f"- **Version:** {src['version']}")
        lines.append(f"- **Modified:** {src['modified']}")
        lines.append(f"- **URL:** {src['url']}")
        lines.append("")
        
    lines.append("## Statistics")
    for col, counts in provenance['counts'].items():
        lines.append(f"- **{col}**: {counts['techniques']} techniques, {counts['subtechniques']} sub-techniques")
        
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Generate Frame Extension from Source")
    parser.add_argument("--config", required=True, help="Path to extension.yml")
    parser.add_argument("--outdir", required=True, help="Output directory")
    parser.add_argument("--no-cache", action="store_true", help="Disable caching (not implemented in this minimal version)")
    
    args = parser.parse_args()
    
    try:
        config = load_config(args.config)
        validate_config(config)
        
        adapter_name = config['adapter']
        adapter_mod = get_adapter_module(adapter_name)
        
        # Instantiate adapter
        adapter = adapter_mod.get_adapter(config)
        
        print(f"Adapter '{adapter_name}' loaded. Fetching data...")
        result = adapter.fetch_data()
        
        items = result['items']
        provenance = result['provenance']
        
        print(f"Fetched {len(items)} items.")
        
        # Generate LEGEND.md
        legend_content = generate_legend(items, config, provenance)
        legend_path = os.path.join(args.outdir, config['output']['file'])
        with open(legend_path, 'w') as f:
            f.write(legend_content)
        print(f"Wrote {legend_path}")
        
        # Generate SOURCE.md
        source_content = generate_source_md(provenance)
        source_path = os.path.join(args.outdir, "SOURCE.md")
        with open(source_path, 'w') as f:
            f.write(source_content)
        print(f"Wrote {source_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
