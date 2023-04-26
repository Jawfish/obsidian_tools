# turns WikiLinks into Markdown links
# [[example link]] -> [example link](example%20link.md)
# [[example link|Example Link]] -> [Example Link](example%20link.md)
# [[example link]] in parent directory -> [example link](../example%20link.md)

import os
import re

def map_directory(directory):
    file_map = {}
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.lower().endswith('.md'):
                file_map[file.lower()] = os.path.join(root, file)
            else:
                file_map[file.lower()] = os.path.join(root, file)
    return file_map

def process_wikilink(match, file_path, file_map):
    wikilink = match.group(1)
    if "|" in wikilink:
        filename, title = wikilink.split("|")
    else:
        filename, title = wikilink, wikilink

    target_filename = filename.lower()
    target_file_path = None
    target_extension = ""

    for file_key in file_map:
        if file_key.startswith(target_filename):
            target_file_path = file_map[file_key]
            target_extension = os.path.splitext(file_key)[1]
            break

    if target_file_path is None:
        print(f"Warning: File {target_filename} not found for WikiLink '{wikilink}' in file {file_path}.")
        return f"[{title}]({filename.replace(' ', '%20')}{target_extension})"

    rel_path = os.path.relpath(target_file_path, start=os.path.dirname(file_path)).replace(" ", "%20")
    print(f"Processing WikiLink '{wikilink}' in file {file_path}: [{title}]({rel_path})")
    return f"[{title}]({rel_path})"

def convert_wikilinks(file_path, file_map):
    with open(file_path, "r") as file:
        content = file.read()

    content = re.sub(r"\[\[(.*?)\]\]", lambda match: process_wikilink(match, file_path, file_map), content)

    with open(file_path, "w") as file:
        file.write(content)

def process_directory(directory):
    file_map = map_directory(directory)

    for file_path in file_map.values():
        if file_path.lower().endswith('.md'):
            print(f"Processing file: {file_path}")
            convert_wikilinks(file_path, file_map)

if __name__ == "__main__":
    directory = input("Enter the path to the directory: ")
    process_directory(directory)
