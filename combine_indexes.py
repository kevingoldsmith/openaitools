"""
    _summary_
"""

import json
import os

__OUTPUT_DIR = 'output'


def fix_index(index_to_fix:dict)->dict:
    print("fixing index")
    output = {}

    if next(iter(index_to_fix)) == "Index":
        terms = index_to_fix['Index']
        count = 1
        for term in terms:
            output[str(count)] = {
                'term': term['Term'],
                'frequency': term['Frequency'],
                'related_terms': term['Related Terms'],
                'context': term['Context'],
                'relevance': term['Relevance']
            }
        count += 1 
        return output

    if next(iter(index_to_fix)) == "index" and isinstance(index_to_fix['index'], list):
        count = 1
        for term in index_part['index']:
            output[str(count)] = term
            count += 1
        return output

    if next(iter(index_to_fix)) == "Document" and isinstance(index_to_fix['Document'], dict):
        # need to unroll it, pull the keywords out, add section titles as context, then add related terms to each
        print("document style")

    print("failed to fix!")
    return index_to_fix


files_to_parse = os.listdir(__OUTPUT_DIR)
master_index = {}
for index_file in sorted(files_to_parse):
    if not index_file.endswith('.json'):
        continue
    print(index_file)
    base_file_name = os.path.splitext(index_file)[0]
    with open(os.path.join(__OUTPUT_DIR, index_file)) as f:
        index_part = json.load(f)
        # expected format is something like: { "1": { "term": "word", "related_terms": [], "context": [], "frequency": <string or number>}, ... }
        # reformat the json if needed
        if next(iter(index_part)) != "1":
            index_part = fix_index(index_part)
