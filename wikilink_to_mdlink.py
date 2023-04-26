# turns WikiLinks into Markdown links
# [[example link]] -> [example link](example%20link.md)
# [[example link|Example Link]] -> [Example Link](example%20link.md)
# [[example link]] in parent directory -> [example link](../example%20link.md)

import os
import re

def process_wikilink(match, file_path):
    wikilink = match.group(1)
    if "|" in wikilink:
        filename, title = wikilink.split("|")
    else:
        filename, title = wikilink, wikilink

    filename = filename.replace(" ", "%20")
    rel_path = os.path.relpath(os.path.join(os.path.dirname(file_path), filename), start=os.path.dirname(file_path))
    return f"[{title}]({rel_path})"

def convert_wikilinks(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    content = re.sub(r"\[\[(.*?)\]\]", lambda match: process_wikilink(match, file_path), content)

    with open(file_path, "w") as file:
        file.write(content)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                convert_wikilinks(file_path)

if __name__ == "__main__":
    directory = input("Enter the path to the directory: ")
    process_directory(directory)
