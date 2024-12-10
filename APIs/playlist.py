import requests
import random

BASE_URL = "https://api.jamendo.com/v3.0/tracks/"
API_KEY = "141e0653" 

def fetch_songs_based_on_workouts(workout_count):
    """
    Fetch songs from the Jamendo API based on the number of workouts.

    Args:
        workout_count : integer number of workouts completed by the user. It helps in determining the intensity.

    Returns:
        songs : list of song names and their artists based on workout count.
    """
    params = {
        "client_id": API_KEY,
    }

    duration_min = workout_count * 100
    if(duration_min>500):
        duration_min = 500
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() 
        data = response.json()
        
        if "results" in data:
            songs = []
            for song in data["results"]:
                if song.get("duration", 0) >= duration_min:
                    song_name = song.get("name", "Unknown")
                    artist_name = song.get("artist_name", "Unknown")
                    songs.append(f"{song_name} by {artist_name}")
            
            return songs
        else:
            return ["No songs found for the given criteria."]
    
    except requests.exceptions.RequestException as e:
        return [f"An error occurred: {e}"]
    
def fetch_random_song():
    """
    Fetch a random song from the Jamendo API.

    Returns:
        str: A random song name and its artist.
    """
    params = {
        "client_id": API_KEY,
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            song = random.choice(data["results"])
            song_name = song.get("name", "Unknown")
            artist_name = song.get("artist_name", "Unknown")
            return f"{song_name} by {artist_name}"
        else:
            return "No songs found."
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    workout_count = 2 # fixed number, in reality it should be the length of workouts
    songs = fetch_songs_based_on_workouts(workout_count)
    songs = fetch_random_song()
    print("Recommended Songs:")
    #for song in songs:
        #print(song)
    print(songs)