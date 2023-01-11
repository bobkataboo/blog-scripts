import requests
import asyncio
import json
from bs4 import BeautifulSoup

url = 'https://biopedia.bg/latest/1'
pages = 13

async def make_api_call(i):
    response = requests.get(f"https://biopedia.bg/latest/{i}")
    return response

async def get_latest_articles():
    articles = []
    for i in range(pages):
        # code to be executed inside the loop
        print(i)
        task = asyncio.create_task(make_api_call(i))
        response = await task
        print(response.status_code)
        if response.status_code == 200:
        # Parse the HTML of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            json_data = soup.find(id='__NEXT_DATA__').string
            data = json.loads(json_data)
            articles_array = data.get('props').get('pageProps').get('articles').get('data')
            articles.extend(articles_array)

            # print(articles_array)
            with open(f'latest_article_{i}.html', 'w') as file:
                file.write('const data = ' + json_data)
            # with open(f'latest_article_{i}.py', 'w') as file:
            #     file.write('data = ' + json_data)
        # file.write('const data = ' + json_data)
    # The request failed
        else:
            print(f'Request for page {i} failed with status code {response.status_code}')
    slug_array = []
    # print('len' + len(articles))
    for article in articles:
        # slug_array += article.get('attributes').get('slug')
        slug_array.extend([f"'{article.get('attributes').get('slug')}'"])
        print(article.get('attributes').get('slug'))
    print(slug_array)
    # print(", ".join(slug_array))
    with open(f'latest_article_slugs.py', 'w') as file:
        fml = ", ".join(slug_array)
        file.write(f"data = [{fml}]")
    return slug_array