import os

def fix_essay_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix 1: Remove animation delays
    content = content.replace('style="animation-delay: 0.1s;"', '')
    content = content.replace('style="animation-delay: 0.2s;"', '')
    content = content.replace('style="animation-delay: 0.3s;"', '')
    content = content.replace('style="animation-delay: 0.4s;"', '')
    content = content.replace('style="animation-delay: 0.5s;"', '')
    content = content.replace('style="animation-delay: 0.6s;"', '')
    content = content.replace('style="animation-delay: 0.7s;"', '')
    content = content.replace('style="animation-delay: 0.8s;"', '')
    content = content.replace('style="animation-delay: 0.9s;"', '')
    content = content.replace('style="animation-delay: 1.0s;"', '')
    content = content.replace('style="animation-delay: 1.1s;"', '')
    content = content.replace('style="animation-delay: 1.2s;"', '')

    # Fix 2: Update text width and paragraph spacing in CSS
    content = content.replace('padding: 1.4vw 10vw 2.1vw 3vw;', 'padding: 1.4vw 25vw 1.4vw 3vw;')
    
    # Fix 3: Adjust paragraph margins
    content = content.replace('margin: 5px 0;', 'margin: 12px 0;')
    content = content.replace('margin: 15px 0;', 'margin: 12px 0;')
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_essays_folder():
    essays_dir = 'essays'
    for filename in os.listdir(essays_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(essays_dir, filename)
            print(f"Fixing {filename}...")
            fix_essay_file(file_path)
            print(f"Completed {filename}")

if __name__ == '__main__':
    process_essays_folder() 