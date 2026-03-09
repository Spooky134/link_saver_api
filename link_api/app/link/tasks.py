import app.collection.models
import app.link.models
import app.user.models
from app.core import broker
from app.core.logging import get_logger
from app.core.unit_of_work import UnitOfWork
from app.link.repositories import LinkRepository
from app.link.utils.async_link_parser import AsyncLinkInfoParser
from app.link.utils.constants import HEADERS

logger = get_logger(__name__)


@broker.task
async def parse_and_update_link_task(user_id: int, link_id: int) -> None:
    logger.info(f"Parsing link {link_id} for user {user_id}")
    link_parser = AsyncLinkInfoParser(headers=HEADERS)
    async with UnitOfWork() as uow:
        link_repo = LinkRepository(uow.session)
        try:
            link = await link_repo.get(user_id, link_id)
            if not link:
                logger.info(f"Link {link_id} for user {user_id} not found.")
                return

            parsed_link = await link_parser.fetch(link.url)

            await link_repo.update(user_id, link_id, parsed_link)
            await uow.commit()
        except Exception as e:
            logger.error(e)
