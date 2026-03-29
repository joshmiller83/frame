import requests
import json
import datetime
import re

class MitreAttackStixAdapter:
    def __init__(self, config):
        self.config = config
        self.source_config = config['source']

    def _to_pascal_case(self, kebab_str):
        if not kebab_str: return ""
        # Handle spaces if they exist, though phases are usually kebab
        return "".join(word.capitalize() for word in re.split(r'[\s\-_]+', kebab_str))

    def fetch_data(self):
        index_url = self.source_config['index_url']
        collections_to_fetch = self.source_config['collections']
        include_hierarchy = self.config.get('output', {}).get('include_hierarchy_in_id', False)
        
        print(f"Fetching index from {index_url}...")
        try:
            r = requests.get(index_url)
            r.raise_for_status()
            index_data = r.json()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch index: {e}")

        # Store all techniques to resolve relationships
        # Key: MitreID, Value: Object
        all_techniques_map = {}
        provenance_details = []
        counts = {c: {"techniques": 0, "subtechniques": 0} for c in collections_to_fetch}

        # 1. Fetch and Parse
        for collection in index_data.get('collections', []):
            name = collection.get('name')
            if name in collections_to_fetch:
                # Determine version (first is latest usually)
                versions = collection.get('versions', [])
                if not versions:
                    continue
                
                target_version_obj = versions[0]
                target_url = target_version_obj.get('url')
                version_str = target_version_obj.get('version')
                modified = target_version_obj.get('modified')

                print(f"Processing collection: {name} (Version: {version_str})")
                
                provenance_details.append({
                    "collection": name,
                    "version": version_str,
                    "url": target_url,
                    "modified": modified
                })

                # Fetch Bundle
                try:
                    b_req = requests.get(target_url)
                    b_req.raise_for_status()
                    bundle_data = b_req.json()
                except Exception as e:
                    print(f"Warning: Failed to fetch bundle for {name}: {e}")
                    continue

                # Process Objects
                for obj in bundle_data.get('objects', []):
                    if obj.get('type') != 'attack-pattern':
                        continue
                    if obj.get('revoked') or obj.get('x_mitre_deprecated'):
                        continue
                    
                    # Extract ID
                    ext_refs = obj.get('external_references', [])
                    mitre_id = None
                    for ref in ext_refs:
                        if ref.get('source_name') == 'mitre-attack' and 'external_id' in ref:
                            mitre_id = ref['external_id']
                            break
                    
                    if not mitre_id:
                        continue

                    # Count
                    is_sub = '.' in mitre_id
                    if is_sub:
                        counts[name]['subtechniques'] += 1
                    else:
                        counts[name]['techniques'] += 1

                    # Store (latest wins)
                    all_techniques_map[mitre_id] = {
                        "id": mitre_id,
                        "label": obj.get('name'),
                        "description": obj.get('description', ''),
                        "phases": [
                            p['phase_name'] 
                            for p in obj.get('kill_chain_phases', []) 
                            if p.get('kill_chain_name') == 'mitre-attack' or p.get('kill_chain_name') == 'mitre-mobile-attack' or p.get('kill_chain_name') == 'mitre-ics-attack'
                        ]
                    }

        # 2. Build Hierarchy & Items
        items = []
        
        # Sort by ID for deterministic processing
        sorted_ids = sorted(all_techniques_map.keys())

        for mid in sorted_ids:
            obj = all_techniques_map[mid]
            
            generated_ids = []
            
            if include_hierarchy:
                tactics = set()
                
                # If technique, use its phases
                if '.' not in mid:
                    for p in obj['phases']:
                        tactics.add(self._to_pascal_case(p))
                else:
                    # If sub-technique, find parent
                    parent_id = mid.split('.')[0]
                    parent = all_techniques_map.get(parent_id)
                    if parent:
                        for p in parent['phases']:
                            tactics.add(self._to_pascal_case(p))
                    else:
                        # Fallback if parent not found in dataset (e.g. if we missed it somehow)
                        # or try to use own phases if they exist (rare for subs)
                        for p in obj['phases']:
                            tactics.add(self._to_pascal_case(p))
                
                if not tactics:
                    # Orphaned or no tactics? Just use ID.
                    generated_ids.append(mid)
                else:
                    for t in tactics:
                        generated_ids.append(f"{t}.{mid}")
            else:
                generated_ids.append(mid)
            
            for gid in generated_ids:
                items.append({
                    "id": gid,
                    "label": obj['label'],
                    "description": obj['description']
                })

        # Provenance Report
        provenance = {
            "index_url": index_url,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "sources": provenance_details,
            "counts": counts
        }

        return {
            "items": items,
            "provenance": provenance
        }

def get_adapter(config):
    return MitreAttackStixAdapter(config)