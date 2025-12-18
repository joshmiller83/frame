import requests
import json
import datetime

class MitreAttackStixAdapter:
    def __init__(self, config):
        self.config = config
        self.source_config = config['source']

    def fetch_data(self):
        index_url = self.source_config['index_url']
        collections_to_fetch = self.source_config['collections']
        version_rule = self.source_config.get('version_rule', 'latest')
        
        print(f"Fetching index from {index_url}...")
        try:
            r = requests.get(index_url)
            r.raise_for_status()
            index_data = r.json()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch index: {e}")

        techniques = {}  # Use dict to deduplicate by ID
        provenance_details = []
        
        counts = {c: {"techniques": 0, "subtechniques": 0} for c in collections_to_fetch}

        for collection in index_data.get('collections', []):
            name = collection.get('name')
            if name in collections_to_fetch:
                # Determine version
                versions = collection.get('versions', [])
                if not versions:
                    continue
                
                # Sort versions (assuming semantic versioning in date-like or number-like strings)
                # Actually MITRE index versions are usually just strings, often dates or X.Y
                # The index.json lists them. We'll pick the last one in the list as latest 
                # or try to sort if needed. The index spec says 'versions' is a list.
                # Usually the API returns them sorted (descending) so the first one is the latest.
                # We'll pick the first one in the list as latest if version_rule is latest.
                
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

                    # Add to map (deduplicate, latest wins if overlap across collections - typically they are distinct or identical)
                    techniques[mitre_id] = {
                        "id": mitre_id,
                        "label": obj.get('name'),
                        "description": obj.get('description', '')
                    }

        # Convert to list
        items = list(techniques.values())
        
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
