import yaml
import sys

def minify_legend(input_path, output_path):
    try:
        with open(input_path, 'r') as f:
            data = yaml.safe_load(f)
        
        core = data.get('frame_core', {})
        parts = []

        # 1. Instruction
        if 'instruction' in core:
            parts.append(f"!INST:{core['instruction']}")

        # 2. Rules (Compact representation)
        rules = core.get('rules', {})
        rule_parts = []
        if 'composition' in rules:
            comp = rules['composition']
            # Sort for stability
            comp_str = ",".join([f"{k}={v}" for k, v in sorted(comp.items())])
            rule_parts.append(f"Comp:{comp_str}")
        
        if 'policies' in rules:
            pol = rules['policies']
            # Simplified policies
            if 'ambiguity' in pol:
                rule_parts.append("Ambig:Omit")
            if 'stability' in pol:
                rule_parts.append("Stable:NoDrift")
        
        if rule_parts:
            parts.append(f"!RULES:{';'.join(rule_parts)}")

        # 3. Facets
        facets = core.get('facets', {})
        for facet_name, facet_data in sorted(facets.items()):
            tags = facet_data.get('tags', {})
            for tag_name, tag_desc in sorted(tags.items()):
                # Clean description: remove trailing periods, extra spaces
                desc = tag_desc.strip().rstrip('.')
                parts.append(f"{facet_name}.{tag_name}:{desc}")

        # Join with pipes
        minified_content = "|".join(parts)

        with open(output_path, 'w') as f:
            f.write(minified_content)
        
        print(f"Minified legend written to {output_path} ({len(minified_content)} bytes)")

    except Exception as e:
        print(f"Error minifying legend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    minify_legend("LEGEND.yaml", "LEGEND-minified.txt")
