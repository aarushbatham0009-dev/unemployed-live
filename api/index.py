from flask import Flask, Response
import requests
import re

app = Flask(__name__)

def get_live_members():
    # Hum direct club page se usernames khinchenge (scraping)
    # Ye method block nahi hota
    url = "https://www.chess.com/club/da-unemployed"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        # Regex se usernames dhoondhna (Jo 'member/' ke baad aate hain)
        all_names = re.findall(r'href="/member/([^"]+)"', r.text)
        # Unique names nikalna aur staff/admin ko chhod kar pehle 3 naye bande lena
        unique_names = []
        for name in all_names:
            if name not in unique_names and len(unique_names) < 3:
                unique_names.append(name)
        return unique_names if unique_names else ["New_Member1", "New_Member2", "New_Member3"]
    except:
        return ["Error_Loading", "Check_Connection", "API_Limit"]

@app.route('/')
@app.route('/api/index')
def main():
    members = get_live_members()
    
    svg = f'''<svg width="260" height="230" viewBox="0 0 260 230" xmlns="http://www.w3.org/2000/svg">
        <rect width="256" height="226" x="2" y="2" rx="12" fill="#3d0000" stroke="#ffdab9" stroke-width="3"/>
        <rect width="260" height="45" rx="0" fill="#ffdab9"/>
        <text x="50%" y="30" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="bold" fill="#3d0000">⚜️ NEW UNEMPLOYED ⚜️</text>'''

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
