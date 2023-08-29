"""
    _summary_
"""

import json
import os

__OUTPUT_DIR = 'output'

def is_valid_index_json(index_part:dict)->bool:
    for key in index_part:
        if not key.isdigit():
            return False
        if not int(key) in range(1,50):
            return False
        value = index_part[key]
        if not isinstance(value, dict):
            return False
        if not "term" in value:
            return False
        if not isinstance(value['term'], str):
            return False
        if not "related_terms" in value:
            return False
        if not isinstance(value['related_terms'], list):
            return False
        if not "context" in value:
            return False
        if not isinstance(value['context'], list):
            return False
    return True

files_to_parse = os.listdir(__OUTPUT_DIR)
master_index = {}
for index_file in sorted(files_to_parse):
    if not index_file.endswith('.json'):
        continue
    
    print(f"loading: {index_file}")
    base_file_name = os.path.splitext(index_file)[0]
    print(base_file_name)
    with open(os.path.join(__OUTPUT_DIR, index_file)) as f:
        index_part = json.load(f)
        for index_number, index_term in index_part.items():
            term = index_term['term']
            context = {'reference': base_file_name, 'context': index_term['context']}
            related_terms = index_term['related_terms']

            # If term already exists in master_index
            if term in master_index:
                # Combine context
                master_index[term]['context'].append(context)
                
                # Combine related terms
                master_index[term]['related_terms'] = list(set(master_index[term]['related_terms'] + related_terms))
            else:
                master_index[term] = {'context':[context], 'related_terms': related_terms}

print("writing master index file")
with open("master_index.json", "w") as f:
    f.write(json.dumps(master_index, indent=2, sort_keys=True))
