import configparser
import json
import os

import openai


__CONTENT_DIR = 'content'
__OUTPUT_DIR = 'output'
__CONTENT_PROMPT_LENGTH=200

prompt = """Using the following criteria for selection, provide a JSON-formatted structured index of the following chunk of text, ignoring Markdown syntax like bullet points and links but considering headers for context. and limit the length of the index to 25 terms:
a. Relevance to leadership of software development organizations
b. Keywords include agile, management, software architecture and engineering
c. Word is used frequently
d. Term is specific and precise
e. Suggest related terms for cross-referencing
f. Accommodate professional-level reader comprehension
g. Consistent, organized and comprehensive results
h. Proper Names
"""

config_parser = configparser.ConfigParser()
config_parser.read('openaiconfig.ini')
openai_secret = config_parser['keys']['openaikey']
openai.api_key = openai_secret
files_to_parse = os.listdir(__CONTENT_DIR)

for mdfile in sorted(files_to_parse):
  if not mdfile.endswith('.md'):
    continue
  print(mdfile)
  base_file_name = os.path.splitext(mdfile)[0]
  
  sections = []
  current_section = { 'title': '', 'contents': [] }
  with open(os.path.join(__CONTENT_DIR, mdfile)) as f:
    for line in f:
      if not line.startswith('# '):
        if line != '\n':
          current_section['contents'].append(line)
      else:
        sections.append(current_section)
        current_section = {'title': line[2:], 'contents': []}
    sections.append(current_section)

  section_number = 1
  for section in sections:
    if (len(section['contents'])) < 5:
      continue
    print(f"{section['title']}: {len(section['contents'])} lines")
    section_parts = [section['contents'][i * __CONTENT_PROMPT_LENGTH:(i + 1) * __CONTENT_PROMPT_LENGTH] for i in range((len(section['contents']) + __CONTENT_PROMPT_LENGTH - 1) // __CONTENT_PROMPT_LENGTH )] 
    print(f"parts: {len(section_parts)}")

    lines = 0
    for part in section_parts:
      print('calling OpenAI')
      text = ''.join(part)
      response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
          {
            "role": "user",
            "content": prompt+text
          }
        ],
        temperature=0.5,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )

      print('writing files')
      if not os.path.exists(__OUTPUT_DIR):
        os.mkdir(__OUTPUT_DIR)
      outfile = os.path.join(__OUTPUT_DIR, f"{base_file_name}-{section_number:02d}-{''.join(x for x in section['title'] if x.isalnum())}-{lines:04d}-{(lines+len(part)):04d}")
      with open(outfile+'.txt', 'w') as f:
        f.write(json.dumps(response, indent=2))

      with open(outfile+'.json', 'w') as f:
        result = response['choices'][0]['message']['content']
        result_json = json.loads(result)
        f.write(json.dumps(result_json, indent=2))

      lines+=len(part)
      section_number += 1

  print('\n')
