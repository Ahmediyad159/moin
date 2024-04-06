from flask import Flask, redirect, url_for, session, request
from requests_oauthlib import OAuth2Session


app = Flask(__name__)
app.secret_key = 'ae277d97cd5efcc4fee854cdb114fea0'

# Discord OAuth2 configuration
CLIENT_ID = '1226173204826161212'
CLIENT_SECRET = 'BB17Lnz8cNtE-aG8Xj5NemAP1k6WWi11'
REDIRECT_URI = 'https://localhost:5000/callback'
DISCORD_API_URL = 'https://discord.com/api'


@app.route('/')
def home():
    return '<a href="/login">Login with Discord</a>'

@app.route('/login')
def login():
    scope = ['identify', 'guilds']
    discord = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=scope)
    authorization_url, _ = discord.authorization_url(f'{DISCORD_API_URL}/oauth2/authorize')
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    discord = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    token = discord.fetch_token(f'{DISCORD_API_URL}/oauth2/token',
                                 client_secret=CLIENT_SECRET,
                                 authorization_response=request.url)
    session['discord_token'] = token

    # Fetch user's info
    user_info = discord.get(f'{DISCORD_API_URL}/users/@me').json()
    session['user'] = user_info

    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    if 'discord_token' in session:
        user_info = session['user']
        return f"""
            <h1>Welcome, {user_info['username']}#{user_info['discriminator']}!</h1>
            <img src="https://cdn.discordapp.com/avatars/{user_info['id']}/{user_info['avatar']}.png" alt="Avatar">
            <br>
            <a href="/manage">Manage</a>
        """
    else:
        return redirect(url_for('login'))

@app.route('/manage')
def manage():
    if 'discord_token' in session:
        return 'You are authorized to manage.'
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
