from sqlalchemy.ext.asyncio import AsyncSession
from app.link.repositories import LinkRepository
from app.link.entities import CreateLinkEntity



async def test_add_and_get_link(db_session: AsyncSession):
    user_id, new_link_id = 1, 11
    link_repo = LinkRepository(db_session)
    create_link = CreateLinkEntity(
        url="https://habr.com/ru/companies/ruvds/articles/416821/",
    )
    new_link = await link_repo.add(user_id=user_id, entity=create_link)
    assert new_link.id == new_link_id
    assert new_link.user_id == user_id

    new_link = await link_repo.get_with_collections(user_id=user_id, link_id=new_link.id)

    assert new_link is not None





