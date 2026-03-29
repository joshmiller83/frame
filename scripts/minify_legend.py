import yaml
import sys

def minify_legend(input_path, output_path):
    try:
        with open(input_path, 'r') as f:
            data = yaml.safe_load(f)
        
        core = data.get('frame_core', {})
        
        instruction = core.get('instruction', '')
        addendum = "Only one tag per facet."
        full_prompt = f"{instruction} {addendum}"
        
        facet_lines = []
        facets = core.get('facets', {})
        for facet_name, facet_data in sorted(facets.items()):
            tags = facet_data.get('tags', {})
            for tag_name in sorted(tags.keys()):
                facet_lines.append(f"{facet_name}.{tag_name}")

        content = f"{full_prompt}\n\n" + "\n".join(facet_lines)

        with open(output_path, 'w') as f:
            f.write(content)
        
        print(f"Minified legend written to {output_path} ({len(content)} bytes)")

    except Exception as e:
        print(f"Error minifying legend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    minify_legend("LEGEND-frame-core.yaml", "LEGEND-frame-core-minified.txt")

