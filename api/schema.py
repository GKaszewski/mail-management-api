from typing import List
from ninja import Schema


class NewMailMessageIn(Schema):
    from_email: str
    subject: str
    body: str # plain text fallback
    to: str
    html_body: str | None = None
    cc: str | None = None
    bcc: str | None = None
    attachments: List[tuple] = []


class NewBulkMailMessageIn(Schema):
    from_email: str
    messages: List[NewMailMessageIn]