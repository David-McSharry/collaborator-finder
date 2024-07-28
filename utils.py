import random
import aiohttp
from bs4 import BeautifulSoup


async def get_random_proxy():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.sslproxies.org/') as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            proxies = []
            for row in soup.find('table', attrs={'class': 'table table-striped table-bordered'}).find_all('tr')[1:]:
                tds = row.find_all('td')
                try:
                    ip = tds[0].text.strip()
                    port = tds[1].text.strip()
                    proxies.append(f'http://{ip}:{port}')
                except IndexError:
                    continue
            return random.choice(proxies) if proxies else None
