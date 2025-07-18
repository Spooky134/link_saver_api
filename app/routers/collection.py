from fastapi import APIRouter, HTTPException, status
from app.schemas.collection import CollectionResponse, CollectionCreate, CollectionUpdate
from datetime import datetime
from app.db.database import get_db
from fastapi import Depends, Query
from app.db.models import Link, Collection, link_collection
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from app.schemas.link import LinkResponse

router = APIRouter()


@router.get("/", response_model=list[CollectionResponse])
async def read_collections(db: AsyncSession = Depends(get_db)):
    results = await db.execute(
        select(Collection).options(selectinload(Collection.links))  # Жадная загрузка ссылок
    )
    collections = results.scalars().all()

    return collections


@router.get("/{collection_id}", response_model=CollectionResponse)
async def read_collection(collection_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Collection)
        .options(selectinload(Collection.links))  # Жадная загрузка ссылок
        .where(Collection.id == collection_id)
    )
    collection = result.scalar_one_or_none()

    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    return collection


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(collection_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Collection)
        .options(selectinload(Collection.links))  # Жадная загрузка связей
        .where(Collection.id == collection_id)
    )

    collection = result.scalar_one_or_none()

    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    await db.delete(collection)
    await db.commit()

    return None


@router.post("/", response_model=CollectionResponse, status_code=201)
async def create_collection(collection: CollectionCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Collection)
                                .where(Collection.name == str(collection.name)))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Collection with this name already exists"
        )
    
    dt = datetime.now()
    
    new_collection = Collection(name=collection.name,
                                description=collection.description,
                                time_create=dt,
                                time_update=dt
                                )
    
    # Если переданы link_ids - привязываем существующие ссылки
    if hasattr(collection, 'link_ids') and collection.link_ids:
        # Проверяем существование ссылок
        links = await db.execute(
            select(Link)
            .where(Link.id.in_(collection.link_ids))
        )
        found_links = links.scalars().all()
        
        # Проверяем, что все ссылки найдены
        if len(found_links) != len(collection.link_ids):
            raise HTTPException(
                status_code=404,
                detail="One or more links not found"
            )
        
        # Привязываем ссылки к коллекции
        new_collection.links = found_links

    db.add(new_collection)
    await db.commit()
    
    result = await db.execute(
        select(Collection)
        .options(selectinload(Collection.links))
        .where(Collection.id == new_collection.id)
    )

    return result.scalar_one()


@router.put("/{collection_id}", response_model=CollectionResponse)
async def update_collection(collection_id:int, collection_update: CollectionUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Collection)
        .options(selectinload(Collection.links))
        .where(Collection.id == collection_id)
    )
    collection = result.scalar_one_or_none()

    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    update_data = collection_update.model_dump(
        exclude_unset=True,
        exclude={"link_ids"}  # Исключаем поле link_ids из общего обновления
    )

     # Если переданы link_ids - обновляем связи
    if hasattr(collection_update, 'link_ids') and collection_update.link_ids is not None:
        # Получаем новые ссылки
        links_result = await db.execute(
            select(Link)
            .where(Link.id.in_(collection_update.link_ids)))
        new_links = links_result.scalars().all()
        
        # Проверяем, что все ссылки существуют
        if len(new_links) != len(collection_update.link_ids):
            raise HTTPException(
                status_code=404,
                detail="One or more links not found"
            )
        
        # Обновляем связи
        collection.links = new_links

    # Обновляем остальные поля
    for field, value in update_data.items():
        setattr(collection, field, value)

    collection.time_update = datetime.now()


    await db.commit()
    await db.refresh(collection)

    return collection


@router.get("/{collection_id}/links", response_model=list[LinkResponse])
async def get_collection_links(
    collection_id: int,
    db: AsyncSession = Depends(get_db)
):
    # 1. Проверяем существование коллекции
    collection_exists = await db.execute(
        select(Collection).where(Collection.id == collection_id))
    if not collection_exists.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Collection not found")

    # 2. Получаем ссылки коллекции с подгруженными коллекциями для каждой ссылки
    links_result = await db.execute(
        select(Link)
        .join(Link.collections)
        .options(
            selectinload(Link.collections)  # Жадная загрузка коллекций для каждой ссылки
        )
        .where(Collection.id == collection_id)
    )
    links = links_result.scalars().all()

    return links


@router.post("/{collection_id}/links", response_model=list[LinkResponse])
async def add_links_to_collection(
    collection_id: int,
    link_ids: list[int],  # ID ссылок для добавления
    db: AsyncSession = Depends(get_db)
):
    # 1. Получаем коллекцию со всеми текущими ссылками
    collection = await db.execute(
        select(Collection)
        .options(selectinload(Collection.links))
        .where(Collection.id == collection_id)
    )
    collection = collection.scalar_one_or_none()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    # 2. Получаем новые ссылки для добавления
    new_links = await db.execute(
        select(Link)
        .where(Link.id.in_(link_ids)))
    new_links = new_links.scalars().all()

    # 3. Проверяем, что все ссылки существуют
    if len(new_links) != len(link_ids):
        raise HTTPException(
            status_code=404,
            detail="One or more links not found"
        )

    # 4. Добавляем только новые ссылки (без дубликатов)
    current_link_ids = {link.id for link in collection.links}
    for link in new_links:
        if link.id not in current_link_ids:
            collection.links.append(link)

    await db.commit()
    
    links_result = await db.execute(
        select(Link)
        .join(Link.collections)
        .options(
            selectinload(Link.collections)  # Жадная загрузка коллекций для каждой ссылки
        )
        .where(Collection.id == collection_id)
    )
    links = links_result.scalars().all()
    return links


@router.get("/{collection_id}/count",response_model=dict)
async def get_links_count(collection_id: int, db: AsyncSession = Depends(get_db)):
    if not await db.get(Collection, collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    result = await db.execute(
        select(func.count())
        .select_from(link_collection)
        .where(link_collection.c.collection_id == collection_id)
    )

    return {"count_links" : result.scalar_one()}



@router.delete("/{collection_id}/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_link_from_collection(
    collection_id: int,
    link_id: int,
    db: AsyncSession = Depends(get_db)
):
    # Получаем коллекцию со ссылками
    collection = await db.execute(
        select(Collection)
        .options(selectinload(Collection.links))
        .where(Collection.id == collection_id)
    )
    collection = collection.scalar_one_or_none()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    # Находим ссылку в коллекции
    link_to_remove = next(
        (link for link in collection.links if link.id == link_id),
        None
    )
    
    if not link_to_remove:
        raise HTTPException(status_code=404, detail="Link not found in this collection")

    # Удаляем связь
    collection.links.remove(link_to_remove)
    await db.commit()
    
    return None


@router.get("/search/", response_model=list[CollectionResponse])
async def search_collection(name: str = Query(..., min_length=1, example="String"), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Collection)
        .options(selectinload(Collection.links))
        .where(Collection.name.ilike(f"%{name}%"))
        .limit(20)
    )
    
    return result.scalars().all()



# Для ссылок:
# Фильтрация по типу
# GET /links?type=article

# Поиск по домену
# GET /links/search?domain=github.com

# Последние добавленные
# GET /links/recent?limit=5

# Статистика
# GET /links/stats (количество по типам)

# Общие:
# Массовое удаление
# POST /batch-delete (тело: {"ids": [1,2,3]})

# Проверка существования URL
# GET /links/exists?url=...