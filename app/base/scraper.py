from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from base.models import Movie
from base.tmdb_helpers import TMDBClient
import time
import environ
import re

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

def scrape_imdb_top_250():
    # Downloading imdb top 250 movie's data
    url = "https://www.imdb.com/chart/top/"
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.8"  # Set language to English
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    titles = [t.get_text() for t in soup.find_all("h3", class_="ipc-title__text")][1:251]
    meta_containers = soup.find_all("div", class_="sc-b85248f1-5 kZGNjY cli-title-metadata")
    year = []
    duration = []

    for container in meta_containers:
        meta_items = container.find_all("span", class_="sc-b85248f1-6 bnDqKN cli-title-metadata-item")
        if len(meta_items) >= 2:
            year.append(meta_items[0].get_text())
            duration.append(meta_items[1].get_text())
        else:
            year.append(None)
            duration.append(None)

    rankings = [r.get_text() for r in soup.find_all("span", class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating")]
    poster_paths = [p['src'] for p in soup.find_all("img", class_="ipc-image")]

    movies = [{
        "title": t,
        "year": y, 
        "duration": d,
        "ranking": r,
        "poster_path": p} for t, y, d, r, p in zip(titles, year, duration, rankings, poster_paths)]
     
    return movies



def scrape_fimlweb_top_250():
    url = "https://www.filmweb.pl/ranking/film"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)



    # Scrolling the page by 1000 pixels each time
    for _ in range(45):  # Increase the number of iterations if needed
        driver.execute_script("window.scrollBy(0, 750);")
        time.sleep(0.2)  # Wait for the page to load
    

    # Now you can use Selenium to extract data
    try:
        titles = [element.get_attribute('textContent') for element in driver.find_elements(By.CSS_SELECTOR, 'h2.rankingType__title a[itemprop="url"]')]
    except:
        titles = None
    try:
        original_titles = [element.get_attribute('textContent')[:-5]  for element in driver.find_elements(By.CSS_SELECTOR, 'p.rankingType__originalTitle')]
    except:
        original_titles = None
    try:
        years = [element.get_attribute('textContent')[-4:]  for element in driver.find_elements(By.CSS_SELECTOR, 'p.rankingType__originalTitle')]
    except:
        years = None
    try:
        rankings = [element.get_attribute('textContent') for element in driver.find_elements(By.CSS_SELECTOR, 'span.rankingType__rate--value')]
    except:
        rankings = None
    try:
        poster_paths = [element.get_attribute('textContent') for element in driver.find_elements(By.CSS_SELECTOR, 'span[itemprop="image"]')]
    except:
        poster_paths = None

    # Create the movies list
    movies = [{
        "title": t,
        'original_title': o,
        "year": y,
        "ranking": r,
        "poster_path": p
    } for t, o, y, r, p in zip(titles, original_titles, years, rankings, poster_paths)]

    driver.quit()

    return movies



def scrape_oscar_best_picture():
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.8"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    tmdb_client = TMDBClient()
    # Znajdź wszystkie tabele zawierające listę zwycięzców Najlepszego Filmu
    tables = soup.find_all("table", class_="wikitable")[:-1]
    winners = []

    for table in tables:
        rows = table.find_all("tr")[1:]  # Pomijamy wiersz nagłówkowy
        nominations = []
        winner_movie = None
        current_year = None
        for row in rows:
            # Jeśli wiersz ma tylko jedną komórkę, to jest to rok
            if len(row.select('td')) == 1:
                # Jeśli current_year jest już ustawione, dodajemy poprzedniego zwycięzcę do listy
                if current_year and winner_movie:
                    winner_movie['nominations'] = nominations
                    winners.append(winner_movie)
                    nominations = []
                    winner_movie = None
                current_year = re.sub(r'\[\w\]', '', row.select('td')[0].get_text(strip=True)).split()[0]
            else:
                try:
                    # Jeśli wiersz ma więcej niż jedną komórkę, to są to dane o filmie
                    film = row.select('td')[0].get_text(strip=True).replace('/', ' ')  # Pobierz nazwę filmu
                    studio = row.select('td')[1].get_text(strip=True)  # Pobierz nazwę studia filmowego
                    is_winner = 'style' in row.attrs and 'background:#FAEB86' in row['style']
                    if is_winner:
                        winner_movie = {
                            'year': current_year,
                            'release_year': current_year[:4],
                            'title': film,
                            'poster_path': tmdb_client.get_single_movie_core(film, current_year[:4])['poster_path'],
                            'studio': studio
                        }
                    else:
                        nominations.append({
                            'title': film,
                            'release_year': current_year[:4],
                            'studio': studio
                        })
                except IndexError:
                    continue
        # Dodajemy ostatniego zwycięzcę z tabeli do listy
        if current_year and winner_movie:
            winner_movie['nominations'] = nominations
            winners.append(winner_movie)

    return winners


# def scrape_movie_wallpaper(title, year):
    
#     #klucz API
#     api_key = env("GOOGLE_API_KEY")

#     #identyfikator silnika wyszukiwania
#     cx = env("CX")

#     # Zapytanie wyszukiwania
#     query = f"movie wallpaper {title} {year}"

#     # URL API
#     url = f"https://www.googleapis.com/customsearch/v1"

#     # Parametry zapytania
#     params = {
#         'key': api_key,
#         'cx': cx,
#         'q': query,
#         'searchType': 'image',
#         'num': 1
#     }

#     # Wykonaj zapytanie do API
#     response = requests.get(url, params=params)
#     # Przetwórz odpowiedź
#     data = response.json()
#     image_url = data['items'][0]['link']

#     return image_url


