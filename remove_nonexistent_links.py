# Remove non-existent links from markdown files,
# replacing them with the link title
import os
import re
from pathlib import Path
from urllib.parse import unquote

def find_markdown_files(root_directory):
    markdown_files = []
    for root, _, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def process_file(file_path, dry_run=False):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    modified_content = content
    for title, link in links:
        if not link.endswith('.md'):
            continue

        decoded_link = unquote(link)
        link_path = (Path(file_path).parent / decoded_link).resolve()
        if not link_path.exists() or not link_path.is_file():
            modified_content = modified_content.replace(f'[{title}]({link})', title)
            if dry_run:
                print(f'File: {file_path}\nOriginal: [{title}]({link})\nModified: {title}\n')

    if not dry_run:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)

def main():
    root_directory = input('Enter the path to your markdown files directory: ')
    dry_run = input('Is this a dry run? (Y/N): ').lower() == 'y'
    markdown_files = find_markdown_files(root_directory)
    for file_path in markdown_files:
            process_file(file_path, dry_run)

if __name__ == '__main__':
    main()
