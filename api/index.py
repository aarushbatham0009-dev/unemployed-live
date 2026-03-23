from flask import Flask, Response
import requests

app = Flask(__name__)

def get_club_members():
    # Aapke club ka official slug 'da-unemployed' hai
    url = "https://api.chess.com/pub/club/da-unemployed/members"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        data = requests.get(url, headers=headers).json()
        # Latest 3 members (all_time list ke aakhir se 3)
        return data.get('all_time', [])[-3:][::-1]
    except:
        return []

@app.route('/')
@app.route('/api/index')
def main():
    members = get_club_members()
    
    # Theme: Dark Red and Peach
    svg_code = f'''<svg width="260" height="230" viewBox="0 0 260 230" xmlns="http://www.w3.org/2000/svg">
        <rect width="256" height="226" x="2" y="2" rx="12" fill="#3d0000" stroke="#ffdab9" stroke-width="3"/>
        <rect width="260" height="45" rx="0" fill="#ffdab9"/>
        <text x="50%" y="30" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="bold" fill="#3d0000">⚜️ NEW UNEMPLOYED ⚜️</text>
    '''

    for i, m in enumerate(members):
        name = m['username']
        y = 65 + (i * 50)
        # Har member ke liye alag clickable link
        svg_code += f'''
        <a href="https://www.chess.com/member/{name}" target="_blank">
            <rect x="15" y="{y}" width="230" height="40" rx="8" fill="rgba(255,218,185,0.1)" stroke="#d4af37" stroke-width="1"/>
            <text x="30" y="{y+25}" font-family="Georgia, serif" font-size="16" font-weight="bold" fill="#ffd700">@</text>
            <text x="50" y="{y+25}" font-family="Georgia, serif" font-size="14" font-weight="bold" fill="#ffdab9">{name}</text>
        </a>'''

    svg_code += '<text x="50%" y="215" text-anchor="middle" font-family="Georgia, serif" font-size="9" fill="#d4af37" opacity="0.8">TAP ID TO VIEW PROFILE</text></svg>'
    
    return Response(svg_code, mimetype='image/svg+xml')
