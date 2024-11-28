import os

def modify_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find the .text p CSS rule and modify the margin
    old_css = """    .text p {
      margin: 20px 0;"""
    new_css = """    .text p {
      margin: 10px 0;"""
    
    modified_content = content.replace(old_css, new_css)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)

def process_essays():
    essays_dir = 'essays'
    for filename in os.listdir(essays_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(essays_dir, filename)
            print(f"Processing {filename}...")
            modify_file(file_path)
            print(f"Completed {filename}")

if __name__ == '__main__':
    process_essays()