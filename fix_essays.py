import os

def fix_essay_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix 1: Remove display:none from body
    content = content.replace('<body style="display:none;">', '<body>')
    
    # Fix 2: Update visibility and display in text class
    content = content.replace('''      display: none;
      opacity: 0;
      font-size: 18px;
      line-height: 21px;
      font-variant-ligatures: normal;
      visibility: hidden;''', '''      display: block;
      opacity: 1;
      font-size: 18px;
      line-height: 21px;
      font-variant-ligatures: normal;
      visibility: visible;''')
    
    # Fix 3: Update text p class
    content = content.replace('''      opacity: 0;
      display: none;
      visibility: hidden;''', '''      opacity: 1;
      display: block;
      visibility: visible;''')
    
    # Fix 4: Standardize temper script
    content = content.replace('temper-key.js', 'temper.js')

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