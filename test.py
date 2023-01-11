import requests
from bs4 import BeautifulSoup

url = 'https://biopedia.bg/latest/1'
pages = 13

response = requests.get(url)

# The request was successful
if response.status_code == 200:
    # Parse the HTML of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    with open('example.html', 'w') as file:
        file.write('const data = ' + soup.find(id='__NEXT_DATA__').string)

# The request failed
else:
    print(f'Request failed with status code {response.status_code}')
