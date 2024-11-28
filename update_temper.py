import os

def update_temper_script(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove existing temper script if present
    if 'temper.js' in content:
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if 'temper.js' not in line:
                new_lines.append(line)
        content = '\n'.join(new_lines)
    
    # Add new temper scripts before </body>
    new_scripts = '''  <script type="text/javascript">const fs = 3.5;</script>
  <script type="text/javascript" src="https://temper.one/temper.js"></script>'''
    
    content = content.replace('</body>', f'{new_scripts}\n</body>')
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_essays_folder():
    essays_dir = 'essays'
    for filename in os.listdir(essays_dir):
        if filename.endswith('.html') and filename != 'essays.html':
            file_path = os.path.join(essays_dir, filename)
            print(f"Processing {filename}...")
            update_temper_script(file_path)
            print(f"Completed {filename}")

if __name__ == '__main__':
    process_essays_folder()