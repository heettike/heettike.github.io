import os
import re
from bs4 import BeautifulSoup
from datetime import datetime

def extract_essay_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract title
    title = soup.find('h1', class_='title')
    title = title.text.strip() if title else os.path.basename(file_path).replace('.html', '')
    
    # Extract date
    date_elem = soup.find('p', class_='date')
    date_str = date_elem.text.strip() if date_elem else None
    
    # Extract content paragraphs
    content_paragraphs = []
    text_div = soup.find('div', class_='text')
    if text_div:
        # Get regular paragraphs (excluding back link and date)
        paragraphs = text_div.find_all('p')
        seen_content = set()  # Track seen content to avoid duplicates
        for p in paragraphs:
            if (not p.get('class', [''])[0] in ['back-link', 'date'] and  # Skip back link and date
                p.text.strip() and  # Skip empty paragraphs
                '← back' not in p.text):  # Skip back link text
                content = p.text.strip()
                if content not in seen_content:  # Only add if not seen before
                    content_paragraphs.append(content)
                    seen_content.add(content)
        
        # Get subtitle if exists
        subtitle = text_div.find('p', class_='subtitle')
        if subtitle and subtitle.text.strip() not in seen_content:
            content_paragraphs.insert(0, subtitle.text.strip())
            seen_content.add(subtitle.text.strip())
        
        # Get ordered list items if exist
        ol = text_div.find('ol')
        if ol:
            list_items = ol.find_all('li')
            # Add a blank line before the list if we have other content
            if content_paragraphs:
                content_paragraphs.append('')  # Add spacing
            for i, item in enumerate(list_items, 1):
                content_paragraphs.append(f"{i}. {item.text.strip()}")
        
        # Get image if exists
        img = text_div.find('img', class_='main-image')
        if img:
            img_src = img.get('src', '')
            if img_src.startswith('..'):
                img_src = img_src[2:]  # Remove leading ..
            if img_src:
                content_paragraphs.insert(0, f'<img src="{img_src}" alt="{img.get("alt", "")}" class="main-image" style="width: 100%; height: auto; margin-bottom: 30px;">')
    
    return {
        'title': title,
        'date': date_str,
        'content': content_paragraphs
    }

def parse_date(date_str):
    if not date_str:
        return datetime.min
    
    try:
        # Try first format: "27 Mar, 2024"
        return datetime.strptime(date_str, '%d %b, %Y')
    except ValueError:
        try:
            # Try second format: "Mar 27, 2024"
            return datetime.strptime(date_str, '%b %d, %Y')
        except ValueError:
            return datetime.min

def generate_new_essays_html():
    essays_dir = 'essays'
    essays = []
    seen_titles = set()  # Track seen titles to avoid duplicates
    
    # Add local essays
    for filename in os.listdir(essays_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(essays_dir, filename)
            essay_info = extract_essay_info(file_path)
            
            # Add all essays
            if essay_info['title'] not in seen_titles:
                essays.append(essay_info)
                seen_titles.add(essay_info['title'])
    
    # Add external essays
    external_essays = [
        {
            'title': 'household',
            'date': '15 Dec, 2023',
            'external_url': 'https://musingsbyh33t.substack.com/p/household?r=1gwe4m'
        },
        {
            'title': 'we take ourselves too seriously',
            'date': '1 Dec, 2023',
            'external_url': 'https://musingsbyh33t.substack.com/p/we-take-ourselves-too-seriously?r=1gwe4m'
        },
        {
            'title': 'being critical',
            'date': '15 Nov, 2023',
            'external_url': 'https://musingsbyh33t.substack.com/p/being-critical?r=1gwe4m'
        },
        {
            'title': '22nd year of life',
            'date': '1 Nov, 2023',
            'external_url': 'https://musingsbyh33t.substack.com/p/the-22nd-year-of-my-life?r=1gwe4m'
        },
        {
            'title': '21st year of life',
            'date': '15 Oct, 2023',
            'external_url': 'https://musingsbyh33t.substack.com/p/the-21st-year-of-my-life?r=1gwe4m'
        },
        {
            'title': 'leap of faith',
            'date': '1 Oct, 2023',
            'external_url': 'https://musingsbyh33t.substack.com/p/leap-of-faith?r=1gwe4m'
        },
        {
            'title': 'good addiction',
            'date': '15 Sep, 2023',
            'external_url': 'https://musingsbyh33t.substack.com/p/good-addiction-products?r=1gwe4m'
        },
        {
            'title': 'corporate to startups: 180° flip',
            'date': '1 Sep, 2023',
            'external_url': 'https://musingsbyh33t.substack.com/p/corporate-to-startups-how-my-life?r=1gwe4m'
        },
        {
            'title': 'monthly resolutions',
            'date': '15 Aug, 2023',
            'external_url': 'https://musingsbyh33t.substack.com/p/monthly-resolutions-update-612?r=1gwe4ml'
        },
        {
            'title': "beginner's guide to $$",
            'date': '1 Aug, 2023',
            'external_url': 'https://musingsbyh33t.substack.com/p/beginners-guide-to-personal-finance?r=1gwe4m'
        },
        {
            'title': 'out of sync',
            'date': '15 Jul, 2023',
            'external_url': 'https://musingsbyh33t.substack.com/p/out-of-sync?r=1gwe4m'
        },
        {
            'title': '3 years in du',
            'date': '1 Jul, 2023',
            'external_url': 'https://musingsbyh33t.substack.com/p/3-years-in-delhi-university-would?r=1gwe4m'
        }
    ]
    
    for essay in external_essays:
        if essay['title'] not in seen_titles:
            essays.append(essay)
            seen_titles.add(essay['title'])
    
    # Sort essays by date (newest first)
    essays.sort(key=lambda x: parse_date(x['date']), reverse=True)
    
    # Generate the new essays.html content
    template = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>essays - heet tike</title>
  
  <link class="googlefont" href="https://fonts.googleapis.com/css2?family=Ovo&display=swap" rel="stylesheet">
  
  <style>
    body {
      margin: 0;
      padding: 0;
      background: #000000;
      color: #ffffff;
      font-family: 'Ovo', serif;
    }
    
    .text {
      max-width: 680px;
      margin: 0 auto;
      padding: 40px 20px;
    }
    
    .back-link {
      color: #999;
      text-decoration: none;
      opacity: 0.5;
    }
    
    .back-link:hover {
      opacity: 1;
    }
    
    .title {
      margin-bottom: 0;
      font-size: 36px;
      line-height: 1.2;
    }
    
    .intro {
      margin: 30px 0;
      font-size: 18px;
      opacity: 0.8;
    }
    
    .essay-container {
      margin-top: 40px;
    }
    
    .essay-item, .stream-item {
      margin-bottom: 60px;
      padding-bottom: 40px;
      border-bottom: 2px solid rgba(255,255,255,0.2);
    }
    
    .essay-date, .stream-date {
      color: #999;
      font-size: 14px;
      opacity: 0.5;
      margin-bottom: 10px;
    }
    
    .essay-title {
      font-size: 24px;
      margin-bottom: 20px;
      line-height: 1.3;
    }
    
    .essay-title a {
      color: #ffffff;
      text-decoration: none;
      opacity: 0.8;
      transition: opacity 0.2s ease;
    }
    
    .essay-title a:hover {
      opacity: 1;
    }
    
    .essay-content, .stream-content {
      line-height: 1.6;
      font-size: 18px;
    }
    
    .stream-media {
      margin-top: 20px;
    }
    
    .stream-media img {
      max-width: 100%;
      border-radius: 4px;
    }
    
    .stream-media audio {
      width: 100%;
      margin-top: 10px;
    }
    
    .main-image {
      width: 100%;
      height: auto;
      margin-bottom: 30px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="text">
    <p>
      <a href="/" class="back-link">← back</a>
    </p>
    
    <h1 class="title">essays</h1>
    
    <div class="essay-container" id="combined-container">
'''
    
    # Add essays
    for essay in essays:
        template += f'''
      <div class="essay-item">
        <div class="essay-date">{essay.get('date', '')}</div>
'''
        
        if 'external_url' in essay:
            template += f'''
        <h2 class="essay-title">
          <a href="{essay['external_url']}" target="_blank">{essay['title']}</a>
        </h2>
'''
        else:
            template += f'''
        <h2 class="essay-title">
          <a href="essays/{essay['title'].lower().replace(' ', '')}.html">{essay['title']}</a>
        </h2>
'''
            if essay.get('content'):
                template += '''
        <div class="essay-content">
'''
                for paragraph in essay['content']:
                    if paragraph.startswith('<img'):
                        template += f'          {paragraph}\n'
                    else:
                        template += f'          <p>{paragraph}</p>\n'
                template += '        </div>\n'
        template += '      </div>\n'
    
    # Add streams integration
    template += '''
    </div>
  </div>

  <script>
    const USERNAME = 'heettike';
    
    // Store all essays from the page
    const essays = [];
    document.querySelectorAll('.essay-item').forEach(item => {
      const dateElem = item.querySelector('.essay-date');
      if (dateElem) {
        essays.push({
          type: 'essay',
          date: dateElem.textContent,
          html: item.outerHTML,
          timestamp: new Date(dateElem.textContent).getTime()
        });
      }
    });
    
    async function fetchStreams() {
      const CORS_PROXIES = [
        'https://api.allorigins.win/raw?url=',
        'https://corsproxy.io/?',
        'https://cors-anywhere.herokuapp.com/',
        'https://proxy.cors.sh/'
      ];
      
      let error;
      for (const proxy of CORS_PROXIES) {
        try {
          console.log('Trying proxy:', proxy);
          const STREAMS_URL = `https://streams.place/${USERNAME}/json`;
          const finalUrl = proxy + encodeURIComponent(STREAMS_URL);
          console.log('Fetching from URL:', finalUrl);
          
          const response = await fetch(finalUrl, {
            headers: {
              'Accept': 'application/json',
              'x-requested-with': 'XMLHttpRequest',
              'origin': 'https://heettike.github.io'
            }
          });
          
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          const streams = await response.json();
          console.log('Received streams:', streams);
          
          if (!streams || !Array.isArray(streams) || streams.length === 0) {
            console.log('No streams found or invalid response');
            renderContent(essays);
            return;
          }
          
          // Convert streams to same format as essays
          const formattedStreams = streams.map(stream => {
            const date = new Date(parseInt(stream.timestamp));
            const formattedDate = date.toLocaleDateString('en-US', {
              day: 'numeric',
              month: 'short',
              year: 'numeric'
            });
            
            let mediaHtml = '';
            if (stream.media && stream.media.length > 0) {
              stream.media.forEach(media => {
                if (media.type === 'photo') {
                  mediaHtml += `<div class="stream-media">
                    <img src="${media.urlToFile}" alt="Stream media" loading="lazy">
                  </div>`;
                } else if (media.type === 'animation') {
                  mediaHtml += `<div class="stream-media">
                    <img src="${media.urlToFile}" alt="Stream animation" loading="lazy">
                  </div>`;
                } else if (media.type === 'audio') {
                  mediaHtml += `<div class="stream-media">
                    <audio controls preload="none">
                      <source src="${media.urlToFile}" type="audio/ogg">
                      Your browser does not support the audio element.
                    </audio>
                  </div>`;
                }
              });
            }
            
            const streamHtml = `
              <div class="stream-item">
                <div class="stream-date">${formattedDate}</div>
                <div class="stream-content">${stream.html || stream.text}</div>
                ${mediaHtml}
              </div>
            `;
            
            return {
              type: 'stream',
              date: formattedDate,
              html: streamHtml,
              timestamp: parseInt(stream.timestamp)
            };
          });
          
          // Combine and sort all content
          const allContent = [...essays, ...formattedStreams].sort((a, b) => b.timestamp - a.timestamp);
          renderContent(allContent);
          return; // Success! Exit the function
          
        } catch (e) {
          console.error(`Error with proxy ${proxy}:`, e);
          error = e; // Store the last error
          continue; // Try next proxy
        }
      }
      
      // If we get here, all proxies failed
      console.error('All proxies failed. Last error:', error);
      console.error('Error details:', {
        message: error.message,
        stack: error.stack
      });
      renderContent(essays);
    }
    
    function renderContent(content) {
      const container = document.getElementById('combined-container');
      container.innerHTML = content.map(item => item.html).join('\n');
    }
    
    // Call fetchStreams immediately and set up periodic refresh
    fetchStreams().catch(err => {
      console.error('Top level error:', err);
    });
    
    // Refresh streams every 2 minutes
    setInterval(fetchStreams, 2 * 60 * 1000);
  </script>
  
  <script type="text/javascript">const fs = 3.5;</script>
  <script type="text/javascript" src="https://temper.one/temper.js"></script>
</body>
</html>'''

    # Write the new content to essays.html
    with open('essays.html', 'w', encoding='utf-8') as f:
        f.write(template)

if __name__ == '__main__':
    generate_new_essays_html() 
    generate_new_essays_html() 