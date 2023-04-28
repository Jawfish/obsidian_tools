import os
import re
import urllib.parse


def markdown_to_wikilink(match):
    title, path = match.groups()
    path = urllib.parse.unquote(path)
    filename = os.path.splitext(os.path.basename(path))[0]
    wikilink = f"[[{filename}|{title}]]"
    return wikilink


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    modified_content = re.sub(r"\[(.+?)\]\((.+?\.md)\)", markdown_to_wikilink, content)

    if content != modified_content:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(modified_content)


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                process_file(filepath)


if __name__ == "__main__":
    directory = input("Enter the path to the directory you want to process: ")
    process_directory(directory)
    print("Processing completed.")
