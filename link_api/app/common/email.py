async def send_email(to: str, subject: str, body: str) -> None:
    print(f"Sending email to {to}")
    print(f"Subject: {subject}")
    print(body)