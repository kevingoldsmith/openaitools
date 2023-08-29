"""
    _summary_
"""

import json
import os

__OUTPUT_DIR = 'output'


def fix_index(index_to_fix:dict)->dict:
    print("fixing index")
    output = {}
    first_index = next(iter(index_to_fix))

    if first_index == "Index":
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

    if first_index == "index" and isinstance(index_to_fix[first_index], list):
        count = 1
        for term in index_part['index']:
            output[str(count)] = term
            count += 1
        return output
    
    if first_index == "index" and isinstance(index_to_fix[first_index], dict):
        return index_to_fix[first_index]

    if first_index == "Document" and isinstance(index_to_fix[first_index], dict):
        # need to unroll it, pull the keywords out, add section titles as context, then add related terms to each
        print("document style")
    
    if isinstance(index_to_fix[first_index], dict) and "Related Terms" in index_to_fix[first_index]:
        # need to turn each dictionary item into the proper format, extract anything in the proper names list into their own index items
        print("dict style")

    print("FAILED TO FIX!")
    return index_to_fix


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
#        if not "context" in value:
#            return False
#        if not isinstance(value['context'], list):
#            return False
        # don't care about other stuff at the moment
    return True

files_to_parse = os.listdir(__OUTPUT_DIR)
master_index = {}
for index_file in sorted(files_to_parse):
    if not index_file.endswith('.json'):
        continue
    print(index_file)
    base_file_name = os.path.splitext(index_file)[0]
    with open(os.path.join(__OUTPUT_DIR, index_file)) as f:
        index_part = json.load(f)
        # expected format is: { "1": { "term": "word", "related_terms": [], "context": [], "frequency": <string or number>}, ... }
        # context may be missing
        # reformat the json if needed
        if next(iter(index_part)) != "1":
            index_part = fix_index(index_part)
        print(f"valid index: {is_valid_index_json(index_part)}")
