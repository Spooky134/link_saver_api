from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.link import LinkCreate, LinkResponse, LinkUpdate
from app.parser.async_parser import AsyncLinkInfoParser
from app.parser.parser import LinkInfoParser
from datetime import datetime
from app.db.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.models import Collection, Link
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from asyncio import to_thread

router = APIRouter()


@router.get("/", response_model=list[LinkResponse])
async def read_links(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Link).options(selectinload(Link.collections)))
    links = result.scalars().all()

    return links


@router.get("/{link_id}", response_model=LinkResponse)
async def read_link(link_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Link)
        .options(selectinload(Link.collections))  # Жадная загрузка коллекций
        .where(Link.id == link_id)
    )
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    return link

@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(link_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Link)
        .options(selectinload(Link.collections))  # Жадная загрузка связей
        .where(Link.id == link_id)
    )
    link = result.scalar_one_or_none()
    
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    await db.delete(link)
    await db.commit()

    return None

# TODO если при парсинге ошибка чтобы не падал сервер
@router.post("/", response_model=LinkResponse, status_code=201)
async def create_link(link_create: LinkCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Link).where(Link.url == str(link_create.url)))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Link already exists"
        )

    #TODO переписать на асинхронно
    parser = LinkInfoParser(str(link_create.url))    
    await to_thread(parser.fetch)

    dt = datetime.now()
    new_link = Link(
        title=parser.title,
        description=parser.description,
        url=str(link_create.url),
        image=parser.image,
        link_type=parser.link_type,
        time_create=dt,
        time_update=dt,
        collections=[]
    )

    db.add(new_link)
    await db.commit()

    #TODO непонятно зачем запрос на получение коллеций если их нет
    result = await db.execute(
        select(Link)
        .options(selectinload(Link.collections))
        .where(Link.id == new_link.id)
    )

    return result.scalar_one()

@router.put("/{link_id}", response_model=LinkResponse)
async def update_link(link_id:int, link_update: LinkUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Link)
        .options(selectinload(Link.collections))  # Жадная загрузка коллекций
        .where(Link.id == link_id)
    )
    link = result.scalar_one_or_none()
    
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    update_data = link_update.model_dump(exclude_unset=True, exclude={"collection_ids"})
    
    #TODO костыль
    if "image" in update_data:
        update_data["image"] = str(update_data["image"])

    update_data['time_update'] = datetime.now()

    # Если переданы collection_ids - обновляем коллекции
    if link_update.collection_ids is not None:
        # Получаем новые коллекции
        collections = await db.execute(
            select(Collection)
            .where(Collection.id.in_(link_update.collection_ids)))
        new_collections = collections.scalars().all()
        
        # Проверяем, что все коллекции существуют
        if len(new_collections) != len(link_update.collection_ids):
            raise HTTPException(
                status_code=404,
                detail="One or more collections not found"
            )
        
        # Очищаем старые и добавляем новые связи
        link.collections = new_collections

    for field, value in update_data.items():
        setattr(link, field, value)

    await db.commit()
    await db.refresh(link)

    return link


