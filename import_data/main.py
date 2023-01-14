import asyncio
import glob
import json
import ast
from pprint import pprint
import re
import requests
import urllib.request
from operator import attrgetter

headers = {'content-type': 'application/json'}

folder_path = '../extract_data/articles-bulgarianbeauty/*.js'

def prepare_article(data):
    def get(value):
        return data.get(value)
    article = {
        'title': get('title'),
        'description': get('description'),
        'slug': get('slug'),
        'content': get('content'),
        'metaTitle': get('metaTitle') or '',
        'releaseDate': get('releaseDate'),
        'readTime': get('readTime') or '5 мин.',
        'popular': get('popular') == 'True',
        'exclusive': get('exclusive') == 'True',
        'exclusiveText': get('exclusiveText') or '',
        'editorChoice': get('editorChoice') == 'True',
        'image': get('image'),
        'categories': [],
        'site': {
            'id': get('site').get('data').get('id')
        },
        'contentsTable': get('contentsTable')
    }

    for category in get('categories').get('data'):
        article['categories'].append(category.get('id'))


    return article

def download_image(image):
    image_url = image.get('url')
    img_data = requests.get(image_url).content
    files = {'files': (image.get('name'), img_data, 'image', {'uri': ''})}
    response = requests.post('http://localhost:1337/api/upload', files=files)
    json = response.json()
    image_id = json[0].get('id')
    print(json[0].get('id'))

    return image_id

async def prepare_image(image):
    download_response = urllib.request.urlretrieve(image.get('url'), image.get('name'))
    print('mAGAGAGAGAGAGAmm?')
    files = {'files': ('Screenshot_5.png', open(image.get('name'), 'rb'), 'image', {'uri': ''})}
    upload_response = requests.post('http://localhost:1337/api/upload', files=files, headers=headers)
    print(upload_response.reason)

    return await upload_response

async def upload_article(article):
    print(article.get('readTime'))
    # for key, value in article:
    #     print(key)
    print('mmmkaay')
    # print(file_object.get('attributes'))
    try:
        image = article.get('image').get('data').get('attributes')
        image_id = download_image(image)
        print(image_id)
        article['image'] = image_id
        response = requests.post('http://localhost:1337/api/articles', json={"data": article})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Request failed with error: ", e)

async def main():
    articles = []
    print('bo')
    index = 0
    fails = 0
    for file_path in glob.glob(folder_path):
        with open(file_path) as f:
            try:
                file_object =  eval((f.read().replace('const data = ', '')))
                article = prepare_article(file_object.get('attributes'))
                # article['id'] = file_object.get('id')
                # print(article)
                articles.append(article)
                # if (index < 3):
                # print(article.get('readTime'))
                # # for key, value in article:
                # #     print(key)
                # print('mmmkaay')
                # # print(file_object.get('attributes'))
                # try:
                #     image = file_object.get('attributes').get('image').get('data').get('attributes')
                #     image_id = download_image(image)
                #     print(image_id)
                #     article['image'] = image_id
                #     response = requests.post('http://127.0.0.1:1337/api/articles', json={"data": article})
                #     response.raise_for_status()
                # except requests.exceptions.RequestException as e:
                #     print("Request failed with error: ", e)
                # print(image_response)
            except:
                fails += 1

        index += 1
    
    print(articles)
    sorted_articles = sorted(articles, key=lambda x: x["id"])
    for article in sorted_articles:
        print(article.get('id'))
        await upload_article(article)


asyncio.run(main())
