from enum import Enum


class LinkType(str, Enum):
      WEBSITE = 'website'
      BOOK = 'book'
      ARTICLE ='article'
      MUSIC = 'music'
      VIDEO = 'video'