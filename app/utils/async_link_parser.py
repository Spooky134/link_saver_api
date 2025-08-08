import aiohttp
from bs4 import BeautifulSoup
from typing import Optional, Dict
import asyncio
import json

#TODO перенести в файлы конфигураций
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.google.com/",
}


# TODO безопасность
class AsyncLinkInfoParser:
    VALID_LINK_TYPES = ("website", "book", "article", "music", "video")
    DEFAULT_LINK_TYPE = "website"

    def __init__(self, headers: Optional[Dict] = None, timeout: int = 10) -> None:
        self._headers = headers or HEADERS
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._soup = None
        self._og_data = None

    async def fetch(self, url: str) -> dict:
        """Fetch and parse URL content."""
        if not url:
            raise ValueError("URL cannot be empty")
        self._url = url
        try:
            # TODO ошибка ssl сертификатов
            async with aiohttp.ClientSession(headers=self._headers, timeout=self._timeout, connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(self._url) as response:
                    response.raise_for_status()
                    html = await response.text()
                    self._soup = BeautifulSoup(html, 'html.parser')
                    if not self._soup:
                        raise ValueError("Failed to parse page content")
                    self._parse_og_tags()
        except aiohttp.ClientError as e:
            raise Exception(f"Request error: {e}")
        

        return {"title": self._get_title(),
                "description": self._get_description(),
                "url": self._get_url(),
                "image": self._get_image(),
                "link_type": self._get_link_type()
                }

    def _parse_og_tags(self) -> None:
        """Parse Open Graph meta tags."""
        if not self._soup:
            return
        
        og_tags = self._soup.find_all('meta', attrs={
            'property': lambda x: x and x.startswith('og:')
        })
        
        self._og_data = {
            tag['property'].strip('og:'): tag['content'] 
            for tag in og_tags 
            if 'content' in tag.attrs
        }
    
    def _get_url(self) -> str:
        """Get URL"""
        return self._url
     
    def _get_title(self) -> str:
        """Get page title."""
        if self._og_data and "title" in self._og_data:
            return self._og_data["title"]

        title = self._soup.find("title")
        return title.text if title else None

    def _get_description(self) -> str:
        """Get page description."""
        if self._og_data and "description" in self._og_data:
            return self._og_data["description"]
            
        description = self._soup.find("meta", attrs={"name": "description"})
        return description["content"] if description and "content" in description.attrs else None

    def _get_image(self) -> str:
        """Get preview image URL."""
        return self._og_data.get("image", None) if self._og_data else None

    def _get_link_type(self) -> str:
        """Get link type with validation."""
        if self._og_data and "type" in self._og_data:
            return self._normalize_link_type(self._og_data["type"])
        return self.DEFAULT_LINK_TYPE

    def _normalize_link_type(self, type_str: str) -> str:
        """Normalize link type to predefined values."""
        if not type_str:
            return self.DEFAULT_LINK_TYPE
        
        type_str = type_str.lower()
        for valid_type in self.VALID_LINK_TYPES:
            if valid_type in type_str:
                return valid_type
            
        return self.DEFAULT_LINK_TYPE


def checker(control_data, data):
    for control_obj, obj in zip(control_data, data):
        print(control_obj==obj)

async def main():
    data = []
    pr = AsyncLinkInfoParser(HEADERS)
    with open("app/utils/test.txt", "r") as f:
        for line in f:
            url = line.strip()
            print(f"|{url}|")
            link_info = await pr.fetch(url)
            data.append(link_info)
             
    with open("app/utils/results.json", "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    with open('app/utils/data.json', 'r', encoding='utf-8') as f:
        control_data = json.load(f)

    checker(control_data, data)


if __name__ == "__main__":
    asyncio.run(main())