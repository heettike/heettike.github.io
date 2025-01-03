import os

def update_essay_style(file_path, title):
    new_head = f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{title} - heet tike</title>
  
  <link class="googlefont" href="https://fonts.googleapis.com/css2?family=Ovo&display=swap" rel="stylesheet">
  
  <style>
    body {{
      margin: 0;
      padding: 0;
      background: #000000;
      color: #ffffff;
      font-family: 'Ovo', serif;
    }}
    
    .text {{
      max-width: 680px;
      margin: 0 auto;
      padding: 40px 20px;
    }}
    
    .back-link {{
      color: #999;
      text-decoration: none;
      opacity: 0.5;
    }}
    
    .back-link:hover {{
      opacity: 1;
    }}
    
    .title {{
      margin-bottom: 0;
      font-size: 36px;
      line-height: 1.2;
    }}
    
    .date {{
      color: #999;
      margin-top: 5px;
      margin-bottom: 30px;
      opacity: 0.5;
    }}
    
    p {{
      line-height: 1.6;
      margin-bottom: 20px;
      font-size: 18px;
    }}
  </style>
</head>'''

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Find the body content
    body_start = content.find('<body')
    if body_start == -1:
        return
        
    body_content = content[body_start:]
    
    # Create new file content
    new_content = new_head + '\n' + body_content
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def process_essays():
    essays_dir = 'essays'
    essays = {
        'couchsurfing.html': 'couch surfing',
        'createartffs.html': 'create art ffs',
        'fewthingsaboutmoney.html': 'a few things about money',
        'metaonmoney.html': 'meta on money',
        'opportunitycost.html': 'opportunity cost',
        'perception.html': 'perception',
        'problemsolvers.html': 'problem solvers',
        'pursuit.html': 'pursuit',
        'rejection.html': 'rejection',
        'youthwastedonbeingyoung.html': 'youth wasted on being young'
    }
    
    for filename, title in essays.items():
        file_path = os.path.join(essays_dir, filename)
        if os.path.exists(file_path):
            print(f"Updating {filename}...")
            update_essay_style(file_path, title)
            print(f"Completed {filename}")

if __name__ == '__main__':
    process_essays() 