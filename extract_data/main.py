from get_latest_articles import get_latest_articles
from get_articles import get_articles
from get_articles_clean_slug import get_articles_clean_slug
import asyncio

async def main():
    print('bo')
    await get_articles()
    # await get_articles_clean_slug()
    # article_slugs = await get_latest_articles()

asyncio.run(main())
