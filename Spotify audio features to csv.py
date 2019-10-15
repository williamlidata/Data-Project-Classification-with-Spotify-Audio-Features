import spotipy
import csv
import spotipy.util as util

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2

# api access
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"

credentials = oauth2.SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET)

token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)

sp = spotipy.Spotify(client_credentials_manager = credentials)

# albums to include
album_ids =  [
    "7mzrIsaAjnXihW3InKjlC3", #Taylor Swift
    "2dqn5yOQWdyGwOpOIi9O4x", #Fearless
    "5EpMjweRD573ASl7uNiHym", #Speak Now
    "1KlU96Hw9nlvqpBPlSqcTV", #Red
    "34OkZVpuzBa9y40DCy0LPR", #1989
    "6DEjYFkNZh67HP7R9PSZvv", #Reputation
    "1NAmidJlEaVgA3MpcPFYGq", #Lover
    "7vzYp7FrKnTRoktBYsx9SF", #Holiday collection
]

# audio feature header for csv file
audio_features_header = [
  "danceability",
  "energy",
  "key",
  "loudness",
  "mode",
  "speechiness",
  "acousticness",
  "instrumentalness",
  "liveness",
  "valence",
  "tempo",
  "type",
  "id",
  "uri",
  "track_href",
  "analysis_url",
  "duration_ms",
  "time_signature"
]

# extract data to csv file
csv_file = open('taylor swift discography spotify audio features.csv', 'w', newline = '')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['album_id', 'album_name', 'track_id', 'track_name', 'release_date'] + audio_features_header)

full_track_list = []
# extract spotify uri id for every song in album list
for album_id in album_ids:
    for item, track in enumerate(sp.album(album_id)['tracks']['items']):
        full_track_list.append(track['uri'])

# extract metadata for each track
for track_id in full_track_list:
    track_data = sp.track(track_id)
    album_id = track_data['album']['id']
    album_name = track_data['album']['name']
    track_id = track_data['id']
    track_name = track_data['name']
    release_date = track_data['album']['release_date']

#extract spotify "audio features" data for each track
#documentation for audio features description: 
#https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
    audio_features = []
    #extract values only from each dictionary pair
    for item in sp.audio_features(track_id):
        for key, value in item.items():
            audio_features.append(value)
            
    csv_writer.writerow([album_id, album_name, track_id, track_name, release_date] + audio_features)

csv_file.close()
