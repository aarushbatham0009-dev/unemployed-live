from flask import Flask, Response
import requests
import random

app = Flask(__name__)

def get_club_members():
    url = "https://api.chess.com/pub/club/da-unemployed/members"
    # Random User-Agents taaki Chess.com block na kare
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    ]
    headers = {'User-Agent': random.choice(user_agents)}
    
    try:
        # Timeout ko thoda badha diya hai
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            members = data.get('all_time', [])
            return members[-3:][::-1] if members else []
        return []
    except:
        return []

@app.route('/')
@app.route('/api/index')
def main():
    members = get_club_members()
    
    # SVG Design
    svg = f'''<svg width="260" height="230" viewBox="0 0 260 230" xmlns="http://www.w3.org/2000/svg">
        <rect width="256" height="226" x="2" y="2" rx="12" fill="#3d0000" stroke="#ffdab9" stroke-width="3"/>
        <rect width="260" height="45" rx="0" fill="#ffdab9"/>
        <text x="50%" y="30" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="bold" fill="#3d0000">⚜️ NEW UNEMPLOYED ⚜️</text>'''

    if not members:
        # Agar data nahi mila toh purane static names dikha dega backup ke liye
        svg += '<text x="50%" y="130" text-anchor="middle" font-family="Georgia" font-size="12" fill="#ffdab9">Updating Feed...</text>'
    else:
        for i, m in enumerate(members):
            name = m['username']
            y = 65 + (i * 50)
            svg += f'''
            <a href="https://www.chess.com/member/{name}" target="_blank">
                <rect x="15" y="{y}" width="230" height="40" rx="8" fill="rgba(255,218,185,0.1)" stroke="#d4af37" stroke-width="1"/>
                <text x="30" y="{y+25}" font-family="Georgia, serif" font-size="16" font-weight="bold" fill="#ffd700">@</text>
                <text x="50" y="{y+25}" font-family="Georgia, serif" font-size="14" font-weight="bold" fill="#ffdab9">{name}</text>
            </a>'''

    svg += '<text x="50%" y="215" text-anchor="middle" font-family="Georgia, serif" font-size="9" fill="#d4af37" opacity="0.8">TAP ID TO VIEW PROFILE</text></svg>'
    return Response(svg, mimetype='image/svg+xml', headers={'Cache-Control': 'no-cache'})
