from typing import List, Optional

from ninja import Schema, Form, UploadedFile, File


class UserSchema(Schema):
    username: str
    is_authenticated: bool


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