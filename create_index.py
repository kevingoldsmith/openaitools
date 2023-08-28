import configparser
import os

import openai


__CONTENT_DIR = 'content'

config_parser = configparser.ConfigParser()
config_parser.read('openaiconfig.ini')
openai_secret = config_parser['keys']['openaikey']

files_to_parse = os.listdir(__CONTENT_DIR)
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
  
  print('\n')

""" openai.api_key = openai_secret

response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {
      "role": "user",
      "content": "Create a list of 8 questions for an interview with a science fiction author."
    }
  ],
  temperature=0.5,
  max_tokens=1024,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response) """