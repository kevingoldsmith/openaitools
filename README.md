# openaitools
playing with the OpenAI API.

Add your OpenAI key into a new "openaiconfig.ini" file. The file format is
[keys]
openaikey: <your open ai key>

* **create_index_files.py/combine_indexes.py/convert_docx_to_md.sh**: This is a tool I created to generate an index from a collection of markdown files. I got the idea from [this post on reddit](https://www.reddit.com/r/ChatGPT/comments/14tivjt/how_to_index_a_textbook_with_chatgpt/?rdt=55220), but wanted to make something that was more automated. To use it, put your markdown files (you can use the convert_docx_to_md script to do this if you have Pandoc installed) into a "content" directory. Install the libraries in the requirements.txt files, and then run create_index_files.py followed by combine_indexes.py. The result is a file called master_index.json. The output directory will have the intermediate index files. This is in case there is an error running the script. You can run it again, and it will pick up from where it left off (saving you some $$).

Feel free to contribute! I'm more open to Pull requests than to issues, but I will try to answer any issues that are posted.
