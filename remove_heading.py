import os
import re

def remove_related_heading_and_content(file_path, heading, level):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Regular expression to match the specified heading and its contents
    pattern = rf'({level * "#"} {heading}(?:\r?\n(?!(?:\r?\n)?\s*{level * "#"}).*)*)'
    modified_content, count = re.subn(pattern, '', content, flags=re.MULTILINE)

    return modified_content, count > 0

def process_directory(directory_path, heading, level):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                modified_content, is_modified = remove_related_heading_and_content(file_path, heading, level)

                if is_modified:
                    print(f'Removal found in {file_path}')
                    confirm = input('Do you want to remove the heading and its content? (Y/N): ').lower()
                    if confirm == 'y':
                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.write(modified_content)
                        print(f'Successfully removed the heading and its content from {file_path}')
                    else:
                        print(f'Skipped removal for {file_path}')
                else:
                    print(f'No matching heading found in {file_path}')

if __name__ == '__main__':
    directory_path = input('Enter the path to your markdown files directory: ')
    heading = input('Enter the heading to remove: ')
    level = int(input('Enter the level of the heading to remove (1, 2, 3, etc.): '))
    process_directory(directory_path, heading, level)
