import requests
import datetime
import collections

class SchemaOrgAdapter:
    def __init__(self, config):
        self.config = config
        self.source_config = config['source']

    def fetch_data(self):
        url = self.source_config['url']
        max_depth = self.source_config.get('max_depth')
        
        print(f"Fetching Schema.org data from {url}...")
        
        try:
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch Schema.org data: {e}")

        graph = data.get('@graph', [])
        
        print(f"Processing {len(graph)} items from graph...")
        
        term_to_node = {}
        children_map = collections.defaultdict(list)
        
        # Helper to extract simple term from ID
        def get_term(node_id):
            if not node_id: return None
            # Handle http://schema.org/Thing
            if 'schema.org/' in node_id:
                return node_id.split('schema.org/')[-1]
            # Handle schema:Thing
            elif node_id.startswith('schema:'):
                return node_id.split(':')[-1]
            return None

        # 1. First pass: Identify all classes and build hierarchy
        for node in graph:
            node_types = node.get('@type', [])
            if isinstance(node_types, str):
                node_types = [node_types]
                
            if 'rdfs:Class' not in node_types:
                continue
                
            term = get_term(node.get('@id'))
            if not term:
                continue
                
            term_to_node[term] = node
            
            # Identify parents
            parents = node.get('rdfs:subClassOf', [])
            if isinstance(parents, dict):
                parents = [parents]
            elif isinstance(parents, str): 
                # Sometimes it might be a raw string URL if not fully expanded, 
                # but usually in this JSON-LD it's a list of dicts or a dict with @id.
                # Just in case:
                pass 
                
            for p in parents:
                if isinstance(p, dict):
                    p_id = p.get('@id')
                    p_term = get_term(p_id)
                    if p_term:
                        children_map[p_term].append(term)

        # 2. Filter by depth if required
        valid_terms = set()
        
        if max_depth is not None:
            print(f"Filtering hierarchy to depth {max_depth} starting from 'Thing'...")
            # BFS
            queue = [('Thing', 0)]
            visited = set()
            
            while queue:
                current_term, depth = queue.pop(0)
                
                if current_term in visited:
                    continue
                visited.add(current_term)
                
                # If term exists in our node map, it's valid to include
                if current_term in term_to_node:
                    valid_terms.add(current_term)
                
                # If we haven't reached max depth, add children to queue
                if depth < max_depth:
                    for child in children_map.get(current_term, []):
                        queue.append((child, depth + 1))
        else:
            valid_terms = set(term_to_node.keys())

        # 3. Build result items
        items = []
        for term in valid_terms:
            node = term_to_node[term]
            
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

        print(f"Selected {len(items)} items after filtering.")

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