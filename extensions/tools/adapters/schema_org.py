import requests
import datetime

class SchemaOrgAdapter:
    def __init__(self, config):
        self.config = config
        self.source_config = config['source']

    def fetch_data(self):
        url = self.source_config['url']
        print(f"Fetching Schema.org data from {url}...")
        
        try:
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch Schema.org data: {e}")

        graph = data.get('@graph', [])
        items = []
        
        print(f"Processing {len(graph)} items from graph...")
        
        for node in graph:
            # We are looking for Classes.
            # @type can be a string or list.
            node_types = node.get('@type', [])
            if isinstance(node_types, str):
                node_types = [node_types]
                
            if 'rdfs:Class' not in node_types:
                continue
                
            # Extract ID (Term)
            node_id = node.get('@id')
            if not node_id:
                continue
            
            # node_id is typically "schema:Person" or "http://schema.org/Person"
            if 'schema.org/' in node_id:
                term = node_id.split('schema.org/')[-1]
            elif node_id.startswith('schema:'):
                term = node_id.split(':')[-1]
            else:
                # Skip non-schema.org terms (e.g. external mapped ontologies)
                continue
                
            # Label
            label = node.get('rdfs:label', term)
            if isinstance(label, dict):
                label = label.get('@value', term)
                
            # Description
            description = node.get('rdfs:comment', '')
            if isinstance(description, dict):
                description = description.get('@value', '')
                
            items.append({
                "id": term,
                "label": label,
                "description": description
            })

        provenance = {
            "index_url": url,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "sources": [{
                "collection": "Schema.org",
                "version": "latest", 
                "url": url,
                "modified": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }],
            "counts": {
                "Schema.org": {"techniques": len(items), "subtechniques": 0} 
            }
        }
        
        return {
            "items": items,
            "provenance": provenance
        }

def get_adapter(config):
    return SchemaOrgAdapter(config)
