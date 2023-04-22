# Fixes WikiLinks that contain a forward slash
# caused by the link conversion plugin in Obsidian
import os
import re

def modify_wikilinks(match):
    link = match.group(1)
    return f"[[{link.split('/')[-1]}]]"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    modified_content = re.sub(r'\[\[(.+?)\]\]', modify_wikilinks, content)

    if content != modified_content:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(modified_content)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    directory = input("Enter the path to the directory you want to process: ")
    process_directory(directory)
    print("Processing completed.")
