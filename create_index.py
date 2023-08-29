import configparser
import json
import os

import openai


__CONTENT_DIR = 'content'
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
output_part = 1

for mdfile in sorted(files_to_parse):
  if not mdfile.endswith('.md'):
    continue
  print(mdfile)
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

  for section in sections:
    if (len(section['contents'])) < 5:
      continue
    print(f"{section['title']}: {len(section['contents'])} lines")
    section_parts = [section['contents'][i * 200:(i + 1) * 200] for i in range((len(section['contents']) + 200 - 1) // 200 )] 
    print(f"parts: {len(section_parts)}")

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
      outfile = f"output-{output_part:03d}"
      with open(outfile+'.txt', 'w') as f:
        f.write(json.dumps(response, indent=2))

      with open(outfile+'.json', 'w') as f:
        result = response['choices'][0]['message']['content']
        result_json = json.loads(result)
        f.write(json.dumps(result_json, indent=2))

      output_part += 1

  print('\n')

""" print('calling OpenAI')
response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {
      "role": "user",
      "content": prompt+test_content
    }
  ],
  temperature=0.5,
  max_tokens=4096,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print('writing files')
with open('output.txt', 'w') as f:
  f.write(json.dumps(response, indent=2))

with open('results.json', 'w') as f:
  result = response['choices'][0]['message']['content']
  result_json = json.loads(result)
  f.write(json.dumps(result_json, indent=2))
 """
