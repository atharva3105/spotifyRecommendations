from flask import Flask, url_for, session, request, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
import json
from dmwfunc import *


app = Flask(__name__)

app.secret_key = "irknk4lkqgewlkngqobgt"
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'


@app.route('/', methods=['GET', 'POST'])
def login():

    return render_template('base.html')


@app.route('/login')
def spologin():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)


@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/getTracks")


@app.route('/logout')
def logout():
    session.clear()
    for key in list(session.keys()):
        session.pop(key)
    return redirect("https://www.spotify.com/logout/")


@app.route('/search', methods=['GET', 'POST'])
def search():

    data = pd.read_csv("songs2.csv")
    df = pd.DataFrame(data)
    songs = []
    for i in range(0, len(df['id'])):
        s = df.iloc[i]["name"]
        songs += [s]
    if request.method == 'POST':
        song = request.form["nm"]
        if song not in songs:
            return render_template('search.html')
        else:
            try:
                token_info, token_valid = get_token()
                if not token_valid:
                    assert False, "Invalid token"
            except:
                return redirect("/")
            sp = spotipy.Spotify(auth=session.get(
                'token_info').get('access_token'))
            index = 0
            for i, s in enumerate(songs):
                if (s == song):
                    index = i
                    break
            idd = df['id'][index]
            rec = song_recommender(df, idd)
            songs = []
            artist = []
            for i in rec:
                row = df.iloc[i][:]
                songs += [row[0]]
                artist += [row[2]]
            img1 = []
            img2 = []
            img3 = []
            for i in rec:
                s = sp.track(df['id'][i])
                i1 = s["album"]["images"][0]["url"]
                i2 = s["album"]["images"][1]["url"]
                i3 = s["album"]["images"][2]["url"]
                img1 += [str(i1)]
                img2 += [str(i2)]
                img3 += [str(i3)]
            return render_template("recm.html", arrr=zip(songs, artist, img1, img2, img3))

    else:
        return render_template('search.html', songs=songs)
        # return str(songs)


@app.route('/getTracks', methods=['GET', 'POST'])
def get_all_tracks():

    try:
        token_info, token_valid = get_token()
        if not token_valid:
            assert False, "Invalid token"
    except:
        return redirect("/")
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    data = pd.read_csv("songs2.csv")
    df = pd.DataFrame(data)

    try:
        usong = sp.current_user_saved_tracks(limit=1, offset=0)["items"]
    except:
        return render_template('base.html')

    idd = str(usong[0]["track"]["id"])
    audio = sp.audio_features(idd)
    if idd not in df["id"]:
        print("song not in list")
        data = get_row(audio, usong)
        df = df.append(data, ignore_index=True)
    rec = song_recommender(df, idd)
    songs = []
    artist = []
    for i in rec:
        row = df.iloc[i][:]
        songs += [row[0]]
        artist += [row[2]]

    img1 = []
    img2 = []
    img3 = []
    for i in rec:
        s = sp.track(df['id'][i])
        i1 = s["album"]["images"][0]["url"]
        i2 = s["album"]["images"][1]["url"]
        i3 = s["album"]["images"][2]["url"]
        img1 += [str(i1)]
        img2 += [str(i2)]
        img3 += [str(i3)]

    # for i in rec:
    #     roww = df.iloc[i][:]
    #     ans += [roww[0]+" - "+roww[2]]
    return render_template("recm.html", arrr=zip(songs, artist, img1, img2, img3))


# Checks to see if token is valid and gets a new token if not


def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(
            session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="9552a5a29def45b69b181ddb8b4f719b",
        client_secret="b6eb27f34bd544f0bb3ac475e6fcab28",
        redirect_uri=url_for('authorize', _external=True),
        scope="user-library-read")


if __name__ == "__main__":
    DEBUG = True
    HOST = '0.0.0.0'
    app.run(debug=DEBUG, host=HOST)
