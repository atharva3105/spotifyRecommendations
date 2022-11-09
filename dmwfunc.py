import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
import re


def preprocess(df):
    # df = df.drop(["preview"], axis=1)
    df = df.drop_duplicates()


def select_cols(df):
    df1 = df[['artist', 'id', 'name', 'danceability', 'energy', 'key', 'loudness', 'mode',
              'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',  "popularity"]]
    return df1


def select_col_vec(df):

    df1 = df[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
              'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',  "popularity"]]
    return df1


def song_recommender(df, song_id):

    songs_ids = pd.Series(df.index, index=df['id'])
    scaler = MinMaxScaler()
    df2 = select_col_vec(df)
    model = scaler.fit(df2)
    scaled_data = model.transform(df2)
    rec = cosine_similarity(scaled_data)
    index = df[df['id'] == song_id].index[0]
    # index of the song using its id
    idx = songs_ids[song_id]
    # get cosine similarity scores for that song, sort them and get top 10 similar
    scores = list(enumerate(rec[index]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:12]

    # get the indexes of top 10 similar songs
    rec_songs_idxs = [i[0] for i in sorted_scores]
    return rec_songs_idxs


def get_row(audio, usong):
    id = usong[0]["track"]["id"]
    art = usong[0]["track"]["artists"][0]["name"]
    pop = usong[0]["track"]["popularity"]
    name = usong[0]["track"]["name"]
    audio_fe = audio[0]
    danceability = audio_fe["danceability"]
    energy = audio_fe["energy"]
    key = audio_fe["key"]
    loudness = audio_fe["loudness"]
    mode = audio_fe["mode"]
    speechiness = audio_fe["speechiness"]
    acousticness = audio_fe["acousticness"]
    instrumentalness = audio_fe["instrumentalness"]
    liveness = audio_fe["liveness"]
    valence = audio_fe["valence"]
    tempo = audio_fe["tempo"]
    anss = {'artist': art, 'id': id, 'name': name, 'danceability': danceability, 'energy': energy, 'key': key, 'loudness': loudness, 'mode': mode,
            'speechiness': speechiness, 'acousticness': acousticness, 'instrumentalness': instrumentalness, 'liveness': liveness, 'valence': valence, 'tempo': tempo,  "popularity": pop}

    return anss


def get_loud(df, rec):
    loud = []
    for i in rec:
        l = df[i]['loudness']
        loud += [l]
    return loud


def get_pop(df, rec):
    pop = []
    for i in rec:
        p = df[i]["popularity"]
        loud += [p]
    return loud
