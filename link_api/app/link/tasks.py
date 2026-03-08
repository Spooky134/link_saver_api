from app.core.logger import get_logger
from app.core.unit_of_work import UnitOfWork
from app.link.repositories import LinkRepository
from app.link.utils.async_link_parser import AsyncLinkInfoParser, HEADERS


logger = get_logger(__name__)


async def parse_and_update_link_task(user_id: int, link_id: int):
    link_parser = AsyncLinkInfoParser(
        headers=HEADERS
    )
    async with UnitOfWork() as uow:
        link_repo = LinkRepository(uow.session)
        try:
            link = await link_repo.get(user_id, link_id)
            if not link:
                return
            parsed_link = await link_parser.fetch(link.url)

            await link_repo.update(user_id, link_id, parsed_link)
            await uow.commit()
        except Exception as e:
            logger.error(e)


