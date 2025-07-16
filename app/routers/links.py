from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.links import LinkCreate, LinkResponse, LinkUpdate
from app.parser.async_parser import AsyncLinkInfoParser
from app.parser.parser import LinkInfoParser

from datetime import datetime
router = APIRouter()

fake_db = [{
    "id": 1,
    "title": "official Python",
    "description": "mainresurses",
    "url": "https://python.org",
    "image": "https://python.org/static/img/python-logo.png",
    "link_type": "article",
    "time_create": "2023-11-15T10:30:00",
    "time_update": "2024-02-20T14:45:30",
},]


def find_in_db(id: int) -> dict:
    for link in fake_db:
        if link["id"]==id:
            return link
    return None

@router.get("/", response_model=list[LinkResponse])
async def read_links():
    return fake_db


@router.get("/{link_id}", response_model=LinkResponse)
async def read_link(link_id: int):
    link = find_in_db(link_id)
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")

    return link


@router.delete("/{link_id}", response_model=LinkResponse)
async def delete_link(link_id: int):
    link = find_in_db(link_id)
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    
    fake_db.remove(link)

    return link


@router.post("/", response_model=LinkResponse, status_code=201)
async def create_link(link: LinkCreate):

    #TODO переписать на асинхронно
    url = link.url
    parser = LinkInfoParser(url)    
    parser.fetch()

    dt = datetime.now()
    new_link = {"id": len(fake_db)+1,
                "title": parser.title,
                "description": parser.description,
                "url": url,
                "image": parser.image,
                "link_type": parser.link_type,
                "time_create": dt,
                "time_update": dt,
                }


    fake_db.append(new_link)

    return new_link

@router.put("/{link_id}", response_model=LinkResponse)
async def update_link(link_id:int, link_update: LinkUpdate):
    link = find_in_db(link_id)
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    
    update_dict = link_update.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        link[key] = value

    link['time_update'] = datetime.now()
    return link
