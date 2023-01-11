from get_latest_articles import get_latest_articles
from get_articles import get_articles
import asyncio

async def main():
    print('bo')
    await get_articles()
    # article_slugs = await get_latest_articles()

asyncio.run(main())
