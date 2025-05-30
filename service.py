import pandas as pd
from youtube_search import YoutubeSearch

from model import Playlist

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

df = pd.read_csv("hf://datasets/noelmurti/spotify_data/spotify_dataset.csv")

emotion_feature_map = {
    "Anger": {
        "Energy": 90,
        "Danceability": 40,
        "Positiveness": 20,
        "Speechiness": 30,
        "Liveness": 60,
        "Acousticness": 10,
        "Instrumentalness": 20
    },
    "Love": {
        "Energy": 60,
        "Danceability": 80,
        "Positiveness": 90,
        "Speechiness": 40,
        "Liveness": 50,
        "Acousticness": 30,
        "Instrumentalness": 20
    },
    "Hope": {
        "Energy": 70,
        "Danceability": 60,
        "Positiveness": 90,
        "Speechiness": 30,
        "Liveness": 40,
        "Acousticness": 40,
        "Instrumentalness": 30
    },
    "Excitement": {
        "Energy": 95,
        "Danceability": 90,
        "Positiveness": 85,
        "Speechiness": 40,
        "Liveness": 70,
        "Acousticness": 10,
        "Instrumentalness": 10
    },
    "Calmness": {
        "Energy": 20,
        "Danceability": 40,
        "Positiveness": 70,
        "Speechiness": 20,
        "Liveness": 30,
        "Acousticness": 90,
        "Instrumentalness": 80
    },
    "Sadness": {
        "Energy": 20,
        "Danceability": 30,
        "Positiveness": 10,
        "Speechiness": 30,
        "Liveness": 30,
        "Acousticness": 80,
        "Instrumentalness": 70
    },
    "Loneliness": {
        "Energy": 30,
        "Danceability": 20,
        "Positiveness": 15,
        "Speechiness": 60,
        "Liveness": 40,
        "Acousticness": 70,
        "Instrumentalness": 60
    },
    "Dream": {
        "Energy": 40,
        "Danceability": 50,
        "Positiveness": 60,
        "Speechiness": 30,
        "Liveness": 30,
        "Acousticness": 85,
        "Instrumentalness": 90
    }
}
features = ['Energy','Danceability','Positiveness','Speechiness','Liveness','Acousticness','Instrumentalness']

def calculate_emotion_distance(emotion, emotion_vector):
    return sum(abs(emotion_feature_map[emotion][k] - emotion_vector[k]) for k in features)

df['Anger'] = df.apply(lambda row: calculate_emotion_distance('Anger', row), axis=1)
df['Love'] = df.apply(lambda row: calculate_emotion_distance('Love', row), axis=1)
df['Hope'] = df.apply(lambda row: calculate_emotion_distance('Hope', row), axis=1)
df['Excitement'] = df.apply(lambda row: calculate_emotion_distance('Excitement', row), axis=1)
df['Calmness'] = df.apply(lambda row: calculate_emotion_distance('Calmness', row), axis=1)
df['Dream'] = df.apply(lambda row: calculate_emotion_distance('Dream', row), axis=1)
df['Sadness'] = df.apply(lambda row: calculate_emotion_distance('Sadness', row), axis=1)
df['Loneliness'] = df.apply(lambda row: calculate_emotion_distance('Loneliness', row), axis=1)

genres = {}
for genre_cell in df["Genre"]:
    if isinstance(genre_cell, str):
        # 콤마로 나누기
        genre_list = [g.strip() for g in genre_cell.split(',')]
        for g in genre_list:
            genres[g] = genres.get(g, 0) + 1

def get_songs(emotion, genres, tempo, length, orderBy):

    def filter_genre(genre):
        genre_list = [g.strip() for g in genre.split(',')]
        if 'hip hop' in genre:
            genre_list.append('hip-hop')
        elif 'hip-hop' in genre:
            genre_list.append('hip-hop')
        for g in genre_list:
            if g in genres:
                return True
        return False
    df['TempoDiff'] = (df['Tempo'] - tempo).abs()
    popularity = {
        'Popularity':85,
        'Random': 0,
    }
    df['TempSort'] = df['Genre'].apply(filter_genre)
    res = df[(df[emotion] < 140) & (df['Popularity'] > popularity[orderBy])].sort_values(by=['TempSort', emotion, 'TempoDiff'], ascending=[False, True, True]).sample(frac=1).head(length)[['Artist(s)', 'song']]
    print(res)
    return res

def get_youtube(artist, song):
    res = sorted(YoutubeSearch(artist + ' - ' + song, max_results=10).to_dict(), key=lambda x: x['views'], reverse=True)[0]
    response = {}
    response['title'] = res['title']
    response['url'] = "youtube.com"+res['url_suffix']
    response['channel'] = res['channel']
    response['thumbnail'] = res['thumbnails'][0]
    response['duration'] = res['duration']
    response['views'] = res['views']
    response['publish_time'] = res['publish_time']
    return response

def get_playlist(dto: Playlist):
    emotion = dto.emotion
    genre = dto.genres if dto.genres else list(genres.keys())
    tempo = dto.tempo
    length = dto.length
    orderBy = dto.orderBy

    songs = get_songs(emotion, genre, tempo, length, orderBy).to_dict(orient='records')
    result = []
    for song in songs:
        youtube = get_youtube(song['Artist(s)'], song['song'])
        result.append(youtube)
    return result
