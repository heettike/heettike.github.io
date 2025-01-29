import os
import re

def reduce_font_sizes(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Reduce font sizes by 30%
    replacements = {
        'font-size: 26px': 'font-size: 18px',
        'line-height: 30px': 'line-height: 21px',
        'font-size: 52px': 'font-size: 36px',
        'line-height: 60px': 'line-height: 42px'
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    with open(file_path, 'w') as file:
        file.write(content)

def process_essays_folder():
    essays_dir = 'essays'
    for filename in os.listdir(essays_dir):
        if filename.endswith('.html') and filename != 'words.html':
            file_path = os.path.join(essays_dir, filename)
            reduce_font_sizes(file_path)

if __name__ == '__main__':
    process_essays_folder()