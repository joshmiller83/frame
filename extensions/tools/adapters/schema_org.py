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
        include_hierarchy = self.config.get('output', {}).get('include_hierarchy_in_id', False)
        
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

        # 2. Filter by depth if required and build paths
        term_to_path = {} # term -> list of path components
        
        # If we need depth filtering OR hierarchy names, we must do traversal
        if max_depth is not None or include_hierarchy:
            print(f"Traversing hierarchy from 'Thing' (max_depth={max_depth})...")
            # BFS: (current_term, depth, path_list)
            queue = [('Thing', 0, ['Thing'])]
            visited = set()
            
            while queue:
                current_term, depth, current_path = queue.pop(0)
                
                # If term exists in our node map, record its path if first seen
                if current_term in term_to_node and current_term not in term_to_path:
                    term_to_path[current_term] = current_path
                
                if current_term in visited:
                    continue
                visited.add(current_term)
                
                # If we haven't reached max depth (if set), add children
                if max_depth is None or depth < max_depth:
                    for child in children_map.get(current_term, []):
                        # Ensure we don't cycle
                        if child not in visited:
                            new_path = current_path + [child]
                            queue.append((child, depth + 1, new_path))
        else:
            # Flat list if no traversal needed
            for term in term_to_node:
                term_to_path[term] = [term]

        # 3. Build result items
        items = []
        for term, path in term_to_path.items():
            if term not in term_to_node:
                continue
                
            node = term_to_node[term]
            
            # Label
            label = node.get('rdfs:label', term)
            if isinstance(label, dict):
                label = label.get('@value', term)
                
            # Description
            description = node.get('rdfs:comment', '')
            if isinstance(description, dict):
                description = description.get('@value', '')
            
            # Determine ID
            if include_hierarchy:
                item_id = ".".join(path)
            else:
                item_id = term
                
            items.append({
                "id": item_id,
                "label": label,
                "description": description
            })

        print(f"Selected {len(items)} items.")

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
