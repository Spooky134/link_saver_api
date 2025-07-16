import httpx
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any

class AsyncLinkInfoParser:
    def __init__(self, url: str) -> None:
        self.url = url
        self.soup: Optional[BeautifulSoup] = None
        self.og_data: Dict[str, str] = {}
    
    async def fetch(self) -> None:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.url,
                    follow_redirects=True,
                    timeout=10.0  # Важно установить таймаут
                )
                response.raise_for_status()  # Проверяем на ошибки 4XX/5XX
                
                self.soup = BeautifulSoup(response.content, 'html.parser')
                if not self.soup:
                    raise ValueError("Failed to parse page content")
                
                # Извлекаем OG-теги
                og_tags = self.soup.find_all('meta', attrs={
                    'property': lambda x: x and x.startswith('og:')
                })
                self.og_data = {
                    tag['property'].strip('og:'): tag['content'] 
                    for tag in og_tags 
                    if 'content' in tag.attrs
                }
                
            except (httpx.HTTPError, httpx.TimeoutException) as e:
                raise ValueError(f"Request failed: {str(e)}")
    
    def get_title(self) -> str:
        if self.og_data.get('title'):
            return self.og_data['title']
        
        if self.soup and (title_tag := self.soup.find('title')):
            return title_tag.text
        return ""
    
    def get_link_type(self) -> str:
        if not self.og_data.get('type'):
            return 'website'
        
        link_type = self.og_data['type'].lower()
        for known_type in ('website', 'book', 'article', 'music', 'video'):
            if known_type in link_type:
                return known_type
        return link_type
    
    def get_description(self) -> str:
        if self.og_data.get('description'):
            return self.og_data['description']
        
        if self.soup and (desc_tag := self.soup.find('meta', attrs={'name': 'description'})):
            return desc_tag.get('content', '')
        return ""
    
    def get_image_url(self) -> Optional[str]:
        return self.og_data.get('image')