import os
import requests
from dotenv import load_dotenv


def get_games(api_key, games):
    url = f"https://api.rawg.io/api/games"
    params = {
        "key": api_key,
        "genres": "strategy",
        "page_size": 10,
        "metacritic": "100",
        "tags": "multiplayer"
    }
    response = requests.get(url, params)
    response.raise_for_status()
    response = response.json()
    for element in response["results"]:
        name = element['name']
        date = element['released']
        slug = element['slug']
        game_url = f"https://rawg.io/games/{slug}"
        id = element['id']
        screenshots = []
        store_urls = []
        params = {
            "key": api_key,
            "game_pk": id
        }
        screenshots_url = f"https://api.rawg.io/api/games/{id}/screenshots"
        screenshots_urls = requests.get(screenshots_url, params)
        screenshots_urls.raise_for_status()
        screenshots_urls = screenshots_urls.json()["results"]
        for screen_url in screenshots_urls:
            screen = screen_url["image"]
            screenshots.append(screen)
        stores_url = f"https://api.rawg.io/api/games/{id}/stores"
        stores_urls = requests.get(stores_url, params)
        stores_urls.raise_for_status()
        stores_urls = stores_urls.json()["results"]
        for store_link in stores_urls:
            store_url = store_link["url"]
            store_urls.append(store_url)
        game = (f"название: {name} дата выхода: {date} ссылка: {game_url}  скриншоты: {screenshots} где купить: {store_urls}")
        games.append(game)
    return games


if __name__ == "__main__":
    load_dotenv(".env")
    api_key = os.environ["API_KEY"]
    games = []
    games = get_games(api_key, games)
    for game in games:
        print(f"{game}\n")
