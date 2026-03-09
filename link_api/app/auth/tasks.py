from app.common.email import send_email
from app.core import broker
from app.core.logging import get_logger

logger = get_logger(__name__)


@broker.task
async def send_reset_password_email(email: str, reset_link: str) -> None:
    logger.info(f"Sending reset link to email: {email}")

    await send_email(
        to=email,
        subject="Password reset",
        body=f"Click the link to reset your password: {reset_link}",
    )
