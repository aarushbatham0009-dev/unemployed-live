from flask import Flask, Response
import requests

app = Flask(__name__)

def get_club_members():
    url = "https://api.chess.com/pub/club/da-unemployed/members"
    
    # Bilkul fresh aur real-looking headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    session = requests.Session()
    try:
        # 30 seconds ka heavy timeout
        response = session.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            # Sabse naye members ko nikalna
            res = data.get('all_time', [])
            if res:
                return [m['username'] for m in res[-3:][::-1]]
        return []
    except Exception as e:
        return []

@app.route('/')
@app.route('/api/index')
def main():
    members = get_club_members()
    
    svg = f'''<svg width="260" height="230" viewBox="0 0 260 230" xmlns="http://www.w3.org/2000/svg">
        <rect width="256" height="226" x="2" y="2" rx="12" fill="#3d0000" stroke="#ffdab9" stroke-width="3"/>
        <rect width="260" height="45" rx="0" fill="#ffdab9"/>
        <text x="50%" y="30" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="bold" fill="#3d0000">⚜️ NEW UNEMPLOYED ⚜️</text>'''

    if not members:
        # Agar ye dikhe, matlab Chess.com ne Vercel ko 100% block kiya hai
        svg += '<text x="50%" y="130" text-anchor="middle" font-family="Georgia" font-size="12" fill="#ffdab9">Server Blocked by Chess.com</text>'
    else:
        for i, name in enumerate(members):
            y = 65 + (i * 50)
            svg += f'''
            <a href="https://www.chess.com/member/{name}" target="_blank">
                <rect x="15" y="{y}" width="230" height="40" rx="8" fill="rgba(255,218,185,0.1)" stroke="#d4af37" stroke-width="1"/>
                <text x="30" y="{y+25}" font-family="Georgia, serif" font-size="16" font-weight="bold" fill="#ffd700">@</text>
                <text x="50" y="{y+25}" font-family="Georgia, serif" font-size="14" font-weight="bold" fill="#ffdab9">{name}</text>
            </a>'''

    svg += '<text x="50%" y="215" text-anchor="middle" font-family="Georgia, serif" font-size="9" fill="#d4af37" opacity="0.8">TAP ID TO VIEW PROFILE</text></svg>'
    return Response(svg, mimetype='image/svg+xml', headers={'Cache-Control': 'no-cache, no-store, must-revalidate'})
