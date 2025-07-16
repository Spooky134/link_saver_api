import requests
from bs4 import BeautifulSoup

class LinkInfoParser:
      def __init__(self, url: str) -> None:
            self.__url = url
            self.__soup = None
            self.__og_data = {}

      
      def fetch(self):
            response = requests.get(self.__url)

            if response.status_code == 200:
                  self.__soup = BeautifulSoup(response.content, 'html.parser')
                  if self.__soup is None:
                        raise Exception("Faild to fetch page content")
            
            og_tags = self.__soup.find_all('meta', attrs={'property': lambda x: x and x.startswith('og:')})
            if og_tags:
                  self.__og_data = {tag['property'].strip('og:'): tag['content'] for tag in og_tags if 'content' in tag.attrs}

      @property
      def url(self):
            return self.__url

      @property     
      def title(self):
            title = self.__og_data.get('title', self.__soup.find('title').text)

            return title
      
      @property
      def link_type(self):
            link_type = self.__og_data.get('type', 'website')
            link_type = self.link_type_format(link_type)

            return link_type
      
      @property
      def description(self):
            description = self.__og_data.get('description', self.__soup.find('meta', attrs={'name': 'description'}).text)

            return description

      @property
      def image(self):
            image_url = self.__og_data.get('image', None)
            return image_url
      
      def link_type_format(self, string):
            types = ('website', 'book', 'article', 'music', 'video')
            for type_link in types:
                  if type_link in string:
                        return type_link
            return string