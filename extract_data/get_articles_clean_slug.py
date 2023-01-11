import requests
import asyncio
import json
from bs4 import BeautifulSoup

async def make_api_call(url):
    api_url = f"https://bulgarianbeauty.bg/{url.strip()}"
    print(api_url)
    response = requests.get(api_url)
    return response

async def get_articles_clean_slug():
    articles_data = []
    with open('slugs.txt', 'r') as file:
        for clean_url in file.readlines():
            # clean_url = line.split(',')[0]
            # print(clean_url)
             # TODO make check for blog artile urls only
            task = asyncio.create_task(make_api_call(clean_url))
            response = await task
            print(clean_url, response.status_code)
            if response.status_code == 200:
        # Parse the HTML of the page
                soup = BeautifulSoup(response.content, 'html.parser')

                json_data = soup.find(id='__NEXT_DATA__').string
                data = json.loads(json_data)
                # print(data)
                articles_data.extend([data])
                # with open(clean_url + '.js', 'w') as new_file:
                #     new_file.write(f"const data = {data}" )
            else:
                print(clean_url, response.status_code)

    for article in articles_data:
        # print(article)
        article = article.get('props').get('pageProps').get('article')
        if (article):
            slug = article.get('attributes').get('slug')
            with open(f'{slug}.js', 'w') as file:
                file.write(f"const data = {article}")
        

