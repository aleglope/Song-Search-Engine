import requests
from bs4 import BeautifulSoup


def fetch_songs_from_billboard(date):
    """
    Fetches the list of top 100 songs from the Billboard Hot 100 chart for a given date.

    Parameters:
        date (str): The date in YYYY-MM-DD format to fetch the songs for.

    Returns:
        list of str: A list of strings, each containing "song title by artist",
        or an empty list if an error occurs.
    """

    # Build the URL for the Billboard Hot 100 list based on the provided date
    url = f"https://www.billboard.com/charts/hot-100/{date}"
    print(f"Fetching data from: {url}")

    # Attempt to make the HTTP request with a timeout of 10 seconds
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Ensure a successful response is received
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again or check your connection.")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error occurred: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return []

    # Use BeautifulSoup to parse the page content
    web_page = response.text
    soup = BeautifulSoup(web_page, "html.parser")

    # Initialize lists to store song titles and artists
    songs = []
    artists = []

    # Find all elements that contain the song data
    tag = soup.find_all(name="li", class_="lrv-u-width-100p")

    # Process each song and artist entry
    for i in tag:
        t = i.find_all(name="ul")
        for j in t:
            t1 = j.find_all(name="li")
            for k in t1:
                t2 = k.find_all(name="h3")
                for l in t2:
                    t3 = l.get_text()
                    songs.append(str(t3).strip("\n\t"))
                t4 = k.find_all(name="span")
                for m in t4:
                    t5 = m.get_text()
                    artists.append(str(t5).strip("\n\t"))

    # Assume every 16th element in the artists list corresponds to the song's artist
    artists = artists[::16]

    # Combine songs and artists into a list of strings
    combined_song_artist = [f"{songs[i]} by {artists[i]}" for i in range(len(songs))]
    return combined_song_artist
